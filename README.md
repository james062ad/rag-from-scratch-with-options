
# 🧠 RAG from Scratch – Extended Edition: Project Summary & Reflection

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-ready-brightgreen?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-informational?logo=postgresql)
![Lovable](https://img.shields.io/badge/Frontend-Lovable.dev-ff69b4?logo=bolt)
![Status](https://img.shields.io/badge/System-Working-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue)


## 🔧 What We Built

This project expands on the basic RAG (Retrieval-Augmented Generation) assignment to create a **fully operational AI-powered research assistant**. The extended version includes:

- A **FastAPI backend** that supports:
  - GPT-based response generation from user queries
  - Vector-based similarity search using pgvector
  - Synthetic paper ingestion and embedding
- A **PostgreSQL vector database** (Dockerized) with `pgvector`
- A **Lovable.dev frontend** to interactively:
  - Ask research questions
  - Retrieve context chunks
  - Display LLM-generated answers
- A full **development workflow** using:
  - `poetry` for dependency management
  - `.env` and `.env.example` for clean configuration
  - `ngrok` for public testing from a local backend

## ⚠️ Challenges Faced (and How We Solved Them)

| Issue | Resolution |
|-------|------------|
| ❌ Internal Server Errors (500) | Mismatch between database column name (`chunk` vs `text`) in SQL queries. Fixed by inspecting schema using `\d papers`. |
| ❌ HEAD Requests Failing (405) | The FastAPI backend only supports `POST`, not `HEAD`. Updated Lovable’s `checkServerStatus` function to use `POST`. |
| ❌ Ngrok Disconnection | New tunnels required re-pasting the URL into Lovable. Handled with clear ngrok instructions and prompts. |
| ❌ Vector column casting issues | `embedding` column was not updated to `vector(1536)`. Resolved via custom script `alter_embedding_column.py`. |
| ❌ Misconfigured `.env` | Default `POSTGRES_USER` was not aligned with the Docker setup. Updated to use `myuser`, `mypassword`, `mydb`. |
| ❌ JSON decoding errors | Caused by malformed or empty POST payloads. Fixed with improved validation and Swagger testing. |

## ✅ Assignment Objectives (Extended)

| Requirement | Met? | Where? |
|-------------|------|--------|
| PostgreSQL + pgvector | ✅ | Docker + `init_pgvector.sql` |
| Embedding with OpenAI | ✅ | `get_query_embedding()` |
| Vector similarity search | ✅ | `retrieve_top_chunks()` |
| GPT answer generation | ✅ | `/generate` endpoint |
| FastAPI server | ✅ | `src/main.py` |
| Config via `.env` | ✅ | `.env`, `.env.example` |
| Poetry setup | ✅ | `pyproject.toml` |
| Optional frontend | ✅ | Lovable.dev interface |
| Remote testing (optional) | ✅ | `ngrok` integration |
| Optional tools | ✅ | `check_schema.py`, `alter_embedding_column.py` |

## 📚 Alignment with *Designing LLM Applications with LangChain*

| Book Concept | This Project |
|--------------|--------------|
| **RAG Pipeline** | Custom-built, no LangChain |
| **Retriever design** | PostgreSQL + pgvector + cosine distance |
| **Chunk management** | Synthetic ingestion and embedding |
| **Prompt templating** | Fixed format in backend |
| **Multi-stage reasoning** | Future roadmap potential |
| **Frontend integration** | Achieved using Lovable.dev |
| **Edge deployment** | Tested via ngrok tunnel |

## 💡 Lessons Learned

- A mismatch between schema and assumptions (like missing `text` columns) can silently break a backend — **check with `\d` first**.
- `HEAD` requests aren’t always supported by FastAPI routes — use `POST` for server status checks when needed.
- Environment and tooling setup (Docker, Poetry, Ngrok) are **essential for smooth development** — automation and logs save hours.
- Testing with **Swagger** is critical before connecting to frontends like **Lovable**.

## ✅ Current Status

✅ Working end-to-end:  
- Ask a question  
- Retrieve relevant chunks  
- Generate GPT-based response  
- Visualize results in frontend

---

## 📘 Conceptual Overview

Want to understand how the backend, database, GPT, and frontend all connect?

👉 [Click here to read the full system overview](./RAG_Conceptual_Overview.md)

------

## 📝 To-Do (Post-MVP Enhancements)

- [ ] Investigate why `chunks_used` is sometimes empty
  - Possibly adjust `top_k`, similarity threshold, or fallback logic
  - Ensure source filtering matches indexed data

- [ ] Add chunk relevance scoring and display (e.g. similarity scores)

- [ ] Enhance ingestion logging with per-source summary

- [ ] Add flag to generate from GPT only (without retrieval) for testing

- [ ] Deploy backend and frontend for public demo

- [ ] 🕒 Add “Last ArXiv Sync” panel to Lovable frontend
  - Show last ingestion timestamp for visibility
  - Backend should expose `/last-sync` API

- [ ] 📥 Add “Trigger Ingestion” button to Lovable
  - Calls `/trigger-arxiv-sync` endpoint in FastAPI
  - Useful for tutor testing + visibility

- [ ] 📊 Show ArXiv source document count
  - e.g. “ArXiv: 42 docs” — proves ingestion growth

- [ ] (Optional) 🧠 Add ingestion history modal or JSON log
