import requests
from datetime import datetime

def get_current_time() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

OLLAMA_URL = "http://ollama:11434"
MODEL = "qwen3:8b"


def ask_llm(prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["response"]

print(get_current_time())

