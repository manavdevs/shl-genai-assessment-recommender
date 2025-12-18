# embeddings/build_faiss_index.py
import json
import faiss
import numpy as np
import os

INPUT = "data/processed/assessments_embeddings.json"
INDEX_DIR = "embeddings/faiss_index"
INDEX_PATH = f"{INDEX_DIR}/index.bin"

os.makedirs(INDEX_DIR, exist_ok=True)

with open(INPUT) as f:
    data = json.load(f)

vectors = np.array([item["embedding"] for item in data]).astype("float32")

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

faiss.write_index(index, INDEX_PATH)

print("FAISS index built")
print("Vectors:", index.ntotal)
print("Dimension:", index.d)
