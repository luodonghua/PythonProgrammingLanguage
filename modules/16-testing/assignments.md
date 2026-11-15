---
layout: module
module: 16-testing
kind: assignments
title: Testing with pytest - assignments
permalink: /modules/16-testing/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Assignments 2 and 4 contain a file `implementations.py` with the functions the grader runs your test cases against. Leave it unchanged.

Run all tests for this topic:

```bash
uv run pytest modules/16-testing
```

---

<div class="assignment" markdown="1">

## Assignment 1: Make the tests pass

**Goal:** Read a test file that acts as the specification and write `parse_duration` so that every test passes. Practises reading tests, parsing text and raising `ValueError`.

**Files:** [`starter.py`]({{ 'modules/16-testing/assignments/a1-parse-duration/starter.py' | relative_url }}), test file `test_a1_parse_duration.py` in the same folder.

```python
{% include_relative assignments/a1-parse-duration/starter.py %}
```

Run: `uv run pytest modules/16-testing/assignments/a1-parse-duration`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-parse-duration/solution.py %}
```

The regular expression `(\d+)([dhms])` matches one part at a time. The code walks along the text, checks that units appear in order and only once, and raises `ValueError` as soon as a piece does not match. This is the test-first style: the tests came first.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Write the tests (leap years)

**Goal:** Instead of writing the function, write the test cases. Your cases must accept the correct leap-year function and catch six buggy ones.

**Files:** [`starter.py`]({{ 'modules/16-testing/assignments/a2-test-leap-year/starter.py' | relative_url }}), test file `test_a2_test_leap_year.py` in the same folder. The folder also contains `implementations.py` (the correct function and six buggy ones).

```python
{% include_relative assignments/a2-test-leap-year/starter.py %}
```

Run: `uv run pytest modules/16-testing/assignments/a2-test-leap-year`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-test-leap-year/solution.py %}
```

Each bug needs a specific year. 1900 exposes "divisible by 4 only", 2000 exposes "forgot the 400 rule", 1800 exposes "divisible by 200", and 1600 exposes "divisible by 1000". A good test suite is a set of inputs chosen to expose mistakes. The ordinary years 2024 and 2023 are not enough.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: To-do list in a JSON file

**Goal:** Implement a small JSON-backed to-do list. The tests show the pytest tools for this kind of code, `tmp_path`, `monkeypatch` and `capsys`.

**Files:** [`starter.py`]({{ 'modules/16-testing/assignments/a3-todo-file/starter.py' | relative_url }}), test file `test_a3_todo_file.py` in the same folder.

```python
{% include_relative assignments/a3-todo-file/starter.py %}
```

Run: `uv run pytest modules/16-testing/assignments/a3-todo-file`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-todo-file/solution.py %}
```

Every function takes the file path as a parameter, so tests can pass a path inside `tmp_path`. `prompt_add` calls `input()` directly, which lets `monkeypatch` replace it. Functions that raise leave the file unchanged because they check before they save.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Write the tests (clamp)

**Goal:** Write test cases for `clamp(x, low, high)`, including a case that expects an exception, so that six buggy versions are caught.

**Files:** [`starter.py`]({{ 'modules/16-testing/assignments/a4-test-clamp/starter.py' | relative_url }}), test file `test_a4_test_clamp.py` in the same folder. The folder also contains `implementations.py` (the correct function and six buggy ones).

```python
{% include_relative assignments/a4-test-clamp/starter.py %}
```

Run: `uv run pytest modules/16-testing/assignments/a4-test-clamp`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-test-clamp/solution.py %}
```

Boundary values catch the bugs: a value exactly on each edge, a float inside the range, `low == high`, and `low > high` with an expected `ValueError`. Cases that stay in the middle of the range pass for nearly every buggy version.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="16-testing:assignments"> I have finished the assignments</label></li>
</ul>
