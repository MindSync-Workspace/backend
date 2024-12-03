import chromadb
from app.utils.embed import generate_embedding

client = chromadb.PersistentClient(path="./db")

notes_collection = client.get_or_create_collection(
    name="notes",
)


async def add_note_to_collection(note_id: str, text: str, metadata: dict = None):

    # embedding = await generate_embedding(text)
    notes_collection.upsert(
        ids=[str(note_id)],
        documents=[text],
        metadatas=[metadata or {}],
    )
    ## TODO: 1 collection 1 docs (bcs text splitting)


async def query_note_similar(text: str, user_id: int, n_results: int = 3):
    results = notes_collection.query(query_texts=[text], n_results=n_results)
    return results


async def get_notes_on_vector_db(note_id: int):

    results = notes_collection.get(ids=[str(note_id)])
    return results


# async def get_notes_on_vector_db_by_user_id(user_id: int):

#     results = notes_collection.get(where={"user_id": user_id})
#     return results


async def process_note(note, user_id):
    results = await get_notes_on_vector_db(note["id"])
    if len(results["ids"]) == 0:
        await add_note_to_collection(
            note_id=note["id"], metadata={"user_id": user_id}, text=note["text"]
        )
        print(f"Note ID {note['id']} berhasil ditambahkan.")
