from langchain_google_vertexai import VertexAIEmbeddings
import vertexai
from langchain_google_genai import GoogleGenerativeAIEmbeddings


PROJECT_ID = "mindsync-101010"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

vertexai.init(project=PROJECT_ID, location=LOCATION)


def get_embedding_function():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key="AIzaSyAy-jpRv3In-ksCNc1PJi2Rw46HHwKH_xw",
    )
    return embeddings
