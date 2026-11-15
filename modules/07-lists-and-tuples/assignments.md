---
layout: module
module: 07-lists-and-tuples
kind: assignments
title: "Lists and tuples - assignments"
permalink: /modules/07-lists-and-tuples/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/07-lists-and-tuples
```

---

<div class="assignment" markdown="1">

## Assignment 1: Four list utilities

**Goal:** Write `rotate`, `flatten`, `dedupe` and `running_totals`, all without changing the input list. Practises slicing, `extend` and `append`, membership with `in` and accumulators.

**Files:** [`starter.py`]({{ 'modules/07-lists-and-tuples/assignments/a1-list-tools/starter.py' | relative_url }}), test file `test_a1_list_tools.py` in the same folder.

```python
{% include_relative assignments/a1-list-tools/starter.py %}
```

Run: `uv run pytest modules/07-lists-and-tuples/assignments/a1-list-tools`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-list-tools/solution.py %}
```

`rotate` reduces `k` with `%` and joins two slices, which always make new lists. `flatten` uses `extend` for list items and `append` for the rest. `dedupe` checks `item not in result`, which keeps the first occurrence and the order. This is simple but slow for long lists. The next topic shows a faster way with sets.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Leaderboard

**Goal:** Sort `(name, score)` tuples, pick the best and worst, and give tied players the same rank. Practises `sorted` with `key=`, slicing, tuple unpacking and `enumerate`.

**Files:** [`starter.py`]({{ 'modules/07-lists-and-tuples/assignments/a2-leaderboard/starter.py' | relative_url }}), test file `test_a2_leaderboard.py` in the same folder.

```python
{% include_relative assignments/a2-leaderboard/starter.py %}
```

Run: `uv run pytest modules/07-lists-and-tuples/assignments/a2-leaderboard`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-leaderboard/solution.py %}
```

The sort key `(-score, name)` sorts by score descending and then by name ascending, because tuples compare item by item. `ranking` uses `enumerate(..., start=1)` for the position and changes the rank only when the score changes, which gives 1, 2, 2, 4.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Matrices

**Goal:** Transpose, build, multiply and rotate matrices stored as lists of lists. Practises nested lists, comprehensions and `zip(*rows)`.

**Files:** [`starter.py`]({{ 'modules/07-lists-and-tuples/assignments/a3-matrix/starter.py' | relative_url }}), test file `test_a3_matrix.py` in the same folder.

```python
{% include_relative assignments/a3-matrix/starter.py %}
```

Run: `uv run pytest modules/07-lists-and-tuples/assignments/a3-matrix`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-matrix/solution.py %}
```

`zip(*matrix)` turns the columns into tuples, and `list(column)` makes them lists again. Rotating clockwise is a transpose followed by reversing each row. `identity` uses a comprehension so that every row is a separate list.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Records and summaries

**Goal:** Split a list into chunks, parse messy text lines into `(name, quantity, price)` tuples, and summarise them. Practises slicing, tuples, unpacking and defensive parsing.

**Files:** [`starter.py`]({{ 'modules/07-lists-and-tuples/assignments/a4-records/starter.py' | relative_url }}), test file `test_a4_records.py` in the same folder.

```python
{% include_relative assignments/a4-records/starter.py %}
```

Run: `uv run pytest modules/07-lists-and-tuples/assignments/a4-records`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-records/solution.py %}
```

`chunk` slices with `items[start : start + size]` for every `start` from `range(0, len(items), size)`. `parse_records` skips bad lines with `continue` and stores valid ones as tuples. `max(..., key=...)` finds the most valuable record, and unpacking with `_` ignores the fields you do not need.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="07-lists-and-tuples:assignments"> I have finished the assignments</label></li>
</ul>
