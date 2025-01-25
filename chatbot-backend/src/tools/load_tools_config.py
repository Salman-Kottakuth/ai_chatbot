import os
import yaml
from dotenv import load_dotenv
from pyprojroot import here

# Load environment variables from .env file
load_dotenv()

class LoadToolsConfig:
    def __init__(self) -> None:
        try:
            with open(here("configs/tools_config.yml")) as cfg:
                app_config = yaml.load(cfg, Loader=yaml.FullLoader)
        except FileNotFoundError:
            raise RuntimeError("Configuration file 'tools_config.yml' not found.")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing YAML file: {str(e)}")

        # # Set environment variables
        # try:
        #     os.environ['OPENAI_API_KEY'] = os.getenv("OPEN_AI_API_KEY")
        
        # Set environment variables
        try:
            os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
            

            # os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")
        except Exception as e:
            raise RuntimeError(f"Error setting environment variables: {str(e)}")

        try:
            # Primary agent
            self.primary_agent_llm = app_config["primary_agent"]["llm"]
            self.primary_agent_llm_temperature = app_config["primary_agent"]["llm_temperature"]

           


            # # Pinecone Q & A RAG Tool configs
            # self.pinecone_rag = app_config["pinecone_rag"]["llm"]
            # self.hrms_rag_llm_temperature = float(app_config["pinecone_rag"]["llm_temperature"])
            # self.pinecone_rag_embedding_model = app_config["pinecone_rag"]["embedding_model"]
            # self.pinecone_rag_k = app_config["pinecone_rag"]["k"]

            # # FAISS Tool Configs
            # self.faiss_tool_db_faiss_path = app_config["faiss_tool"]["db_faiss_path"]
            # self.faiss_tool_csv_file_path = app_config["faiss_tool"]["csv_file_path"]
            # self.faiss_tool_k = app_config["faiss_tool"]["k"]
            # self.faiss_tool_embedding_model = app_config["faiss_tool"]["embedding_model"]
            # # self.faiss_tool_temperature = app_config["faiss_tool"]["temperature"]




            # Graph configs
            self.thread_id = str(app_config["graph_configs"]["thread_id"])

        except KeyError as e:
            raise RuntimeError(f"Missing configuration key: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error loading configurations: {str(e)}")
