---
layout: module
module: 17-debugging
kind: assignments
title: Debugging - assignments
permalink: /modules/17-debugging/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/17-debugging
```

---

<div class="assignment" markdown="1">

## Assignment 1: Fix five bugs

**Goal:** Five short functions each hide one classic bug. Read the failing tests, find the cause and fix it. Practises the bug families (mutable default, off-by-one, integer division, shared rows, shadowed built-in).

**Files:** [`starter.py`]({{ 'modules/17-debugging/assignments/a1-fix-the-bugs/starter.py' | relative_url }}), test file `test_a1_fix_the_bugs.py` in the same folder.

```python
{% include_relative assignments/a1-fix-the-bugs/starter.py %}
```

Run: `uv run pytest modules/17-debugging/assignments/a1-fix-the-bugs`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-fix-the-bugs/solution.py %}
```

The fixes are small: `cart=None` and create the list inside, `range(1, n + 1)`, `/` instead of `//`, a list comprehension that builds a new row each time, and a variable name that does not hide `max`. Also use `>` instead of `>=` so ties keep the first word.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Logging instead of print

**Goal:** Configure a logger that writes to a stream, then make a function report what it does through the `logging` module. The tests read the log records with `caplog`.

**Files:** [`starter.py`]({{ 'modules/17-debugging/assignments/a2-logging/starter.py' | relative_url }}), test file `test_a2_logging.py` in the same folder.

```python
{% include_relative assignments/a2-logging/starter.py %}
```

Run: `uv run pytest modules/17-debugging/assignments/a2-logging`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-logging/solution.py %}
```

`configure_logger` removes old handlers before adding one, so calling it twice does not print every message twice. `process_orders` passes values as arguments (`"skipping order %s: bad quantity %s", order_id, qty`), which keeps the message template separate from the data. `logger.exception` inside `except` records the traceback at `ERROR` level.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Facts from a traceback

**Goal:** Use the `traceback` module to find the function, line number and source text where an exception was raised, and to build a small error report.

**Files:** [`starter.py`]({{ 'modules/17-debugging/assignments/a3-traceback-info/starter.py' | relative_url }}), test file `test_a3_traceback_info.py` in the same folder.

```python
{% include_relative assignments/a3-traceback-info/starter.py %}
```

Run: `uv run pytest modules/17-debugging/assignments/a3-traceback-info`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-traceback-info/solution.py %}
```

`traceback.extract_tb(exc.__traceback__)` returns frames, oldest call first. The last frame is where the error was raised, and the length of the list is the depth. Catching `Exception` (not `BaseException`) lets Ctrl+C still stop the program.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Bisect to the first bad version

**Goal:** Write a binary search that finds the first bad version of a project with very few checks, and count the checks. This is the idea behind `git bisect`.

**Files:** [`starter.py`]({{ 'modules/17-debugging/assignments/a4-bisect/starter.py' | relative_url }}), test file `test_a4_bisect.py` in the same folder.

```python
{% include_relative assignments/a4-bisect/starter.py %}
```

Run: `uv run pytest modules/17-debugging/assignments/a4-bisect`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-bisect/solution.py %}
```

Keep a range `low..high` that must contain the answer. Test the middle. If it is bad, the answer is at or before it (`high = middle`). If it is good, the answer is after it (`low = middle + 1`). Each check halves the range, so 1000 versions need about 10 checks.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="17-debugging:assignments"> I have finished the assignments</label></li>
</ul>
