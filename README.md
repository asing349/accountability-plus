# Accountability++

A modular, AI-powered platform for in-depth incident and case research, summarization, and entity extraction. Leverage the power of large language models and web scraping to transform unstructured data into actionable insights.

## Table of Contents

- [Demo] (#demo)
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup (.env)](#environment-setup-env)
  - [Ollama Model Setup](#ollama-model-setup)
  - [Supabase Database Setup](#supabase-database-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Frontend Access](#frontend-access)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Contact](#contact)

## Demo


https://github.com/user-attachments/assets/0b7acba7-3889-4cdf-8aec-a86742113320


## Overview

Accountability++ is a multi-agent AI system designed to automate the process of researching and analyzing incidents or cases from various online sources. It orchestrates a series of specialized microservices to classify queries, perform web searches, scrape content, summarize information, extract key entities, and store the processed data in a vector database for efficient retrieval.

## Features

- **Intelligent Query Classification:** Categorizes user queries to streamline the research process.
- **Automated Web Search:** Discovers relevant articles and information from the web.
- **Content Scraping:** Extracts clean text content from identified web pages.
- **Advanced Summarization:** Generates comprehensive, structured summaries of complex cases.
- **Key Entity Extraction:** Identifies and extracts critical information such as accused parties, victims, organizations, crimes, and outcomes.
- **Vector Database Integration:** Stores processed data and their embeddings for fast semantic search and caching.
- **Modular Microservices Architecture:** Easily scalable and maintainable components.
- **Dockerized Deployment:** Simple setup and consistent environment across development and production.
- **CLI-Themed Frontend:** A sleek, terminal-like user interface for an immersive experience.

## Tech Stack

- **Backend:** Python (FastAPI)
- **Frontend:** React.js (with Chakra UI)
- **Containerization:** Docker & Docker Compose
- **Database:** PostgreSQL (via Supabase)
- **LLM Orchestration:** LangChain / LangGraph (experimental)
- **Local LLM Runtime:** Ollama
- **Web Search API:** SerpAPI
- **Monitoring:** Prometheus (configured)

## Architecture

The system is built as a collection of independent microservices orchestrated by a central `orchestrator` component.

- **`orchestrator`**: The core service that manages the workflow:
  1.  Receives user queries.
  2.  Checks for cached results in `mcp_vectorstore`.
  3.  Calls `mcp_classifier` to categorize the query.
  4.  Uses `mcp_websearch` to find relevant articles.
  5.  Passes URLs to `mcp_scraper` to extract content.
  6.  Sends scraped text to `mcp_summarizer`.
  7.  Feeds summaries to `mcp_entity_extractor`.
  8.  Bundles all data and sends to `mcp_vectorstore` for vectorization and storage.
  9.  Returns the comprehensive processed report.
- **`mcp_classifier`**: Classifies queries using an LLM.
- **`mcp_websearch`**: Performs web searches via SerpAPI.
- **`mcp_scraper`**: Scrapes content from URLs using `trafilatura`.
- **`mcp_summarizer`**: Summarizes content using an LLM.
- **`mcp_entity_extractor`**: Extracts structured entities from summaries using an LLM.
- **`mcp_vectorstore`**: Manages vector embeddings and stores/retrieves data from PostgreSQL.
- **`langgraph_test`**: An experimental alternative orchestrator built with LangGraph.
- **`frontend`**: The React.js user interface.
- **`prometheus`**: For monitoring the orchestrator.

## Getting Started

Follow these steps to get Accountability++ up and running on your local machine.

### Prerequisites

Ensure you have the following installed:

- **Docker & Docker Compose:** [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Node.js & npm:** (Required for frontend development/build, though Docker handles most of it) [Install Node.js](https://nodejs.org/en/download/) (v18+ recommended)
- **Python 3.10+:** (Required for backend development, though Docker handles most of it) [Install Python](https://www.python.org/downloads/)
- **Ollama:** [Download and Install Ollama](https://ollama.com/download) (Ensure it's running locally before starting Docker Compose)

### Environment Setup (.env)

Create a `.env` file in the root directory of the project by copying `.env.example`:

```bash
cp .env.example .env
```

Then, populate the `.env` file with your specific configurations:

```
# Supabase PostgreSQL Database Configuration
PG_DB=your_db_name
PG_USER=your_db_user
PG_PASS=your_db_password
PG_HOST=your_supabase_db_host
PG_PORT=5432

# Ollama Configuration (ensure Ollama is running locally)
OLLAMA_BASE_URL=http://host.docker.internal:11434 # Use this for Docker on Mac/Windows
# OLLAMA_BASE_URL=http://172.17.0.1:11434 # Use this for Docker on Linux (bridge network gateway)
# OLLAMA_BASE_URL=http://localhost:11434 # Use this if Ollama is running directly on the host and not accessible via docker.internal

# Specify Ollama Models to Use
# These models need to be pulled into your local Ollama instance
OLLAMA_MODEL=mistral # Used by mcp_classifier
MODEL_SUMMARIZER=gemma3n # Used by mcp_summarizer
OLLAMA_MODEL_VEC=nomic-embed-text # Used by mcp_vectorstore

# SerpAPI Configuration (for web search)
SERPAPI_KEY=your_serpapi_api_key # Get one from https://serpapi.com/
```

### Ollama Model Setup

Before running the application, you need to download the required LLM models into your local Ollama instance. Open your terminal and run the following commands:

```bash
ollama pull mistral
ollama pull gemma3n
ollama pull nomic-embed-text
```

Ensure Ollama is running in the background.

### Supabase Database Setup

Accountability++ uses a PostgreSQL database, typically hosted on [Supabase](https://supabase.com/).

1.  **Create a Supabase Project:**

    - Go to [Supabase](https://supabase.com/) and create a new project.
    - Note down your **Database Host**, **Database Name**, **User**, and **Password**. These go into your `.env` file.

2.  **Apply Database Schema:**
    The `query_embeddings` table is crucial for the `mcp_vectorstore` service. You need to create this table in your Supabase project.

    Go to your Supabase project's SQL Editor and run the following `CREATE TABLE` statement:

    ```sql
    CREATE TABLE public.query_embeddings (
      id uuid NOT NULL DEFAULT gen_random_uuid(),
      query text NOT NULL UNIQUE,
      tags text[],
      category text,
      scraper_output text,
      summarizer_output text,
      websearch_output jsonb,
      entity_output jsonb,
      all_text text NOT NULL,
      embedding vector(768) NOT NULL, -- Requires pgvector extension
      timestamp timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
      CONSTRAINT query_embeddings_pkey PRIMARY KEY (id)
    );
    ```

    **Important:** This schema requires the `pgvector` PostgreSQL extension. In Supabase, you can enable this extension from the "Database" -> "Extensions" section of your project dashboard.

## Running the Application

Once all prerequisites are met and your `.env` file is configured, navigate to the root directory of the project in your terminal and run:

```bash
docker-compose up --build
```

This command will:

- Build all Docker images for the microservices and the frontend.
- Start all services defined in `docker-compose.yml`.
- Expose the frontend on `http://localhost:3000`.
- Expose the main orchestrator API on `http://localhost:8000`.

## Project Structure

```
.
├── .env.example             # Example environment variables
├── .env                     # Your local environment variables
├── docker-compose.yml       # Defines all services and their configurations
├── README.md                # This file
├── docs/                    # Project documentation (e.g., API contracts)
├── frontend/                # React.js user interface
│   ├── public/
│   ├── src/
│   ├── Dockerfile           # Frontend Docker build instructions
│   └── package.json
├── mcp_classifier/          # Microservice for query classification
├── mcp_entity_extractor/    # Microservice for entity extraction
├── mcp_scraper/             # Microservice for web content scraping
├── mcp_summarizer/          # Microservice for content summarization
├── mcp_vectorstore/         # Microservice for vector database operations
├── mcp_websearch/           # Microservice for web search
├── orchestrator/            # Main orchestration service
├── langgraph_test/          # Experimental LangGraph orchestrator
```

## Frontend Access

After running `docker-compose up --build`, open your web browser and navigate to:

[http://localhost:3000](http://localhost:3000)

You will be greeted by the CLI-themed interface where you can enter your queries.

## API Endpoints

The primary API endpoint for interacting with the system is the `orchestrator` service:

- **`POST /process`**: Submits a query to the entire pipeline.
  - **URL:** `http://localhost:8000/process`
  - **Body:** `{"query": "Your research query here"}`
  - **Response:** A comprehensive JSON object containing the summarized text, extracted entities, and reference links.

An experimental LangGraph orchestrator is also available:

- **`POST /process`**: (LangGraph) Submits a query to the LangGraph pipeline.
  - **URL:** `http://localhost:8007/process`

## Troubleshooting

- **`docker-compose up --build` fails:**
  - Check Docker Desktop is running.
  - Ensure you have enough system resources (RAM, CPU) allocated to Docker.
  - Review the error messages in the console for specific service failures.
- **Frontend "Load failed" or "Network Error":**
  - Ensure `http://localhost:3000` is correctly mapped to container port 80 in `docker-compose.yml`.
  - Verify that `REACT_APP_API_URL` in `docker-compose.yml` is set to `http://localhost:8000`.
  - Confirm the `orchestrator` service is running and accessible on `http://localhost:8000`.
  - Check browser console for CORS errors. The `orchestrator` has CORS enabled for `localhost:3000`.
- **Backend services (e.g., `mcp_classifier`) fail to start or connect to Ollama:**
  - Ensure Ollama is installed and running on your host machine.
  - Verify that the Ollama models (`mistral`, `gemma3n`, `nomic-embed-text`) have been successfully pulled (`ollama pull <model_name>`).
  - Double-check `OLLAMA_BASE_URL` in your `.env` file. Use `http://host.docker.internal:11434` for Mac/Windows Docker, or `http://172.17.0.1:11434` for Linux Docker.
- **`mcp_vectorstore` fails to connect to database or `websearch_output` is `null`:**
  - Verify all `PG_` environment variables in `.env` are correct and match your Supabase project.
  - Ensure the `query_embeddings` table exists in your Supabase project and the `pgvector` extension is enabled.
  - Confirm the table schema matches the one provided in [Supabase Database Setup](#supabase-database-setup).
- **"No summary available" or incorrect entity display:**
  - Ensure the `orchestrator` and `mcp_summarizer` services are running correctly.
  - Rebuild the Docker images to ensure the latest code changes are applied.

## Contact

For any questions or feedback, feel free to reach out:

- **GitHub:** [https://github.com/asing349](https://github.com/asing349?tab=repositories)
- **LinkedIn:** [https://www.linkedin.com/in/itsmejait](https://www.linkedin.com/in/itsmejait)
