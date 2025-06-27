# MCP Scraper

## Overview

**Scraper MCP (Microservice Control Point)** is a modular, stateless microservice that receives a batch of article URLs and extracts the main article text from each link. It is designed to be a single-purpose, Dockerized service within a larger content processing pipeline, making it easy to orchestrate, scale, or replace independently.

- **Purpose:** Extracts clean article text from a list of URLs.
- **How:** Uses the `trafilatura` library to download and parse the main content.
- **Why MCP:** Exposes a single `/scrape` API endpoint, focusing on content extraction as one step in a multi-stage pipeline.

---

## How It Works

1. Receives a POST request with a batch of article URLs (and optional metadata).
2. For each URL, attempts to download and extract the main article text using `trafilatura`.
3. Returns a result for each link, including extraction status (`success` or failure reason) and the extracted text (if successful).

---

## API Usage

### Endpoint

```
POST /scrape
```

### Example Request

```
POST /scrape
Content-Type: application/json

{
  "articles": [
    {
      "url": "https://www.nbcnews.com/storyline/las-vegas-shooting/las-vegas-police-release-report-lessons-2017-mass-shooting-killed-n1028636",
      "title": "Las Vegas police release report on lessons from 2017 mass shooting that killed 58",
      "source": "NBC News",
      "published": "07/10/2019, 07:00 AM, +0000 UTC"
    },
    // ... more articles ...
  ]
}
```

### Example Response

```
{
  "results": [
    {
      "url": "https://www.nbcnews.com/storyline/las-vegas-shooting/las-vegas-police-release-report-lessons-2017-mass-shooting-killed-n1028636",
      "title": "Las Vegas police release report on lessons from 2017 mass shooting that killed 58",
      "source": "NBC News",
      "published": "07/10/2019, 07:00 AM, +0000 UTC",
      "status": "success",
      "text": "...extracted article text..."
    },
    {
      "url": "https://www.wsj.com/articles/mgm-resorts-reaches-settlement-in-2017-las-vegas-massacre-11570116720?...",
      "title": "MGM Resorts Reaches Settlement in 2017 Las Vegas Mass Shooting",
      "source": "WSJ",
      "published": "10/03/2019, 07:00 AM, +0000 UTC",
      "status": "download_failed",
      "text": ""
    },
    // ... more results ...
  ]
}
```

---

## Response Structure

- **results**: List of objects, one per input article.
  - `url`: The original article URL
  - `title`: (Optional) Title of the article
  - `source`: (Optional) Source or publisher
  - `published`: (Optional) Publication date
  - `status`: `success` if extraction succeeded, or a string describing the failure reason (e.g., `download_failed`)
  - `text`: The extracted main article text (empty if extraction failed)

---

## Notes

- The service is stateless and can be horizontally scaled.
- Designed for use in a pipeline with other MCPs (e.g., summarizer, classifier).
- For more details on deployment or integration, see the main project README or contact the maintainers.
