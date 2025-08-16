import json
from .config import SETTINGS

def ask_llm(log_excerpt: str) -> dict:
    if SETTINGS.provider == "openai":
        import openai
        openai.api_key = SETTINGS.openai_api_key
        msg = [
            {"role":"system","content": "You are an expert AWS Glue/Spark reliability engineer."},
            {"role":"user","content": f"""Analyze logs and output strict JSON with keys:
issue_type, confidence, explanation, fixes, references.
Logs:
```{log_excerpt}```"""}
        ]
        resp = openai.chat.completions.create(
            model=SETTINGS.model,
            messages=msg,
            temperature=0.2,
            max_tokens=SETTINGS.max_tokens,
        )
        text = resp.choices[0].message.content
    else:
        # Bedrock example with Claude (pseudo-minimal)
        import boto3, json as pyjson
        bedrock = boto3.client("bedrock-runtime", region_name=SETTINGS.aws_region)
        body = {
            "messages": [
              {"role": "system", "content": [{"text": "You are an expert AWS Glue/Spark reliability engineer."}]},
              {"role": "user", "content": [{"text": f"Analyze logs and output strict JSON with keys issue_type, confidence, explanation, fixes, references.\nLogs:\n```{log_excerpt}```"}]}
            ],
            "max_tokens": SETTINGS.max_tokens,
            "temperature": 0.2
        }
        resp = bedrock.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )
        text = json.loads(resp["body"].read())["output"]["message"]["content"][0]["text"]

    # try to locate JSON in response
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return {"issue_type":"unknown","confidence":0.2,"explanation":text,"fixes":[],"references":[]}
