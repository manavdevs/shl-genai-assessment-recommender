from retrieval.embed_query import embed_query
from retrieval.search import search
from reranking.rerank import rerank

query = "Looking for a backend Python developer assessment"

query_embedding = embed_query(query)
candidates = search(query_embedding)

results = rerank(query, candidates)

print("\nFinal Reranked Results:\n")
for r in results:
    print(f"- {r['name']} | {r['url']}")
