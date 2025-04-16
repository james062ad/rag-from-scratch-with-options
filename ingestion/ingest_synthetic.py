import os
from dotenv import load_dotenv
from openai import OpenAI
import psycopg2

# Load environment variables
load_dotenv()

# Setup OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# PostgreSQL connection parameters
DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# --- 1. Define synthetic examples ---
synthetic_papers = [
    {
        "title": "Advances in Perovskite Solar Cells",
        "summary": "Recent developments have significantly improved efficiency and stability...",
        "chunks": [
            "Perovskite materials are revolutionising solar cell design due to their high light absorption.",
            "Challenges remain in moisture sensitivity and scale-up manufacturing processes."
        ]
    },
    {
        "title": "Graphene Applications in Energy Storage",
        "summary": "Graphene-based electrodes offer high conductivity and surface area...",
        "chunks": [
            "Graphene supercapacitors store energy by fast surface charge accumulation.",
            "Integration with lithium-ion systems remains an area of active research."
        ]
    }
]

# --- 2. Embedding Function ---
def embed_text(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# --- 3. Insert into DB ---
def insert_into_db(paper):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        for chunk in paper["chunks"]:
            embedding = embed_text(chunk)

            cursor.execute("""
                INSERT INTO papers (title, summary, chunk, embedding)
                VALUES (%s, %s, %s, %s)
            """, (paper["title"], paper["summary"], chunk, embedding))

        conn.commit()
        print(f"Inserted: {paper['title']}")

    except Exception as e:
        print(f"Error inserting: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# --- 4. Run Ingestion ---
if __name__ == "__main__":
    for paper in synthetic_papers:
        insert_into_db(paper)
