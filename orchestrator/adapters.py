import re

# --- 1. Classifier Adapter ---
def classifier_to_query(cls_out, original_query):
    # Use the original query string, tags, and categories from classifier output
    return {
        "query": original_query,
        "tags": cls_out.get("tags", []),
        "categories": cls_out.get("categories", []),
    }

# --- 2. Search Adapter ---
def search_to_urls(search_out):
    urls = []
    # Take top 5 from each, but avoid duplicates by URL
    seen = set()
    for key in ["most_relevant", "most_recent"]:
        for art in search_out.get(key, [])[:5]:
            url = art.get("url")
            title = art.get("title", "")
            if url and url not in seen:
                urls.append({"url": url, "title": title})
                seen.add(url)
    return {"articles": urls}

# --- 3. Scraper Adapter ---
def scraper_to_corpus(scrape_out):
    # Handles: {'results': [{'text': ...}, ...]}
    texts = [art.get("text", "") for art in scrape_out.get("results", []) if art.get("text")]
    return {"merged_text": " ".join(texts)}

# --- 4. Summarizer Adapter ---
def summarizer_to_summary_text(sm_out):
    # Handles: {'raw_output': "..."}
    # The entity extractor expects: {'summary_text': {...}}
    return {"summary_text": sm_out}

# --- 5. Entity Extractor Adapter (NEW) ---
def entity_output_adapter(entity_raw):
    """
    Converts raw entity output string into structured keys.
    Handles:
      Accused: ...
      Victims: ...
      Orgs/Courts or Organizations: ...
      Verdict/final outcome: ...
      Crime: ...
      Outcome: ...
    """
    text = entity_raw.get("raw_output", "")
    accused = re.search(r"Accused:\s*(.*)", text)
    victims = re.search(r"Victims:\s*(.*)", text)
    orgs = re.search(r"(?:Organizations|orgs|Courts or Organizations|Organisations/Courts):\s*(.*)", text)
    verdict = re.search(r"(?:Verdict\s*/\s*final outcome|Verdict|final outcome):\s*(.*)", text)
    crime = re.search(r"Crime:\s*(.*)", text)
    outcome = re.search(r"Outcome:\s*(.*)", text)
    return {
        "accused": [x.strip() for x in accused.group(1).split(",")] if accused and accused.group(1) else [],
        "victims": [x.strip() for x in victims.group(1).split(",")] if victims and victims.group(1) else [],
        "orgs": [x.strip() for x in orgs.group(1).split(",")] if orgs and orgs.group(1) else [],
        "verdict": verdict.group(1).strip() if verdict and verdict.group(1) else "",
        "crime": crime.group(1).strip() if crime and crime.group(1) else "",
        "outcome": outcome.group(1).strip() if outcome and outcome.group(1) else "",
    }


# --- 6. Vectorizer Payload Assembler ---
def assemble_vectorizer_payload(query, cls_out, scrape_out, sm_out, ent_out):
    """
    ent_out here should be the output of entity_output_adapter, NOT the raw string!
    """
    return {
        "query": query,
        "tags": cls_out.get("tags", []),
        "category": cls_out.get("category", ""),
        "scraper_output": scrape_out,         # Dict from scraper_to_corpus
        "summarizer_output": sm_out,          # Dict from summarizer_to_summary_text
        "entity_output": ent_out,             # Dict from entity_output_adapter
    }
