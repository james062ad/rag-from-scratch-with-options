import os
import openai
import psycopg2
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# PostgreSQL connection parameters
DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

# FastAPI setup
app = FastAPI()

# Allow CORS for testing with frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class Query(BaseModel):
    query: str

# 🔍 Embed query using OpenAI
def get_query_embedding(text: str) -> List[float]:
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]

# 🔍 Retrieve similar chunks from DB (🛠️ FIXED CASTING!)
def retrieve_top_chunks(embedding: List[float]) -> List[str]:
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # ✅ Explicit cast to ::vector
        cur.execute(
            "SELECT chunk FROM papers ORDER BY embedding <-> %s::vector LIMIT 3",
            (embedding,)
        )
        results = [row[0] for row in cur.fetchall()]
        return results
    except Exception as e:
        print("❌ Error retrieving chunks:", e)
        return []
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

# 🧠 Generate answer using GPT
def generate_answer(query: str, chunks: List[str]) -> str:
    context = "\n".join(chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

# 🚀 Endpoint
@app.post("/generate")
async def generate(data: Query):
    try:
        embedding = get_query_embedding(data.query)
        chunks = retrieve_top_chunks(embedding)
        answer = generate_answer(data.query, chunks)
        return {
            "query": data.query,
            "answer": answer,
            "chunks_used": chunks
        }
    except Exception as e:
        print("❌ Internal Server Error:", e)
        return {"error": "Internal Server Error"}, 500
