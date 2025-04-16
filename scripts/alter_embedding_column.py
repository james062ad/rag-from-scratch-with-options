import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# ✅ Corrected: Alter the right table (chunks)
sql = """
ALTER TABLE chunks
ALTER COLUMN embedding TYPE vector(1536);
"""

# Run the command
try:
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("✅ Column successfully updated to vector(1536) in 'chunks'")
except Exception as e:
    print("❌ Error:", e)
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
