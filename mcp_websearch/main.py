import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from search_client import fetch_articles
from relevance import score_articles
from utils import deduplicate_articles, sort_by_relevance, sort_by_recency

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

app = FastAPI()

@app.post("/search")
async def web_search(request: Request):
    data = await request.json()
    for field in ("query", "tags", "categories"):
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    query = data["query"]
    tags = data["tags"]
    categories = data["categories"]

    try:
        articles = fetch_articles(query, tags, categories, k=20)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Web search API failed: {str(e)}")

    if not articles:
        return JSONResponse({"most_relevant": [], "most_recent": []})

    unique_articles = deduplicate_articles(articles)
    if not unique_articles:
        return JSONResponse({"most_relevant": [], "most_recent": []})

    scored_articles = score_articles(unique_articles, tags, query)
    most_relevant = sort_by_relevance(scored_articles)[:10]
    most_recent = sort_by_recency(scored_articles)[:10]

    return JSONResponse({
        "most_relevant": most_relevant,
        "most_recent": most_recent
    })
