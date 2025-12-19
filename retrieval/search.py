import json
import faiss
import numpy as np

INDEX_PATH = "embeddings/faiss_index/index.bin"
DATA_PATH = "data/processed/assessments_embeddings.json"
TOP_K = 10

def apply_duration_bias(results, max_duration):
    """
    Softly prioritize assessments within max_duration.
    Does NOT hard-filter.
    """
    if max_duration is None:
        return results

    def duration_score(item):
        dur = item.get("duration_minutes")

        if dur is None:
            return 1.0          # neutral
        if dur <= max_duration:
            return 0.0          # best
        return 2.0              # worst

    return sorted(results, key=duration_score)

def apply_soft_skill_boost(results, soft_skill_intent):
    if not soft_skill_intent:
        return results

    def soft_skill_score(item):
        t = item.get("test_format")
        if t in ["P", "A", "D"]:
            return 0.0   # boost
        return 1.0       # neutral

    return sorted(results, key=soft_skill_score)

def search(query_embedding: list,top_k: int = TOP_K,max_duration: int | None = None,soft_skill_intent: bool = False):


    index = faiss.read_index(INDEX_PATH)

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []

    for rank, idx in enumerate(indices[0]):
        item = data[idx]
        item_copy = item.copy()
        item_copy["rank"] = rank + 1
        item_copy["distance"] = float(distances[0][rank])
        results.append(item_copy)


    results = apply_duration_bias(results, max_duration)
    results = apply_soft_skill_boost(results, soft_skill_intent)
    return results



