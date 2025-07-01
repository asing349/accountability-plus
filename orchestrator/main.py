import asyncio
import time
from typing import Dict

import http_clients as hc
import adapters as ad
from metrics import LATENCY, FAILURES

async def process_query(original_query: str) -> Dict:
    cache = await hc.vector_cache_probe(original_query)
    print("\n[ORCH] cache probe output:", cache)
    if cache.get("hits"):
        print("[ORCH] cache HIT, skipping pipeline.")
        record_id = cache["hits"][0]["id"]
        record = await hc.get_record_by_id(record_id)
        return {
            "query": original_query, # Added original query
            "cached": True,
            "vector_id": record_id,
            "summary_text": record.get("summarizer_output"),
            "entity_output": record.get("entity_output"),
            "websearch_output": record.get("websearch_output")
        }

    # === BEGIN: Vectorizer payload ===
    vectorizer_payload = {
        "query": original_query,
        "tags": None,
        "category": None,
        "scraper_output": None,
        "summarizer_output": None,
        "websearch_output": None,
        "entity_output": None
    }
    # === END: Vectorizer payload ===

    # --- Classifier ---
    print("\n[ORCH] classifier input:", original_query)
    t0 = time.perf_counter()
    try:
        cls_out = await hc.call_classifier(original_query)
        print("[ORCH] classifier output (raw):", cls_out)
    except Exception as e:
        FAILURES.labels("classifier").inc()
        print(f"[ERROR] MCP classifier failed: {e}")
        return {"error": f"classifier MCP failed: {e}"}
    LATENCY.labels("classifier").observe(time.perf_counter() - t0)

    # Update vec payload
    vectorizer_payload["tags"] = cls_out.get("tags", [])
    vectorizer_payload["category"] = cls_out.get("category", "")

    search_in = ad.classifier_to_query(cls_out, original_query)
    print("[ORCH] classifier_to_query (adapted):", search_in)

    # --- Search ---
    t0 = time.perf_counter()
    try:
        search_out = await hc.call_search(search_in)
        print("\n[ORCH] search output (raw):", search_out)
    except Exception as e:
        FAILURES.labels("search").inc()
        print(f"[ERROR] MCP search failed: {e}")
        return {"error": f"search MCP failed: {e}"}
    LATENCY.labels("search").observe(time.perf_counter() - t0)

    # Update vec payload
    vectorizer_payload["websearch_output"] = search_out

    scraper_in = ad.search_to_urls(search_out)
    print("[ORCH] search_to_urls (adapted):", scraper_in)

    # --- Scraper ---
    t0 = time.perf_counter()
    try:
        scrape_out = await hc.call_scraper(scraper_in)
        print("\n[ORCH] scraper output (raw):", scrape_out)
    except Exception as e:
        FAILURES.labels("scraper").inc()
        print(f"[ERROR] MCP scraper failed: {e}")
        return {"error": f"scraper MCP failed: {e}"}
    LATENCY.labels("scraper").observe(time.perf_counter() - t0)

    summarizer_in = ad.scraper_to_corpus(scrape_out)
    print("[ORCH] scraper_to_corpus (adapted):", summarizer_in)

    # Update vec payload
    # scraper_output must be a string: merged text, not a dict
    vectorizer_payload["scraper_output"] = summarizer_in.get("merged_text", "")

    # --- Summarizer ---
    t0 = time.perf_counter()
    try:
        sm_out = await hc.call_summarizer(summarizer_in)
        print("\n[ORCH] summarizer output (raw):", sm_out)
    except Exception as e:
        FAILURES.labels("summarizer").inc()
        print(f"[ERROR] MCP summarizer failed: {e}")
        return {"error": f"summarizer MCP failed: {e}"}
    LATENCY.labels("summarizer").observe(time.perf_counter() - t0)

    entity_in = ad.summarizer_to_summary_text(sm_out)
    print("[ORCH] summarizer_to_summary_text (adapted):", entity_in)

    # Update vec payload
    # summarizer_output must be a string, not dict; use raw_output if present
    if isinstance(sm_out, dict) and "raw_output" in sm_out:
        vectorizer_payload["summarizer_output"] = sm_out["raw_output"]
    else:
        vectorizer_payload["summarizer_output"] = str(sm_out)

    # --- Entity Extractor ---
    t0 = time.perf_counter()
    try:
        ent_raw = await hc.call_entity_extractor(entity_in)
        print("\n[ORCH] entity_extractor output (raw):", ent_raw)
        ent_out = ad.entity_output_adapter(ent_raw)
        print("[ORCH] entity_output_adapter (parsed):", ent_out)
    except Exception as e:
        FAILURES.labels("entity").inc()
        print(f"[ERROR] MCP entity_extractor failed: {e}")
        return {"error": f"entity_extractor MCP failed: {e}"}
    LATENCY.labels("entity").observe(time.perf_counter() - t0)

    # Update vec payload
    # entity_output is a dict, so just assign the adapted output
    vectorizer_payload["entity_output"] = ent_out

    # --- Vectorizer ---
    # (The existing code also does this, but now it's using your running payload variable)
    print("[ORCH] assemble_vectorizer_payload (adapted):", vectorizer_payload)
    t0 = time.perf_counter()
    try:
        vec_out = await hc.call_vectorizer(vectorizer_payload)
        print("\n[ORCH] vectorizer output (raw):", vec_out)
    except Exception as e:
        FAILURES.labels("vectorizer").inc()
        print(f"[ERROR] MCP vectorizer failed: {e}")
        return {"error": f"vectorizer MCP failed: {e}"}
    LATENCY.labels("vectorizer").observe(time.perf_counter() - t0)

    return {
        "query": original_query, # Added original query
        "cached": False,
        "vector_id": vec_out.get("id"),
        "summary_text": sm_out.get("raw_output") if isinstance(sm_out, dict) else sm_out,
        "entity_output": ent_out,
        "websearch_output": vectorizer_payload.get("websearch_output")
    }


if __name__ == "__main__":
    # Example usage
    async def main():
        query = "What happened to the USS Indianapolis?"
        result = await process_query(query)
        print("\n--- FINAL RESULT ---")
        print(result)

    asyncio.run(main())