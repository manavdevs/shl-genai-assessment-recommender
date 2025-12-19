from fastapi import FastAPI
from backend.schemas import RecommendationRequest, RecommendationResponse
from retrieval.embed_query import embed_query
from retrieval.search import search
from reranking.rerank import rerank
from utils.duration_extractor import extract_max_duration_minutes
from utils.intent_detector import has_soft_skill_intent
from reranking.balance import balance_by_test_type




TEST_TYPE_MAP = {
    "K": "Knowledge & Skills",
    "P": "Personality & Behaviour",
    "A": "Ability",
    "S": "Simulation",
    "E": "Exercises",
    "D": "Development"
}

app = FastAPI(title="SHL GenAI Assessment Recommender")

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    max_duration = extract_max_duration_minutes(request.query)
    soft_skill_intent = has_soft_skill_intent(request.query)
    query_embedding = embed_query(request.query)

    candidates = search(query_embedding,max_duration=max_duration,soft_skill_intent=soft_skill_intent,top_k=10)
    reranked = rerank(request.query, candidates)
    results = balance_by_test_type(reranked, top_k=request.top_k)

    if not reranked:
        reranked = candidates[:request.top_k]

    print({
    "max_duration": max_duration,
    "soft_skill_intent": soft_skill_intent
})


    formatted = []

    for r in results:
        test_code = r.get("test_type")

        formatted.append({
            "name": r["name"],
            "url": r["url"],
            "test_type": [TEST_TYPE_MAP.get(test_code, test_code)] if test_code else [],
            "remote_support": "Yes" if r.get("remote_support") else "No",
            "adaptive_support": "Yes" if r.get("adaptive_support") else "No",
            "description": r.get("description"),    
            "duration": r.get("duration_minutes")
        })

    return {"recommended_assessments": formatted}
