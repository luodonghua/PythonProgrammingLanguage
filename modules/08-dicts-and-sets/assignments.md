---
layout: module
module: 08-dicts-and-sets
kind: assignments
title: "Dictionaries and sets - assignments"
permalink: /modules/08-dicts-and-sets/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/08-dicts-and-sets
```

---

<div class="assignment" markdown="1">

## Assignment 1: Word frequency

**Goal:** Split text into words, count them with a plain dict, list the most common ones and find the distinct words. Practises `dict.get`, sorting with a key and `set`.

**Files:** [`starter.py`]({{ 'modules/08-dicts-and-sets/assignments/a1-word-frequency/starter.py' | relative_url }}), test file `test_a1_word_frequency.py` in the same folder.

```python
{% include_relative assignments/a1-word-frequency/starter.py %}
```

Run: `uv run pytest modules/08-dicts-and-sets/assignments/a1-word-frequency`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-word-frequency/solution.py %}
```

`counts.get(word, 0) + 1` reads the current count or starts at 0. The sort key `(-count, word)` sorts by count descending and then alphabetically, because tuples compare item by item. A `set` removes duplicates and `sorted` gives it an order.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Group, invert and merge

**Goal:** Group items by a key function, invert a dict, merge settings with defaults, build a dict with a comprehension and find the first duplicate. Practises `defaultdict`, `setdefault`, `|` and sets.

**Files:** [`starter.py`]({{ 'modules/08-dicts-and-sets/assignments/a2-group-and-invert/starter.py' | relative_url }}), test file `test_a2_group_and_invert.py` in the same folder.

```python
{% include_relative assignments/a2-group-and-invert/starter.py %}
```

Run: `uv run pytest modules/08-dicts-and-sets/assignments/a2-group-and-invert`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-group-and-invert/solution.py %}
```

`defaultdict(list)` creates the list the first time a key appears. `defaults | settings` makes a new dict where the right-hand side wins, so the arguments stay unchanged. `first_duplicate` keeps a `seen` set, and `item in seen` is fast.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Guest lists

**Goal:** Compare two guest lists with set operators and clean up messy names first. Practises `&`, `|`, `-`, `^` and set comprehensions.

**Files:** [`starter.py`]({{ 'modules/08-dicts-and-sets/assignments/a3-guest-lists/starter.py' | relative_url }}), test file `test_a3_guest_lists.py` in the same folder.

```python
{% include_relative assignments/a3-guest-lists/starter.py %}
```

Run: `uv run pytest modules/08-dicts-and-sets/assignments/a3-guest-lists`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-guest-lists/solution.py %}
```

Turn each list into a set, apply one operator and sort the result for a stable answer. `normalize` uses a set comprehension that strips and title-cases each name, so `"ann "` and `"ANN"` become the same guest.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Nested data and inventories

**Goal:** Read and write values deep inside nested dicts, add up inventories and count records by a field. Practises `in`, `setdefault`, `Counter` and defensive lookups.

**Files:** [`starter.py`]({{ 'modules/08-dicts-and-sets/assignments/a4-nested-data/starter.py' | relative_url }}), test file `test_a4_nested_data.py` in the same folder.

```python
{% include_relative assignments/a4-nested-data/starter.py %}
```

Run: `uv run pytest modules/08-dicts-and-sets/assignments/a4-nested-data`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-nested-data/solution.py %}
```

`get_path` walks one key at a time and returns the default as soon as a key is missing or the current value is not a dict. `set_path` uses `setdefault(key, {})` to create the missing levels. `Counter.update` adds counts instead of replacing them.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="08-dicts-and-sets:assignments"> I have finished the assignments</label></li>
</ul>
