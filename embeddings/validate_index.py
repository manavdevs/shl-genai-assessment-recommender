import json
import faiss

EMBEDDINGS_PATH = "data/processed/assessments_embeddings.json"
INDEX_PATH = "embeddings/faiss_index/index.bin"

def main():
    with open(EMBEDDINGS_PATH, "r") as f:
        data = json.load(f)

    index = faiss.read_index(INDEX_PATH)

    print("Metadata records:", len(data))
    print("FAISS vectors:", index.ntotal)
    print("Embedding dimension:", index.d)

    assert len(data) == index.ntotal, "❌ Count mismatch!"
    assert index.d == len(data[0]["embedding"]), "❌ Dimension mismatch!"

    print("✅ FAISS index and embeddings are consistent")

if __name__ == "__main__":
    main()
