import os
import json
import openai
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI settings
openai.api_key = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = "text-embedding-ada-002"

# DB config
DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

def embed(text):
    response = openai.Embedding.create(input=text, model=EMBED_MODEL)
    return response["data"][0]["embedding"]

def insert_paper(conn, title, summary, chunk, embedding, source):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO papers (title, summary, chunk, embedding, source)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, summary, chunk, embedding, source))
        conn.commit()

def ingest_tutor_data():
    data_dir = "data-downloads"
    conn = psycopg2.connect(**DB_PARAMS)
    source_tag = "tutor"

    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                papers = json.load(f)
                for paper in papers:
                    title = paper.get("title", "").strip()
                    summary = paper.get("summary", "").strip()

                    if not summary:
                        continue

                    chunk = summary  # Use summary as chunk
                    embedding = embed(chunk)
                    insert_paper(conn, title, summary, chunk, embedding, source_tag)
                    print(f"✅ Inserted: {title}")

    conn.close()
    print("🎉 All tutor papers ingested.")

if __name__ == "__main__":
    ingest_tutor_data()
