import requests
import os
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path="../.env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
MODEL_SUMMARIZER = os.getenv("MODEL_SUMMARIZER", "gemma3n:e4b")

def run_ollama(merged_text: str) -> dict:
    prompt = f"""
    You are an expert legal and crime analyst. Given the following news articles about a single crime or tragedy, provide a comprehensive report containing the following sections clearly:

    1. COMPREHENSIVE SUMMARY:
        - Clearly state who was involved (victims, accused, authorities).
        - Clearly describe what happened with all main facts.
        - Clearly mention when and where the incident occurred.
        - Clearly state the motive (if known).
        - Clearly state the outcome of the incident (final legal results or punishment).

    2. TIMELINE OF EVENTS:
        Provide a concise chronological list of key events with dates.

    3. LIST OF:
        - Victims (names if available)
        - Accused/Suspects (names)
        - Authorities involved
        - Locations involved (specific locations)
        - Organizations involved (e.g., Police departments, FBI)

    4. ONE-LINE INCIDENT DESCRIPTION:
        - Provide a very concise one-line summary of the incident.

    5. ONE-LINE FINAL OUTCOME:
        - Provide a very concise one-line summary of the final outcome (legal verdict, punishment, unresolved status).

    ==== NEWS ARTICLES ====
    {merged_text}

    Clearly separate each section with clear headings.
    """

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL_SUMMARIZER,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    raw_output = response.json().get("response", "").strip()

    return {"raw_output": raw_output}

