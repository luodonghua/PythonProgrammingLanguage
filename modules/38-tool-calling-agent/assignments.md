---
layout: module
module: 38-tool-calling-agent
kind: assignments
title: "Applying it: a tool-calling agent - assignments"
permalink: /modules/38-tool-calling-agent/assignments/
---
Build the core of a tool-calling agent from scratch, one stage at a time: a tool registry that describes its tools, a safe dispatcher, the agent loop, parallel tool calls and a stream of events. There is no vendor library and no network. A scripted `FakeModel` plays the part of the language model. The message format is simplified, and real APIs differ in detail.

{% include practice-setup.md %}

This topic uses `pydantic` (`validate_call` checks tool arguments), which the project already lists. Each stage is self-contained. Assignments 2 to 5 include a short copy of the code from the earlier stages in `starter.py`, so you can do them in any order. Tests are `async def` functions and need no decorator, because the project runs `pytest-asyncio` in auto mode.

Run all tests for this topic:

```bash
uv run pytest modules/38-tool-calling-agent
```

---

<div class="assignment" markdown="1">

## Assignment 1: Tool registry and schemas

**Goal:** Write a `ToolRegistry` with a `@tool` decorator and `schemas()`, which describes each tool's name, description, parameters and required parameters as JSON Schema. Practises `inspect.signature`, `get_type_hints`, `get_origin` and `get_args`.

**Files:** [`starter.py`]({{ 'modules/38-tool-calling-agent/assignments/a1-registry-schema/starter.py' | relative_url }}), test file `test_a1_registry_schema.py` in the same folder.

```python
{% include_relative assignments/a1-registry-schema/starter.py %}
```

Run: `uv run pytest modules/38-tool-calling-agent/assignments/a1-registry-schema`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-registry-schema/solution.py %}
```

`type_schema` maps scalars with a dictionary and handles `list[T]` and `T | None` by recursion. `schemas()` walks `inspect.signature`, uses `get_type_hints` for the types, and marks a parameter as required when its default is `inspect.Parameter.empty`. The `Union` check covers both `Optional[int]` and `int | None`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Dispatch with validation and error results

**Goal:** Write `dispatch`, which runs one tool call and always returns a tool message. Unknown tools, bad JSON, wrong arguments and tool exceptions become `error: ...` messages. Practises `validate_call`, JSON parsing and defensive error handling.

**Files:** [`starter.py`]({{ 'modules/38-tool-calling-agent/assignments/a2-dispatch/starter.py' | relative_url }}), test file `test_a2_dispatch.py` in the same folder.

```python
{% include_relative assignments/a2-dispatch/starter.py %}
```

Run: `uv run pytest modules/38-tool-calling-agent/assignments/a2-dispatch`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-dispatch/solution.py %}
```

`validate_call(func)(**args)` checks the arguments against the type hints. A `ValidationError` is caught before the general `Exception`, because the first one gives a better message. An async tool returns a coroutine, so the code awaits it when `inspect.isawaitable` is true. An outer `try` makes sure that `dispatch` never raises.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: The agent loop

**Goal:** Write `run_agent`, which calls the model, runs tool requests, feeds the results back and stops at the final answer or at a step limit. The tests use a scripted fake model that makes mistakes and then recovers.

**Files:** [`starter.py`]({{ 'modules/38-tool-calling-agent/assignments/a3-agent-loop/starter.py' | relative_url }}), test file `test_a3_agent_loop.py` in the same folder.

```python
{% include_relative assignments/a3-agent-loop/starter.py %}
```

Run: `uv run pytest modules/38-tool-calling-agent/assignments/a3-agent-loop`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-agent-loop/solution.py %}
```

The loop keeps one `messages` list. Each reply and each tool message is appended, so the model sees the whole history on the next step. Reaching the end of the `for` loop without a final answer raises `MaxStepsError`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Parallel tool calls

**Goal:** Write `dispatch_all`, which runs the tool calls of one reply at the same time in a `TaskGroup`, keeps the call order of the results and can limit concurrency. Practises `TaskGroup`, `Semaphore` and result ordering.

**Files:** [`starter.py`]({{ 'modules/38-tool-calling-agent/assignments/a4-parallel-tools/starter.py' | relative_url }}), test file `test_a4_parallel_tools.py` in the same folder.

```python
{% include_relative assignments/a4-parallel-tools/starter.py %}
```

Run: `uv run pytest modules/38-tool-calling-agent/assignments/a4-parallel-tools`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-parallel-tools/solution.py %}
```

Each call becomes a task. Reading `task.result()` in the order of the task list keeps the call order. `dispatch` never raises, so a failing tool cannot cancel the group. An optional semaphore limits how many tools run together.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 5: Streamed events with a trace id

**Goal:** Turn the loop into an async generator that yields `tool_call`, `tool_result`, `final` and `error` events, each carrying a trace id that tools can read from a `ContextVar`. This one is optional.

**Files:** [`starter.py`]({{ 'modules/38-tool-calling-agent/assignments/a5-event-stream/starter.py' | relative_url }}), test file `test_a5_event_stream.py` in the same folder.

```python
{% include_relative assignments/a5-event-stream/starter.py %}
```

Run: `uv run pytest modules/38-tool-calling-agent/assignments/a5-event-stream`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a5-event-stream/solution.py %}
```

The generator sets the `ContextVar` before its first event and resets it in `finally`. Tools run in the same task, so they see the id. The `finally` also runs when the consumer closes the stream early with `aclose()`.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="38-tool-calling-agent:assignments"> I have finished the assignments</label></li>
</ul>
