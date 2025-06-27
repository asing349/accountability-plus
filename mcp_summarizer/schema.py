from pydantic import BaseModel

class SummarizeRequest(BaseModel):
    merged_text: str

class SummarizeRawResponse(BaseModel):
    output: str
