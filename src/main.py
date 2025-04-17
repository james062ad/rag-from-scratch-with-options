from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

from src.retrieval.retrieve_chunks import retrieve_top_chunks
from src.retrieval.generate_answer import get_query_embedding
from src.retrieval.db_utils import connect_db, ensure_pgvector

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# FastAPI app
app = FastAPI()

# CORS middleware (for Lovable or local frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure pgvector extension is enabled on DB
ensure_pgvector()

# Request body model
class QueryRequest(BaseModel):
    query: str
    source: str | None = None  # Optional source filter: "tutor", "arxiv", "synthetic", "all"

@app.post("/generate")
async def generate(request: QueryRequest):
    query = request.query
    source_filter = request.source

    # 1. Embed the query
    embedding = get_query_embedding(query)

    # 2. Retrieve top chunks from DB
    chunks = retrieve_top_chunks(embedding, source_filter=source_filter)

    # 3. Format context
    context = "\n\n".join([f"{chunk['text']}" for chunk in chunks])

    # 4. Build prompt
    prompt = f"""
You are a scientific assistant. Use only the following excerpts to answer the question.

{context}

Question: {query}
Answer:"""

    # 5. Call GPT
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful scientific assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    answer = completion.choices[0].message.content.strip()

    # 6. Return response
    return {
        "query": query,
        "source": source_filter,
        "answer": answer,
        "chunks_used": chunks
    }
