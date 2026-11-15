"""Assignment 1: a tool registry that describes its tools.

A *tool* is an ordinary Python function that an agent may call. The agent must
know each tool's name, purpose and parameters. This is usually sent to the
model as a JSON Schema. You build the schema from the function itself, using
its docstring and its type hints (topic 31).
"""

import inspect
import types
from collections.abc import Callable
from typing import Union, get_args, get_origin, get_type_hints

SCALARS = {int: "integer", float: "number", str: "string", bool: "boolean"}


def type_schema(tp) -> dict:
    """Return the JSON Schema for a type hint.

    * ``int`` -> ``{"type": "integer"}``, ``float`` -> ``"number"``,
      ``str`` -> ``"string"``, ``bool`` -> ``"boolean"``.
    * ``list[T]`` -> ``{"type": "array", "items": type_schema(T)}``.
    * ``T | None`` (also ``Optional[T]``) -> the schema of ``T``.
    * Anything else raises ``TypeError`` with the type in the message.
    """
    # TODO: handle scalars, list[T] and T | None; raise TypeError otherwise.
    ...


class ToolRegistry:
    """Collects tool functions and describes them.

    * ``@registry.tool`` registers a function under ``func.__name__`` and
      returns the function unchanged. Registering a name twice raises
      ``ValueError``.
    * ``get(name)`` returns the function, or ``None`` if there is none.
    * ``names()`` returns the registered names in registration order.
    * ``schemas()`` returns one dict per tool, in registration order:

          {"name": "add",
           "description": "Add two numbers.",
           "parameters": {"type": "object",
                          "properties": {"a": {"type": "number"}, ...},
                          "required": ["a", "b"]}}

      ``description`` is the first line of the docstring (``""`` if there is
      none). ``properties`` has one entry per parameter, made with
      ``type_schema`` from ``typing.get_type_hints(func)``. ``required`` lists,
      in order, the parameters that have no default value. A parameter
      without a type hint raises ``TypeError`` (when ``schemas`` is called).
    """

    def __init__(self) -> None:
        self._tools: dict[str, Callable] = {}

    def tool(self, func: Callable) -> Callable:
        # TODO: reject duplicates, store the function, return it.
        ...

    def get(self, name: str) -> Callable | None:
        # TODO
        ...

    def names(self) -> list[str]:
        # TODO
        ...

    def schemas(self) -> list[dict]:
        # TODO: use inspect.signature, typing.get_type_hints and inspect.getdoc.
        ...


registry = ToolRegistry()


@registry.tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@registry.tool
def search(query: str, limit: int = 3, tags: list[str] | None = None) -> str:
    """Search the notes."""
    return f"results for {query}"


if __name__ == "__main__":
    import json

    print(json.dumps(registry.schemas(), indent=2))
