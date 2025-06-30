from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from scraper import scrape_articles

app = FastAPI()

@app.post("/scrape")
async def scrape_endpoint(request: Request):
    data = await request.json()
    articles = data.get("articles", [])
    if not isinstance(articles, list) or not articles:
        raise HTTPException(status_code=400, detail="Input must contain a non-empty 'articles' list.")
    print(f"[SCRAPER] Started scraping {len(articles)} articles...")  # LOG for admin/monitoring
    results = scrape_articles(articles)  # This should block until scraping is done
    print(f"[SCRAPER] Finished scraping {len(articles)} articles.")
    return JSONResponse({"results": results})  # 200 OK is returned *only when done*
