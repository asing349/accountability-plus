import asyncio
import json
from typing import Any, Dict
import aiohttp

URLS: Dict[str, str] = {
    "classifier":   "http://mcp_classifier:8001/classify",
    "search":       "http://mcp_websearch:8006/search",
    "scraper":      "http://mcp_scraper:8002/scrape",
    "summarizer":   "http://mcp_summarizer:8003/summarize_case_raw",
    "entity":       "http://mcp_entity_extractor:8004/extract_raw",
    "vectorizer":   "http://mcp_vectorstore:8005/vectorize",
    "vectorstore":  "http://mcp_vectorstore:8005/query",
    "record":       "http://mcp_vectorstore:8005/record"  # New endpoint
}

# Define timeouts per MCP
SCRAPER_TIMEOUT = aiohttp.ClientTimeout(total=180)
DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=120)

HEADERS = {"Content-Type": "application/json"}
RETRIES = 3
BACKOFF = 0.5

async def _post(url: str, payload: Dict[str, Any], timeout: aiohttp.ClientTimeout) -> Dict[str, Any]:
    attempt = 0
    while attempt < RETRIES:
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=HEADERS) as r:
                    r.raise_for_status()
                    return await r.json()
        except Exception as exc:
            attempt += 1
            if attempt >= RETRIES:
                print(f"[http_clients] giving up on {url} – {exc}")
                return {}
            await asyncio.sleep(BACKOFF * (2 ** (attempt - 1)))

async def _get(url: str, timeout: aiohttp.ClientTimeout) -> Dict[str, Any]:
    attempt = 0
    while attempt < RETRIES:
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as r:
                    r.raise_for_status()
                    return await r.json()
        except Exception as exc:
            attempt += 1
            if attempt >= RETRIES:
                print(f"[http_clients] giving up on {url} – {exc}")
                return {}
            await asyncio.sleep(BACKOFF * (2 ** (attempt - 1)))

async def call_classifier(query: str) -> Dict[str, Any]:
    return await _post(URLS["classifier"], {"query": query}, DEFAULT_TIMEOUT)

async def call_search(query_payload: Dict[str, Any]) -> Dict[str, Any]:
    return await _post(URLS["search"], query_payload, DEFAULT_TIMEOUT)

async def call_scraper(url_list_payload: Dict[str, Any]) -> Dict[str, Any]:
    # Scraper gets 180s timeout
    return await _post(URLS["scraper"], url_list_payload, SCRAPER_TIMEOUT)

async def call_summarizer(corpus_payload: Dict[str, Any]) -> Dict[str, Any]:
    return await _post(URLS["summarizer"], corpus_payload, DEFAULT_TIMEOUT)

async def call_entity_extractor(summary_payload: Dict[str, Any]) -> Dict[str, Any]:
    return await _post(URLS["entity"], summary_payload, DEFAULT_TIMEOUT)

async def call_vectorizer(bundle_payload: Dict[str, Any]) -> Dict[str, Any]:
    return await _post(URLS["vectorizer"], bundle_payload, DEFAULT_TIMEOUT)

async def vector_cache_probe(query: str) -> Dict[str, Any]:
    return await _post(URLS["vectorstore"], {"query": query}, DEFAULT_TIMEOUT)

async def get_record_by_id(record_id: str) -> Dict[str, Any]:
    url = f'{URLS["record"]}/{record_id}'
    return await _get(url, DEFAULT_TIMEOUT)