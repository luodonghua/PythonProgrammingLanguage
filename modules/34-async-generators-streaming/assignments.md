---
layout: module
module: 34-async-generators-streaming
kind: assignments
title: "Async generators and streaming - assignments"
permalink: /modules/34-async-generators-streaming/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

The tests are `async def` functions and run with pytest-asyncio in auto mode. They never wait for real time: sources use `asyncio.sleep(0)` and the tests inject a fake `sleep` where a delay is needed.

Assignments 3 and 4 start background tasks. If a solution forgets to cancel them, a test can wait forever, so those test files stop a test after 5 seconds and report it as failed.

Run all tests for this topic:

```bash
uv run pytest modules/34-async-generators-streaming
```

---

<div class="assignment" markdown="1">

## Assignment 1: Ticker, chunks and a session

**Goal:** Write your first async generators (a timer and a text chunker), read a stream into a list, stop early without leaking the source, and build an async context manager.

**Files:** [`starter.py`]({{ 'modules/34-async-generators-streaming/assignments/a1-ticker-and-chunks/starter.py' | relative_url }}), test file `test_a1_ticker_and_chunks.py` in the same folder.

```python
{% include_relative assignments/a1-ticker-and-chunks/starter.py %}
```

Run: `uv run pytest modules/34-async-generators-streaming/assignments/a1-ticker-and-chunks`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-ticker-and-chunks/solution.py %}
```

The generators are loops with `yield`. `take` closes the stream in `finally`, so the source's own cleanup runs at once. `@asynccontextmanager` turns a generator with one `yield` into an `async with` block, and `finally` makes "close" happen on errors too.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Aggregate a stream

**Goal:** Compute running totals and a summary while items arrive, and rebuild complete lines from chunks that split text anywhere.

**Files:** [`starter.py`]({{ 'modules/34-async-generators-streaming/assignments/a2-aggregate-stream/starter.py' | relative_url }}), test file `test_a2_aggregate_stream.py` in the same folder.

```python
{% include_relative assignments/a2-aggregate-stream/starter.py %}
```

Run: `uv run pytest modules/34-async-generators-streaming/assignments/a2-aggregate-stream`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-aggregate-stream/solution.py %}
```

Each function keeps only a small state (a total, or a text buffer) and handles one item at a time. `lines_from_chunks` splits the buffer with `split("\n", 1)` as long as it contains a newline, then yields what is left at the end.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Buffer a stream with a bounded queue

**Goal:** Read a source ahead of the consumer with a producer task and a bounded `asyncio.Queue`, so a slow consumer slows the producer (backpressure).

**Files:** [`starter.py`]({{ 'modules/34-async-generators-streaming/assignments/a3-buffered-stream/starter.py' | relative_url }}), test file `test_a3_buffered_stream.py` in the same folder.

```python
{% include_relative assignments/a3-buffered-stream/starter.py %}
```

Run: `uv run pytest modules/34-async-generators-streaming/assignments/a3-buffered-stream`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-buffered-stream/solution.py %}
```

The producer puts a `DONE` marker at the end, and the consumer stops when it sees it. `buffered` cancels and awaits the producer in `finally`, so nothing is left running when the reader stops early. `aclosing` makes the source stream close when the producer is cancelled.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Merge streams and limit each wait

**Goal:** Merge several async streams in arrival order, and add a time limit to the wait for each item.

**Files:** [`starter.py`]({{ 'modules/34-async-generators-streaming/assignments/a4-merge-and-timeout/starter.py' | relative_url }}), test file `test_a4_merge_and_timeout.py` in the same folder.

```python
{% include_relative assignments/a4-merge-and-timeout/starter.py %}
```

Run: `uv run pytest modules/34-async-generators-streaming/assignments/a4-merge-and-timeout`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-merge-and-timeout/solution.py %}
```

One pump task per stream feeds a shared queue, and the generator counts "done" messages. Errors travel through the queue as messages and are raised in the reader. `with_item_timeout` wraps each `anext` in `asyncio.timeout`, so the limit applies to one item, not to the whole stream.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="34-async-generators-streaming:assignments"> I have finished the assignments</label></li>
</ul>
