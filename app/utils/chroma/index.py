import chromadb
from chromadb.config import Settings

client = chromadb.HttpClient(
    host="https://chroma-3650861314.asia-east1.run.app",
    port=443,
    ssl=True,
    settings=Settings(
        chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
        chroma_client_auth_credentials="mindsyncanjayslebew",
        anonymized_telemetry=False,
    ),
)


def get_client():
    """Mengembalikan instance ChromaDB client"""
    return client


notes_collection = client.get_or_create_collection(
    name="notes",
)
