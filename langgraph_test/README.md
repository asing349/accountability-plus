# LangGraph Orchestrator (Experimental)

## Overview

The **LangGraph Orchestrator** is an experimental pipeline controller for the Accountability Plus platform, built using the [LangGraph](https://github.com/langchain-ai/langgraph) library. It demonstrates how to model the multi-step MCP pipeline as a directed graph, enabling flexible, modular, and maintainable orchestration of microservices.

This orchestrator mirrors the classic pipeline (Classifier → Websearch → Scraper → Summarizer → Entity Extractor → Vectorstore) but leverages LangGraph's stateful, node-based workflow for clarity and extensibility.

---

## How It Works

- **Graph-based Workflow:** Each pipeline step is a node in a LangGraph state graph. The graph manages state transitions and data flow between nodes.
- **Cache Probe:** The pipeline first checks the vectorstore for a cached result. If found, it skips the rest of the pipeline.
- **Modular Nodes:** Each node (classifier, search, scraper, summarizer, entity extractor, vectorizer) is an async function that calls the corresponding MCP microservice and updates the workflow state.
- **Adapters:** Helper functions convert outputs between MCPs to ensure compatibility.
- **Async API:** The FastAPI server exposes a `/process` endpoint that runs the graph asynchronously for each query.

---

## Endpoints

### `/process` (POST)

- **Description:** Runs the full LangGraph-based pipeline for a given query.
- **Request:**
  ```json
  { "query": "Las Vegas mass shooting 2017" }
  ```
- **Response:**
  ```json
  {
    "cached": false,
    "vector_id": "...",
    "summary_text": "...",
    "entity_output": { ... }
  }
  ```
  If a cached result is found, returns `{ "cached": true, "vector_id": "..." }`.

---

## Pipeline Flow

1. **Cache Probe:** Check for existing vectorstore entry.
2. **Classifier:** Tag and categorize the query.
3. **Websearch:** Retrieve relevant articles.
4. **Scraper:** Extract article text.
5. **Summarizer:** Summarize merged text.
6. **Entity Extractor:** Extract structured entities.
7. **Vectorstore:** Store all results and embedding.

The graph is defined in `graph.py` and can be easily extended or modified.

---

## Example Usage

```bash
curl -X POST http://localhost:8007/process -H "Content-Type: application/json" -d '{"query": "Las Vegas mass shooting 2017"}'
```

---

## Requirements

- Python 3.10+
- FastAPI
- LangGraph
- aiohttp, httpx
- psycopg2-binary (for vectorstore communication)
- uvicorn

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Notes

- This orchestrator is experimental and intended for research, prototyping, or demonstration.
- The pipeline logic is fully async and can be extended with new nodes or conditional branches.
- For more details on the LangGraph library, see [LangGraph documentation](https://github.com/langchain-ai/langgraph).
