PROMPT_TEMPLATE = """
You are an expert legal and crime analyst. You are given multiple news articles about a single tragedy, crime, or legal case. Read all the provided articles and produce the following:

1. A COMPREHENSIVE NARRATIVE SUMMARY combining all articles. Include:
   - Who was involved (victims, accused, authorities)
   - What happened, with main facts
   - When it happened (chronology)
   - Where (locations, courthouse if mentioned)
   - Why (motives if present)
   - Outcome (who was punished, what finally happened, legal result, was justice served?)
2. A TIMELINE of events, with dates and concise descriptions.
3. A LIST of:
   - Victims (names only, if present)
   - Accused/suspects (names)
   - Courthouse(s) (if any)
4. ONE-LINE description of the incident.
5. ONE-LINE final outcome.

===== ARTICLES =====
{merged_text}
"""
