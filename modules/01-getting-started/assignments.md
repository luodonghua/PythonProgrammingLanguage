---
layout: module
module: 01-getting-started
kind: assignments
title: Getting started - assignments
permalink: /modules/01-getting-started/assignments/
---
Three short tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/01-getting-started
```

---

<div class="assignment" markdown="1">

## Assignment 1: Hello, you

**Goal:** write a function that builds a greeting and returns it. Practise `def`, `return`, `strip()` and f-strings.

**Files:** [`starter.py`]({{ 'modules/01-getting-started/assignments/a1-hello/starter.py' | relative_url }}), test file `test_a1_hello.py` in the same folder.

```python
{% include_relative assignments/a1-hello/starter.py %}
```

Run: `uv run pytest modules/01-getting-started/assignments/a1-hello`

Also run the script itself: `uv run modules/01-getting-started/assignments/a1-hello/starter.py`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-hello/solution.py %}
```

`strip()` removes spaces at both ends. An empty string is falsy, so `if not name` catches both `""` and `"   "`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Check your Python version

**Goal:** report which Python you are running and decide whether it is new enough. Practise `sys.version_info` and tuple comparison.

**Files:** [`starter.py`]({{ 'modules/01-getting-started/assignments/a2-version-check/starter.py' | relative_url }}), test file `test_a2_version_check.py`.

```python
{% include_relative assignments/a2-version-check/starter.py %}
```

Run: `uv run pytest modules/01-getting-started/assignments/a2-version-check`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-version-check/solution.py %}
```

Tuples compare from the first element, so `(3, 15) >= (3, 14)` is `True` and `(3, 9) >= (3, 14)` is `False`. Slicing with `[:2]` keeps just major and minor.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Terminal commands in Python

**Goal:** do what `pwd` and `ls *.py` do, using `pathlib`. Practise `Path`, `iterdir()` and `sorted()`.

**Files:** [`starter.py`]({{ 'modules/01-getting-started/assignments/a3-terminal/starter.py' | relative_url }}), test file `test_a3_terminal.py`. The tests build their own temporary folders, so you need no data files.

```python
{% include_relative assignments/a3-terminal/starter.py %}
```

Run: `uv run pytest modules/01-getting-started/assignments/a3-terminal`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-terminal/solution.py %}
```

`is_file()` rejects folders, including a folder named `weird.py`. `iterdir()` is not recursive, so files in sub-folders are skipped.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="01-getting-started:assignments"> I have finished the assignments</label></li>
</ul>
