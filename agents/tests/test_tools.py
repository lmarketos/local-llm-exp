from agent import (
    calculate,
    execute_tool,
    get_current_time,
    get_tool_definitions,
    reverse_text,
)


def test_calculate():
    assert calculate("2 + 2") == "4"


def test_calculate_all_binary_operators():
    assert calculate("10 - 3") == "7"
    assert calculate("6 * 7") == "42"
    assert calculate("20 / 4") == "5.0"
    assert calculate("20 // 3") == "6"
    assert calculate("20 % 3") == "2"
    assert calculate("2 ** 8") == "256"


def test_calculate_unary_operators():
    assert calculate("-5") == "-5"
    assert calculate("+5") == "5"


def test_calculate_nested_expression():
    assert calculate("(2 + 3) * 4") == "20"


def test_calculate_exponent_limit():
    result = execute_tool(
        {
            "function": {
                "name": "calculate",
                "arguments": {
                    "expression": "2 ** 101",
                },
            }
        }
    )

    assert result == {
        "success": False,
        "error": "Exponent is too large.",
    }


def test_calculate_unsupported_expression():
    result = execute_tool(
        {
            "function": {
                "name": "calculate",
                "arguments": {
                    "expression": "abs(-5)",
                },
            }
        }
    )

    assert result == {
        "success": False,
        "error": "Unsupported expression.",
    }


def test_reverse_text():
    assert reverse_text("hello") == "olleh"


def test_get_current_time():
    result = get_current_time()

    assert isinstance(result, str)
    assert len(result) > 0


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


def test_unknown_tool():
    result = execute_tool(
        {
            "function": {
                "name": "does_not_exist",
                "arguments": {},
            }
        }
    )

    assert result == {
        "success": False,
        "error": "Unknown tool: does_not_exist",
    }

