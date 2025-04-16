
# 🧠 RAG from Scratch – Extended Edition: Project Summary & Reflection

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

import os
import openai
import psycopg2
import numpy as np
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

app = FastAPI()

# Allow frontend tools like Lovable.dev or Swagger to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    query: str

# Embedding helper
def get_query_embedding(query: str):
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Chunk retriever
def retrieve_top_chunks(embedding, top_k=3):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    embedding_str = "[" + ",".join([str(x) for x in embedding]) + "]"

    sql = f"""
    SELECT chunk, embedding
    FROM papers
    ORDER BY embedding <-> %s
    LIMIT {top_k};
    """

    cur.execute(sql, (embedding_str,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in rows]

# GPT answer generator
def generate_gpt_answer(query, chunks):
    context = "\n\n".join(chunks)
    prompt = f"""You are an expert research assistant. Use the context below to answer the question.

Context:
{context}

Question: {query}

Answer:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": prompt }
        ]
    )
    return response['choices'][0]['message']['content']

# Endpoint
@app.post("/generate")
async def generate(req: QueryRequest):
    try:
        embedding = get_query_embedding(req.query)
        chunks = retrieve_top_chunks(embedding)
        answer = generate_gpt_answer(req.query, chunks)

        return {
            "query": req.query,
            "answer": answer,
            "chunks_used": chunks
        }
    except Exception as e:
        return {
            "error": str(e)
        }
