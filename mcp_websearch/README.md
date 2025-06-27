# MCP Websearch

## Overview

`mcp_websearch` is a microservice within the MCP (Modular Content Processing) platform. It provides web search capabilities, returning relevant and recent news articles for a given query, along with metadata such as tags and categories. This service is designed to be used as part of a larger pipeline for content analysis, classification, and summarization.

---

## API Usage

### Endpoint

```
POST /search
```

### Example Request

```
POST /search
Content-Type: application/json

{
  "query": "Las Vegas mass shooting",
  "tags": ["Las Vegas", "mass shooting", "2017"],
  "categories": ["crime", "legal"]
}
```

### Example Response

```
{
  "most_relevant": [
    {
      "title": "Las Vegas police release report on lessons from 2017 mass shooting that killed 58",
      "url": "https://www.nbcnews.com/storyline/las-vegas-shooting/las-vegas-police-release-report-lessons-2017-mass-shooting-killed-n1028636",
      "source": {
        "name": "NBC News",
        "icon": "https://encrypted-tbn1.gstatic.com/faviconV2?url=https://www.nbcnews.com&client=NEWS_360&size=96&type=FAVICON&fallback_opts=TYPE,SIZE,URL"
      },
      "published": "07/10/2019, 07:00 AM, +0000 UTC",
      "snippet": "",
      "relevance_score": 10.0
    },
    // ... more articles ...
  ],
  "most_recent": [
    {
      "title": "The Las Vegas shooter's road to 47 guns",
      "url": "https://www.cnn.com/2017/10/06/us/stephen-paddock-47-guns",
      "source": {
        "name": "CNN",
        "icon": "https://encrypted-tbn2.gstatic.com/faviconV2?url=https://www.cnn.com&client=NEWS_360&size=96&type=FAVICON&fallback_opts=TYPE,SIZE,URL"
      },
      "published": "10/06/2017, 07:00 AM, +0000 UTC",
      "snippet": "",
      "relevance_score": 4.0
    },
    // ... more articles ...
  ]
}
```

---

## Response Structure

- **most_relevant**: List of 10 articles most relevant to the query, sorted by relevance score.
- **most_recent**: List of 10 the most recent articles related to the query.
- Each article contains:
  - `title`: Headline of the article
  - `url`: Direct link to the article
  - `source`: Object with `name`, `icon`, and optionally `authors`
  - `published`: Publication date/time (string)
  - `snippet`: (May be empty) Short excerpt or summary
  - `relevance_score`: Numeric score indicating relevance

> **How results are selected:**
>
> - The service initially retrieves 20 articles for the query.
> - Relevance is calculated for each article.
> - Duplicate articles are removed.
> - The top 10 articles are returned in each category: `most_relevant` and `most_recent`.

---

> **How results are selected:**
>
> - The service initially retrieves 20 articles for the query.
> - Relevance is calculated for each article.
> - Duplicate articles are removed.
> - The top 10 articles are returned in each category: `most_relevant` and `most_recent`.

## Notes

- This service is intended for use as part of the MCP pipeline, but can be queried directly for web search needs.
- For more details on integration or advanced usage, see the main project README or contact the maintainers.
