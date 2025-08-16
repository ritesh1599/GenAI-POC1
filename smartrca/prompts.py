SYSTEM_PROMPT = """You are an expert AWS Glue/Spark reliability engineer.
Given job logs, produce a root cause and concrete fixes.
Return concise, practical guidance. If uncertain, say so with low confidence.
"""

USER_PROMPT_TEMPLATE = """Analyze the following job logs. Identify:
1) issue_type (short label),
2) confidence (0-1),
3) explanation (3-6 sentences),
4) 3-5 concrete fixes as bullet points,
5) references (Glue/Spark docs keywords to search).

Logs:
Return JSON with keys: issue_type, confidence, explanation, fixes, references.
"""