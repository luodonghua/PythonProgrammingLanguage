---
layout: module
module: 25-capstone
kind: assignments
title: "Basic capstone: expense tracker - assignments"
permalink: /modules/25-capstone/assignments/
---
Five stages of one project: an expense tracker. Each stage lives in its own folder with its own tests and repeats the few pieces it needs (such as the `Expense` dataclass), so you can do the stages in any order. Doing them 1 to 5 shows how the layers fit together. Stage 5 is a stretch task.

{% include practice-setup.md %}

No extra libraries are needed. Stages use `csv`, `sqlite3`, `argparse`, `json`, `decimal` and `dataclasses` from the standard library. Money is always a `Decimal` (or whole cents in the database), never a `float`.

Run all tests for this topic:

```bash
uv run pytest modules/25-capstone
```

---

<div class="assignment" markdown="1">

## Assignment 1: Stage 1: parse expenses.csv

**Goal:** Turn CSV rows into `Expense` dataclasses. Validate every field, and collect an error with its line number for each bad row instead of stopping. Practises `csv.DictReader`, `Decimal`, dataclasses and error handling.

**Files:** [`starter.py`]({{ 'modules/25-capstone/assignments/a1-parse-csv/starter.py' | relative_url }}), test file `test_a1_parse_csv.py` in the same folder. Data file: `expenses.csv` (it contains five bad rows on purpose).

```python
{% include_relative assignments/a1-parse-csv/starter.py %}
```

Run: `uv run pytest modules/25-capstone/assignments/a1-parse-csv`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-parse-csv/solution.py %}
```

`parse_row` holds all the rules and raises `ValueError`. `parse_expenses` loops, catches `ValueError`, and uses `reader.line_num` for the message. `Decimal("abc")` raises `InvalidOperation`, so it is caught and re-raised as `ValueError`. The check `exponent < -2` finds amounts with more than two decimals without calling `quantize`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Stage 2: SQLite repository

**Goal:** Write `ExpenseRepository` with `add`, `list_expenses` (optionally for one month) and `totals_by_category`. Practises `sqlite3`, `?` parameters, `GROUP BY` and converting between `Decimal` and integer cents.

**Files:** [`starter.py`]({{ 'modules/25-capstone/assignments/a2-repository/starter.py' | relative_url }}), test file `test_a2_repository.py` in the same folder.

```python
{% include_relative assignments/a2-repository/starter.py %}
```

Run: `uv run pytest modules/25-capstone/assignments/a2-repository`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-repository/solution.py %}
```

The table stores `cents` as an `INTEGER`, so sums are exact. `with self.conn:` commits each insert. The month filter uses `substr(day, 1, 7) = ?` with a parameter, and the totals query sorts in SQL with `ORDER BY total DESC, category`. `Decimal(cents).scaleb(-2)` shifts the decimal point and keeps two decimals.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Stage 3: monthly report

**Goal:** Format a month of expenses as a fixed-width text table, and find the top category. Practises f-string format specs (width, alignment, thousands separator), sorting with a tuple key and pure functions.

**Files:** [`starter.py`]({{ 'modules/25-capstone/assignments/a3-report/starter.py' | relative_url }}), test file `test_a3_report.py` in the same folder.

```python
{% include_relative assignments/a3-report/starter.py %}
```

Run: `uv run pytest modules/25-capstone/assignments/a3-report`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-report/solution.py %}
```

A shared helper `_totals` computes the sorted totals. Sorting with the key `(-total, name)` puts big totals first and breaks ties A-Z. The format spec `>12,.2f` right-aligns in 12 columns with a thousands separator and two decimals. The function returns a string, so the CLI decides where to print it.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Stage 4: command-line interface

**Goal:** Wire the layers together with `argparse` sub-commands `add`, `list` and `report`. `main(argv)` returns an exit code and sends errors to standard error. Practises `argparse`, exit codes, `capsys` testing and `try/finally`.

**Files:** [`starter.py`]({{ 'modules/25-capstone/assignments/a4-cli/starter.py' | relative_url }}), test file `test_a4_cli.py` in the same folder.

```python
{% include_relative assignments/a4-cli/starter.py %}
```

Run: `uv run pytest modules/25-capstone/assignments/a4-cli`

From a terminal you can also try it: `uv run python modules/25-capstone/assignments/a4-cli/solution.py --db /tmp/e.db add 2024-03-01 food 4.50`.

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-cli/solution.py %}
```

`build_parser` only describes the command line. `main` parses, runs the right branch inside `try`, turns a `ValueError` into an `error:` message on `stderr` with code 1, and closes the repository in `finally`. Usage errors never reach that code, because `argparse` exits with status 2 by itself.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 5: Stage 5 (stretch): export to JSON

**Goal:** Write expenses to a JSON file and read them back, with validation of the file's structure. Practises `json`, `Decimal` and dates as strings, and defensive parsing.

**Files:** [`starter.py`]({{ 'modules/25-capstone/assignments/a5-export-json/starter.py' | relative_url }}), test file `test_a5_export_json.py` in the same folder.

```python
{% include_relative assignments/a5-export-json/starter.py %}
```

Run: `uv run pytest modules/25-capstone/assignments/a5-export-json`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a5-export-json/solution.py %}
```

JSON has no `Decimal` or `date`, so both are strings and the importer rebuilds them. `sorted` is stable, so equal dates keep their input order. The importer checks the structure step by step and raises `ValueError` with a clear message, including the item number.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="25-capstone:assignments"> I have finished the assignments</label></li>
</ul>
