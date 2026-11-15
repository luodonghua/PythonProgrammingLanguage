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
    # TODO: build a dict of {name: (type, default)} and call create_model.
    ...


def strip_titles(schema):
    """Return a copy of a JSON Schema without the "title" keys pydantic adds.

    Remove a "title" key only when its value is a string (a property that is
    itself called "title" has a dict value and must stay). Work recursively
    through dicts and lists.
    """
    # TODO: recurse through dicts and lists.
    ...


def pydantic_schema(func) -> dict:
    """Return the JSON Schema of `model_for(func)` with titles removed."""
    # TODO: combine model_for, model_json_schema and strip_titles.
    ...


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
    # TODO: model.model_validate(args), catch ValidationError, use exc.errors().
    ...


if __name__ == "__main__":
    def search(query: str, limit: int = 10) -> list:
        """Search the catalogue."""
        return []

    print(pydantic_schema(search))
    print(validate_args(search, {"query": "cats", "limit": "5"}))
