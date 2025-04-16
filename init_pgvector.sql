-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the main table for storing paper chunks
CREATE TABLE papers (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  chunk TEXT NOT NULL,
  embedding vector(384)
);
