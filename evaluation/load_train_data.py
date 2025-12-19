import pandas as pd

def load_train_data(path: str):
    df = pd.read_excel(path, sheet_name="Train-Set")

    df.columns = [c.strip().lower() for c in df.columns]

    if "query" not in df.columns or "assessment_url" not in df.columns:
        raise ValueError("Train sheet must contain 'query' and 'assessment_url' columns")

    grouped = (
        df.groupby("query")["assessment_url"]
        .apply(list)
        .reset_index()
    )

    data = []
    for _, row in grouped.iterrows():
        data.append({
            "query": row["query"],
            "relevant_urls": row["assessment_url"]
        })

    return data
