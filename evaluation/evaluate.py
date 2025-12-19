from tqdm import tqdm

from evaluation.load_train_data import load_train_data
from evaluation.recall_at_k import recall_at_k

from retrieval.embed_query import embed_query
from retrieval.search import search
from reranking.rerank import rerank
from reranking.balance import balance_by_test_type
from utils.duration_extractor import extract_max_duration_minutes
from utils.intent_detector import has_soft_skill_intent


TRAIN_PATH = "data/train/Gen_AI Dataset.xlsx"
TOP_K = 10
RETRIEVAL_K = 50   # important for recall


def main():
    train_data = load_train_data(TRAIN_PATH)
    recalls = []

    for item in tqdm(train_data, desc="Evaluating"):
        query = item["query"]
        relevant_urls = set(item["relevant_urls"])

        # 1️⃣ Intent extraction (same as backend)
        max_duration = extract_max_duration_minutes(query)
        soft_skill_intent = has_soft_skill_intent(query)

        # 2️⃣ Embed query
        query_embedding = embed_query(query)

        # 3️⃣ Over-retrieve
        candidates = search(
            query_embedding,
            top_k=RETRIEVAL_K,
            max_duration=max_duration,
            soft_skill_intent=soft_skill_intent
        )

        # 4️⃣ Rerank
        reranked = rerank(query, candidates, top_k=RETRIEVAL_K)

        # 5️⃣ Balance + cut to TOP_K
        final_results = balance_by_test_type(reranked, top_k=TOP_K)

        # 6️⃣ Extract URLs
        retrieved_urls = [r["url"] for r in final_results]

        # 7️⃣ Recall@10
        recall = recall_at_k(
            retrieved=retrieved_urls,
            relevant=relevant_urls,
            k=TOP_K
        )

        recalls.append(recall)

    mean_recall = sum(recalls) / len(recalls)

    print(f"Total queries evaluated: {len(train_data)}")
    print(f"\n📊 Mean Recall@{TOP_K}: {mean_recall:.4f}")


if __name__ == "__main__":
    main()
