import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

EMBEDDING_MODEL = "models/text-embedding-004"

def embed_query(query: str):
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=query
    )
    return result["embedding"]
