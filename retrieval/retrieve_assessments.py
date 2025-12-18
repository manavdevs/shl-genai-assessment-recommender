from retrieval.embed_query import embed_query
from retrieval.load_index import load_faiss_index, load_metadata
from retrieval.search import search_faiss

def retrieve_assessments(query: str, top_k=10):
    index = load_faiss_index()
    metadata = load_metadata()

    query_embedding = embed_query(query)
    indices, distances = search_faiss(index, query_embedding, top_k)

    results = []
    for idx, score in zip(indices, distances):
        item = metadata[idx]
        results.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"],
            "description": item["description"],
            "score": float(score)
        })

    return results
