"""Assignment 3: Call a function with arguments that came from JSON.

JSON arguments come from outside your program, so they must be checked before
the call. `call_with_json_args` validates a dict of arguments against the
function's signature and type hints, then calls the function.
"""

import inspect
import types
import typing
from typing import Literal, get_args, get_origin, get_type_hints

UNION_ORIGINS = (typing.Union, types.UnionType)
JSON_NAMES = {
    int: "integer",
    float: "number",
    str: "string",
    bool: "boolean",
    list: "array",
    dict: "object",
    type(None): "null",
}


class ArgumentError(Exception):
    """Raised when JSON arguments do not fit a function.

    `errors` is a list of human-readable messages.
    """

    def __init__(self, errors: list[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


def json_type_name(value) -> str:
    """Name of the JSON type of a Python value (provided, no change needed)."""
    for py_type, name in JSON_NAMES.items():
        if type(value) is py_type:
            return name
    return type(value).__name__


def matches(value, hint) -> bool:
    """Return True if `value` fits the type hint `hint`.

    Supported hints: int, float, str, bool, list[T], Literal[...], X | None,
    and any other class (checked with isinstance).
    Rules:
      - A bool is NOT an int or a float, although `isinstance(True, int)` is True.
      - An int is accepted where a float is expected.
      - list[T] needs a list whose items all match T.
    """
    # TODO: handle unions, Literal and list[T] with get_origin/get_args.
    # Then treat bool specially, accept int for float, and use isinstance.
    ...


def call_with_json_args(func, args: dict):
    """Validate `args` and return `func(**args)`.

    Check every parameter of `func` in signature order (skip *args and
    **kwargs). Collect ALL problems, then raise one ArgumentError(errors):
      - a required parameter that is missing:  "missing argument: <name>"
      - a value of the wrong type (only when the parameter has a type hint):
            "argument <name>: expected <hint>, got <json type name>"
        where <hint> is `hint.__name__` for a plain class such as int, and
        `str(hint)` for anything else, for example "list[str]". Use
        `json_type_name(value)` for the last part.
    After the parameter checks, add one message per unknown key, in sorted
    order:  "unknown argument: <name>".
    If there are no problems, call the function with keyword arguments.
    Parameters that are not in `args` keep their defaults.
    """
    # TODO: collect errors in a list, raise ArgumentError(errors) if not empty.
    ...


if __name__ == "__main__":
    def add(a: int, b: int = 1) -> int:
        return a + b

    print(call_with_json_args(add, {"a": 2}))
    try:
        call_with_json_args(add, {"a": "2", "c": 0})
    except ArgumentError as exc:
        print(exc.errors)
