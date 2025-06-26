# Query Classifier MCP (`mcp_classifier`)

## Overview

The **Query Classifier MCP** is the first microservice in the Accountability++ pipeline.  
It takes a user's question about a public tragedy, crime, or high-profile event and transforms it into structured data—ready for automated web search, tracking, and summarization.

This service uses a local large language model (LLM), such as Mistral via Ollama, to analyze the query and provide:

- **Top two event categories** (chosen from: crime, accident, politics, legal, protest, other)
- **Confidence score** for the main category
- **Three concise, relevant tags** (keywords/entities)
- **Status** indicating the reliability of the classification

---

## How It Works

1. **User Query:**  
   The service receives a natural-language question, for example:  
   _"Las Vegas mass shooting 2017"_

2. **Classification and Tag Extraction:**  
   The model:

   - Assigns the two most probable categories
   - Calculates a confidence score for the primary category
   - Extracts three short tags representing the key topic, entity, or location

3. **Result Formatting:**  
   The result is structured in a consistent JSON format and includes a status code (`ok` or `low_confidence`) based on a configurable threshold.

---

## Example

**Request (what you POST):**

```json
{
  "query": "Las Vegas mass shooting 2017"
}
```

**Response (what you get back):**

```json
{
  "categories": ["crime", "legal"],
  "confidence": 0.98,
  "tags": ["Las Vegas", "mass shooting", "2017"],
  "status": "ok",
  "model_used": "ollama:mistral"
}
```

---

## Role in the Accountability++ Pipeline

- The **categories** and **tags** are used to create targeted web searches for the most current and relevant information on the incident.
- **Downstream microservices** (such as web search, article scraper, and summarizer) consume this structured output to automate the discovery, extraction, and summarization of facts, timelines, and legal progress.
- The **confidence score** and **status** allow downstream services or the user interface to identify when human review or query refinement is needed.

---

## API Usage

- **Endpoint:** `POST /classify`
- **Request Body:**
  ```json
  {
    "query": "Your incident query here",
    "model": "optional-model-name"
  }
  ```
- **Response:**
  - `categories`: The top two predicted categories (string array)
  - `confidence`: Confidence score for the first category (float)
  - `tags`: Three relevant tags (string array)
  - `status`: `"ok"` or `"low_confidence"`
  - `model_used`: The LLM/model used

---

## How to Run

1. Make sure you have [Ollama](https://ollama.com/) installed and running your desired LLM.
2. Configure `.env` with at least:
   ```
   OLLAMA_BASE_URL=http://host.docker.internal:11434
   OLLAMA_MODEL=mistral
   MIN_CONFIDENCE=0.6
   ```
3. Build and launch with Docker Compose:
   ```sh
   docker-compose up --build
   ```
4. Test with Postman or curl:
   ```sh
   curl -X POST "http://localhost:8001/classify"       -H "Content-Type: application/json"       -d '{"query": "Las Vegas mass shooting 2017"}'
   ```

---

## Why Use This Service?

- Provides **consistent, structured outputs** from open-ended queries
- **Enhances search and analysis** by producing precise tags and categories
- Flexible for any downstream information retrieval, investigation, or reporting tasks

---

**Contact:**  
For questions or contributions, reach out to the Accountability++ team.
