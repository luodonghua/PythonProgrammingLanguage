---
layout: module
module: 18-text-data
kind: assignments
title: "Text data: CSV, JSON and regex - assignments"
permalink: /modules/18-text-data/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Three of these tasks come with small data files (`sales.csv`, `inventory.csv`, `people.csv`) in the assignment folders. Do not move them. Your code reads them with paths the tests pass in.

Run all tests for this topic:

```bash
uv run pytest modules/18-text-data
```

---

<div class="assignment" markdown="1">

## Assignment 1: Sum a CSV column

**Goal:** Read a CSV file with `csv.DictReader` and add up a column, including a total of quantity times price. Practises the `csv` module, type conversion and `KeyError` for a missing column.

**Files:** [`starter.py`]({{ 'modules/18-text-data/assignments/a1-sum-column/starter.py' | relative_url }}), test file `test_a1_sum_column.py` in the same folder. The data file `sales.csv` is in the same folder.

```python
{% include_relative assignments/a1-sum-column/starter.py %}
```

Run: `uv run pytest modules/18-text-data/assignments/a1-sum-column`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-sum-column/solution.py %}
```

`DictReader` gives a `str` for every field, so each value goes through `float()` or `int()`. `reader.fieldnames` is `None` for an empty file, which is why the code checks it before raising `KeyError`. A product name such as `"notebook, A5"` is one field because the `csv` module honours the quotes.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: CSV to JSON converter

**Goal:** Convert each CSV field to the best Python type and write the rows as an indented JSON array. Practises `json.dump` and a small conversion function.

**Files:** [`starter.py`]({{ 'modules/18-text-data/assignments/a2-csv-to-json/starter.py' | relative_url }}), test file `test_a2_csv_to_json.py` in the same folder. The data file `inventory.csv` is in the same folder.

```python
{% include_relative assignments/a2-csv-to-json/starter.py %}
```

Run: `uv run pytest modules/18-text-data/assignments/a2-csv-to-json`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-csv-to-json/solution.py %}
```

`convert_value` tries `int`, then `float`, and falls back to the text. The order matters, because `float("12")` would turn whole numbers into floats. An empty field becomes `None`, which JSON writes as `null`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Regex extractor

**Goal:** Extract e-mail addresses and ISO dates from text and parse a log line into a dict. Practises `findall`, groups, named groups and `fullmatch`.

**Files:** [`starter.py`]({{ 'modules/18-text-data/assignments/a3-regex-extract/starter.py' | relative_url }}), test file `test_a3_regex_extract.py` in the same folder.

```python
{% include_relative assignments/a3-regex-extract/starter.py %}
```

Run: `uv run pytest modules/18-text-data/assignments/a3-regex-extract`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-regex-extract/solution.py %}
```

Compile the patterns once at module level. The date pattern uses the look-arounds `(?<!\d)` and `(?!\d)` so a longer run of digits does not match. `dict.fromkeys` removes duplicate e-mails while keeping order. `fullmatch` with named groups returns `groupdict()` or `None`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Clean data and collect errors

**Goal:** Validate every row of a messy CSV, keep the good rows and report each bad row with its line number and reason. Practises error handling per row and regex validation.

**Files:** [`starter.py`]({{ 'modules/18-text-data/assignments/a4-clean-rows/starter.py' | relative_url }}), test file `test_a4_clean_rows.py` in the same folder. The data file `people.csv` is in the same folder.

```python
{% include_relative assignments/a4-clean-rows/starter.py %}
```

Run: `uv run pytest modules/18-text-data/assignments/a4-clean-rows`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-clean-rows/solution.py %}
```

The loop checks the problems in the stated order and uses `continue` after recording the first one, so a row gives at most one error. `csv.reader` gives plain lists, which makes the field-count check easy. `enumerate(..., start=1)` keeps line numbers matching the file.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="18-text-data:assignments"> I have finished the assignments</label></li>
</ul>
