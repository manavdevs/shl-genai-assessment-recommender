def build_embedding_text(assessment: dict) -> str:
    parts = []

    if assessment.get("name"):
        parts.append(f"Assessment Name: {assessment['name']}")

    if assessment.get("description"):
        parts.append(f"Description: {assessment['description']}")

    if assessment.get("job_levels"):
        parts.append(
            "Job Levels: " + ", ".join(assessment["job_levels"])
        )

    if assessment.get("test_format"):
        parts.append(f"Test Type: {assessment['test_format']}")

    return "\n".join(parts)
if __name__ == "__main__":
    import json

    with open("data/processed/assessments_full.json") as f:
        sample = json.load(f)[0]

    print(build_embedding_text(sample))
