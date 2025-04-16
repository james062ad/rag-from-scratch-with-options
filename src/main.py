from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import psycopg2
import os

# Load environment variables from .env
load_dotenv()

# Create FastAPI app instance
app = FastAPI()

# PostgreSQL connection config
DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class QueryRequest(BaseModel):
    query: str

# --- Helper Functions ---

# Embed query using OpenAI
def embed_query(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Retrieve top-k chunks from pgvector-enabled DB
def retrieve_top_chunks(query_vector, top_k=3):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, summary, chunk
            FROM papers
            ORDER BY embedding <-> %s::vector
            LIMIT %s;
        """, (query_vector, top_k))

        return cursor.fetchall()
    except Exception as e:
        print("❌ Retrieval error:", e)
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# Build prompt for OpenAI GPT
def build_prompt(query, chunks):
    context = "\n---\n".join([f"{chunk}" for (_, _, chunk) in chunks])
    return (
        f"You are a helpful research assistant.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{query}\n\n"
        f"Answer:"
    )

# Generate final answer using OpenAI GPT
def generate_answer(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- FastAPI Route ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG app!"}

@app.post("/generate")
def generate(query_request: QueryRequest):
    query = query_request.query
    query_vector = embed_query(query)
    top_chunks = retrieve_top_chunks(query_vector)
    prompt = build_prompt(query, top_chunks)
    answer = generate_answer(prompt)

    return {
        "query": query,
        "answer": answer,
        "chunks_used": [chunk for (_, _, chunk) in top_chunks]
    }
