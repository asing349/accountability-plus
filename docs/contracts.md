# Canonical I/O contracts (post-adapter shapes)

| MCP              | Request ⭢ Response (only fields we KEEP afterwards)          |
| ---------------- | ------------------------------------------------------------ |
| classifier       | `{query}` ⭢ `{query,tags,categories}`                        |
| search           | `{query,tags,categories}` ⭢ _two lists_                      |
| scraper          | `{articles:[{url, …}]}` ⭢ `{results:[{url,status,text}]}`    |
| summarizer       | `{text}` ⭢ `{raw_output}`                                    |
| entity-extractor | `{summary_text}` ⭢ `{entity_output}`                         |
| vectorizer       | **fully-bundled payload** (see sample below) ⭢ `{vector_id}` |

Vectorizer payload (exact order & field names):

```json
{
  "query": "...",
  "tags": ["..."],
  "category": "crime",
  "scraper_output": "...(whole corpus)...",
  "summarizer_output": "...(raw_output)...",
  "entity_output": {...}
}
```
