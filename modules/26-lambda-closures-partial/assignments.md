---
layout: module
module: 26-lambda-closures-partial
kind: assignments
title: "Lambda, closures and partial - assignments"
permalink: /modules/26-lambda-closures-partial/assignments/
---
Four tasks on small functions: sorting with `key=`, closures with `nonlocal`, `functools.partial`, and function tables with pipelines. Each one is a few lines of code, but the ideas are used everywhere in Python programs.

{% include practice-setup.md %}

No extra libraries are needed. You use `functools` and `operator` from the standard library.

Run all tests for this topic:

```bash
uv run pytest modules/26-lambda-closures-partial
```

---

<div class="assignment" markdown="1">

## Assignment 1: Sorting with key functions

**Goal:** Rank students by score and name, pick the longest words, sort dictionaries by several fields, and find the cheapest and most expensive item. Practises lambdas, tuple keys, `itemgetter` and `min`/`max` with `key=`.

**Files:** [`starter.py`]({{ 'modules/26-lambda-closures-partial/assignments/a1-sorting/starter.py' | relative_url }}), test file `test_a1_sorting.py` in the same folder.

```python
{% include_relative assignments/a1-sorting/starter.py %}
```

Run: `uv run pytest modules/26-lambda-closures-partial/assignments/a1-sorting`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-sorting/solution.py %}
```

A tuple key sorts by several values, and a minus sign on a number reverses that part (`-s["score"]`). `itemgetter(*fields)` builds the same kind of tuple key without a lambda. `key=prices.get` passes each dictionary key to `get`, so `min` compares the prices.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Closures and late binding

**Goal:** Write a counter, a call limiter and a history recorder as closures, and fix a list of lambdas that all see the last loop value. Practises `nonlocal` and the late-binding fix.

**Files:** [`starter.py`]({{ 'modules/26-lambda-closures-partial/assignments/a2-closures/starter.py' | relative_url }}), test file `test_a2_closures.py` in the same folder.

```python
{% include_relative assignments/a2-closures/starter.py %}
```

Run: `uv run pytest modules/26-lambda-closures-partial/assignments/a2-closures`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-closures/solution.py %}
```

`counter` and `allow` rebind a variable, so they declare `nonlocal`. `record` only calls `.append`, which changes the list without rebinding the name, so it needs no `nonlocal`. The fix `lambda x, i=i: x + i` evaluates `i` when each lambda is created.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Pre-filled functions with partial

**Goal:** Build loggers and number parsers with `functools.partial`, write your own `my_partial`, and make discount functions with keyword-only options. Practises `partial`, keyword arguments and closures.

**Files:** [`starter.py`]({{ 'modules/26-lambda-closures-partial/assignments/a3-partial/starter.py' | relative_url }}), test file `test_a3_partial.py` in the same folder.

```python
{% include_relative assignments/a3-partial/starter.py %}
```

Run: `uv run pytest modules/26-lambda-closures-partial/assignments/a3-partial`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-partial/solution.py %}
```

`partial(log, sink, "INFO", prefix)` fills the first three parameters, so the result takes only `message`. `my_partial` is a closure over the fixed arguments. Merging the dictionaries with `{**fixed_kwargs, **kwargs}` lets later keywords override earlier ones, as in the real `partial`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Pipelines, function tables and callbacks

**Goal:** Write `pipeline`, a calculator driven by a table of `operator` functions, a small event bus of callbacks, and a helper that applies many functions safely. Practises functions as values and closures that share state.

**Files:** [`starter.py`]({{ 'modules/26-lambda-closures-partial/assignments/a4-pipelines/starter.py' | relative_url }}), test file `test_a4_pipelines.py` in the same folder.

```python
{% include_relative assignments/a4-pipelines/starter.py %}
```

Run: `uv run pytest modules/26-lambda-closures-partial/assignments/a4-pipelines`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-pipelines/solution.py %}
```

`calculate` has no `if`/`elif` chain: the table maps each symbol to a function, and an unknown symbol is rejected before the lookup. `make_event_bus` returns two closures that share one dictionary of callback lists. `setdefault` creates the list on first use.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="26-lambda-closures-partial:assignments"> I have finished the assignments</label></li>
</ul>
