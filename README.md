# RAG from Scratch – Extended Edition 🧪✨

This repository builds on the MVP version of the RAG system submitted for the Oxford LLMOps assignment.

It serves as a sandbox for exploring optional enhancements and advanced features including UI integration, live data ingestion, LLMOps, and CI/CD.

---

## 🔍 What This Repo Adds

- ✅ Frontend integration via Lovable.dev or Gradio
- ✅ Modular expansion of ingestion sources (arXiv, papers-downloads/)
- ✅ Optional LLMOps support via Opik for tracing and scoring
- ✅ Planned GitHub Actions for CI
- ✅ Additional components for deployment to Hugging Face or Render
- ✅ Schema validation tools to catch DB/backend mismatches

---

## 🌱 Based on

The MVP version lives at:  
👉 https://github.com/james062ad/rag-from-scratch

That version is locked and represents the original assignment submission. This version is **safe to iterate on, deploy, and expand**.

---

## 📂 Project Structure

```text
rag-from-scratch-with-options/
├── ingestion/
├── retrieval/
├── src/
├── scripts/
├── .env.example
├── RAG_Checklist.md        ✅
├── check_schema.py         ✅
├── docker-compose.yml
├── pyproject.toml
├── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/james062ad/rag-from-scratch-with-options.git
cd rag-from-scratch-with-options
```

### 2. Set Up Poetry and Docker

```bash
poetry install
poetry shell
docker-compose up -d
```

### 3. Ingest Test Data

```bash
python ingestion/ingest_synthetic.py
```

### 4. Run the App

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Then visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 💬 Query Example (POST `/generate`)

```json
{
  "query": "How does graphene support energy storage?"
}
```

Expected Response:

```json
{
  "query": "...",
  "answer": "...",
  "chunks_used": [ "...", "...", "..." ]
}
```

---

## 🛡️ Schema Validation Tools

To prevent database mismatches (like referencing non-existent columns), this project includes:

### 📋 `RAG_Checklist.md`
- Preflight DB + backend alignment checklist
- Covers `.env`, Docker, schema inspection, and test flow

### 🧪 `check_schema.py`
- Python script to check for required columns in the `papers` table
- Helps ensure `chunk`, `summary`, and `embedding` exist

To run:

```bash
python check_schema.py
```

---

## 💡 Ideas to Explore

- 🌐 Host backend on Render
- 🌸 Build UI in Gradio / Lovable.dev
- 📈 Add Opik tracing
- 🔄 Schedule ingestion from arXiv RSS feeds
- 🧪 Add LLM evaluation or scoring rules

---

## 🧠 Why This Matters

This repo demonstrates technical curiosity, engineering control, and passion for learning beyond minimum submission requirements. It showcases professional dev practices while remaining grounded in explainability and modularity.

---

## 🏁 Status

MVP cloned and bootstrapped.  
This branch is now open for experimentation and deployment. 🚀
