import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

# Load .env environment variables
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# PostgreSQL connection config
DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# --- 1. Define the test query ---
query = "What are the energy storage benefits of graphene?"

# --- 2. Embed the query using OpenAI ---
def embed_query(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# --- 3. Perform vector search in pgvector-enabled table ---
def retrieve_top_chunks(query_vector, top_k=3):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # SQL with correct vector casting
        cursor.execute("""
            SELECT title, summary, chunk
            FROM papers
            ORDER BY embedding <-> %s::vector
            LIMIT %s;
        """, (query_vector, top_k))

        results = cursor.fetchall()
        return results

    except Exception as e:
        print("❌ Error during retrieval:", e)
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# --- 4. Run the search ---
if __name__ == "__main__":
    print("🔍 Embedding query...")
    embedded_query = embed_query(query)

    print("📥 Retrieving top chunks from database...")
    top_chunks = retrieve_top_chunks(embedded_query, top_k=3)

    print("\n🧠 Top Relevant Chunks:")
    for i, (title, summary, chunk) in enumerate(top_chunks, start=1):
        print(f"\n#{i}")
        print(f"Title: {title}")
        print(f"Summary: {summary}")
        print(f"Chunk: {chunk}")
