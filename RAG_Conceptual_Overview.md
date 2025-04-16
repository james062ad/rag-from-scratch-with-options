# 🧠 Conceptual Overview: How the RAG System Works

## 1. 🧱 PostgreSQL + pgvector (Database)
This is your **knowledge store** — it contains the embedded chunks of research data that your RAG system retrieves when answering a query.

- **Why it’s used**:  
  Traditional SQL databases don’t support similarity search. `pgvector` allows you to store and search **vector embeddings** directly in PostgreSQL, so you can find chunks **"close" in meaning** to the user’s question.

- **How it fits**:  
  When a question is asked, the system embeds the query and runs a vector similarity search on the `embedding` column to retrieve the top-k relevant text chunks.

---

## 2. 🐍 FastAPI (API Server)
This is your **backend brain** — a Python service that handles incoming questions and returns answers.

- **Why it’s used**:  
  FastAPI is fast, minimal, and perfect for async tasks like embedding and GPT calls.

- **Key routes**:
  - `POST /generate`: Accepts a question, embeds it, runs similarity search on the DB, builds a prompt using retrieved chunks, sends it to OpenAI, and returns:
    ```json
    {
      "query": "...",
      "answer": "...",
      "chunks_used": [...]
    }
    ```

---

## 3. 🔐 OpenAI API
This is the **LLM brain** — you use it to generate embeddings and complete GPT responses.

- **Why it’s used**:
  - `Embedding API`: Turns the user query and text chunks into vector form.
  - `ChatCompletion API`: Given a prompt with retrieved text, it generates the final answer.

---

## 4. 📖 Swagger UI (FastAPI Docs)
This is your **interactive playground** for testing the backend.

- **Why it’s used**:  
  FastAPI automatically generates Swagger docs at `http://localhost:8000/docs`. You can:
  - Test the `POST /generate` route
  - See the curl request format
  - View JSON response data

---

## 5. 🌍 Ngrok (Tunnel for Public Access)
This is your **bridge to the internet** — it exposes your `localhost:8000` FastAPI app via a secure public URL.

- **Why it’s used**:  
  - So **Lovable.dev**, which runs in the browser (client-side), can talk to your FastAPI backend (server-side).
  - It bypasses firewalls or localhost restrictions.

- **How it works**:  
  When you run:
  ```bash
  ngrok http 8000
  ```
  You get a URL like:
  ```
  https://1234-5678-90.ngrok-free.app
  ```
  This is what Lovable uses in its fetch requests.

---

## 6. 💖 Lovable.dev Frontend
This is your **user-facing interface** — a no-code UI where users ask questions and see results.

- **Why it’s used**:
  - Offers a polished, public-friendly frontend
  - Fully integrated with backend via Ngrok URL

- **How it works**:
  - The user types a question
  - JavaScript sends a `POST` request to `/generate` using Ngrok URL
  - Displays:
    - ✍️ The question
    - 💡 The answer from GPT
    - 📄 The supporting chunks

- **Bonus features**:
  - "Check connection" (uses a test POST)
  - Debug logs
  - Error display if server unreachable

---

## 🔁 How It All Connects (High Level)

```
[User @ Lovable.dev] --> [POST /generate] --> [FastAPI]
                                             |
                                             |--> Embed query (OpenAI)
                                             |--> Search vectors (pgvector)
                                             |--> Compose prompt
                                             |--> Call GPT
                                             |--> Return answer + chunks
```

---

## ✅ Summary

| Component     | Role                                 | Why It Matters                          |
|---------------|--------------------------------------|------------------------------------------|
| PostgreSQL + pgvector | Stores embedded chunks           | Enables semantic search                 |
| FastAPI       | Backend API                          | Processes questions and delivers answers |
| OpenAI        | Embeds and answers                   | Core LLM intelligence                    |
| Swagger UI    | Test interface for API               | Developer debugging + verification       |
| Ngrok         | Tunnel from localhost to web         | Makes backend accessible to frontend     |
| Lovable.dev   | Frontend UI                          | User-facing query interface              |