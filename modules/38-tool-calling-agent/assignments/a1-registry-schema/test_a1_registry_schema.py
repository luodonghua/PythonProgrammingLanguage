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
        (int | None, {"type": "integer"}),
        (list[str] | None, {"type": "array", "items": {"type": "string"}}),
    ],
)
def test_type_schema(hint, expected):
    assert m.type_schema(hint) == expected


@pytest.mark.parametrize("hint", [dict, set[int], bytes, int | str])
def test_type_schema_unsupported(hint):
    with pytest.raises(TypeError):
        m.type_schema(hint)


def test_optional_from_typing_module():
    from typing import Optional

    assert m.type_schema(Optional[int]) == {"type": "integer"}


def test_register_get_names():
    reg = m.ToolRegistry()

    @reg.tool
    def first() -> str:
        return "1"

    @reg.tool
    def second() -> str:
        return "2"

    assert first() == "1"  # the decorator returns the function unchanged
    assert reg.get("second") is second
    assert reg.get("nope") is None
    assert reg.names() == ["first", "second"]


def test_duplicate_name_is_rejected():
    reg = m.ToolRegistry()

    @reg.tool
    def same() -> str:
        return "a"

    with pytest.raises(ValueError):

        @reg.tool
        def same() -> str:  # noqa: F811
            return "b"


def test_schema_of_a_simple_tool():
    reg = m.ToolRegistry()

    @reg.tool
    def add(a: float, b: float) -> float:
        """Add two numbers.

        Longer text that is not part of the description.
        """
        return a + b

    assert reg.schemas() == [
        {
            "name": "add",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
            },
        }
    ]


def test_defaults_are_not_required_and_types_are_converted():
    reg = m.ToolRegistry()

    @reg.tool
    def search(query: str, limit: int = 3, tags: list[str] | None = None) -> str:
        return query

    (schema,) = reg.schemas()
    params = schema["parameters"]
    assert params["required"] == ["query"]
    assert list(params["properties"]) == ["query", "limit", "tags"]
    assert params["properties"]["limit"] == {"type": "integer"}
    assert params["properties"]["tags"] == {"type": "array", "items": {"type": "string"}}


def test_missing_docstring_gives_empty_description():
    reg = m.ToolRegistry()

    @reg.tool
    def quiet() -> None:
        return None

    assert reg.schemas()[0]["description"] == ""
    assert reg.schemas()[0]["parameters"] == {"type": "object", "properties": {}, "required": []}


def test_schemas_keep_registration_order():
    reg = m.ToolRegistry()

    @reg.tool
    def zebra() -> None: ...

    @reg.tool
    def apple() -> None: ...

    assert [s["name"] for s in reg.schemas()] == ["zebra", "apple"]


def test_parameter_without_type_hint_is_an_error():
    reg = m.ToolRegistry()

    @reg.tool
    def sloppy(x) -> None: ...

    with pytest.raises(TypeError):
        reg.schemas()


def test_module_registry_has_the_demo_tools():
    assert m.registry.names() == ["add", "search"]
