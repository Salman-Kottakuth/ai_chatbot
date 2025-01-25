
from typing import Tuple
# from src.chatbot.load_config import LoadProjectConfig
from src.tools.load_tools_config import LoadToolsConfig
from src.agent_graph.build_full_graph import build_graph


# Load configurations with error handling
try:
    # PROJECT_CFG = LoadProjectConfig()
    TOOLS_CFG = LoadToolsConfig()
except RuntimeError as e:
    raise RuntimeError(f"Configuration loading failed: {str(e)}")

# Build the agent graph with error handling
try:
    graph = build_graph()
except Exception as e:
    raise RuntimeError(f"Failed to build the agent graph: {str(e)}")

config = {"configurable": {"thread_id": TOOLS_CFG.thread_id}}

class ChatBot:
    """
    A class to handle chatbot interactions by utilizing a pre-defined agent graph. The chatbot processes
    user messages, generates appropriate responses.

    Attributes:
        config (dict): A configuration dictionary that stores specific settings such as the `thread_id`.

    Methods:
        respond(message: str) -> Tuple:
            Processes the user message through the agent graph and generates a response.
            Returns the chatbot's response.
    """

    @staticmethod
    def respond(message: str) -> Tuple:
        """
        Processes a user message using the agent graph, generates a response
        Args:
            message (str): The user message to process.

        Returns:
            Tuple: Returns an empty string (representing the new user input placeholder) and the chatbot's response.
        """
        try:
            # The config is the **second positional argument** to stream() or invoke()!
            events = list(graph.stream(
                {"messages": [("user", message)]}, config, stream_mode="values"
            ))

            # Extract the last event's message content 
            chatbot_response = events[-1]["messages"][-1].content
            print(chatbot_response)

            return "", chatbot_response 
        except Exception as e:
            return f"Error processing message: {str(e)}", ""
