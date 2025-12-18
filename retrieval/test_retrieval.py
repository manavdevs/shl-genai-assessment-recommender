from retrieval.embed_query import embed_query
from retrieval.search import search

query = "Looking for a backend Python developer assessment"

query_embedding = embed_query(query)
results = search(query_embedding)

print("\nTop matching assessments:\n")
for r in results:
    print(
        f"{r['rank']}. {r['name']}\n"
        f"   Distance: {r['distance']:.4f}\n"
        f"   URL: {r['url']}\n"
    )
