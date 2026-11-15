"""Assignment 4: Let pydantic do the schema and validation work.

In assignments 2 and 3 you wrote a schema builder and a validator by hand.
Pydantic can build both from the same signature: make a model whose fields are
the function's parameters, then use the model.
"""

import inspect
from typing import Any, get_type_hints

from pydantic import BaseModel, ConfigDict, ValidationError, create_model


class ArgumentError(Exception):
    """Raised when JSON arguments do not fit a function (provided)."""

    def __init__(self, errors: list[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


def model_for(func) -> type[BaseModel]:
    """Build a pydantic model class with one field per parameter of `func`.

    - Field type: the type hint, or `Any` when the parameter has no hint.
    - A parameter without a default is a required field (use `...`).
    - A parameter with a default gets that default.
    - Skip `*args` and `**kwargs`.
    - Reject unknown keys: pass `__config__=ConfigDict(extra="forbid")`.
    - Name the model after the function: `create_model(func.__name__, ...)`.
    """
    hints = get_type_hints(func)
    fields = {}
    for name, param in inspect.signature(func).parameters.items():
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        default = ... if param.default is inspect.Parameter.empty else param.default
        fields[name] = (hints.get(name, Any), default)
    return create_model(func.__name__, __config__=ConfigDict(extra="forbid"), **fields)


def strip_titles(schema):
    """Return a copy of a JSON Schema without the "title" keys pydantic adds.

    Remove a "title" key only when its value is a string (a property that is
    itself called "title" has a dict value and must stay). Work recursively
    through dicts and lists.
    """
    if isinstance(schema, dict):
        return {
            key: strip_titles(value)
            for key, value in schema.items()
            if not (key == "title" and isinstance(value, str))
        }
    if isinstance(schema, list):
        return [strip_titles(item) for item in schema]
    return schema


def pydantic_schema(func) -> dict:
    """Return the JSON Schema of `model_for(func)` with titles removed."""
    return strip_titles(model_for(func).model_json_schema())


def validate_args(func, args: dict) -> dict:
    """Validate `args` for `func` with pydantic and return the clean values.

    On success return `model.model_dump()`, a dict of every parameter, with
    defaults filled in and values coerced (the string "5" becomes the int 5
    for an int field).
    On failure raise ArgumentError. Its `errors` list has one entry per
    pydantic error, in pydantic's order, formatted as "<location>: <type>"
    where <location> joins `error["loc"]` with dots and <type> is
    `error["type"]`. Examples: "a: int_parsing", "b.0: string_type",
    "z: extra_forbidden", "a: missing".
    """
    model = model_for(func)
    try:
        return model.model_validate(args).model_dump()
    except ValidationError as exc:
        errors = [
            f"{'.'.join(str(part) for part in err['loc'])}: {err['type']}"
            for err in exc.errors()
        ]
        raise ArgumentError(errors) from exc


if __name__ == "__main__":
    def search(query: str, limit: int = 10) -> list:
        """Search the catalogue."""
        return []

    print(pydantic_schema(search))
    print(validate_args(search, {"query": "cats", "limit": "5"}))
