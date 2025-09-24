# prompts.py

def build_prompt(log: str, context: list = None) -> str:
    """
    Build a structured prompt for the LLM.

    Args:
        log (str): The Glue/Spark log text to analyze.
        context (list): Optional list of knowledge chunks retrieved via RAG.

    Returns:
        str: The final prompt text to send to the LLM.
    """
    base_instruction = (
        "You are an expert AWS Glue/Spark engineer. "
        "Analyze the following log and provide the root cause, probable fixes, and explanation in JSON format.\n"
    )

    if context:
        context_text = "\n".join(context)
        prompt = f"{base_instruction}\nRelevant Knowledge:\n{context_text}\n\nLog:\n{log}"
    else:
        prompt = f"{base_instruction}\nLog:\n{log}"

    prompt += "\n\nReturn the output in JSON with keys: issue_type, confidence, explanation, fixes, references."

    return prompt
