# prompts.py
"""
Central place for all LLM prompts.
"""

PROMPT_TEMPLATE = (
    "You will be given a case summary.\n"
    "Return EXACTLY four plain lines, no bullets, nothing extra:\n"
    "  • Line 1 – accused (comma-separated, or blank)\n"
    "  • Line 2 – victims (comma-separated, or blank)\n"
    "  • Line 3 – courts or organizations (comma-separated, or blank)\n"
    "  • Line 4 – verdict / final outcome (one concise line, or blank)\n"
    "  • Line 5 – crime / initial charge (one concise line, or blank)\n"
    "  Answer in the given pattern - Accused:   ;; Victims:      ;;Organisations/Courts:        ;;Outcome:        ;; Crime:         ;;"
    "CASE SUMMARY:\n{summary_text}"
)
