---
layout: module
module: 38-tool-calling-agent
kind: learn
title: "Applying it: a tool-calling agent"
permalink: /modules/38-tool-calling-agent/
---

<div class="box key" markdown="1">

## Key learning points

- A **tool-calling agent** is a loop: ask the model, run the tools it requests, give it the results, and repeat until it answers in plain text. A **step limit** stops endless loops.
- A **tool** is a normal Python function. A **registry** collects tools, and a **JSON Schema** built from each signature (topic 31) tells the model how to call it.
- The model's arguments are **untrusted input**. Validate them (topic 30). Return every failure as an `"error: ..."` tool result, so the model can read it and correct itself.
- Several tool calls in one reply can run **concurrently** with a `TaskGroup` (topic 33). Return the results in call order.
- Yield **events** from an async generator (topic 34), and carry a `trace_id` in a `ContextVar` (topic 29).
- Test the loop with a scripted **`FakeModel`**. No API key, no network and no randomness are involved.

</div>

This topic puts the second half of the course together. There is no vendor library here. Everything is plain Python, so you can see what an agent framework does for you. The message format below is **simplified**. Real model APIs use different field names and extra fields, but the structure is the same.

## 1. The shape of an agent

A conversation is a list of messages. Each message is a dict:

| Role | Fields | Meaning |
|---|---|---|
| `user` | `content` | What the user asked |
| `assistant` | `content` (text or `None`), optional `tool_calls` | The model's reply |
| `tool` | `tool_call_id`, `content` | The result of one tool call |

A tool call is a dict `{"id": "c1", "name": "add", "arguments": '{"a": 2, "b": 3}'}`. The `arguments` are **JSON text**, because that is what a model produces. The `id` ties a result to its call.

The loop:

1. Send the messages to the model.
2. No tool calls in the reply? That is the final answer.
3. Otherwise run each tool call, append the results, and go to step 1.

## 2. Tools and schemas

```python
TOOLS = {}


def tool(func):
    TOOLS[func.__name__] = func
    return func


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b
```

This is the registry pattern from topic 27. The model never sees Python code. It sees a **schema**, which is built from the function:

```python
import inspect
from typing import get_type_hints

JSON_TYPES = {int: "integer", float: "number", str: "string", bool: "boolean"}


def schema_of(func):
    hints = get_type_hints(func)
    sig = inspect.signature(func)
    return {
        "name": func.__name__,
        "description": inspect.getdoc(func).splitlines()[0],
        "parameters": {
            "type": "object",
            "properties": {n: {"type": JSON_TYPES[hints[n]]} for n in sig.parameters},
            "required": [n for n, p in sig.parameters.items() if p.default is p.empty],
        },
    }
```

```text
{"name": "add", "description": "Add two integers.", "parameters": {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"]}}
```

The description comes from the docstring, so **write good docstrings**. The model decides which tool to use by reading them. Assignment 1 extends this to `list[T]`, `T | None` and defaults.

## 3. Dispatch: validate, run, report errors as results

A model is a text generator, and it makes mistakes: a tool name that does not exist, broken JSON, `"two"` instead of `2`. A crash helps nobody. The agent returns the error as the **tool result**, and the model usually fixes the call on the next step.

```python
import json
from pydantic import ValidationError, validate_call


async def dispatch(call):
    func = TOOLS.get(call["name"])
    if func is None:
        return {"role": "tool", "tool_call_id": call["id"], "content": f"error: unknown tool {call['name']!r}"}
    try:
        args = json.loads(call["arguments"] or "{}")
        result = validate_call(func)(**args)
        content = result if isinstance(result, str) else json.dumps(result)
    except (json.JSONDecodeError, ValidationError) as exc:
        content = f"error: {type(exc).__name__}"
    return {"role": "tool", "tool_call_id": call["id"], "content": content}
```

`pydantic.validate_call(func)` wraps the function so that its type hints are **checked at call time**. `"3"` becomes `3` (pydantic's normal conversion), and `"two"` raises `ValidationError`. Missing and unexpected arguments are rejected too. A useful error text names the parameter, which assignment 2 asks for. An exception raised **inside** the tool must also become an error result, and tools that are `async def` must be awaited.

## 4. The loop and the fake model

```python
class FakeModel:
    def __init__(self, replies):
        self.replies = list(replies)

    async def complete(self, messages):
        return self.replies.pop(0)


async def run_agent(model, user_message, max_steps=5):
    messages = [{"role": "user", "content": user_message}]
    for step in range(1, max_steps + 1):
        reply = await model.complete(messages)
        messages.append(reply)
        calls = reply.get("tool_calls") or []
        if not calls:
            return reply["content"], messages
        for call in calls:
            messages.append(await dispatch(call))
    raise RuntimeError("too many steps")
```

`FakeModel` replays prepared replies. Here is a script in which the model first makes a mistake and then corrects it:

```python
model = FakeModel([
    {"role": "assistant", "content": None,
     "tool_calls": [{"id": "c1", "name": "add", "arguments": '{"a": "two", "b": 3}'}]},
    {"role": "assistant", "content": None,
     "tool_calls": [{"id": "c2", "name": "add", "arguments": '{"a": 2, "b": 3}'}]},
    {"role": "assistant", "content": "2 + 3 = 5"},
])
answer, messages = await run_agent(model, "What is 2 + 3?")   # inside an async function
print(answer)
for m in messages:
    print(m["role"], "|", m.get("content"), "|", [c["name"] for c in m.get("tool_calls", [])])
```

```text
2 + 3 = 5
user | What is 2 + 3? | []
assistant | None | ['add']
tool | error: ValidationError | []
assistant | None | ['add']
tool | 5 | []
assistant | 2 + 3 = 5 | []
```

The test does not check that a real model is smart. It checks that **your loop** handles the error result, stops at the final answer, and respects `max_steps`. The step limit matters, because a real model can keep asking for tools forever, and every step costs time and money.

## 5. Parallel tool calls

When a reply holds several tool calls, they are independent, so run them together:

```python
calls = [{"id": str(i), "name": "add", "arguments": json.dumps({"a": i, "b": i})} for i in range(3)]
async with asyncio.TaskGroup() as group:
    tasks = [group.create_task(dispatch(c)) for c in calls]
print([t.result()["content"] for t in tasks])
```

```text
['0', '2', '4']
```

Reading `task.result()` in the order of `tasks` keeps the results in call order. Because `dispatch` never raises, one failing tool cannot cancel the others (a `TaskGroup` cancels all tasks when one raises). To limit the load, add an `asyncio.Semaphore`.

## 6. Streaming events and trace ids

A user interface wants progress ("calling search", "result", "final answer") and not a long silence. Turn the loop into an **async generator** that yields event dicts, and let the caller use `async for`:

```python
async for event in run_agent_events(model, tools, "who am I?", trace_id="demo-1"):
    print(event)
```

```text
{'type': 'tool_call', 'name': 'whoami', 'arguments': '{}', 'trace_id': 'demo-1'}
{'type': 'tool_result', 'name': 'whoami', 'content': 'running under trace demo-1', 'trace_id': 'demo-1'}
{'type': 'final', 'content': 'done', 'trace_id': 'demo-1'}
```

The `trace_id` is stored in a `ContextVar`. Tools, log filters and nested calls can read it without a parameter, and tasks that run concurrently each keep their own value. Assignment 5 builds exactly this output.

## 7. Safety notes

- **Tool arguments are untrusted.** A model can be tricked by text in a web page or a user message (prompt injection). Never pass its arguments to a shell (`shell=True`) or build SQL from them. Use parameters and validation.
- **Give tools the least power they need.** A `read_note` tool is safer than a `run_python` tool.
- **Limit steps, time and output size.** The loop has a step limit. Add timeouts (topic 33) to slow tools, and cut very long results.
- **Keep secrets out of messages.** The messages go to the model provider and into logs (topic 36).

<div class="box warn" markdown="1">

## Common mistakes

- **Raising when a tool call is bad.** The loop stops and the model never gets the chance to correct itself. Return an `"error: ..."` result.
- **No step limit.** A confused model loops forever.
- **Trusting the arguments.** Always validate with the tool's type hints.
- **Losing the order of results.** Match results to calls by `tool_call_id`, and keep call order when you run them concurrently.
- **Testing with a real model.** The tests become slow, costly and random. Script a `FakeModel` and use real models only in a few manual checks.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

This whole page is about agents, so here is the link to real products. A provider API (OpenAI, Anthropic, Google and others) sends the tool schemas along with the messages and returns tool calls in its own format. Field names, the way arguments are encoded, and streaming details differ. The loop is the same: **call, run tools, append results, repeat**. If you replace `FakeModel` with a class that has the same `complete(messages)` method and talks to a provider, your loop, registry and tests keep working. Frameworks add retries, memory and planning on top of this core.

</div>

## Try it yourself

1. Add a tool `word_count(text: str) -> int` to the registry. Print its schema.
2. Write a `FakeModel` script in which the model asks for a tool that does not exist, then gives a final answer. What does the tool message say?
3. Add a second tool and write one reply with two tool calls. Run them with a `TaskGroup` and check the order of the results.

## Further reading

- [`asyncio.TaskGroup`](https://docs.python.org/3/library/asyncio-task.html#task-groups)
- [`contextvars`](https://docs.python.org/3/library/contextvars.html)
- [`inspect.signature`](https://docs.python.org/3/library/inspect.html#inspect.signature)
- [pydantic `validate_call`](https://docs.pydantic.dev/latest/concepts/validation_decorator/)
- [JSON Schema](https://json-schema.org/understanding-json-schema)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="38-tool-calling-agent:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/38-tool-calling-agent/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/38-tool-calling-agent/assignments/' | relative_url }}).
