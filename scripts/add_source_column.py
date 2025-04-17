import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection params
DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# Connect and run ALTER TABLE to add the source column
try:
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("""
        ALTER TABLE papers
        ADD COLUMN IF NOT EXISTS source TEXT;
    """)
    conn.commit()
    print("✅ 'source' column added to 'papers' table.")
except Exception as e:
    print("❌ Failed to add column:", e)
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
