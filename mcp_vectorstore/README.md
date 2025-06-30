# MCP Vectorstore

## Overview

**Vectorstore MCP (Microservice Control Point)** is a modular, stateless microservice for storing, embedding, and semantically searching case-related data. It is designed to serve as a vector database and retrieval-augmented generation (RAG) cache for the MCP pipeline, enabling fast similarity search and retrieval of relevant cases or articles.

- **Purpose:** Store and embed aggregated case data, and provide semantic search over stored records.
- **How:** Uses the `nomic-embed-text` model (via Ollama) to generate embeddings, and stores them in a PostgreSQL database (with pgvector or similar extension).
- **Why MCP:** Exposes `/vectorize` and `/query` endpoints, making it easy to orchestrate, scale, or replace as part of a multi-stage pipeline.

---

## Models Used

- **Embedding Model:** `nomic-embed-text` (served via Ollama, configurable via `OLLAMA_MODEL_VEC` environment variable)
- **Vector Dimension:** Default 768 (configurable via `VECTOR_DIM` environment variable)
- **Database:** PostgreSQL (with vector support, e.g., pgvector)

---

## How It Works

1. **/vectorize**: Accepts a batch of case/article data, generates an embedding, and stores the record with a UUID.
2. **/query**: Accepts a query string, generates an embedding, and returns the most similar stored records based on vector similarity.

---

## API Usage

### 1. `/vectorize` (POST)

**Request:**

```json
{
  "query": "Las Vegas shooting case 2017",
  "tags": ["Las Vegas", "mass shooting", "2017"],
  "category": "crime",
  "scraper_output": "...",
  "summarizer_output": "...",
  "websearch_output": { ... },
  "entity_output": { ... }
}
```

**Response:**

```json
{
  "id": "65388143-fb82-4167-9032-fada80aa2cae",
  "query": "Las Vegas shooting case 2017",
  "message": "Embedding generated and stored. Use the UUID for retrieval.",
  "timestamp": "2025-06-30T01:51:29.487262"
}
```

---

### 2. `/query` (POST)

**Request:**

```json
{
  "query": "Las Vegas Mass Shooting",
  "top_k": 1
}
```

**Response:**

```json
{
  "hits": [
    {
      "id": "65388143-fb82-4167-9032-fada80aa2cae",
      "query": "Las Vegas shooting case 2017",
      "score": 0.545455
    }
  ]
}
```

---

## Response Structure

- **/vectorize** returns a UUID and confirmation message for the stored embedding.
- **/query** returns a list of the most similar stored queries, each with its UUID, original query, and similarity score.

---

## Notes

- The embedding model and Ollama endpoint are configurable via environment variables (`OLLAMA_MODEL_VEC`, `OLLAMA_BASE_URL`).
- The service is stateless and horizontally scalable.
- Designed for use in a pipeline with other MCPs (e.g., summarizer, classifier, entity extractor).
- Requires a PostgreSQL database with vector support (e.g., pgvector).
- For more details on deployment or integration, see the main project README or contact the maintainers.
