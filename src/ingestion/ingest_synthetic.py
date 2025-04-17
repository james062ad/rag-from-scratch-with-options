import os
import json
import openai
import psycopg2
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-ada-002"

# DB connection params
DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

def get_embedding(text: str) -> list:
    response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response["data"][0]["embedding"]

def insert_paper(conn, title, summary, chunk, embedding):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO papers (title, summary, chunk, embedding)
            VALUES (%s, %s, %s, %s)
        """, (title, summary, chunk, embedding))
        conn.commit()

def load_and_insert_all():
    conn = psycopg2.connect(**DB_PARAMS)

    folder = "data-downloads"
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                papers = json.load(f)
                for paper in papers:
                    title = paper.get("title", "")
                    summary = paper.get("summary", "")
                    chunks = paper.get("chunks", [])
                    for chunk in chunks:
                        emb = get_embedding(chunk)
                        insert_paper(conn, title, summary, chunk, emb)
                    print(f"✅ Inserted {len(chunks)} chunks from: {title}")
    conn.close()
    print("🚀 All files processed.")

if __name__ == "__main__":
    load_and_insert_all()
