def build_rerank_prompt(query: str, candidates: list) -> str:
    candidate_text = ""
    for i, c in enumerate(candidates, 1):
        candidate_text += (
            f"{i}. Name: {c['name']}\n"
            f"   Description: {c.get('description', '')}\n"
            f"   Test Type: {c.get('test_type', '')}\n\n"
        )

    prompt = f"""
You are an expert talent assessment consultant.

A recruiter is hiring based on the following requirement:
"{query}"

Below is a list of SHL assessments retrieved based on semantic similarity.
Your task is to select the BEST assessments for this role.

Instructions:
- Select the top 3 to 5 assessments
- Prefer role relevance over generic skill coverage
- Avoid redundant or overlapping assessments
- Provide a short justification for each selection

Assessments:
{candidate_text}

Respond in JSON with the following format:
[
  {{
    "name": "...",
    "reason": "..."
  }}
]
"""
    return prompt.strip()
