from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    query: str

class Assessment(BaseModel):
    name: str
    url: str

class RecommendationResponse(BaseModel):
    results: List[Assessment]
