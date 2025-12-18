import json

with open("data/processed/assessments_embeddings.json") as f:
    data = json.load(f)

print(len(data))

print(len(data[0]["embedding"]))

print(any(item.get("embedding") is None for item in data))
