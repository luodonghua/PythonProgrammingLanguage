---
layout: module
module: 33-taskgroup-timeouts-cancellation
kind: assignments
title: TaskGroup, timeouts and cancellation - assignments
permalink: /modules/33-taskgroup-timeouts-cancellation/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

The tests are `async def` functions and run with pytest-asyncio in auto mode. They use `asyncio.sleep(0)` and events instead of real waiting. A few tests give a short timeout (0.01 s) to a job that can never finish, so the result does not depend on how fast your machine is.

Run all tests for this topic:

```bash
uv run pytest modules/33-taskgroup-timeouts-cancellation
```

---

<div class="assignment" markdown="1">

## Assignment 1: Fan out with a TaskGroup

**Goal:** Fetch many names at once with a TaskGroup and let failures reach the caller as an ExceptionGroup. Then write a version that keeps the successes and reports each failure.

**Files:** [`starter.py`]({{ 'modules/33-taskgroup-timeouts-cancellation/assignments/a1-fan-out/starter.py' | relative_url }}), test file `test_a1_fan_out.py` in the same folder.

```python
{% include_relative assignments/a1-fan-out/starter.py %}
```

Run: `uv run pytest modules/33-taskgroup-timeouts-cancellation/assignments/a1-fan-out`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-fan-out/solution.py %}
```

`TaskGroup` waits for every task and cancels the rest on the first failure. The partial version catches errors inside a small wrapper, so the group never sees them and all tasks run to the end.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Handle several errors with except*

**Goal:** Flatten nested exception groups, and sort the errors of a failed job by type with `except*`.

**Files:** [`starter.py`]({{ 'modules/33-taskgroup-timeouts-cancellation/assignments/a2-except-star/starter.py' | relative_url }}), test file `test_a2_except_star.py` in the same folder.

```python
{% include_relative assignments/a2-except-star/starter.py %}
```

Run: `uv run pytest modules/33-taskgroup-timeouts-cancellation/assignments/a2-except-star`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-except-star/solution.py %}
```

`except* ValueError` gives you an `ExceptionGroup` with only the matching members. You cannot `return` inside the block, so the solution stores the messages in variables and returns after the `try`. Unmatched types still propagate.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Timeouts and cancel

**Goal:** Return a default when a job is too slow, give each job its own limit, cancel a task safely, and write a job that always cleans up.

**Files:** [`starter.py`]({{ 'modules/33-taskgroup-timeouts-cancellation/assignments/a3-timeouts/starter.py' | relative_url }}), test file `test_a3_timeouts.py` in the same folder.

```python
{% include_relative assignments/a3-timeouts/starter.py %}
```

Run: `uv run pytest modules/33-taskgroup-timeouts-cancellation/assignments/a3-timeouts`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-timeouts/solution.py %}
```

`asyncio.timeout` cancels the job and raises `TimeoutError` at the end of the block. `finally` runs on success, error and cancellation, so "close" is always logged.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: A worker pool with a Queue

**Goal:** Process items with a fixed number of workers fed by an `asyncio.Queue`, and keep results in input order.

**Files:** [`starter.py`]({{ 'modules/33-taskgroup-timeouts-cancellation/assignments/a4-worker-pool/starter.py' | relative_url }}), test file `test_a4_worker_pool.py` in the same folder.

```python
{% include_relative assignments/a4-worker-pool/starter.py %}
```

Run: `uv run pytest modules/33-taskgroup-timeouts-cancellation/assignments/a4-worker-pool`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-worker-pool/solution.py %}
```

Workers loop forever on `queue.get()`. `queue.join()` returns when every item has called `task_done()`. Then the workers are cancelled so the TaskGroup can end. The number of workers is the concurrency limit.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="33-taskgroup-timeouts-cancellation:assignments"> I have finished the assignments</label></li>
</ul>
