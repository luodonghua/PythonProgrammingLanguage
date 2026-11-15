---
layout: module
module: 29-context-managers-contextvars
kind: assignments
title: "Context managers and contextvars - assignments"
permalink: /modules/29-context-managers-contextvars/assignments/
---
Five tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/29-context-managers-contextvars
```

---

<div class="assignment" markdown="1">

## Assignment 1: Timer and temporary environment

**Goal:** Write a `Timer` context manager class (with an injected clock) and a `temporary_env` context manager function. Practises `__enter__`, `__exit__`, `@contextmanager` and `finally`.

**Files:** [`starter.py`]({{ 'modules/29-context-managers-contextvars/assignments/a1-timer-env/starter.py' | relative_url }}), test file `test_a1_timer_env.py` in the same folder.

```python
{% include_relative assignments/a1-timer-env/starter.py %}
```

Run: `uv run pytest modules/29-context-managers-contextvars/assignments/a1-timer-env`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-timer-env/solution.py %}
```

`Timer.__exit__` returns `False`, so errors are not hidden, and it records the time in every case. `temporary_env` remembers the old values first, and puts them back in `finally`, so a failing block cannot leave the environment changed.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Rollback and error collector

**Goal:** Write a `transaction` manager that commits a working copy only on success, and an `ErrorCollector` that swallows chosen exceptions. Practises how `__exit__` and `@contextmanager` treat exceptions.

**Files:** [`starter.py`]({{ 'modules/29-context-managers-contextvars/assignments/a2-transactions/starter.py' | relative_url }}), test file `test_a2_transactions.py` in the same folder.

```python
{% include_relative assignments/a2-transactions/starter.py %}
```

Run: `uv run pytest modules/29-context-managers-contextvars/assignments/a2-transactions`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-transactions/solution.py %}
```

In `transaction`, the commit lines come after `yield`. If the block raises, the exception is thrown into the generator at the `yield`, so the commit never runs and `db` stays unchanged. `ErrorCollector.__exit__` returns `True` only for the listed types, which is what swallows the error.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: ExitStack and redirect_stdout

**Goal:** Open any number of files with `ExitStack`, capture what a function prints, and close several objects in reverse order. Practises the tools in `contextlib`.

**Files:** [`starter.py`]({{ 'modules/29-context-managers-contextvars/assignments/a3-exitstack/starter.py' | relative_url }}), test file `test_a3_exitstack.py` in the same folder.

```python
{% include_relative assignments/a3-exitstack/starter.py %}
```

Run: `uv run pytest modules/29-context-managers-contextvars/assignments/a3-exitstack`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-exitstack/solution.py %}
```

`stack.enter_context` registers each file as soon as it is opened. If the third `open` fails, the stack still closes the first two while the error propagates. `redirect_stdout` swaps `sys.stdout` for the buffer and restores it afterwards.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Request id in a ContextVar

**Goal:** Keep a request id in a `ContextVar`, bind it for a block with a token, wrap it in a decorator, and run code in a copy of the context. Practises `set`, `get`, `reset` and `copy_context`.

**Files:** [`starter.py`]({{ 'modules/29-context-managers-contextvars/assignments/a4-request-id/starter.py' | relative_url }}), test file `test_a4_request_id.py` in the same folder.

```python
{% include_relative assignments/a4-request-id/starter.py %}
```

Run: `uv run pytest modules/29-context-managers-contextvars/assignments/a4-request-id`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-request-id/solution.py %}
```

`set()` returns a `Token` and `reset(token)` restores the exact previous value, so nested blocks unwind correctly. `copy_context().run(...)` runs the function in a copy, so its changes disappear when it returns.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 5: Isolation between asyncio tasks

**Goal:** Show with `asyncio.gather` that each task has its own context value, and that a child task starts with a copy of its parent's context. Practises `ContextVar` with async code. The tests are `async def` functions.

**Files:** [`starter.py`]({{ 'modules/29-context-managers-contextvars/assignments/a5-async-isolation/starter.py' | relative_url }}), test file `test_a5_async_isolation.py` in the same folder.

```python
{% include_relative assignments/a5-async-isolation/starter.py %}
```

Run: `uv run pytest modules/29-context-managers-contextvars/assignments/a5-async-isolation`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a5-async-isolation/solution.py %}
```

`gather` wraps each coroutine in a task, and a task copies the current context when it is created. Setting the variable in one task therefore does not change what another task, or the caller, sees.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="29-context-managers-contextvars:assignments"> I have finished the assignments</label></li>
</ul>
