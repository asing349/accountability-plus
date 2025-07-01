from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware # Import CORS
import json

from main import process_query   # Import from main.py in the same folder
from metrics import start_metrics_server
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Orchestrator")
start_metrics_server(9000)

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000", # Allow requests from your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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