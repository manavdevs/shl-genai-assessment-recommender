from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5

class AssessmentResponse(BaseModel):
    name: str
    url: str
    test_type: List[str]
    remote_support: str
    adaptive_support: str
    description: Optional[str]
    duration: Optional[int]

class RecommendationResponse(BaseModel):
    recommended_assessments: List[AssessmentResponse]
