from openai import OpenAI
from typing import List, Dict
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rerank(query: str, candidates: List[Dict], top_k: int = 5) -> List[Dict]:
    prompt = f"""
You are an expert HR assessment recommender.

User query:
"{query}"

Rank the following SHL assessments from most relevant to least relevant.
Return ONLY a numbered list of assessment names.

Assessments:
"""

    for i, c in enumerate(candidates, 1):
        prompt += f"{i}. {c['name']} — {c.get('description', '')}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You rank assessments by relevance."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    ranked_text = response.choices[0].message.content.lower()

    ranked = []
    for c in candidates:
        if c["name"].lower() in ranked_text:
            ranked.append(c)

    return ranked[:top_k]
