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

---

## 🌱 Based on

The MVP version lives at:  
👉 https://github.com/james062ad/rag-from-scratch

That version is locked and represents the original assignment submission. This version is **safe to iterate on, deploy, and expand**.

---

## 📂 Project Structure (Same Base)

```text
rag-from-scratch-with-options/
├── ingestion/
├── retrieval/
├── src/
├── scripts/
├── .env.example
├── docker-compose.yml
├── pyproject.toml
└── README.md
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

### 3. Run the App

```bash
uvicorn src.main:app --reload
```

Test it at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

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
This branch is now open for rapid experimentation and feature enhancement. 🚀

