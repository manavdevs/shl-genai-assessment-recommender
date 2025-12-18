import json
import time
import os
from typing import List

import google.generativeai as genai
from tqdm import tqdm

from config import GEMINI_API_KEY
from embeddings.build_embeddings import build_embedding_text

# -----------------------------
# Gemini Setup
# -----------------------------
genai.configure(api_key=GEMINI_API_KEY)

EMBEDDING_MODEL = "models/text-embedding-004"
BATCH_SIZE = 8        
SLEEP_TIME = 0.5     

INPUT_PATH = "data/processed/assessments_full.json"
OUTPUT_PATH = "data/processed/assessments_embeddings.json"


def generate_embedding(text: str) -> List[float]:
    """Generate a single embedding using Gemini."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text
    )
    return result["embedding"]


def main():
    with open(INPUT_PATH, "r") as f:
        assessments = json.load(f)

    enriched = []

    for item in tqdm(assessments, desc="Embedding assessments"):
        text = build_embedding_text(item)

        if not text or len(text) < 50:
            continue

        embedding = generate_embedding(text)

        enriched.append({
            **item,
            "embedding": embedding
        })

        time.sleep(SLEEP_TIME)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(enriched, f)

    print(f"Saved {len(enriched)} embeddings to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
