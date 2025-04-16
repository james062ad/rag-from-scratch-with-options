import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
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

# --- 1. Embed query ---
def embed_query(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# --- 2. Retrieve top-k relevant chunks ---
def retrieve_top_chunks(query_vector, top_k=3):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, summary, chunk
            FROM papers
            ORDER BY embedding <-> %s::vector
            LIMIT %s;
        """, (query_vector, top_k))

        return cursor.fetchall()

    except Exception as e:
        print("❌ Retrieval error:", e)
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# --- 3. Format prompt for GPT ---
def build_prompt(query, chunks):
    context = "\n---\n".join([f"{chunk}" for (_, _, chunk) in chunks])
    prompt = (
        f"You are an assistant helping scientists summarise research.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{query}\n\n"
        f"Answer:"
    )
    return prompt

# --- 4. Generate answer using GPT ---
def generate_answer(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- 5. Run full RAG pipeline ---
if __name__ == "__main__":
    query = "What are the energy storage benefits of graphene?"

    print("🔍 Embedding query...")
    embedded_query = embed_query(query)

    print("📥 Retrieving relevant chunks...")
    top_chunks = retrieve_top_chunks(embedded_query, top_k=3)

    print("🧠 Building prompt...")
    final_prompt = build_prompt(query, top_chunks)

    print("🤖 Generating answer from GPT...")
    answer = generate_answer(final_prompt)

    print("\n💬 Final Answer:\n")
    print(answer)
