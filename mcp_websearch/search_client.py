import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def fetch_articles(query, tags, categories, k=20):
    if not SERPAPI_KEY:
        raise Exception("SERPAPI_KEY not set in environment variables.")

    tag_str = " ".join(tags)
    category_str = " ".join(categories)
    full_query = f"{query} {tag_str} {category_str}".strip()

    params = {
        "q": full_query,
        "api_key": SERPAPI_KEY,
        "engine": "google_news",
        "num": k
    }

    resp = requests.get("https://serpapi.com/search", params=params, timeout=15)
    if resp.status_code != 200:
        raise Exception(f"SerpAPI returned error: {resp.text}")

    news_results = resp.json().get("news_results", [])
    articles = []
    for res in news_results[:k]:
        articles.append({
            "title": res.get("title", ""),
            "url": res.get("link", ""),
            "source": res.get("source", ""),
            "published": res.get("date", ""),
            "snippet": res.get("snippet", "")
        })
    return articles
