import pytest
from pydantic import BaseModel

from practice import load

m = load(__file__)


def search(query: str, limit: int = 10, tags: list[str] | None = None, *extra, **options):
    """Search."""


def test_model_for_returns_a_model_class():
    model = m.model_for(search)
    assert issubclass(model, BaseModel)
    assert model.__name__ == "search"
    assert list(model.model_fields) == ["query", "limit", "tags"]
    assert model.model_fields["query"].is_required()
    assert not model.model_fields["limit"].is_required()
    assert model.model_fields["limit"].default == 10


def test_model_for_untyped_parameter_is_any():
    def echo(value):
        return value

    model = m.model_for(echo)
    assert model.model_validate({"value": [1, "x"]}).value == [1, "x"]


def test_strip_titles():
    schema = {
        "title": "T",
        "properties": {"title": {"title": "Title", "type": "string"}, "a": {"title": "A", "type": "integer"}},
        "anyOf": [{"title": "X", "type": "null"}],
    }
    assert m.strip_titles(schema) == {
        "properties": {"title": {"type": "string"}, "a": {"type": "integer"}},
        "anyOf": [{"type": "null"}],
    }


def test_strip_titles_does_not_change_input():
    schema = {"title": "T", "type": "object"}
    assert m.strip_titles(schema) == {"type": "object"}
    assert schema == {"title": "T", "type": "object"}


def test_pydantic_schema():
    schema = m.pydantic_schema(search)
    assert schema["type"] == "object"
    assert schema["required"] == ["query"]
    assert schema["properties"]["query"] == {"type": "string"}
    assert schema["properties"]["limit"] == {"type": "integer", "default": 10}
    assert schema["additionalProperties"] is False
    assert "title" not in schema
    assert all("title" not in prop for prop in schema["properties"].values())


def test_validate_args_coerces_and_fills_defaults():
    assert m.validate_args(search, {"query": "cats", "limit": "5"}) == {
        "query": "cats",
        "limit": 5,
        "tags": None,
    }


def test_validate_args_missing_and_extra():
    with pytest.raises(m.ArgumentError) as info:
        m.validate_args(search, {"depth": 2})
    assert info.value.errors == ["query: missing", "depth: extra_forbidden"]


def test_validate_args_bad_types_with_nested_location():
    def tag_all(tags: list[str], limit: int = 1):
        pass

    with pytest.raises(m.ArgumentError) as info:
        m.validate_args(tag_all, {"tags": ["a", 1], "limit": "many"})
    assert info.value.errors == ["tags.1: string_type", "limit: int_parsing"]


def test_validate_args_error_is_chained():
    with pytest.raises(m.ArgumentError) as info:
        m.validate_args(search, {})
    assert info.value.__cause__ is not None
