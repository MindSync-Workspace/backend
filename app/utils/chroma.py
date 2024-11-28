import chromadb
from app.utils.embed import generate_embedding

client = chromadb.Client()

notes_collection = client.get_or_create_collection(name="notes")


async def add_note_to_collection(note_id: str, text: str, metadata: dict = None):

    # embedding = await generate_embedding(text)
    notes_collection.add(
        ids=[note_id],
        documents=[text],
        metadatas=[metadata or {}],
        embeddings=[],
    )
    ## TODO: 1 collection 1 docs (bcs text splitting)


async def query_similar(embedding: list[float], n_results: int = 5):
    """
    Query ChromaDB for similar embeddings.
    """
    results = await notes_collection.query(
        query_embeddings=[embedding], n_results=n_results
    )
    return results
