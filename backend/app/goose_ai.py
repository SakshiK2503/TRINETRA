import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOSE_API_KEY = os.getenv("GOOSE_API_KEY")
GOOSE_MODEL = os.getenv("GOOSE_MODEL", "claude-sonnet-4.6")


def analyze_harassment_goose(text):

    prompt = f"""
You are a women safety AI system.

Analyze this message:

{text}

Return ONLY JSON:
{{
  "threatLevel": "...",
  "severityScore": number,
  "category": "...",
  "escalationRisk": "...",
  "reasoning": "short explanation"
}}
"""

    response = requests.post(
        "https://api.goose.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GOOSE_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": GOOSE_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )

    return response.json()