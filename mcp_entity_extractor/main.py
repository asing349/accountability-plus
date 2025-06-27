# main.py
from fastapi import FastAPI, HTTPException, Request
import os, requests
from dotenv import load_dotenv
from prompts import PROMPT_TEMPLATE     # <-- import prompt here

load_dotenv(dotenv_path="../.env")      # adjust if needed

OLLAMA_HOST  = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL",   "mistral")

app = FastAPI()

@app.post("/extract_raw")
async def extract_raw(request: Request):
    try:
        data = await request.json()
        summary_text = data.get("summary_text", "")
        if not summary_text:
            raise HTTPException(status_code=400, detail="summary_text required")

        # Inject summary into the prompt template
        prompt = PROMPT_TEMPLATE.format(summary_text=summary_text)

        r = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model":  OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False        # single JSON response
            },
            timeout=120
        )
        if r.status_code != 200:
            raise RuntimeError(f"Ollama error {r.status_code}: {r.text}")

        output = r.json().get("response", "")
        return {"raw_output": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
