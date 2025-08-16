from .chunk import clean_log, head_tail
from .llm_client import ask_llm

def analyze_text_log(raw: str) -> dict:
    cleaned = clean_log(raw)
    excerpt = head_tail(cleaned, 64, 128)
    result = ask_llm(excerpt)
    return result
