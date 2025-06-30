from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import json

from main import process_query   # Import from main.py in the same folder
from metrics import start_metrics_server
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Orchestrator")
start_metrics_server(9000)

@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/metrics")
def metrics():
    return StreamingResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/process", response_class=StreamingResponse)
async def process(payload: dict):
    if "query" not in payload:
        raise HTTPException(400, "Need JSON {'query': ...}")

    async def _stream():
        result = await process_query(payload["query"])
        yield json.dumps(result)

    return StreamingResponse(_stream(), media_type="application/json")
