---
layout: module
module: 11-errors-and-exceptions
kind: assignments
title: "Errors and exceptions - assignments"
permalink: /modules/11-errors-and-exceptions/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/11-errors-and-exceptions
```

---

<div class="assignment" markdown="1">

## Assignment 1: Safe conversions

**Goal:** Wrap risky operations such as `int()`, division and indexing so they return a default instead of crashing. Practises catching specific exceptions and not hiding the others.

**Files:** [`starter.py`]({{ 'modules/11-errors-and-exceptions/assignments/a1-safe-conversions/starter.py' | relative_url }}), test file `test_a1_safe_conversions.py` in the same folder.

```python
{% include_relative assignments/a1-safe-conversions/starter.py %}
```

Run: `uv run pytest modules/11-errors-and-exceptions/assignments/a1-safe-conversions`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-safe-conversions/solution.py %}
```

Each function catches exactly the exceptions its docstring names, for example `(ValueError, TypeError)` for `int(text)`. `safe_divide("a", 2)` still raises `TypeError`, because that is a bug and not an expected case. `error_name` is one of the rare places where `except Exception` fits, because it is a boundary that reports any failure.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Custom exceptions and validation

**Goal:** Define `ValidationError`, `ConfigError` and `InsufficientFunds`, raise them with clear messages and chain the original error with `raise ... from`. Practises `raise`, subclassing and exception attributes.

**Files:** [`starter.py`]({{ 'modules/11-errors-and-exceptions/assignments/a2-custom-errors/starter.py' | relative_url }}), test file `test_a2_custom_errors.py` in the same folder.

```python
{% include_relative assignments/a2-custom-errors/starter.py %}
```

Run: `uv run pytest modules/11-errors-and-exceptions/assignments/a2-custom-errors`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-custom-errors/solution.py %}
```

`ValidationError` subclasses `ValueError`, so callers can catch either one. `InsufficientFunds` stores `balance` and `amount` as attributes, so a handler can use the numbers and not parse a message. `raise ConfigError(...) from exc` keeps the original `ValueError` in `__cause__`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Collect errors and keep going

**Goal:** Parse messy `name,age` lines into records plus a list of numbered problems, read files with a fallback, sum mixed values and run tasks where some fail. Practises `try`/`except`/`else`, `continue` and error reports.

**Files:** [`starter.py`]({{ 'modules/11-errors-and-exceptions/assignments/a3-collect-errors/starter.py' | relative_url }}), test file `test_a3_collect_errors.py` in the same folder.

```python
{% include_relative assignments/a3-collect-errors/starter.py %}
```

Run: `uv run pytest modules/11-errors-and-exceptions/assignments/a3-collect-errors`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-collect-errors/solution.py %}
```

`parse_records` checks one rule at a time and uses `continue` after recording a problem, so one bad line never stops the others. `enumerate(lines, start=1)` gives line numbers that match what a person sees in an editor. `run_all` uses `else` for the success path, so only the task call itself sits in the `try` block.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Retry, cleanup and fallbacks

**Goal:** Write a `retry` helper, make sure cleanup always runs with `finally`, try several strategies in turn and parse without hiding unrelated errors. Practises re-raising and the `finally` block.

**Files:** [`starter.py`]({{ 'modules/11-errors-and-exceptions/assignments/a4-retry-and-cleanup/starter.py' | relative_url }}), test file `test_a4_retry_and_cleanup.py` in the same folder.

```python
{% include_relative assignments/a4-retry-and-cleanup/starter.py %}
```

Run: `uv run pytest modules/11-errors-and-exceptions/assignments/a4-retry-and-cleanup`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-retry-and-cleanup/solution.py %}
```

`retry` returns on success and re-raises with a bare `raise` on the last attempt, so the caller sees the real exception and its traceback. Exceptions not listed in `exceptions` pass straight through. `run_with_cleanup` uses `try`/`finally`: the cleanup runs on success and on error, and the error is not swallowed.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="11-errors-and-exceptions:assignments"> I have finished the assignments</label></li>
</ul>
