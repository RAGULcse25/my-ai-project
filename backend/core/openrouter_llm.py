import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# ─────────────────────────────────────────
# TOKEN-EFFICIENT LLM CALLER
# Uses cheapest model per task
# ─────────────────────────────────────────

def call_llm(
    prompt: str,
    model: str = "openrouter/free",
    max_tokens: int = 800,       # Keep LOW to save tokens!
    system: str = "You are a helpful coding assistant. Be concise."
) -> str:
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://seads.app",
    }
    
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0.2,          # Low = focused output
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt}
        ]
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    data = response.json()
    
    # Log token usage
    usage = data.get("usage", {})
    tokens_used = usage.get("total_tokens", 0)
    print(f"    🪙 Tokens used: {tokens_used}")
    
    if "choices" in data and len(data["choices"]) > 0:
        content = data["choices"][0]["message"].get("content")
        return content if content is not None else ""
    else:
        print(f"    ⚠️ Warning: no choices returned from LLM. Data: {data}")
        return ""
