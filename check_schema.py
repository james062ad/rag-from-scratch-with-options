import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port=os.getenv("POSTGRES_PORT", 5432)
)
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'papers'")
columns = [row[0] for row in cur.fetchall()]
required = {"chunk", "summary", "embedding"}

missing = required - set(columns)
if missing:
    print(f"❌ Missing columns: {missing}")
else:
    print("✅ Schema looks good!")