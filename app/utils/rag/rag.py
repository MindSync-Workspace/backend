from langflow.load import run_flow_from_json


def get_chat_response_from_model(text: str):
    TWEAKS = {
        "ParseData-3PZGr": {},
        "Prompt-yeVY3": {},
        "note-yd8NM": {},
        "note-lv8j2": {},
        "note-k57TU": {},
        "TextOutput-MSv3w": {},
        "Memory-zfDMW": {},
        "TextOutput-Np8H9": {},
        "Prompt-f3y8j": {},
        "JSONToDataComponent-d1mjn": {},
        "ParseData-kaknL": {},
        "ParseData-gHb0a": {},
        "ParseData-Xmywd": {},
        "ParseData-O3rDZ": {},
        "ParseData-ludk7": {},
        "ChatOutput-EQZ9A": {},
        "TextOutput-ufvZ9": {},
        "VertexAIEmbeddings-5GuQ2": {},
        "VertexAiModel-HNrxv": {},
        "TextInput-ScQ4r": {},
        "ChatInput-TlXts": {},
        "Chroma-6Uvhd": {},
        "Chroma-hDn6g": {},
        "Chroma-gdeYl": {},
        "TextOutput-oNzh7": {},
        "TextInput-sARVD": {},
        "VertexAiModel-joTdK": {},
    }

    results = run_flow_from_json(
        flow="RAG-MinSync.json",
        input_value="message",
        session_id="",
        fallback_to_env_vars=True,
        tweaks=TWEAKS,
    )
    print(results)
    return results


input_text = "Halo, bagaimana kabar Anda hari ini?"
response = get_chat_response_from_model(input_text)
