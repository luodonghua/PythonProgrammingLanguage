---
layout: module
module: 27-decorators-functools
kind: assignments
title: "Decorators and functools - assignments"
permalink: /modules/27-decorators-functools/assignments/
---
Five tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/27-decorators-functools
```

---

<div class="assignment" markdown="1">

## Assignment 1: Count and log calls

**Goal:** Write two decorators, one that counts calls and one (with an argument) that logs each call and its result. Practises wrappers, `functools.wraps` and decorator factories.

**Files:** [`starter.py`]({{ 'modules/27-decorators-functools/assignments/a1-log-calls/starter.py' | relative_url }}), test file `test_a1_log_calls.py` in the same folder.

```python
{% include_relative assignments/a1-log-calls/starter.py %}
```

Run: `uv run pytest modules/27-decorators-functools/assignments/a1-log-calls`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-log-calls/solution.py %}
```

`count_calls` stores the counter on the wrapper function itself. `log_calls(log)` is a function that returns the decorator, so it has three nested `def`s. The `except ... raise` pair logs the failure and lets the error continue.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Command registry

**Goal:** Build an `@command` decorator that registers functions by name, with or without an argument, and a `run(line)` function that dispatches a text command. Practises registry decorators.

**Files:** [`starter.py`]({{ 'modules/27-decorators-functools/assignments/a2-command-registry/starter.py' | relative_url }}), test file `test_a2_command_registry.py` in the same folder.

```python
{% include_relative assignments/a2-command-registry/starter.py %}
```

Run: `uv run pytest modules/27-decorators-functools/assignments/a2-command-registry`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-command-registry/solution.py %}
```

`command` checks `callable(arg)`. If it got the function directly (`@command`), it registers it. Otherwise `arg` is the name and a decorator is returned. Both forms return the original function, so it stays callable.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Retry with backoff

**Goal:** Write `retry(times, exceptions, delay, backoff, sleep)`. The `sleep` function is injected, so the tests never wait. Practises decorators with arguments and exception handling.

**Files:** [`starter.py`]({{ 'modules/27-decorators-functools/assignments/a3-retry/starter.py' | relative_url }}), test file `test_a3_retry.py` in the same folder.

```python
{% include_relative assignments/a3-retry/starter.py %}
```

Run: `uv run pytest modules/27-decorators-functools/assignments/a3-retry`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-retry/solution.py %}
```

The loop tries up to `times` times. `except exceptions:` catches only the listed types, so other errors propagate at once. The last attempt re-raises instead of sleeping. The wait grows by `backoff` after each failure.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Cache with expiry

**Goal:** Write a cache decorator whose entries expire after a number of seconds, using an injected clock. Practises closures, state in a decorator and fake clocks.

**Files:** [`starter.py`]({{ 'modules/27-decorators-functools/assignments/a4-ttl-cache/starter.py' | relative_url }}), test file `test_a4_ttl_cache.py` in the same folder.

```python
{% include_relative assignments/a4-ttl-cache/starter.py %}
```

Run: `uv run pytest modules/27-decorators-functools/assignments/a4-ttl-cache`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-ttl-cache/solution.py %}
```

A dict maps the argument key to `(stored_at, result)`. Reading the clock once per call keeps the logic simple, and `now - stored_at < seconds` decides if the entry is fresh. Counters and `cache_clear` are attributes on the wrapper.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 5: singledispatch and total_ordering

**Goal:** Use `functools.singledispatch` to describe values by type, and `functools.total_ordering` to compare version numbers. Practises two more `functools` tools.

**Files:** [`starter.py`]({{ 'modules/27-decorators-functools/assignments/a5-dispatch-ordering/starter.py' | relative_url }}), test file `test_a5_dispatch_ordering.py` in the same folder.

```python
{% include_relative assignments/a5-dispatch-ordering/starter.py %}
```

Run: `uv run pytest modules/27-decorators-functools/assignments/a5-dispatch-ordering`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a5-dispatch-ordering/solution.py %}
```

Each `@describe.register` function is chosen by the type annotation of its first parameter. `Version` defines only `__eq__` and `__lt__`. `total_ordering` derives the rest. Comparing numbers as tuples makes `1.10` larger than `1.9`.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="27-decorators-functools:assignments"> I have finished the assignments</label></li>
</ul>
