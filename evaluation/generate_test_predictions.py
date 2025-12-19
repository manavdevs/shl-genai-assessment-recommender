import pandas as pd
from tqdm import tqdm

from retrieval.embed_query import embed_query
from retrieval.search import search
from reranking.rerank import rerank
from reranking.balance import balance_by_test_type
from utils.duration_extractor import extract_max_duration_minutes
from utils.intent_detector import has_soft_skill_intent


TEST_PATH = "data/test/Gen_AI Dataset.xlsx"
OUTPUT_CSV = "data/test/test_predictions.csv"

RETRIEVAL_K = 50
TOP_K = 10


def main():
    df = pd.read_excel(TEST_PATH, sheet_name="Test-Set")

    rows = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating predictions"):
        query = row["Query"]

        # Intent extraction
        max_duration = extract_max_duration_minutes(query)
        soft_skill_intent = has_soft_skill_intent(query)

        # Embed + retrieve
        query_embedding = embed_query(query)
        candidates = search(
            query_embedding,
            top_k=RETRIEVAL_K,
            max_duration=max_duration,
            soft_skill_intent=soft_skill_intent
        )

        # Rerank + balance
        reranked = rerank(query, candidates, top_k=RETRIEVAL_K)
        final_results = balance_by_test_type(reranked, top_k=TOP_K)

        # 🔹 One row per recommendation
        for r in final_results:
            rows.append({
                "Query": query,
                "Assessment_url": r["url"]
            })

    output_df = pd.DataFrame(rows)
    output_df.to_csv(OUTPUT_CSV, index=False)

    print(f"\n✅ Test predictions saved in required format to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
