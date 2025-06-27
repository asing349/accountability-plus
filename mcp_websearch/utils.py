from datetime import datetime, timedelta
import re

def deduplicate_articles(articles):
    seen_urls = set()
    seen_titles = set()
    unique = []
    for article in articles:
        url = article["url"].strip().lower()
        title = article["title"].strip().lower()
        if url in seen_urls or title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(title)
        unique.append(article)
    return unique

def parse_serpapi_date(date_str):
    if not date_str:
        return ""
    now = datetime.utcnow()
    try:
        if "hour" in date_str:
            hours = int(re.search(r"(\d+)", date_str).group(1))
            dt = now - timedelta(hours=hours)
        elif "min" in date_str:
            mins = int(re.search(r"(\d+)", date_str).group(1))
            dt = now - timedelta(minutes=mins)
        elif "day" in date_str:
            days = int(re.search(r"(\d+)", date_str).group(1))
            dt = now - timedelta(days=days)
        elif "week" in date_str:
            weeks = int(re.search(r"(\d+)", date_str).group(1))
            dt = now - timedelta(weeks=weeks)
        elif "month" in date_str:
            months = int(re.search(r"(\d+)", date_str).group(1))
            dt = now - timedelta(days=months*30)
        elif "year" in date_str:
            years = int(re.search(r"(\d+)", date_str).group(1))
            dt = now - timedelta(days=years*365)
        else:
            return date_str
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return date_str

def sort_by_relevance(articles):
    return sorted(articles, key=lambda x: x.get("relevance_score", 0), reverse=True)

def sort_by_recency(articles):
    for a in articles:
        a["_norm_date"] = parse_serpapi_date(a.get("published", ""))
    sorted_articles = sorted(articles, key=lambda x: x.get("_norm_date", ""), reverse=True)
    for a in sorted_articles:
        a.pop("_norm_date", None)
    return sorted_articles
