import json
import faiss
import numpy as np

INDEX_PATH = "embeddings/faiss_index/index.bin"
DATA_PATH = "data/processed/assessments_embeddings.json"
TOP_K = 10


def search(query_embedding: list):
    # Load FAISS index
    index = faiss.read_index(INDEX_PATH)

    # Load metadata
    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    # Convert query to numpy
    query_vector = np.array([query_embedding]).astype("float32")

    # Search
    distances, indices = index.search(query_vector, TOP_K)

    results = []
    for rank, idx in enumerate(indices[0]):
        item = data[idx]
        results.append({
            "rank": rank + 1,
            "name": item["name"],
            "url": item["url"],
            "distance": float(distances[0][rank])
        })

    return results
