from agent import (
    TOOLS,
    calculate,
    execute_tool,
    get_tool_definitions,
    reverse_text,
)


def test_calculate():
    assert calculate("2 + 2") == "4"


def test_reverse_text():
    assert reverse_text("hello") == "olleh"


def test_missing_required_argument():
    result = execute_tool(
        {
            "function": {
                "name": "calculate",
                "arguments": {},
            }
        }
    )

    assert result == {
        "success": False,
        "error": "Missing required argument: expression",
    }

def test_unexpected_argument():
    result = execute_tool(
        {
            "function": {
                "name": "calculate",
                "arguments": {
                    "expression": "2 + 2",
                    "unexpected": "value",
                },
            }
        }
    )

    assert result == {
        "success": False,
        "error": "Unexpected argument: unexpected",
    }

def test_invalid_argument_type():
    result = execute_tool(
        {
            "function": {
                "name": "calculate",
                "arguments": {
                    "expression": 123,
                },
            }
        }
    )

    assert result == {
        "success": False,
        "error": "Invalid type for 'expression': expected string, got int",
    }

def test_division_by_zero():
    result = execute_tool(
        {
            "function": {
                "name": "calculate",
                "arguments": {
                    "expression": "10 / 0",
                },
            }
        }
    )

    assert result == {
        "success": False,
        "error": "division by zero",
    }

def test_tool_definitions():
    definitions = get_tool_definitions()

    names = {
        definition["function"]["name"]
        for definition in definitions
    }

    assert names == {
        "get_current_time",
        "calculate",
        "reverse_text",
    }
