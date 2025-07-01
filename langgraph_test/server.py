from fastapi import FastAPI
from pydantic import BaseModel
from graph import build_graph
import http_clients as hc # Import http_clients

app = FastAPI(title="LangGraph Orchestrator", version="0.1.0")
workflow = build_graph()

class QueryInput(BaseModel):
    query: str

@app.post("/process")
async def process_query(payload: QueryInput):
    try:
        # ---- KEY: initialize vec_payload! ----
        initial_state = {
            "query": payload.query,
            "vec_payload": {
                "query": payload.query,
                "tags": None,
                "category": None,
                "scraper_output": None,
                "summarizer_output": None,
                "websearch_output": None,
                "entity_output": None
            }
        }
        result = await workflow.ainvoke(initial_state)
        
        # Return structure identical to your main.py
        if result.get("cached"):
            record_id = result["vector_id"]
            record = await hc.get_record_by_id(record_id)
            return {
                "query": payload.query, # Original query
                "cached": True,
                "vector_id": record_id,
                "summary_text": record.get("summarizer_output"),
                "entity_output": record.get("entity_output"),
                "websearch_output": record.get("websearch_output")
            }
        
        # For non-cached results, extract from the final state
        sm_out = result.get("sm_out")
        entity_output = result.get("ent_out")
        websearch_output = result.get("vec_payload", {}).get("websearch_output")

        return {
            "query": payload.query, # Original query
            "cached": False,
            "vector_id": result["vector_out"].get("id") if result.get("vector_out") else None,
            "summary_text": sm_out.get("raw_output") if isinstance(sm_out, dict) else sm_out,
            "entity_output": entity_output,
            "websearch_output": websearch_output
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/healthz")
def health():
    return {"ok": True}


if __name__ == "__main__":
    # Example usage
    import asyncio
    async def main():
        test_query = "What happened to the USS Indianapolis?"
        result = await process_query(QueryInput(query=test_query))
        print("\n--- FINAL RESULT ---")
        print(result)
    asyncio.run(main())