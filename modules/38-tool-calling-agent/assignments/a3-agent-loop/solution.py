"""Assignment 3: the agent loop.

An agent is a loop:

    1. Send the conversation to the model.
    2. If the model answers with text only, that is the final answer. Stop.
    3. If the model asks for tools, run them, add the results to the
       conversation and go back to step 1.

A step limit stops a model that never gives a final answer. The model here is a
scripted ``FakeModel`` (it replays prepared replies), so everything is
deterministic. The message format is simplified; real APIs differ in detail.
"""

import inspect
import json
from collections.abc import Callable
from dataclasses import dataclass

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


class MaxStepsError(Exception):
    """The model did not give a final answer within the step limit."""


@dataclass
class AgentResult:
    answer: str
    messages: list[dict]
    steps: int  # how many times the model was called


async def run_agent(
    model,
    registry: ToolRegistry,
    user_message: str,
    *,
    max_steps: int = 5,
    system: str | None = None,
) -> AgentResult:
    """Run the loop and return an ``AgentResult``.

    The conversation is a list of message dicts:

    * start with ``{"role": "system", "content": system}`` when ``system`` is
      not ``None``, then ``{"role": "user", "content": user_message}``;
    * each model reply (an assistant message, a dict with ``"role": "assistant"``,
      ``"content"`` and optionally ``"tool_calls"``) is appended as it is;
    * each tool result from ``dispatch`` is appended after the reply, in the
      order of the tool calls. Run the calls one after the other.

    A step is one call of ``await model.complete(messages)``. After a reply
    without tool calls (missing, ``None`` or an empty list) return
    ``AgentResult(answer=reply["content"] or "", messages=messages, steps=n)``.
    If ``max_steps`` replies were all tool requests, raise
    ``MaxStepsError`` (the message should contain ``max_steps``).
    """
    messages: list[dict] = []
    if system is not None:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user_message})

    for step in range(1, max_steps + 1):
        reply = await model.complete(messages)
        messages.append(reply)
        tool_calls = reply.get("tool_calls") or []
        if not tool_calls:
            return AgentResult(answer=reply.get("content") or "", messages=messages, steps=step)
        for call in tool_calls:
            messages.append(await dispatch(registry, call))
    raise MaxStepsError(f"no final answer after max_steps={max_steps}")


if __name__ == "__main__":
    import asyncio

    tools = ToolRegistry()

    @tools.tool
    def add(a: int, b: int) -> int:
        return a + b

    script = [
        {"role": "assistant", "content": None,
         "tool_calls": [{"id": "c1", "name": "add", "arguments": '{"a": 2, "b": 3}'}]},
        {"role": "assistant", "content": "2 + 3 = 5"},
    ]

    async def main() -> None:
        result = await run_agent(FakeModel(script), tools, "What is 2 + 3?")
        print(result.answer, "after", result.steps, "steps")

    asyncio.run(main())
