"""Assignment 5 (optional): stream what the agent does, with a trace id.

A user interface wants to show progress while the agent works: "calling
search ...", "got a result", the final answer. The agent loop becomes an *async
generator* (topic 34) that yields small event dicts. Every event carries a
``trace_id`` so that the log lines and events of one run can be matched. Tools
can read the id from a ``ContextVar`` (topic 29).
"""

import inspect
import json
import uuid
from collections.abc import AsyncIterator, Callable
from contextvars import ContextVar

from pydantic import ValidationError, validate_call

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="-")


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


class FakeModel:
    """A scripted stand-in for a language model.

    ``FakeModel(replies)`` returns the assistant messages in ``replies`` one by
    one. ``seen`` keeps a copy of the messages list of every call.
    """

    def __init__(self, replies: list[dict]) -> None:
        self._replies = list(replies)
        self.seen: list[list[dict]] = []

    async def complete(self, messages: list[dict]) -> dict:
        self.seen.append(list(messages))
        if not self._replies:
            raise AssertionError("FakeModel script exhausted")
        return self._replies.pop(0)


async def run_agent_events(
    model,
    registry: ToolRegistry,
    user_message: str,
    *,
    max_steps: int = 5,
    trace_id: str | None = None,
) -> AsyncIterator[dict]:
    """Run the agent loop and yield one event dict at a time.

    Use ``trace_id`` if it is given, otherwise ``uuid.uuid4().hex[:8]``. Before
    the first event, set ``trace_id_var`` to it (so tools that run later see it
    with ``trace_id_var.get()``). When the generator ends, reset the variable
    to its old value (``Token`` from ``set``); if resetting raises ``ValueError``
    (the generator was closed in another context), ignore that.

    Events (every dict has the key ``"trace_id"``):

    * ``{"type": "tool_call", "name": ..., "arguments": ..., "trace_id": ...}``
      just before a tool is run (``arguments`` is the JSON text);
    * ``{"type": "tool_result", "name": ..., "content": ..., "trace_id": ...}``
      after it ran (``content`` from ``dispatch``);
    * ``{"type": "final", "content": <answer text>, "trace_id": ...}`` when the
      model answers without tool calls. Then stop;
    * ``{"type": "error", "content": "no final answer after N steps", "trace_id": ...}``
      (N is ``max_steps``) when the step limit is reached. Then stop. Do not raise.

    The loop is the one from assignment 3: messages start with the user
    message, each reply and each tool message is appended, tool calls run one
    after the other.
    """
    # TODO: set trace_id_var, loop like assignment 3, yield events, reset in "finally".
    # The "yield" below makes this function an async generator; delete it when you add your own.
    yield {}


if __name__ == "__main__":
    import asyncio

    tools = ToolRegistry()

    @tools.tool
    def whoami() -> str:
        return f"running under trace {trace_id_var.get()}"

    script = [
        {"role": "assistant", "content": None, "tool_calls": [{"id": "c1", "name": "whoami", "arguments": "{}"}]},
        {"role": "assistant", "content": "done"},
    ]

    async def main() -> None:
        async for event in run_agent_events(FakeModel(script), tools, "who am I?", trace_id="demo-1"):
            print(event)

    asyncio.run(main())
