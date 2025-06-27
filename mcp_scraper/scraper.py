import trafilatura

def scrape_one(article):
    url = article.get("url", "")
    result = {
        "url": url,
        "title": article.get("title", ""),
        "source": article.get("source", ""),
        "published": article.get("published", ""),
        "status": "",
        "text": ""
    }
    if not url:
        result["status"] = "no_url"
        return result

    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            result["status"] = "download_failed"
            return result
        text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
        if text and len(text.strip()) > 100:
            result["status"] = "success"
            result["text"] = text.strip()
        else:
            result["status"] = "no_content"
    except Exception as e:
        result["status"] = f"error: {str(e)}"
    return result

def scrape_articles(article_list):
    return [scrape_one(article) for article in article_list]
