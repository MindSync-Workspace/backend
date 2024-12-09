from langchain_google_vertexai import VertexAIEmbeddings
import vertexai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

PROJECT_ID = "mindsync-101010"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

vertexai.init(project=PROJECT_ID, location=LOCATION)


def get_embedding_function():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    return embeddings
