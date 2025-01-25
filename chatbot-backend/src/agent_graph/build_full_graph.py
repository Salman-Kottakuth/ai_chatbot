from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from datetime import datetime 
from src.tools.load_tools_config import LoadToolsConfig
from src.agent_graph.agent_backend import State, BasicToolNode, route_tools, plot_agent_schema
# from src.agent_graph.tool_pine_rag import hrms_pinecone_rag
# from src.tools.tool_fais_rag import faiss_rag_tool
from src.tools.tool_graph_plot import graph_plot_tool

from langchain_google_genai import ChatGoogleGenerativeAI


# Load configurations for tools and LLM
try:
    TOOLS_CFG = LoadToolsConfig()
except Exception as e:
    raise RuntimeError(f"Error loading tool configurations: {str(e)}")


# Function to get the current date
def get_current_date():
    """Returns the current date as a string."""
    return datetime.now().strftime("%Y-%m-%d")

current_date = get_current_date()



######################################################################################
system_message = f"""
You are Sasha, an AI  agent chat assistant. 
- If the user asks to plot a graph, inquire whether they would prefer a bar chart or a pie chart, and plot the graph accordingly by calling the `tool_graph_plot` based on their preference.
"""
#########################################################################################


def build_graph():
    """
    Builds an agent decision-making graph by combining an LLM with various tools
    and defining the flow of interactions between them.

    This function sets up a state graph where a primary language model (LLM) interacts
    with several predefined tools, enabling conditional tool invocation based on user queries.
    """
    # try:
    #     primary_llm = ChatOpenAI(model=TOOLS_CFG.primary_agent_llm,
    #                              temperature=TOOLS_CFG.primary_agent_llm_temperature)
    # except Exception as e:
    #     raise RuntimeError(f"Error initializing ChatOpenAI: {str(e)}")

    try:
        primary_llm = ChatGoogleGenerativeAI(model=TOOLS_CFG.primary_agent_llm,
                                 temperature=TOOLS_CFG.primary_agent_llm_temperature)
    except Exception as e:
        raise RuntimeError(f"Error initializing ChatOpenAI: {str(e)}")

    graph_builder = StateGraph(State)

    # Define tools
    #####---------------------------------------ADD TOOLS--------------------------------------------#####
    
    tools = [graph_plot_tool]

    #####---------------------------------------ADD TOOLS--------------------------------------------#####
    # Bind the tools to the primary LLM
    try:
        primary_llm_with_tools = primary_llm.bind_tools(tools)
    except Exception as e:
        raise RuntimeError(f"Error binding tools to the LLM: {str(e)}")

    def chatbot(state: State):
        """Executes the primary language model with system role and returns the generated message."""
        try:
            # Generate system message content
            messages = [{"role": "system", "content": system_message}] + state["messages"]
            return {"messages": [primary_llm_with_tools.invoke(messages)]}
        except Exception as e:
            print(f"Error in chatbot execution: {str(e)}")
            return {"messages": []}

    # Add nodes to the graph
    try:
        graph_builder.add_node("chatbot", chatbot)
        
        # Define a tool node to handle tool execution
        #####---------------------------------------ADD TOOLS--------------------------------------------#####

        tool_node = BasicToolNode(tools=[graph_plot_tool])

       #####---------------------------------------ADD TOOLS--------------------------------------------#####



        graph_builder.add_node("tools", tool_node)

        # Set up conditional routing from chatbot to tools or end of conversation
        graph_builder.add_conditional_edges(
            "chatbot",
            route_tools,
            {"tools": "tools", "__end__": "__end__"},
        )

        # Route back to chatbot after tool use to guide the next steps
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")
    except Exception as e:
        raise RuntimeError(f"Error adding nodes or edges to the graph: {str(e)}")

    # Add memory for tracking and saving checkpoints
    try:
        memory = MemorySaver()
        graph = graph_builder.compile(checkpointer=memory)
    except Exception as e:
        raise RuntimeError(f"Error compiling the graph with memory: {str(e)}")

    # Optional: Plot the agent schema for visualization
    try:
        plot_agent_schema(graph)
    except Exception as e:
        print(f"Error plotting agent schema: {str(e)}")

    return graph
