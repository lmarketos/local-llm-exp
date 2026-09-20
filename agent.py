import requests

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


while True:
    prompt = input("\nYou: ")

    if prompt.lower() in {"quit", "exit"}:
        break

    answer = ask_llm(prompt)
    print(f"\nAgent: {answer}")

