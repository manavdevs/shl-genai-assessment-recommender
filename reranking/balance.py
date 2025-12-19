def balance_by_test_type(results, top_k=10):
    """
    Ensure final recommendations include a balanced mix of test types.
    Guarantees at least one technical (K) and one behavioral (P/A/D) if available.
    """

    technical = []
    behavioral = []
    others = []

    for r in results:
        t = r.get("test_type")
        if t == "K":
            technical.append(r)
        elif t in ["P", "A", "D"]:
            behavioral.append(r)
        else:
            others.append(r)

    balanced = []

    if technical:
        balanced.append(technical[0])

    if behavioral:
        balanced.append(behavioral[0])

    remaining = [
        r for r in results
        if r not in balanced
    ]

    balanced.extend(remaining)

    return balanced[:top_k]
