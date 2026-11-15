import json

import pytest

from practice import load

m = load(__file__)


def make_registry():
    reg = m.ToolRegistry()

    @reg.tool
    def add(a: int, b: int = 0) -> int:
        return a + b

    @reg.tool
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    @reg.tool
    async def slow_double(x: int) -> int:
        return x * 2

    @reg.tool
    def explode(x: int) -> int:
        raise ValueError("kaboom")

    @reg.tool
    def listing(items: list[int]) -> dict:
        return {"total": sum(items), "count": len(items)}

    return reg


def call(name, arguments, id="c1"):
    return {"id": id, "name": name, "arguments": arguments}


async def test_success_returns_a_tool_message_with_json_text():
    reg = make_registry()
    result = await m.dispatch(reg, call("add", '{"a": 2, "b": 3}', id="x7"))
    assert result == {"role": "tool", "tool_call_id": "x7", "content": "5"}


async def test_string_result_is_returned_as_it_is():
    result = await m.dispatch(make_registry(), call("greet", '{"name": "Ada"}'))
    assert result["content"] == "Hello, Ada!"


async def test_dict_result_is_json_encoded():
    result = await m.dispatch(make_registry(), call("listing", '{"items": [1, 2, 3]}'))
    assert json.loads(result["content"]) == {"total": 6, "count": 3}


async def test_async_tools_are_awaited():
    result = await m.dispatch(make_registry(), call("slow_double", '{"x": 21}'))
    assert result["content"] == "42"


async def test_defaults_are_used():
    result = await m.dispatch(make_registry(), call("add", '{"a": 4}'))
    assert result["content"] == "4"


@pytest.mark.parametrize("arguments", ["", "   ", None])
async def test_empty_arguments_mean_no_arguments(arguments):
    reg = m.ToolRegistry()

    @reg.tool
    def ping() -> str:
        return "pong"

    result = await m.dispatch(reg, call("ping", arguments))
    assert result["content"] == "pong"


async def test_string_numbers_are_converted_by_validation():
    result = await m.dispatch(make_registry(), call("add", '{"a": "5", "b": 1}'))
    assert result["content"] == "6"


async def test_unknown_tool():
    result = await m.dispatch(make_registry(), call("nope", "{}", id="c9"))
    assert result["role"] == "tool"
    assert result["tool_call_id"] == "c9"
    assert result["content"].startswith("error:")
    assert "nope" in result["content"]


async def test_invalid_json():
    result = await m.dispatch(make_registry(), call("add", '{"a": 1,'))
    assert result["content"].startswith("error:")
    assert "JSON" in result["content"]


@pytest.mark.parametrize("arguments", ["[1, 2]", '"text"', "5", "null"])
async def test_arguments_must_be_a_json_object(arguments):
    result = await m.dispatch(make_registry(), call("add", arguments))
    assert result["content"].startswith("error:")
    assert "object" in result["content"]


async def test_wrong_type_names_the_parameter():
    result = await m.dispatch(make_registry(), call("add", '{"a": "many"}'))
    assert result["content"].startswith("error:")
    assert "a" in result["content"].split("invalid arguments:")[1]
    assert "invalid arguments" in result["content"]


async def test_missing_argument_names_the_parameter():
    result = await m.dispatch(make_registry(), call("greet", "{}"))
    assert result["content"].startswith("error:")
    assert "name" in result["content"]


async def test_unexpected_argument_is_rejected():
    result = await m.dispatch(make_registry(), call("greet", '{"name": "A", "color": "red"}'))
    assert result["content"].startswith("error:")
    assert "color" in result["content"]


async def test_exception_in_tool_becomes_an_error_message():
    result = await m.dispatch(make_registry(), call("explode", '{"x": 1}'))
    assert result["content"].startswith("error:")
    assert "kaboom" in result["content"]
    assert "ValueError" in result["content"]


async def test_dispatch_never_raises_even_for_a_malformed_call():
    result = await m.dispatch(make_registry(), {"id": "z", "name": "add", "arguments": 123})
    assert result["role"] == "tool"
    assert result["tool_call_id"] == "z"
    assert result["content"].startswith("error:")
