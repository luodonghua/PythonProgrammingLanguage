---
layout: module
module: 37-testing-async-fakes
kind: assignments
title: "Testing async code with fakes - assignments"
permalink: /modules/37-testing-async-fakes/assignments/
---
Four tasks about building the tools that make async tests fast and exact: a fake clock, a scripted fake client, a retrying class that takes its dependencies as arguments, and an async worker with a timeout helper. Some tests use `AsyncMock`, so you also see how a library mock is used.

{% include practice-setup.md %}

No extra libraries are needed beyond `pytest` and `pytest-asyncio`, which the project already lists. The tests are `async def` functions. The project runs `pytest-asyncio` in auto mode, so they need no decorator. Nothing here waits for real, except one 0.01-second timeout in assignment 4.

Run all tests for this topic:

```bash
uv run pytest modules/37-testing-async-fakes
```

---

<div class="assignment" markdown="1">

## Assignment 1: A fake clock

**Goal:** Write `FakeClock` with `now`, `advance` and an async `sleep` that records the delay and moves time forward without waiting. Then use it in a `ticker` function.

**Files:** [`starter.py`]({{ 'modules/37-testing-async-fakes/assignments/a1-fake-clock/starter.py' | relative_url }}), test file `test_a1_fake_clock.py` in the same folder.

```python
{% include_relative assignments/a1-fake-clock/starter.py %}
```

Run: `uv run pytest modules/37-testing-async-fakes/assignments/a1-fake-clock`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-fake-clock/solution.py %}
```

`sleep` appends to a list and advances the stored time, so a test can sleep for an hour in microseconds and check `clock.sleeps`. The `await asyncio.sleep(0)` at the end hands control to other tasks, as a real sleep would.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: A scripted fake client

**Goal:** Write `FakeClient`, which returns or raises the items of a script in order, records each call and complains when the code makes more calls than the script allows. Practises writing a fake and a spy.

**Files:** [`starter.py`]({{ 'modules/37-testing-async-fakes/assignments/a2-fake-client/starter.py' | relative_url }}), test file `test_a2_fake_client.py` in the same folder.

```python
{% include_relative assignments/a2-fake-client/starter.py %}
```

Run: `uv run pytest modules/37-testing-async-fakes/assignments/a2-fake-client`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-fake-client/solution.py %}
```

Exceptions in the script are raised, other items are returned. Recording the call first means failed calls are counted too. Raising `AssertionError` on an empty script turns an unplanned extra call into a clear test failure.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: A retrying fetcher

**Goal:** Write `RetryingFetcher`, which retries temporary errors with exponential backoff. The client and `sleep` are injected. The tests use `AsyncMock` and a recording `sleep`.

**Files:** [`starter.py`]({{ 'modules/37-testing-async-fakes/assignments/a3-retrying-fetcher/starter.py' | relative_url }}), test file `test_a3_retrying_fetcher.py` in the same folder.

```python
{% include_relative assignments/a3-retrying-fetcher/starter.py %}
```

Run: `uv run pytest modules/37-testing-async-fakes/assignments/a3-retrying-fetcher`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-retrying-fetcher/solution.py %}
```

`except self.retry_on` accepts a tuple of exception types. On the last attempt the exception is re-raised before any sleep. Because `sleep` and the client are constructor arguments, the tests never wait and never touch the network.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Queue worker and timeout helper

**Goal:** Write `run_worker`, which processes queue items until a stop marker and keeps going after errors, and `call_with_timeout`, which cancels a call that takes too long and returns a default.

**Files:** [`starter.py`]({{ 'modules/37-testing-async-fakes/assignments/a4-worker-and-timeout/starter.py' | relative_url }}), test file `test_a4_worker_and_timeout.py` in the same folder.

```python
{% include_relative assignments/a4-worker-and-timeout/starter.py %}
```

Run: `uv run pytest modules/37-testing-async-fakes/assignments/a4-worker-and-timeout`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-worker-and-timeout/solution.py %}
```

The `finally` block calls `task_done()` exactly once per item, so `queue.join()` always finishes. `asyncio.timeout` cancels the inner call, so its own `finally` runs, and the `TimeoutError` is caught outside the `async with` block.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="37-testing-async-fakes:assignments"> I have finished the assignments</label></li>
</ul>
