---
layout: module
module: 28-iterators-generators
kind: assignments
title: Iterators and generators - assignments
permalink: /modules/28-iterators-generators/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Assignment 3 uses a small data file, `app.log`, in its folder. The test reads it for you.

Run all tests for this topic:

```bash
uv run pytest modules/28-iterators-generators
```

---

<div class="assignment" markdown="1">

## Assignment 1: First generators

**Goal:** Write an endless Fibonacci generator, a `take` helper and a lazy `chunker`. Practises `yield`, laziness and `itertools.islice`.

**Files:** [`starter.py`]({{ 'modules/28-iterators-generators/assignments/a1-generators/starter.py' | relative_url }}), test file `test_a1_generators.py` in the same folder.

```python
{% include_relative assignments/a1-generators/starter.py %}
```

Run: `uv run pytest modules/28-iterators-generators/assignments/a1-generators`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-generators/solution.py %}
```

`fibonacci` keeps two numbers in a loop that never ends. `take` uses `islice`, which stops reading after `n` items. `chunker` pulls `size` items at a time from one shared iterator, and stops when a slice comes back empty.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Iterator classes

**Goal:** Write an iterator class (`Countdown`) and an iterable class (`Playlist`) by hand. Practises `__iter__`, `__next__` and the difference between iterable and iterator.

**Files:** [`starter.py`]({{ 'modules/28-iterators-generators/assignments/a2-iterator-classes/starter.py' | relative_url }}), test file `test_a2_iterator_classes.py` in the same folder.

```python
{% include_relative assignments/a2-iterator-classes/starter.py %}
```

Run: `uv run pytest modules/28-iterators-generators/assignments/a2-iterator-classes`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-iterator-classes/solution.py %}
```

An iterator returns itself from `__iter__` and keeps its position, so it can be used once. An iterable returns a **fresh** iterator from `__iter__`, so it can be looped many times. `repeat` is a generator method that uses `yield from`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Lazy log pipeline

**Goal:** Build a pipeline of generators that reads a log file line by line, parses records, filters by level and counts them. Practises chaining generators and streaming a file.

**Files:** [`starter.py`]({{ 'modules/28-iterators-generators/assignments/a3-log-pipeline/starter.py' | relative_url }}), test file `test_a3_log_pipeline.py` in the same folder. The log file `app.log` is in the same folder.

```python
{% include_relative assignments/a3-log-pipeline/starter.py %}
```

Run: `uv run pytest modules/28-iterators-generators/assignments/a3-log-pipeline`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-log-pipeline/solution.py %}
```

Each stage is a small generator that reads from the previous one. `read_lines` uses `with open(...)` inside a generator, so the file closes when the loop ends. `split(maxsplit=3)` keeps the message together.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Stream tools

**Goal:** Write a `send`-driven running average, a moving average, a duplicate remover and a sorted merge, all lazy. Practises `send`, `deque`, and `heapq.merge`.

**Files:** [`starter.py`]({{ 'modules/28-iterators-generators/assignments/a4-streams/starter.py' | relative_url }}), test file `test_a4_streams.py` in the same folder.

```python
{% include_relative assignments/a4-streams/starter.py %}
```

Run: `uv run pytest modules/28-iterators-generators/assignments/a4-streams`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-streams/solution.py %}
```

`running_average` receives numbers with `yield` as an expression. `moving_average` uses `deque(maxlen=window)`, which drops the oldest value by itself. `merge_sorted` delegates to `heapq.merge`, which only needs the front item of each stream.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="28-iterators-generators:assignments"> I have finished the assignments</label></li>
</ul>
