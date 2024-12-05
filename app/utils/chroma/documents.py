# utils/chroma/documents.py
from .index import get_client

client = get_client()


async def add_docs_to_new_collection(
    document_id: str, text: str, metadata: dict = None
):
    """Menambahkan dokumen ke koleksi dengan ID khusus"""
    documents_collection = client.create_collection(
        name=f"documents_{document_id}",
        # Anda bisa menetapkan fungsi embedding di sini jika diperlukan
        # embedding_function=...
    )
    documents_collection.upsert(
        ids=[str(document_id)],
        documents=[text],
        metadatas=[metadata or {}],
    )

    print(f"Dokumen {document_id} berhasil ditambahkan.")
