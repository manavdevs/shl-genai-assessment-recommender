import json
import faiss
import numpy as np

INDEX_PATH = "embeddings/faiss_index/index.bin"
DATA_PATH = "data/processed/assessments_embeddings.json"
TOP_K = 10


def search(query_embedding: list, top_k: int = TOP_K):
    index = faiss.read_index(INDEX_PATH)

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        item = data[idx]

        # Preserve ALL metadata
        item_copy = item.copy()
        item_copy["rank"] = rank + 1
        item_copy["distance"] = float(distances[0][rank])

        results.append(item_copy)

    return results
