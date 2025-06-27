# MCP Entity Extractor

## Overview

**Entity Extractor MCP (Microservice Control Point)** is a modular, stateless microservice that extracts key entities (such as people, organizations, and other relevant named entities) from a provided summary text. It is designed to be a single-purpose, Dockerized service within a larger content processing pipeline, making it easy to orchestrate, scale, or replace independently.

- **Purpose:** Extracts named entities from a summary or article text.
- **How:** Uses a language model or rule-based logic to identify and return entities in a structured format.
- **Why MCP:** Exposes a single `/extract_entities` API endpoint, focusing on entity extraction as one step in a multi-stage pipeline.

---

## How It Works

1. Receives a POST request with a summary or article text.
2. Processes the text to extract relevant entities (e.g., persons, organizations, locations, etc.).
3. Returns the extracted entities in a structured, line-by-line format.

---

## API Usage

### Endpoint

```
POST /extract_entities
```

### Example Request

```
POST /extract_entities
Content-Type: application/json

{
    "summary_text": "Las Vegas Shooting: Fact Sheet\n==============================\n... (see above for full example) ..."
}
```

### Example Response

```
{
    "raw_output": " Line-1: Stephen Paddock\nLine-2: At least 58 people, over 500 people (injured)\nLine-3: FBI, USA Patriot Act (not mentioned), State Department, Congress, National Rifle Association (NRA)"
}
```

---

## Response Structure

- **raw_output**: A string with each line listing a category of extracted entities:
  - `Line-1`: Persons (e.g., "Stephen Paddock")
  - `Line-2`: Victims or groups (e.g., "At least 58 people, over 500 people (injured)")
  - `Line-3`: Organizations, laws, or other relevant entities (e.g., "FBI, USA Patriot Act (not mentioned), State Department, Congress, National Rifle Association (NRA)")

---

## Notes

- The service is stateless and can be horizontally scaled.
- Designed for use in a pipeline with other MCPs (e.g., summarizer, classifier).
- For more details on deployment or integration, see the main project README or contact the maintainers.
