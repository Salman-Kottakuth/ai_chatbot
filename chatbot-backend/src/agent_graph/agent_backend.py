import json
from IPython.display import Image, display
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_core.messages import ToolMessage
from langgraph.graph.message import add_messages



class State(TypedDict):
    """Represents the state structure containing a list of messages.

    Attributes:
        messages (list): A list of messages, where each message can be processed
        by adding messages using the `add_messages` function.
    """
    messages: Annotated[list, add_messages]


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage.

    This class retrieves tool calls from the most recent AIMessage in the input
    and invokes the corresponding tool to generate responses.

    Attributes:
        tools_by_name (dict): A dictionary mapping tool names to tool instances.
    """

    def __init__(self, tools: list) -> None:
        """Initializes the BasicToolNode with available tools.

        Args:
            tools (list): A list of tool objects, each having a `name` attribute.
        """
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        """Executes the tools based on the tool calls in the last message.

        Args:
            inputs (dict): A dictionary containing the input state with messages.

        Returns:
            dict: A dictionary with a list of `ToolMessage` outputs.

        Raises:
            ValueError: If no messages are found in the input.
        """
        try:
            if messages := inputs.get("messages", []):
                message = messages[-1]
            else:
                raise ValueError("No messages found in input.")

            outputs = []
            for tool_call in message.tool_calls:
                if tool_call["name"] not in self.tools_by_name:
                    raise KeyError(f"Tool '{tool_call['name']}' not found.")
                tool_result = self.tools_by_name[tool_call["name"]].invoke(tool_call["args"])
                outputs.append(
                    ToolMessage(
                        content=json.dumps(tool_result),
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                )
            return {"messages": outputs}

        except Exception as e:
            print(f"Error during tool execution: {str(e)}")
            return {"messages": []}


def route_tools(state: State) -> Literal["tools", "__end__"]:
    """
    Determines whether to route to the ToolNode or end the flow.

    Args:
        state (State): The input state containing a list of messages.

    Returns:
        Literal["tools", "__end__"]: Returns 'tools' if there are tool calls;
        '__end__' otherwise.

    Raises:
        ValueError: If no messages are found in the input state.
    """
    try:
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state: {state}")

        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return "__end__"

    except Exception as e:
        print(f"Error in routing tools: {str(e)}")
        return "__end__"


def plot_agent_schema(graph):
    """Plots the agent schema using a graph object, if possible.

    Args:
        graph: A graph object that has a `get_graph` method, returning a graph
        structure that supports Mermaid diagram generation.

    Returns:
        None
    """
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception as e:
        print(f"Graph could not be displayed: {str(e)}")
