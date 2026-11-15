---
layout: module
module: 35-async-http-httpx
kind: assignments
title: "Async HTTP with httpx - assignments"
permalink: /modules/35-async-http-httpx/assignments/
---
Four tasks on a small, polite HTTP client: retries with backoff, bounded concurrency, a streamed response and rate limits. Every test uses `httpx.MockTransport`, so nothing touches the network and nothing really waits.

{% include practice-setup.md %}

This topic uses `httpx`, which is already listed in the project dependencies (`uv sync` installs it). Tests run async code. The project configures `pytest-asyncio` in auto mode, so you write plain `async def test_...` functions and need no decorator.

Run all tests for this topic:

```bash
uv run pytest modules/35-async-http-httpx
```

---

<div class="assignment" markdown="1">

## Assignment 1: Fetch JSON with retries

**Goal:** Write `fetch_json`, which retries transport errors and 5xx answers with exponential backoff, but raises at once on 4xx. Practises try/except, `raise_for_status` and dependency injection of `sleep`.

**Files:** [`starter.py`]({{ 'modules/35-async-http-httpx/assignments/a1-fetch-json-retry/starter.py' | relative_url }}), test file `test_a1_fetch_json_retry.py` in the same folder.

```python
{% include_relative assignments/a1-fetch-json-retry/starter.py %}
```

Run: `uv run pytest modules/35-async-http-httpx/assignments/a1-fetch-json-retry`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-fetch-json-retry/solution.py %}
```

The loop sleeps before every attempt except the first. The `HTTPStatusError` handler re-raises 4xx errors and records 5xx errors. After the last attempt the stored error is raised. The injected `sleep` makes the test instant.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Fetch many URLs with a limit

**Goal:** Fetch a list of URLs concurrently, keep the result order, return `None` for failures and never run more than `limit` requests at once. Practises `asyncio.gather` and `Semaphore`.

**Files:** [`starter.py`]({{ 'modules/35-async-http-httpx/assignments/a2-bounded-fetch-all/starter.py' | relative_url }}), test file `test_a2_bounded_fetch_all.py` in the same folder.

```python
{% include_relative assignments/a2-bounded-fetch-all/starter.py %}
```

Run: `uv run pytest modules/35-async-http-httpx/assignments/a2-bounded-fetch-all`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-bounded-fetch-all/solution.py %}
```

Each URL gets a small coroutine that holds the semaphore while it makes one request. `gather` returns results in input order. Catching errors inside the coroutine turns a failure into `None` and keeps the other requests alive.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Read a streamed response

**Goal:** Turn a `data:` line stream into an async generator of dicts, and then collect the text. Practises `client.stream`, `aiter_lines` and async generators.

**Files:** [`starter.py`]({{ 'modules/35-async-http-httpx/assignments/a3-stream-events/starter.py' | relative_url }}), test file `test_a3_stream_events.py` in the same folder.

```python
{% include_relative assignments/a3-stream-events/starter.py %}
```

Run: `uv run pytest modules/35-async-http-httpx/assignments/a3-stream-events`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-stream-events/solution.py %}
```

`async with client.stream(...)` keeps the connection open while the generator yields. Returning from the generator at `[DONE]` leaves the `async with` block and closes the connection. `collect_text` consumes the generator with `async for`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Obey 429 and Retry-After

**Goal:** Parse the `Retry-After` header safely and write a GET helper that waits and retries while the server answers 429. Practises header parsing, caps and defaults, and a bounded retry loop.

**Files:** [`starter.py`]({{ 'modules/35-async-http-httpx/assignments/a4-rate-limit/starter.py' | relative_url }}), test file `test_a4_rate_limit.py` in the same folder.

```python
{% include_relative assignments/a4-rate-limit/starter.py %}
```

Run: `uv run pytest modules/35-async-http-httpx/assignments/a4-rate-limit`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-rate-limit/solution.py %}
```

`retry_after_seconds` converts with `float`, falls back to a default for bad values and caps the result. The loop sleeps only when another attempt remains, and raises `RateLimitError` after the last 429.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="35-async-http-httpx:assignments"> I have finished the assignments</label></li>
</ul>
