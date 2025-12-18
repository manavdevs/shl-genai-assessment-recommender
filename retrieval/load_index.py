import faiss
import json

FAISS_INDEX_PATH = "embeddings/faiss_index/index.bin"
METADATA_PATH = "data/processed/assessments_embeddings.json"

def load_faiss_index():
    index = faiss.read_index(FAISS_INDEX_PATH)
    return index

def load_metadata():
    with open(METADATA_PATH, "r") as f:
        return json.load(f)
