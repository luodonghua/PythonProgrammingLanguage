"""Assignment 2: Build a JSON Schema from a function signature.

Tool-calling systems describe each function to the caller as a JSON Schema.
You will generate that description from the function's type hints.
"""

import inspect
import types
import typing
from typing import Literal, get_args, get_origin, get_type_hints

SIMPLE_TYPES = {int: "integer", float: "number", str: "string", bool: "boolean"}
UNION_ORIGINS = (typing.Union, types.UnionType)


def type_to_schema(tp) -> dict:
    """Convert one type hint to a JSON Schema fragment.

    int   -> {"type": "integer"}      float -> {"type": "number"}
    str   -> {"type": "string"}       bool  -> {"type": "boolean"}
    list[T]            -> {"type": "array", "items": <schema of T>}
    Literal["a", "b"]  -> {"enum": ["a", "b"]}
    X | None           -> {"anyOf": [<schema of X>, {"type": "null"}]}
    Any other type raises TypeError(f"unsupported type: {tp!r}").
    """
    # TODO: handle simple types, then use get_origin/get_args for the rest.
    ...


def build_schema(func) -> dict:
    """Describe `func` as a tool definition.

    Return:
      {"name": func.__name__,
       "description": <first line of the docstring, or "">,
       "parameters": {"type": "object",
                      "properties": {<param name>: <schema>, ...},
                      "required": [<names of parameters without a default>]}}

    Rules:
      - Use `typing.get_type_hints(func)` for the types.
      - A parameter with no annotation gets the empty schema {}.
      - Skip `*args` and `**kwargs`.
      - Keep parameters in signature order. "required" is always present
        (an empty list when nothing is required).
    """
    # TODO: loop over inspect.signature(func).parameters.items().
    ...


if __name__ == "__main__":
    import json

    def search(query: str, limit: int = 10, tags: list[str] | None = None) -> list:
        """Search the catalogue."""
        return []

    print(json.dumps(build_schema(search), indent=2))
