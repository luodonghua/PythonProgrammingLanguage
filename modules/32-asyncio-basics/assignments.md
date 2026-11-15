---
layout: module
module: 32-asyncio-basics
kind: assignments
title: "asyncio basics - assignments"
permalink: /modules/32-asyncio-basics/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

The tests are `async def` functions. The project runs pytest-asyncio in auto mode, so you do not need a decorator. Tests never wait for real time: they use `asyncio.sleep(0)` and events, so they are fast and the same on every machine.

Run all tests for this topic:

```bash
uv run pytest modules/32-asyncio-basics
```

---

<div class="assignment" markdown="1">

## Assignment 1: Run jobs concurrently

**Goal:** Run a list of async jobs at the same time and return results in input order. Then make a version that reports each failure without losing the other results.

**Files:** [`starter.py`]({{ 'modules/32-asyncio-basics/assignments/a1-run-jobs/starter.py' | relative_url }}), test file `test_a1_run_jobs.py` in the same folder.

```python
{% include_relative assignments/a1-run-jobs/starter.py %}
```

Run: `uv run pytest modules/32-asyncio-basics/assignments/a1-run-jobs`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-run-jobs/solution.py %}
```

`asyncio.gather` starts all coroutines and keeps the input order. `return_exceptions=True` puts exception objects into the result list, and you label them with `isinstance`. Jobs are passed as factories, so no coroutine exists before you start it.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Bounded concurrency

**Goal:** Process many items with at most N running at once, and build a small meter that records the highest number of overlapping blocks.

**Files:** [`starter.py`]({{ 'modules/32-asyncio-basics/assignments/a2-bounded-concurrency/starter.py' | relative_url }}), test file `test_a2_bounded_concurrency.py` in the same folder.

```python
{% include_relative assignments/a2-bounded-concurrency/starter.py %}
```

Run: `uv run pytest modules/32-asyncio-basics/assignments/a2-bounded-concurrency`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-bounded-concurrency/solution.py %}
```

Each item runs inside `async with semaphore`. The meter is an async context manager, so `__aexit__` runs even when the block raises, which keeps the counter correct.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Async retry with backoff

**Goal:** Retry a failing async call with a doubling delay. The sleep function is injected so tests do not wait.

**Files:** [`starter.py`]({{ 'modules/32-asyncio-basics/assignments/a3-async-retry/starter.py' | relative_url }}), test file `test_a3_async_retry.py` in the same folder.

```python
{% include_relative assignments/a3-async-retry/starter.py %}
```

Run: `uv run pytest modules/32-asyncio-basics/assignments/a3-async-retry`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-async-retry/solution.py %}
```

The loop re-raises on the last attempt and sleeps only between attempts. Taking `sleep` as a parameter lets a test pass a fake that records the delays.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: First result wins, and blocking code in a thread

**Goal:** Return the first finished result and cancel the rest. Also run blocking code with `asyncio.to_thread`.

**Files:** [`starter.py`]({{ 'modules/32-asyncio-basics/assignments/a4-first-and-threads/starter.py' | relative_url }}), test file `test_a4_first_and_threads.py` in the same folder.

```python
{% include_relative assignments/a4-first-and-threads/starter.py %}
```

Run: `uv run pytest modules/32-asyncio-basics/assignments/a4-first-and-threads`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-first-and-threads/solution.py %}
```

`asyncio.wait(..., return_when=FIRST_COMPLETED)` returns sets of finished and pending tasks. Cancel the pending ones, then `await asyncio.gather(*pending, return_exceptions=True)` so their cleanup finishes before you return. `to_thread` moves a blocking call to a worker thread.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="32-asyncio-basics:assignments"> I have finished the assignments</label></li>
</ul>
