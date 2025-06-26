import os
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
FIXED_TEMPERATURE = 0.3
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", 0.6))

app = FastAPI()

class ClassifyRequest(BaseModel):
    query: str
    model: str | None = None

class ClassifyResponse(BaseModel):
    categories: list[str]
    confidence: float
    tags: list[str]
    status: str
    model_used: str

@app.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest):
    model_to_use = req.model or DEFAULT_MODEL
    prompt = (
        "Classify the following user query into ONE best-fit category from this list: "
        "crime, accident, politics, legal, protest, other. "
        "For that best category, provide a confidence score (float between 0.5 and 1.0, never zero) and the three most relevant tags (short keywords or entities). "
        "Then, specify the next best DIFFERENT category from the list above (not the first one). "
        "Return JSON in this format: "
        "{\"categories\": [category1, category2], \"confidence\": <float for category1 only>, \"tags\": [tag1, tag2, tag3]} "
        "Example: {\"categories\": [\"crime\", \"accident\"], \"confidence\": 0.93, \"tags\": [\"Las Vegas\", \"shooting\", \"2017\"]} "
        f"User query: {req.query}"
    )
    payload = {
        "model": model_to_use,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": FIXED_TEMPERATURE,
            "num_predict": 128
        }
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()
        response_text = data["response"]
        fixed_json = response_text.replace("'", '"')
        # --- Robust extraction of the first JSON object ---
        json_match = re.search(r'\{.*?\}', fixed_json, re.DOTALL)
        if not json_match:
            raise HTTPException(status_code=500, detail="No JSON object found in LLM response")
        json_str = json_match.group(0)
        import json as pyjson
        result = pyjson.loads(json_str)
        categories = result.get("categories", [])[:2] if isinstance(result.get("categories", []), list) else []
        confidence = result.get("confidence", 0)
        if isinstance(confidence, dict):
            confidence = list(confidence.values())[0] if confidence else 0
        if not isinstance(confidence, (float, int)):
            try:
                confidence = float(confidence)
            except Exception:
                confidence = 0
        tags = result.get("tags", [])[:3] if isinstance(result.get("tags", []), list) else []
        # Apply confidence threshold
        if not categories:
            status = "unknown"
        elif confidence < MIN_CONFIDENCE:
            status = "low_confidence"
        else:
            status = "ok"
        return ClassifyResponse(
            categories=categories,
            confidence=confidence,
            tags=tags,
            status=status,
            model_used=f"ollama:{model_to_use}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
