from fastapi import FastAPI
from pydantic import BaseModel
from graph import build_graph

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
            return {
                "cached": True,
                "vector_id": result["vector_id"]
            }
        return {
            "cached": False,
            "vector_id": result["vector_out"].get("id") if result.get("vector_out") else None,
            "summary_text": result.get("sm_out"),
            "entity_output": result.get("ent_out")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
