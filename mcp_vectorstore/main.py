"""
Vectorizer MCP
Endpoints:
    POST /vectorize  – store a new aggregated record + embedding
    POST /query      – semantic search for cache / RAG retrieval
"""
#main.py
import os
import uuid
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from fastapi import HTTPException

import httpx
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from db_utils import get_pg_conn
from embedding import embed_text

# ─────────────────────────── FastAPI setup ────────────────────────────
app = FastAPI(title="Vectorizer MCP", version="0.1.0")

VECTOR_DIM = int(os.getenv("VECTOR_DIM", 768))
SIM_THRESHOLD = float(os.getenv("CACHE_SIM_THRESHOLD", 0.9))  # 90 % match


# ─────────────────────────── Pydantic models ──────────────────────────
class VectorizeBody(BaseModel):
    query: str = Field(..., min_length=1)
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    scraper_output: Optional[str] = None
    summarizer_output: Optional[str] = None
    websearch_output: Optional[dict] = None
    entity_output: Optional[dict] = None


class VectorizeResponse(BaseModel):
    id: str
    query: str
    message: str
    timestamp: datetime


class QueryBody(BaseModel):
    query: str
    top_k: int = 3


class QueryHit(BaseModel):
    id: str
    query: str
    score: float


class QueryResponse(BaseModel):
    hits: List[QueryHit]


class RecordResponse(BaseModel):
    query: str
    summarizer_output: Optional[str] = None
    entity_output: Optional[dict] = None
    scraper_output: Optional[str] = None
    websearch_output: Optional[dict] = None


# ───────────────────────────── Endpoints ──────────────────────────────
@app.post("/vectorize", response_model=VectorizeResponse)
def vectorize(body: VectorizeBody):
    """Store a new aggregated record and its embedding; return UUID."""
    # Combine everything into one big context string
    all_parts = [
        body.query,
        " ".join(body.tags or []),
        body.category or "",
        body.scraper_output or "",
        body.summarizer_output or "",
    ]
    if body.websearch_output:
        all_parts.append(str(body.websearch_output))
    if body.entity_output:
        all_parts.append(str(body.entity_output))

    all_text = " ".join(filter(None, all_parts))

    # Generate embedding
    embedding = embed_text(all_text)
    if len(embedding) != VECTOR_DIM:
        raise HTTPException(500, "Unexpected embedding dimension")

    record_id = str(uuid.uuid4())
    now = datetime.utcnow()

    # Insert into Supabase / Postgres
    print(f"[VECTORSTORE] websearch_output before insert: {body.websearch_output}")
    with get_pg_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO query_embeddings (
                id, query, tags, category, scraper_output,
                summarizer_output, websearch_output, entity_output,
                all_text, embedding, timestamp
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (query) DO NOTHING
            """,
            (
                record_id,
                body.query,
                body.tags,
                body.category,
                body.scraper_output,
                body.summarizer_output,
                psycopg2.extras.Json(body.websearch_output) if body.websearch_output is not None else None,
                psycopg2.extras.Json(body.entity_output) if body.entity_output else None,
                all_text,
                embedding,
                now,
            ),
        )

    return {
        "id": record_id,
        "query": body.query,
        "message": "Embedding generated and stored. Use the UUID for retrieval.",
        "timestamp": now,
    }

FUZZY_SIM_THRESHOLD = float(os.getenv("FUZZY_SIM_THRESHOLD", 0.35))

@app.post("/query", response_model=QueryResponse)
def query(body: QueryBody):
    with get_pg_conn() as conn, conn.cursor() as cur:
        # 1️⃣ set the similarity threshold (separate execute)
        cur.execute(
            "SET pg_trgm.similarity_threshold = %s;",
            (FUZZY_SIM_THRESHOLD,)
        )

        # 2️⃣ run the fuzzy-search query
        cur.execute(
            """
            SELECT  id,
                    query,
                    similarity(query, %s) AS score
            FROM    query_embeddings
            WHERE   query %% %s        -- note the double %% !
            ORDER BY score DESC
            LIMIT   %s;
            """,
            (body.query, body.query, body.top_k),
        )
        rows = cur.fetchall()

    hits = [
        QueryHit(id=str(row[0]), query=row[1], score=float(row[2]))
        for row in rows
    ]
    return {"hits": hits}


@app.get("/record/{record_id}", response_model=RecordResponse)
def get_record(record_id: uuid.UUID):
    """Retrieve a specific record by its UUID."""
    with get_pg_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT query, summarizer_output, entity_output, scraper_output, websearch_output
            FROM query_embeddings
            WHERE id = %s
            """,
            (str(record_id),),
        )
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Record not found")

    return RecordResponse(
        query=row[0],
        summarizer_output=row[1],
        entity_output=row[2],
        scraper_output=row[3],
        websearch_output=row[4]
    )


@app.get("/healthz")
def health():
    return {"ok": True}


if __name__ == "__main__":
    # Example usage
    # ... (omitted for brevity)
    pass