# src/retrieval/generate_answer.py

import openai
import os

# Load your API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_query_embedding(query: str) -> list[float]:
    """
    Embeds a text query using the OpenAI Embedding API.
    Returns the embedding vector.
    """
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]
