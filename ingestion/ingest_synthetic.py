import os
import psycopg2
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Synthetic papers
papers = [
    {
        "title": "Graphene Applications in Energy Storage",
        "summary": "Graphene-based electrodes offer high conductivity and surface area...",
        "chunk": "Integration with lithium-ion systems remains an area of active research."
    },
    {
        "title": "Advances in Perovskite Solar Cells",
        "summary": "Recent developments have significantly improved efficiency and stability...",
        "chunk": "Perovskite materials are revolutionising solar cell design due to their high light absorption."
    }
]

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "postgres"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432")
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    text TEXT,
    embedding VECTOR(1536)
);
""")
conn.commit()

# Insert synthetic data
for paper in papers:
    text = f"{paper['title']}\n{paper['summary']}\n{paper['chunk']}"
    print(f"📄 Inserting: {paper['title']}")

    # Generate OpenAI embedding
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response["data"][0]["embedding"]

    cur.execute(
        "INSERT INTO chunks (text, embedding) VALUES (%s, %s)",
        (text, embedding)
    )

conn.commit()
cur.close()
conn.close()

print("✅ Done ingesting synthetic papers.")
