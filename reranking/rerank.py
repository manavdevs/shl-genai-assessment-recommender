from openai import OpenAI
from typing import List, Dict
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rerank(query: str, candidates: List[Dict], top_k: int = 10) -> List[Dict]:
    prompt = f"""
You are an expert HR assessment recommender.

User query:
"{query}"

Rank the following SHL assessments from most relevant to least relevant.
Return ONLY a numbered list of indices (not names).

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

    text = response.choices[0].message.content

    # Extract indices like: 1, 2, 3...
    indices = [int(i) for i in re.findall(r"\b\d+\b", text)]

    ranked = []
    for i in indices:
        if 1 <= i <= len(candidates):
            ranked.append(candidates[i - 1])

    # Fallback safety
    if not ranked:
        ranked = candidates

    return ranked[:top_k]
