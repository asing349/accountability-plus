from langgraph.graph import StateGraph
from typing import TypedDict, Optional, Dict, Any
import adapters as ad
import http_clients as hc

class State(TypedDict, total=False):
    query: str
    cached: Optional[bool]
    vector_id: Optional[str]
    cls_out: Optional[dict]
    search_out: Optional[dict]
    scrape_out: Optional[dict]
    summarizer_in: Optional[dict]
    sm_out: Optional[dict]
    entity_in: Optional[dict]
    ent_out: Optional[dict]
    vector_out: Optional[dict]
    vec_payload: Optional[dict]

# --- 0. Cache Probe ---
async def cache_probe_node(state: State) -> State:
    cache = await hc.vector_cache_probe(state["query"])
    if cache.get("hits"):
        record_id = cache["hits"][0]["id"]
        record = await hc.get_record_by_id(record_id)
        return {
            **state,
            "cached": True,
            "vector_id": record_id,
            "sm_out": record.get("summarizer_output"), # Pass full summary
            "ent_out": record.get("entity_output"),   # Pass full entities
            "websearch_output": record.get("websearch_output"), # Pass websearch_output
            "query": record.get("query") # Pass original query
        }
    # Initialize the vec_payload just like main.py
    return {
        **state,
        "cached": False,
        "vec_payload": {
            "query": state["query"],
            "tags": None,
            "category": None,
            "scraper_output": None,
            "summarizer_output": None,
            "websearch_output": None,
            "entity_output": None
        }
    }

# --- 1. Classifier Node ---
async def classifier_node(state: State) -> State:
    cls_out = await hc.call_classifier(state["query"])
    # Update vec_payload
    vec_payload = dict(state["vec_payload"])
    vec_payload["tags"] = cls_out.get("tags", [])
    vec_payload["category"] = cls_out.get("category", "")
    return {**state, "cls_out": cls_out, "vec_payload": vec_payload}

# --- 2. Search Node ---
async def search_node(state: State) -> State:
    search_in = ad.classifier_to_query(state["cls_out"], state["query"])
    search_out = await hc.call_search(search_in)
    vec_payload = dict(state["vec_payload"])
    vec_payload["websearch_output"] = search_out
    return {**state, "search_out": search_out, "vec_payload": vec_payload}

# --- 3. Scraper Node ---
async def scraper_node(state: State) -> State:
    scraper_in = ad.search_to_urls(state["search_out"])
    scrape_out = await hc.call_scraper(scraper_in)
    summarizer_in = ad.scraper_to_corpus(scrape_out)
    vec_payload = dict(state["vec_payload"])
    # scraper_output must be a string
    vec_payload["scraper_output"] = summarizer_in.get("merged_text", "")
    return {**state, "scrape_out": scrape_out, "summarizer_in": summarizer_in, "vec_payload": vec_payload}

# --- 4. Summarizer Node ---
async def summarizer_node(state: State) -> State:
    sm_out = await hc.call_summarizer(state["summarizer_in"])
    entity_in = ad.summarizer_to_summary_text(sm_out)
    vec_payload = dict(state["vec_payload"])
    # summarizer_output must be string
    if isinstance(sm_out, dict) and "raw_output" in sm_out:
        vec_payload["summarizer_output"] = sm_out["raw_output"]
    else:
        vec_payload["summarizer_output"] = str(sm_out)
    return {**state, "sm_out": sm_out, "entity_in": entity_in, "vec_payload": vec_payload}

# --- 5. Entity Node ---
async def entity_node(state: State) -> State:
    ent_raw = await hc.call_entity_extractor(state["entity_in"])
    ent_out = ad.entity_output_adapter(ent_raw)
    vec_payload = dict(state["vec_payload"])
    vec_payload["entity_output"] = ent_out
    return {**state, "ent_out": ent_out, "vec_payload": vec_payload}

# --- 6. Vectorizer Node ---
async def vectorizer_node(state: State) -> State:
    vec_out = await hc.call_vectorizer(state["vec_payload"])
    return {**state, "vector_out": vec_out}

# --- Build LangGraph ---
def build_graph():
    g = StateGraph(State)
    g.add_node("cache_probe", cache_probe_node)
    g.add_node("classify", classifier_node)
    g.add_node("search", search_node)
    g.add_node("scrape", scraper_node)
    g.add_node("summarize", summarizer_node)
    g.add_node("entity_extract", entity_node)
    g.add_node("vectorize", vectorizer_node)

    g.set_entry_point("cache_probe")
    # Conditional route
    def route_after_probe(state: State):
        return "vectorize" if state.get("cached") else "classify"
    g.add_conditional_edges("cache_probe", route_after_probe, {
        "classify": "classify",
        "vectorize": "vectorize"
    })

    g.add_edge("classify", "search")
    g.add_edge("search", "scrape")
    g.add_edge("scrape", "summarize")
    g.add_edge("summarize", "entity_extract")
    g.add_edge("entity_extract", "vectorize")
    g.set_finish_point("vectorize")
    return g.compile()