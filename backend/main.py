from fastapi import FastAPI
from backend.schemas import RecommendationRequest, RecommendationResponse
from retrieval.embed_query import embed_query
from retrieval.search import search
from reranking.rerank import rerank

app = FastAPI(title="SHL GenAI Assessment Recommender")

@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    query_embedding = embed_query(request.query)
    candidates = search(query_embedding)
    results = rerank(request.query, candidates)

    return {
        "results": [
            {"name": r["name"], "url": r["url"]}
            for r in results
        ]
    }
