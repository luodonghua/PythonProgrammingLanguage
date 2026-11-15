from typing import Literal

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("hint", "expected"),
    [
        (int, {"type": "integer"}),
        (float, {"type": "number"}),
        (str, {"type": "string"}),
        (bool, {"type": "boolean"}),
        (list[int], {"type": "array", "items": {"type": "integer"}}),
        (list[list[str]], {"type": "array", "items": {"type": "array", "items": {"type": "string"}}}),
        (Literal["a", "b"], {"enum": ["a", "b"]}),
        (str | None, {"anyOf": [{"type": "string"}, {"type": "null"}]}),
        (
            list[float] | None,
            {"anyOf": [{"type": "array", "items": {"type": "number"}}, {"type": "null"}]},
        ),
    ],
)
def test_type_to_schema(hint, expected):
    assert m.type_to_schema(hint) == expected


@pytest.mark.parametrize("hint", [dict, set[int], bytes])
def test_type_to_schema_unsupported(hint):
    with pytest.raises(TypeError, match="unsupported type"):
        m.type_to_schema(hint)


def search(query: str, limit: int = 10, tags: list[str] | None = None) -> list:
    """Search the catalogue.

    Longer text that must not appear in the description.
    """
    return []


def test_build_schema_full():
    assert m.build_schema(search) == {
        "name": "search",
        "description": "Search the catalogue.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer"},
                "tags": {"anyOf": [{"type": "array", "items": {"type": "string"}}, {"type": "null"}]},
            },
            "required": ["query"],
        },
    }


def test_build_schema_untyped_and_var_parameters():
    def f(a, b: int, *args, **kwargs):
        pass

    schema = m.build_schema(f)
    assert schema["description"] == ""
    assert schema["parameters"]["properties"] == {"a": {}, "b": {"type": "integer"}}
    assert schema["parameters"]["required"] == ["a", "b"]


def test_build_schema_no_parameters():
    def ping():
        """Check the service."""

    assert m.build_schema(ping)["parameters"] == {"type": "object", "properties": {}, "required": []}


def test_build_schema_literal_and_order():
    def paint(color: Literal["red", "blue"], width: float = 1.0, bold: bool = False):
        pass

    props = m.build_schema(paint)["parameters"]["properties"]
    assert list(props) == ["color", "width", "bold"]
    assert props["color"] == {"enum": ["red", "blue"]}


def test_build_schema_unsupported_hint_raises():
    def f(data: dict):
        pass

    with pytest.raises(TypeError):
        m.build_schema(f)
