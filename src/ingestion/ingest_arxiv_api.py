import os
import requests
import openai
import psycopg2
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI setup
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
        cur.execute(
            """
            INSERT INTO papers (title, summary, chunk, embedding, source)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (title, summary, chunk, embedding, source)
        )
        conn.commit()

def fetch_arxiv(query="graphene", max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    entries = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        summary = entry.find("atom:summary", ns).text.strip()
        entries.append({"title": title, "summary": summary})
    return entries

def ingest_arxiv_data():
    conn = psycopg2.connect(**DB_PARAMS)
    source_tag = "arxiv"
    papers = fetch_arxiv(query="graphene", max_results=10)

    for paper in papers:
        title = paper["title"]
        summary = paper["summary"]
        chunk = summary  # treat summary as the chunk
        embedding = embed(chunk)
        insert_paper(conn, title, summary, chunk, embedding, source_tag)
        print(f"✅ Inserted: {title}")

    conn.close()
    print("🎉 ArXiv papers ingestion complete.")

if __name__ == "__main__":
    ingest_arxiv_data()