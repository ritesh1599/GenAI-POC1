import os
import json
import boto3
import openai
import google.generativeai as genai
from smartrca.config import SETTINGS

# --- Configure OpenAI ---
if SETTINGS.provider.lower() == "openai":
    openai.api_key = SETTINGS.openai_api_key

# --- Configure Gemini ---
if SETTINGS.provider.lower() == "gemini":
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Configure Bedrock ---
if SETTINGS.provider.lower() == "bedrock":
    bedrock_client = boto3.client("bedrock-runtime", region_name=SETTINGS.aws_region)


def ask_llm(prompt: str):
    provider = SETTINGS.provider.lower()

    if provider == "openai":
        resp = openai.chat.completions.create(
            model=SETTINGS.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=SETTINGS.max_tokens,
        )
        text = resp.choices[0].message.content

    elif provider == "gemini":
        model = genai.GenerativeModel(SETTINGS.model)
        resp = model.generate_content(prompt)
        text = resp.text

    elif provider == "bedrock":
        resp = bedrock_client.invoke_model(
            modelId=SETTINGS.model,
            body=json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {"maxTokenCount": SETTINGS.max_tokens}
            }),
            contentType="application/json",
            accept="application/json"
        )
        body = json.loads(resp["body"].read())
        text = body.get("results", [{}])[0].get("outputText", "")

    else:
        raise ValueError(f"Unsupported LLM provider: {SETTINGS.provider}")

    # --- JSON extraction fallback ---
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return {
            "issue_type": "unknown",
            "confidence": 0.2,
            "explanation": text,
            "fixes": [],
            "references": []
        }
