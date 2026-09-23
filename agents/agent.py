import ast
import operator
from datetime import datetime

import requests


OLLAMA_URL = "http://ollama:11434"
MODEL = "qwen3:8b"


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def get_current_time(**kwargs) -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def calculate(expression: str) -> str:
    """Safely evaluate basic arithmetic."""

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

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            return operators[type(node.op)](left, right)

        raise ValueError("Unsupported expression.")

    tree = ast.parse(expression, mode="eval")
    result = evaluate(tree.body)
    return str(result)

def reverse_text(text: str) -> str:
    return text[::-1]

# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOLS = {
    "get_current_time": {
        "function": get_current_time,
        "description": "Get the current local date and time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    "calculate": {
        "function": calculate,
        "description": "Calculate a basic arithmetic expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "The arithmetic expression to calculate, "
                        "such as 25 * 4 + 10."
                    ),
                }
            },
            "required": ["expression"],
        },
    },
    "reverse_text": {
        "function": reverse_text,
        "description": "Reverse a piece of text.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to reverse.",
                }
            },
            "required": ["text"],
        },
    },
}


def get_tool_definitions():
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": tool["description"],
                "parameters": tool["parameters"],
            },
        }
        for name, tool in TOOLS.items()
    ]


# ---------------------------------------------------------------------------
# Model interaction
# ---------------------------------------------------------------------------

def call_model(messages):
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": messages,
            "tools": get_tool_definitions(),
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------------------------
# Tool execution
# ---------------------------------------------------------------------------
def validate_arguments(tool, arguments):
    required = tool["parameters"].get("required", [])

    for name in required:
        if name not in arguments:
            return f"Missing required argument: {name}"
    allowed = tool["parameters"].get("properties", {})

    for name in arguments:
        if name not in allowed:
            return f"Unexpected argument: {name}"

    return None

def validate_argument_types(tool, arguments):
    properties = tool["parameters"].get("properties", {})

    type_map = {
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
    }

    for name, value in arguments.items():
        expected_type = properties[name].get("type")
        python_type = type_map.get(expected_type)

        if python_type is not None and not isinstance(value, python_type):
            return (
                f"Invalid type for '{name}': "
                f"expected {expected_type}, got {type(value).__name__}"
            )

    return None
        
def execute_tool(tool_call):
    name = tool_call["function"]["name"]
    arguments = tool_call["function"]["arguments"]

    tool = TOOLS.get(name)

    if tool is None:
        return {
            "success": False,
            "error": f"Unknown tool: {name}",
        }

    validation_error = validate_arguments(tool, arguments)

    if validation_error:
        return {
            "success": False,
            "error": validation_error,
        }

    type_error = validate_argument_types(tool, arguments)

    if type_error:
        return {
            "success": False,
            "error": type_error,
        }

    function = tool["function"]

    try:
        result = function(**arguments)

        return {
            "success": True,
            "result": result,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

def run_agent():
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
                print("Agent:", data["message"]["content"])
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
                        "content": str(result),
                        "tool_call_id": tool_call.get("id"),
                    }
                )

if __name__ == "__main__":
    run_agent()

