from app.utils.chroma.index import get_client
from app.utils.vertex import get_embedding_function
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from io import BytesIO
from cuid import cuid


def load_documents(path: str):
    document_loader = PyMuPDFLoader(path)
    return document_loader.load()


def load_documents_from_file(file: bytes, filename: str):
    # Simpan file ke lokasi sementara di memori
    with open(filename, "wb") as temp_file:
        temp_file.write(file)

    # Load dokumen menggunakan PyMuPDFLoader
    document_loader = PyMuPDFLoader(filename)
    documents = document_loader.load()

    return documents


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitter.split_documents(documents)


async def add_docs_to_new_collection(
    chunks: list[Document], user_id: int, document_id: int
):
    db = Chroma(
        client=get_client(),
        embedding_function=get_embedding_function(),
    )

    for chunk in chunks:
        chunk.metadata["user_id"] = user_id

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(
        include=[], where={"user_id": user_id}
    )  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # new_chunks = []
    # for chunk in chunks_with_ids:
    #     if chunk.metadata["id"] not in existing_ids:
    #         new_chunks.append(chunk)
    new_chunks = [
        chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids
    ]

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        for chunk in new_chunks:
            chunk.metadata["document_id"] = document_id

        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def reset_database():
    db = Chroma(
        client=get_client(),
        embedding_function=get_embedding_function(),
    )

    db.reset_collection()
