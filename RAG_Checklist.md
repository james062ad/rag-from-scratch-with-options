# ✅ RAG App: Pre-Launch Database & Backend Checklist

This checklist helps ensure the database schema and code match before deploying or testing your RAG system.

---

## 📋 Pre-Launch Checklist

### 🛠 DATABASE SETUP (PostgreSQL)

- [ ] **`.env` variables loaded**
  - Confirm with `echo $POSTGRES_DB` or via Python.

- [ ] **Access Docker container**
  ```bash
  docker exec -it rag-from-scratch-db-1 psql -U myuser -d mydb
  ```

- [ ] **List and inspect tables**
  ```sql
  \dt
  \d papers
  \d chunks
  ```

- [ ] **Verify column names**
  - Ensure columns like `chunk`, `summary`, `embedding` exist.

- [ ] **Optional: Export schema**
  ```bash
  pg_dump -U myuser -d mydb --schema-only > schema.sql
  ```

---

### 🔧 BACKEND CODE (FastAPI)

- [ ] **Check SQL queries for column usage**
  - Ensure `SELECT` statements use valid column names.

- [ ] **Consider SQLAlchemy or Alembic for schema syncing**

---

### 🧪 END-TO-END TESTING

- [ ] **Test POST in Swagger**
  - `http://127.0.0.1:8000/docs` → `/generate`

- [ ] **Expect 200 OK and valid JSON with keys `answer` and `chunks_used`**

- [ ] **Monitor logs**
  ```bash
  docker logs -f rag-from-scratch-db-1
  ```

---

## 🧪 Python Schema Validator

Run this script to validate required columns:

```bash
python check_schema.py
```

---

## ✅ check_schema.py

```python
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
```

---

For additional automation, consider Alembic or pgAdmin for visual schema management.