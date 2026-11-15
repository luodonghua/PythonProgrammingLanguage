---
layout: module
module: 05-conditions-and-match
kind: assignments
title: Conditions and match - assignments
permalink: /modules/05-conditions-and-match/assignments/
---
Four tasks, from simple to a small project. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/05-conditions-and-match
```

---

<div class="assignment" markdown="1">

## Assignment 1: Describe the temperature

**Goal:** Practise `if` / `elif` / `else` and the order of conditions.

**Files:** [`starter.py`]({{ 'modules/05-conditions-and-match/assignments/a1-temperature/starter.py' | relative_url }}), test file `test_a1_temperature.py` in the same folder. The tests need no data files.

```python
{% include_relative assignments/a1-temperature/starter.py %}
```

Run: `uv run pytest modules/05-conditions-and-match/assignments/a1-temperature`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-temperature/solution.py %}
```

Because each `elif` only runs when the earlier tests failed, every branch can assume the earlier ranges are excluded. That is why `celsius < 20` is enough for "mild" after `celsius < 10` has failed.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: FizzBuzz

**Goal:** Practise `%`, ordering of checks, and building a list.

**Files:** [`starter.py`]({{ 'modules/05-conditions-and-match/assignments/a2-fizzbuzz/starter.py' | relative_url }}), test file `test_a2_fizzbuzz.py` in the same folder. The tests need no data files.

```python
{% include_relative assignments/a2-fizzbuzz/starter.py %}
```

Run: `uv run pytest modules/05-conditions-and-match/assignments/a2-fizzbuzz`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-fizzbuzz/solution.py %}
```

The "divisible by both" case must come first, otherwise a multiple of 15 would stop at `Fizz`. `n % 15 == 0` is the same as divisible by both 3 and 5.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Leap years and month lengths

**Goal:** Practise boolean logic, `match` with or-patterns, and raising `ValueError`.

**Files:** [`starter.py`]({{ 'modules/05-conditions-and-match/assignments/a3-leap-year/starter.py' | relative_url }}), test file `test_a3_leap_year.py` in the same folder. The tests need no data files.

```python
{% include_relative assignments/a3-leap-year/starter.py %}
```

Run: `uv run pytest modules/05-conditions-and-match/assignments/a3-leap-year`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-leap-year/solution.py %}
```

`case 1 | 3 | 5 | 7 | 8 | 10 | 12:` lists alternatives. The wildcard `case _:` runs for everything else, so a bad month raises `ValueError`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: A tiny command parser

**Goal:** Practise `match` with sequence patterns, a star pattern and a guard.

**Files:** [`starter.py`]({{ 'modules/05-conditions-and-match/assignments/a4-parse-command/starter.py' | relative_url }}), test file `test_a4_parse_command.py` in the same folder. The tests need no data files.

```python
{% include_relative assignments/a4-parse-command/starter.py %}
```

Run: `uv run pytest modules/05-conditions-and-match/assignments/a4-parse-command`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-parse-command/solution.py %}
```

`case ["go", direction] if direction in DIRECTIONS:` only matches when the guard is true, so `go up` falls through to `case _`. The star pattern `*rest` collects any extra words, so `take brass lamp` works with one or more words.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="05-conditions-and-match:assignments"> I have finished the assignments</label></li>
</ul>
