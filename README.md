# RAG from Scratch – Oxford LLMOps Assignment

A fully functional Retrieval-Augmented Generation (RAG) microservice built using core Python, FastAPI, PostgreSQL with pgvector, and OpenAI embeddings/GPT. This project was developed independently (without using the provided GitHub repo) to demonstrate full comprehension, modular design, and practical engineering capability.

---

## ✅ Features

- ✅ PostgreSQL + pgvector vector store (Dockerised)
- ✅ Ingestion of synthetic research abstracts
- ✅ OpenAI embedding for chunks and queries
- ✅ Vector similarity search (top-k)
- ✅ GPT-3.5 generation using retrieved context
- ✅ Exposed via `/generate` FastAPI endpoint
- ✅ Tested interactively with Swagger UI
- ✅ Modular and explainable pipeline with `.env` and Poetry

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/james062ad/rag-from-scratch.git
cd rag-from-scratch
```

### 2. Install Python Dependencies

```bash
poetry install
poetry shell
```

### 3. Start the Vector Database (Docker)

```bash
docker-compose up -d
```

### 4. (Optional) Ingest Synthetic Data

```bash
python ingestion/ingest_synthetic.py
```

### 5. Run the FastAPI Server

```bash
uvicorn src.main:app --reload
```

### 6. Test the Endpoint in Swagger

Open your browser at:  
👉 `http://127.0.0.1:8000/docs`

Try the `/generate` route with a query like:

```json
{ "query": "What are the benefits of using graphene in energy storage?" }
```

---

## 📂 Project Structure

```text
rag-from-scratch/
├── ingestion/            # Load & embed paper chunks
├── retrieval/            # Search & generate answer
├── src/                  # FastAPI app with /generate
├── scripts/              # Utility scripts (e.g. alter DB)
├── .env.example          # Safe environment config
├── docker-compose.yml    # Docker setup for Postgres
├── pyproject.toml        # Poetry environment
├── Final_Submission_Bundle.zip  # Submission-ready docs
```

---

## 🧠 Assignment & Book Alignment

This project fully satisfies all key requirements from the Oxford LLMOps Assignment:

| Requirement | Met |
|-------------|-----|
| PostgreSQL + pgvector | ✅ Step 3 |
| Embedding with OpenAI | ✅ Step 4, 6 |
| Query similarity search | ✅ Step 6 |
| GPT answer with context | ✅ Step 7 |
| Exposed FastAPI /generate | ✅ Step 8 |
| Structured modular code | ✅ Throughout |
| Book alignment: Ch. 4–8 | ✅ All |

---

## ✨ Optional Enhancements (Next Steps)

- 🔎 Add tracing and scoring with Opik
- 🧠 Ingest `papers-downloads/` and arXiv abstracts
- ⚙️ Add GitHub Actions CI pipeline
- 🌍 Deploy backend to Render or Hugging Face
- 💻 Add a frontend (Gradio or Lovable.dev)

---

## 🏁 Status

✅ MVP complete and fully working.  
🔄 Modular, explainable, deployable — ready for extension and demo.

