# from langflow.load import run_flow_from_json
import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from app.utils.vertex import get_embedding_function
from app.utils.chroma.index import get_client
from langchain_google_vertexai import VertexAI


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
