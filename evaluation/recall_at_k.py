def recall_at_k(retrieved: list, relevant: list, k: int = 50) -> float:
    retrieved_k = retrieved[:k]
    relevant_set = set([r.lower() for r in relevant])

    if not relevant_set:
        return 0.0

    hits = sum(1 for r in retrieved_k if r.lower() in relevant_set)
    return hits / len(relevant_set)
