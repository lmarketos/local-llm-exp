import requests
import ast
import operator
from datetime import datetime

OLLAMA_URL = "http://ollama:11434"
MODEL = "qwen3:8b"


def get_current_time() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def calculate(expression: str) -> str:
    """
    Safely evaluate basic arithmetic expressions.
    Supports +, -, *, /, //, %, and **.
    """

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](evaluate(node.operand))

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = evaluate(node.left)
            right = evaluate(node.right)

            # Prevent excessively large exponentiation.
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            return operators[type(node.op)](left, right)

        raise ValueError("Unsupported expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


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
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The arithmetic expression to calculate, such as 25 * 4 + 10.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]


def call_model(messages):
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

    return response.json()


def execute_tool(tool_call):
    name = tool_call["function"]["name"]
    arguments = tool_call["function"]["arguments"]

    if name == "get_current_time":
        return get_current_time()

    if name == "calculate":
        return calculate(arguments["expression"])

    return f"Unknown tool: {name}"


while True:
    user_input = input("You: ")

    if user_input.lower() in {"exit", "quit"}:
        break

    messages = [
        {
            "role": "user",
            "content": user_input,
        }
    ]

    while True:
        data = call_model(messages)

        tool_calls = data["message"].get("tool_calls", [])

        if not tool_calls:
            print(data["message"]["content"])
            break

        messages.append(data["message"])

        for tool_call in tool_calls:
            print("Tool requested:", tool_call["function"]["name"])
            print("Arguments:", tool_call["function"]["arguments"])

            result = execute_tool(tool_call)

            print("Tool result:", result)

            messages.append(
                {
                    "role": "tool",
                    "content": result,
                }
            )
