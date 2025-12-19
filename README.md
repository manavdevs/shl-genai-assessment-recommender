# SHL GenAI Assessment Recommendation System

This project builds an intelligent recommendation system that suggests relevant **SHL Individual Test Solutions** based on a natural language job description or query.

The repository currently implements the **complete core retrieval pipeline**, producing high-quality, ranked assessment recommendations using modern GenAI techniques.

---

## 🔍 Problem Overview

Recruiters and hiring managers often struggle to identify the most suitable assessments for a given role from a large catalog.

This system solves that by:
- Accepting a free-text job description
- Understanding semantic intent using embeddings
- Retrieving relevant assessments efficiently
- Reranking results using an LLM for true job relevance

---

## 🧠 System Architecture

User Query
↓
Query Embedding (Gemini)
↓
FAISS Vector Search (Top-N candidates)
↓
LLM-based Reranking (OpenAI)
↓  
FastAPI Recommendation API  
↓  
Streamlit Frontend  

This follows a **two-stage retrieval architecture**, which is industry standard for large-scale semantic search systems.

---

## ✅ Implemented Features (Current Phase)

### Step 1 — Data Ingestion
- Scraped SHL Product Catalog (Individual Test Solutions only)
- Extracted assessment metadata:
  - Name
  - URL
  - Test type
  - Remote & adaptive support
  - Description
  - Duration
  - Job levels
  - Languages
- Handled pagination edge cases and deduplication

📁 Output:
- `data/raw/assessments_listing.json`
- `data/processed/assessments_full.json`

---

### Step 2 — Embeddings & Vector Store
- Generated embeddings using **Gemini text-embedding-004**
- Built a **FAISS index** for fast similarity search
- Persisted index to disk

📁 Output:
- `data/processed/assessments_embeddings.json`
- `embeddings/faiss_index/index.bin`

---

### Step 3 — Semantic Retrieval
- Embedded user queries
- Retrieved semantically similar assessments using FAISS
- Verified vector dimensions and index consistency

---

### Step 4 — LLM-based Reranking
- Used **OpenAI (gpt-4o-mini)** to rerank FAISS candidates
- Ranked assessments based on true job relevance, not just similarity
- Produced final, ordered recommendations

This ensures that **similar ≠ relevant** results are filtered correctly.

---

### Step 5 — API & Frontend

#### 🔹 Backend (FastAPI)

- Exposes an Appendix-compliant REST API
- Endpoints:
  - `GET /health`
  - `POST /recommend`

All responses:
- Use JSON
- Return proper HTTP status codes
- Follow the required response schema

#### 🔹 Frontend (Streamlit)

- Interactive UI for entering job descriptions
- Displays ranked SHL assessments with full metadata
- Communicates with backend via HTTP API

---

## 🌐 API Specification (Appendix 2 Compliant)

### Health Check
```bash
GET /health
Response:
{
"status": "healthy"
}

```

### Recommendation Endpoint
```bash

POST /recommend
Content-Type: application/json

Body:
{
"query": "string",
"top_k": 5
}
```


Response:
```json
{
  "recommended_assessments": [
    {
      "name": "Core Java (Advanced Level)",
      "url": "https://www.shl.com/...",
      "description": "...",
      "duration": 30,
      "remote_support": "Yes",
      "adaptive_support": "No",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}
```

## 🧪 How to Run (Core Pipeline)

Install dependencies:
```bash
pip install -r requirements.txt
```

Run retrieval and reranking tests:

```bash
python -m retrieval.test_retrieval  
python -m reranking.test_rerank  
```

Run backend
```bash
uvicorn backend.main:app --reload  
```
Run frontend

```bash
streamlit run frontend/app.py  
```

Swagger UI available at:

http://127.0.0.1:8000/docs


## 📊 Evaluation (Upcoming)

- Recall@10 using the provided train/test dataset  

- Evaluation applied at:  

  -  Retrieval stage  

  - Final recommendation stage  

- Analysis of recommendation balance across test types (e.g., Knowledge & Skills vs Personality & Behaviour)

## ⚠️ Assumptions & Limitations

Some assessments do not expose duration or job level information

Skills are not explicitly listed on most SHL pages and are omitted

Scraping respects rate limits via request delays

Reranking uses a lightweight LLM to minimize cost

## 📌 Notes

- API runs over HTTP locally; HTTPS supported in production deployment  

- The system is modular, reproducible, and maintainable  

- Designed for easy extension and evaluation  


## 👤 Author

Manav Karwa