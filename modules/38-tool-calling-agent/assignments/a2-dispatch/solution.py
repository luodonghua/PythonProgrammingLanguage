"""Assignment 2: run a tool call safely.

The model asks for a tool with a *tool call*: a name and the arguments as JSON
text. The model can make mistakes: wrong name, broken JSON, wrong types. The
program must not crash. It returns the error as the tool's *result*, in plain
words, so the model can read it and try again.

The message format here is simplified. Real model APIs differ in the details.
"""

import inspect
import json
from collections.abc import Callable

from pydantic import ValidationError, validate_call


class ToolRegistry:
    """A table of tools by name. (A short version of the one from assignment 1.)"""

    def __init__(self) -> None:
        self._tools: dict[str, Callable] = {}

    def tool(self, func: Callable) -> Callable:
        """Decorator: register ``func`` under its own name and return it unchanged."""
        self._tools[func.__name__] = func
        return func

    def get(self, name: str) -> Callable | None:
        return self._tools.get(name)


def _tool_message(call: dict, content: str) -> dict:
    return {"role": "tool", "tool_call_id": call.get("id", ""), "content": content}


async def dispatch(registry: ToolRegistry, call: dict) -> dict:
    """Run one tool call and ALWAYS return a tool message (never raise).

    ``call`` looks like ``{"id": "c1", "name": "add", "arguments": '{"a": 1}'}``,
    where ``arguments`` is a JSON text. The result is
    ``{"role": "tool", "tool_call_id": call["id"], "content": <text>}``.
    Missing, empty or blank ``arguments`` mean ``{}`` (no arguments).
    The content is the tool result as text (a ``str`` result as it is, any
    other result with ``json.dumps``), or an error text that starts with
    ``"error:"`` for: an unknown tool, arguments that are not valid JSON or not
    a JSON object, arguments that fail validation, and an exception in the tool.
    """
    try:
        func = registry.get(call["name"])
        if func is None:
            return _tool_message(call, f"error: unknown tool {call['name']!r}")
        raw = (call.get("arguments") or "").strip() or "{}"
        try:
            args = json.loads(raw)
        except json.JSONDecodeError:
            return _tool_message(call, "error: arguments are not valid JSON")
        if not isinstance(args, dict):
            return _tool_message(call, "error: arguments must be a JSON object")
        try:
            result = validate_call(func)(**args)
            if inspect.isawaitable(result):
                result = await result
        except ValidationError as exc:
            problems = "; ".join(
                f"{'.'.join(str(part) for part in err['loc'])}: {err['msg']}" for err in exc.errors()
            )
            return _tool_message(call, f"error: invalid arguments: {problems}")
        except Exception as exc:
            return _tool_message(call, f"error: tool {call['name']!r} failed: {type(exc).__name__}: {exc}")
        return _tool_message(call, result if isinstance(result, str) else json.dumps(result))
    except Exception as exc:  # last safety net: dispatch never raises
        return _tool_message(call, f"error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    import asyncio

    demo = ToolRegistry()

    @demo.tool
    def add(a: int, b: int) -> int:
        return a + b

    async def main() -> None:
        for arguments in ('{"a": 1, "b": 2}', '{"a": "x", "b": 2}', "not json"):
            print(await dispatch(demo, {"id": "c1", "name": "add", "arguments": arguments}))

    asyncio.run(main())
