def score_articles(articles, tags, query):
    tag_set = set([t.lower() for t in tags])
    query_set = set(query.lower().split())
    scored = []
    for article in articles:
        score = 0
        title = article["title"].lower()
        snippet = article.get("snippet", "").lower()
        combined = f"{title} {snippet}"
        for tag in tag_set:
            if tag in combined:
                score += 2
        for word in query_set:
            if word in combined:
                score += 1
        if "reuters" in article["source"] or "nytimes" in article["source"]:
            score += 1
        new_article = dict(article)
        new_article["relevance_score"] = float(score)
        scored.append(new_article)
    return scored
