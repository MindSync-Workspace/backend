# from langflow.load import run_flow_from_json
import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from app.utils.vertex import get_embedding_function
from app.utils.chroma.index import get_client
from langchain_google_vertexai import VertexAI
import pprint

PROMPT_TEMPLATE = """
Anda adalah bot AI yang dirancang untuk membantu pengguna dengan menjelaskan dokumen atau memberikan jawaban terkait topik yang diberikan dengan gaya bahasa yang santai namun tetap profesional.
PANDUAN:
- Berikan penjelasan yang jelas dan mudah dipahami, seperti berbicara dengan teman namun tetap terkesan profesional.
- Fokus untuk menjawab pertanyaan atau menjelaskan isi dokumen sesuai permintaan tanpa membuatnya terlalu rumit.
- Jika dokumen atau pertanyaan kurang jelas, sampaikan dengan sopan bahwa informasi yang tersedia tidak cukup untuk memberikan penjelasan lebih lanjut.
- Hindari menggunakan istilah yang terlalu formal atau teknis, tetapi tetap menjaga kejelasan dan keseriusan informasi.
- Sampaikan informasi penting dengan cara yang mudah dipahami, tanpa menambah informasi yang tidak relevan.
- Hanya Jawab dengan menggunakan bahasa indonesia,tanpa prefix seperti (Oh saya bisa melakukanya,berdasarkan konteks yang anda berikan,dsb)
- Jawab to the point tanpa penambahan seperti,(ada lagi yang bisa saya jawab,Dari yang saya pahami dan sebagainya)

{context}

---
Berikut pertanyaan yang perlu anda tanggapi: {question}

"""


def get_chat_response_from_model(query_text: str, document_id: int):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(client=get_client(), embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(
        query_text, k=5, filter={"document_id": document_id}
    )

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = VertexAI(model_name="gemini-1.0-pro-002")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


SUMMARIZE_PROMPT_TEMPLATE = """Anda adalah asisten AI untuk meringkas teks yang terintegrasi dalam alat pengolah dokumen. Tugas Anda adalah membantu pengguna meringkas teks panjang menjadi ringkasan singkat yang mencakup poin-poin utama dan detail penting
    PANDUAN:
    - Ringkas teks yang diberikan pengguna dengan panjang maksimal 150 kata (lebih sedikit lebih baik).
    - Fokus pada ide utama dan hilangkan detail yang tidak penting.
    - Hindari menambahkan informasi baru atau opini pribadi.
    - Jika teks tidak cukup jelas untuk diringkas, sampaikan dengan sopan bahwa informasi yang tersedia tidak mencukupi.
    - Tetap relevan, jelas, dan singkat dalam respons Anda.
    - Hanya jawab dengan hasil ringkasan tanpa ada embel embel seperti "Ini jawabannya", "Baiklah"
    Berikut teks yang perlu diringkas:
    {context}
    """


def get_summarize_text(document_id: int, user_id: int):

    # Persiapkan DB.
    embedding_function = get_embedding_function()
    db = Chroma(client=get_client(), embedding_function=embedding_function)

    # Ambil semua dokumen berdasarkan document_id.
    results = db.get(where={"user_id": user_id})

    filtered_chunks = get_documents_by_document_id(results, document_id)

    if len(filtered_chunks) == 0:
        print("❌ Tidak ada dokumen dengan document_id yang diminta.")
        return "Tidak ada dokumen yang ditemukan untuk document_id tersebut."
    print(len(filtered_chunks))
    # Gabungkan konten dari semua dokumen untuk membuat konteks.
    context_text = "\n\n---\n\n".join(filtered_chunks)

    # Tentukan prompt untuk model
    prompt_template = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text)

    # Gunakan model untuk merangkum teks
    model = VertexAI(model_name="gemini-1.0-pro-002")
    response_text = model.invoke(prompt)

    # Format dan kembalikan hasil ringkasan

    print(response_text)
    return response_text


def get_documents_by_document_id(chunks, document_id: int):
    print(chunks["metadatas"])
    if not chunks.get("documents") or not chunks.get("metadatas"):
        return []

    # Menggabungkan dokumen dengan metadata
    documents = chunks["documents"]
    metadatas = chunks["metadatas"]

    # Filter dokumen berdasarkan metadata document_id
    filtered_documents = [
        doc
        for doc, meta in zip(documents, metadatas)
        if meta.get("document_id") == document_id
    ]

    return filtered_documents


# def get_chat_response_from_model(text: str):
#     TWEAKS = {
#         "ParseData-3PZGr": {},
#         "Prompt-yeVY3": {},
#         "note-yd8NM": {},
#         "note-lv8j2": {},
#         "note-k57TU": {},
#         "TextOutput-MSv3w": {},
#         "Memory-zfDMW": {},
#         "TextOutput-Np8H9": {},
#         "Prompt-f3y8j": {},
#         "JSONToDataComponent-d1mjn": {},
#         "ParseData-kaknL": {},
#         "ParseData-gHb0a": {},
#         "ParseData-Xmywd": {},
#         "ParseData-O3rDZ": {},
#         "ParseData-ludk7": {},
#         "ChatOutput-EQZ9A": {},
#         "TextOutput-ufvZ9": {},
#         "VertexAIEmbeddings-5GuQ2": {},
#         "VertexAiModel-HNrxv": {},
#         "TextInput-ScQ4r": {},
#         "ChatInput-TlXts": {},
#         "Chroma-6Uvhd": {},
#         "Chroma-hDn6g": {},
#         "Chroma-gdeYl": {},
#         "TextOutput-oNzh7": {},
#         "TextInput-sARVD": {},
#         "VertexAiModel-joTdK": {},
#     }

#     results = run_flow_from_json(
#         flow="RAG-MinSync.json",
#         input_value="message",
#         session_id="",
#         fallback_to_env_vars=True,
#         tweaks=TWEAKS,
#     )
#     print(results)
#     return results


# input_text = "Halo, bagaimana kabar Anda hari ini?"
# response = get_chat_response_from_model(input_text)
