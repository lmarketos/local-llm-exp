import requests
from datetime import datetime

OLLAMA_URL = "http://ollama:11434"
MODEL = "qwen3:8b"


def get_current_time() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local date and time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
]

response = requests.post(
    f"{OLLAMA_URL}/api/chat",
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": "What time is it right now?",
            }
        ],
        "tools": tools,
        "stream": False,
    },
    timeout=120,
)

response.raise_for_status()

data = response.json()

tool_call = data["message"]["tool_calls"][0]

print("Tool requested:", tool_call["function"]["name"])
print("Arguments:", tool_call["function"]["arguments"])

result = get_current_time()

messages = [
    {
        "role": "user",
        "content": "What time is it right now?",
    },
    data["message"],
    {
        "role": "tool",
        "content": result,
    },
]
response = requests.post(
    f"{OLLAMA_URL}/api/chat",
    json={
        "model": MODEL,
        "messages": messages,
        "tools": tools,
        "stream": False,
    },
    timeout=120,
)

response.raise_for_status()

print(response.json()["message"]["content"])

