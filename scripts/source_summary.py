import os
import psycopg2
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

DB_PARAMS = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT", 5432),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

def count_sources():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("SELECT source FROM papers")
        results = cur.fetchall()
        sources = [row[0] or "unknown" for row in results]
        counts = Counter(sources)
        print("\n📊 Source Breakdown:\n")
        for source, count in counts.items():
            print(f"✅ {source:<10}: {count}")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    count_sources()
