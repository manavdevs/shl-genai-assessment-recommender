SHL GenAI Assessment Recommendation System

This project builds an intelligent recommendation system that suggests relevant SHL Individual Test Solutions based on a natural language query or job description.

The repository currently implements the complete data ingestion pipeline, producing a clean, structured dataset ready for semantic search and GenAI-powered recommendations.

📌 Current Phase: Data Ingestion

The goal of this phase is to programmatically extract all individual SHL assessments along with their detailed metadata from the SHL Product Catalog.

The resulting dataset is designed for downstream use in:

Embedding-based retrieval (FAISS)

LLM-assisted ranking and reasoning

API and frontend deployment

📂 Data Source

Website: https://www.shl.com/products/product-catalog/

Scope: Individual Test Solutions only
(Pre-packaged job solutions are intentionally excluded)

🏗 Architecture
Step 1 — Catalog Scraping

File: ingestion/scrape_catalog.py

Iterates through paginated SHL catalog (start=0, 12, 24, …)

Extracts:

Assessment name

Assessment URL

Test type (K, S, P, etc.)

Remote testing support

Adaptive support

Handles pagination edge cases

Deduplicates assessments across pages

Safely terminates scraping at catalog end

📄 Output

data/raw/assessments_listing.json

Step 2 — Assessment Detail Scraping

File: ingestion/scrape_details.py

Visits each assessment detail page

Extracts:

Description

Assessment duration (minutes)

Job levels

Languages

Test type (validated from detail page)

Uses multiple fallback selectors to handle HTML inconsistencies

Gracefully handles missing fields

📄 Output

data/processed/assessments_full.json

Step 3 — Dataset Merging & Enrichment

File: ingestion/merge_assessments.py

Reads catalog listings

Enriches each assessment with detailed metadata

Produces the final structured dataset

Implements rate limiting and error handling

📄 Final Output

data/processed/assessments_full.json

📊 Final Dataset Schema
{
  "name": "ASP.NET 4.5",
  "url": "https://www.shl.com/products/product-catalog/view/asp-net-4-5/",
  "test_type": ["K"],
  "remote_support": "Yes",
  "adaptive_support": "Yes",
  "description": "...",
  "duration_minutes": 30,
  "job_levels": [
    "Professional Individual Contributor",
    "Mid-Professional"
  ],
  "languages": [
    "English (USA)"
  ]
}

▶️ How to Run
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run catalog scraper
python ingestion/scrape_catalog.py

3️⃣ Run assessment enrichment
python ingestion/merge_assessment.py

⚠️ Assumptions & Limitations

Some assessments do not expose duration or job levels; fields may be null

Skills are not explicitly listed on most assessment pages and are therefore omitted

Pagination behavior is inconsistent; safeguards are added to prevent premature termination

Scraping respects rate limits using request delays

🚀 Planned Next Steps

Embed assessment descriptions using a language model

Implement semantic retrieval using FAISS

Add LLM-based reranking

Expose recommendations via FastAPI

Build a lightweight Streamlit frontend

Evaluate using Recall@K metrics

👤 Author

Manav Karwa