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
    if tp in SCALARS:
        return {"type": SCALARS[tp]}
    origin = get_origin(tp)
    if origin is list:
        (item,) = get_args(tp)
        return {"type": "array", "items": type_schema(item)}
    if origin in (Union, types.UnionType):
        options = [arg for arg in get_args(tp) if arg is not type(None)]
        if len(options) == 1:
            return type_schema(options[0])
    raise TypeError(f"unsupported type: {tp!r}")


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
        if func.__name__ in self._tools:
            raise ValueError(f"tool {func.__name__!r} is already registered")
        self._tools[func.__name__] = func
        return func

    def get(self, name: str) -> Callable | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return list(self._tools)

    def schemas(self) -> list[dict]:
        return [self._schema(func) for func in self._tools.values()]

    @staticmethod
    def _schema(func: Callable) -> dict:
        hints = get_type_hints(func)
        properties: dict[str, dict] = {}
        required: list[str] = []
        for name, param in inspect.signature(func).parameters.items():
            if name not in hints:
                raise TypeError(f"parameter {name!r} of {func.__name__} has no type hint")
            properties[name] = type_schema(hints[name])
            if param.default is inspect.Parameter.empty:
                required.append(name)
        doc = inspect.getdoc(func) or ""
        return {
            "name": func.__name__,
            "description": doc.splitlines()[0] if doc else "",
            "parameters": {"type": "object", "properties": properties, "required": required},
        }


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
