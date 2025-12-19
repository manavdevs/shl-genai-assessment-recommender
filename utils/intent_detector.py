SOFT_SKILL_KEYWORDS = [
    "collaborate", "collaboration", "stakeholder", "stakeholders",
    "communication", "interpersonal", "people management",
    "leadership", "cultural", "culture", "team", "relationship",
    "behavior", "personality", "manager", "management"
]


def has_soft_skill_intent(query: str) -> bool:
    q = query.lower()
    return any(keyword in q for keyword in SOFT_SKILL_KEYWORDS)
