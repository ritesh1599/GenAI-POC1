import os
from dataclasses import dataclass

@dataclass
class Settings:
    provider: str = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "bedrock"
    model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")   # change as needed
    max_tokens: int = int(os.getenv("MAX_TOKENS", "800"))
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")

SETTINGS = Settings()
