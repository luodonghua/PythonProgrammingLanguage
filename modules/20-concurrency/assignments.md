---
layout: module
module: 20-concurrency
kind: assignments
title: "Concurrency: threads and processes - assignments"
permalink: /modules/20-concurrency/assignments/
---
Five tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

These tests start threads and processes, but none of them measures time. They use events, barriers and queues, so they give the same result on a fast or a slow computer. The process pool tests start a few worker processes and take about a second.

Run all tests for this topic:

```bash
uv run pytest modules/20-concurrency
```

---

<div class="assignment" markdown="1">

## Assignment 1: Parallel map that keeps order

**Goal:** Write `parallel_map(func, items, workers)` with a thread pool. Results must come back in input order even when jobs finish in a different order. Practises `ThreadPoolExecutor.map` and exception propagation.

**Files:** [`starter.py`]({{ 'modules/20-concurrency/assignments/a1-parallel-map/starter.py' | relative_url }}), test file `test_a1_parallel_map.py` in the same folder.

```python
{% include_relative assignments/a1-parallel-map/starter.py %}
```

Run: `uv run pytest modules/20-concurrency/assignments/a1-parallel-map`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-parallel-map/solution.py %}
```

`Executor.map` already returns results in input order, and it re-raises a job's exception when you read that result. The `with` block waits for all workers before it exits.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Thread-safe counter

**Goal:** Build a `SafeCounter` class that many threads can increment without losing updates, and a helper that runs a task in several threads. Practises `threading.Thread`, `join` and `Lock`.

**Files:** [`starter.py`]({{ 'modules/20-concurrency/assignments/a2-safe-counter/starter.py' | relative_url }}), test file `test_a2_safe_counter.py` in the same folder.

```python
{% include_relative assignments/a2-safe-counter/starter.py %}
```

Run: `uv run pytest modules/20-concurrency/assignments/a2-safe-counter`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-safe-counter/solution.py %}
```

`self._count += n` is a read, an add and a write, so two threads can overwrite each other. Every access goes through `with self._lock:`. The `value` property also takes the lock so it never reads in the middle of an update.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Producer and consumers with a Queue

**Goal:** Feed items through a `queue.Queue` to several consumer threads and collect the results in input order. Practises `Queue`, sentinel values to stop workers, and storing errors as results.

**Files:** [`starter.py`]({{ 'modules/20-concurrency/assignments/a3-producer-consumer/starter.py' | relative_url }}), test file `test_a3_producer_consumer.py` in the same folder.

```python
{% include_relative assignments/a3-producer-consumer/starter.py %}
```

Run: `uv run pytest modules/20-concurrency/assignments/a3-producer-consumer`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-producer-consumer/solution.py %}
```

Each queue entry carries its index, so a consumer can write `results[index]` without a lock (each index is written once). One `None` per consumer ends the loops. Joining the threads guarantees every result is in place before the function returns.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Process pool for CPU-bound work

**Goal:** Split a list into chunks and sum the chunks in separate processes, then check that the work ran in other processes. Practises `ProcessPoolExecutor` and picklable functions.

**Files:** [`starter.py`]({{ 'modules/20-concurrency/assignments/a4-process-pool/starter.py' | relative_url }}), test file `test_a4_process_pool.py` in the same folder.

```python
{% include_relative assignments/a4-process-pool/starter.py %}
```

Run: `uv run pytest modules/20-concurrency/assignments/a4-process-pool`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-process-pool/solution.py %}
```

The built-in `sum` can be pickled, so it can be sent to the workers. `split_chunks` uses `divmod` to share the remainder between the first chunks. The partial sums come back to the parent, which adds them.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 5: A first asyncio.gather

**Goal:** Run several coroutines together with `asyncio.gather`, keep the result order, and turn failures into results with `return_exceptions=True`. These are `async def` tests.

**Files:** [`starter.py`]({{ 'modules/20-concurrency/assignments/a5-gather-intro/starter.py' | relative_url }}), test file `test_a5_gather_intro.py` in the same folder.

```python
{% include_relative assignments/a5-gather-intro/starter.py %}
```

Run: `uv run pytest modules/20-concurrency/assignments/a5-gather-intro`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a5-gather-intro/solution.py %}
```

`gather(*coroutines)` returns results in the order you passed them. With `return_exceptions=True` an error does not cancel the other jobs. It appears in the result list as an exception object, which `isinstance` can detect.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="20-concurrency:assignments"> I have finished the assignments</label></li>
</ul>
