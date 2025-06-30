import os
import httpx
from fastapi import HTTPException

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL_VEC", "nomic-embed-text")
TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", 30))


def embed_text(text: str) -> list[float]:
    """Call Ollama's /api/embeddings endpoint and return the embedding vector."""
    payload = {"model": OLLAMA_MODEL, "prompt": text}
    try:
        r = httpx.post(f"{OLLAMA_URL}/api/embeddings", json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()["embedding"]
    except Exception as exc:
        raise HTTPException(502, f"Ollama embed error: {exc}")
