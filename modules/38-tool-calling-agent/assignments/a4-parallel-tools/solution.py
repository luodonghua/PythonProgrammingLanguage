"""Assignment 4: run several tool calls at the same time.

A model may ask for more than one tool in a single reply ("get the weather in
Paris and in Rome"). The calls do not depend on each other, so the program can
run them concurrently with a ``TaskGroup`` (topic 33). The results must still
be returned in the order of the calls, because the model matches them by id.
"""

import asyncio
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



def _tool_message(call: dict, content: str) -> dict:
    return {"role": "tool", "tool_call_id": call.get("id", ""), "content": content}


async def dispatch_all(registry: ToolRegistry, calls: list[dict], *, limit: int | None = None) -> list[dict]:
    """Run all ``calls`` concurrently and return their tool messages in call order.

    * Use ``asyncio.TaskGroup`` and ``dispatch`` (which never raises, so one
      failing tool does not cancel the others).
    * ``limit`` is the largest number of tools that may run at the same moment.
      ``None`` means no limit. Use an ``asyncio.Semaphore``.
    * An empty ``calls`` list returns ``[]``.
    """
    semaphore = asyncio.Semaphore(limit) if limit is not None else None

    async def run_one(call: dict) -> dict:
        if semaphore is None:
            return await dispatch(registry, call)
        async with semaphore:
            return await dispatch(registry, call)

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(run_one(call)) for call in calls]
    return [task.result() for task in tasks]


if __name__ == "__main__":
    tools = ToolRegistry()

    @tools.tool
    async def lookup(city: str) -> str:
        await asyncio.sleep(0)
        return f"{city}: sunny"

    async def main() -> None:
        calls = [
            {"id": "1", "name": "lookup", "arguments": '{"city": "Paris"}'},
            {"id": "2", "name": "lookup", "arguments": '{"city": "Rome"}'},
        ]
        for message in await dispatch_all(tools, calls):
            print(message)

    asyncio.run(main())
