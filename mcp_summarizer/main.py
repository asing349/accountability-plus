from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from summarizer import run_ollama
import traceback

app = FastAPI()

class SummarizeRequest(BaseModel):
    merged_text: str

@app.post("/summarize_case_raw")
def summarize_case_raw(req: SummarizeRequest):
    try:
        result = run_ollama(req.merged_text)
        return result

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
