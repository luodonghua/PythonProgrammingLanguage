---
layout: module
module: 21-sqlite
kind: assignments
title: Persistence: SQLite - assignments
permalink: /modules/21-sqlite/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

`sqlite3` is part of Python, so there is nothing to install. The tests use an in-memory database (`":memory:"`) or a file in a temporary folder. They create the tables themselves, so you only write the functions. Every function takes an open connection as its first argument.

Run all tests for this topic:

```bash
uv run pytest modules/21-sqlite
```

---

<div class="assignment" markdown="1">

## Assignment 1: To-do store

**Goal:** Build a small to-do store on SQLite with create, add, list, complete and delete functions. Practises `execute`, `?` placeholders, `lastrowid`, `rowcount` and `with conn:`.

**Files:** [`starter.py`]({{ 'modules/21-sqlite/assignments/a1-todo-store/starter.py' | relative_url }}), test file `test_a1_todo_store.py` in the same folder.

```python
{% include_relative assignments/a1-todo-store/starter.py %}
```

Run: `uv run pytest modules/21-sqlite/assignments/a1-todo-store`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-todo-store/solution.py %}
```

Each change runs inside `with conn:`, so it commits when the block ends. `cursor.lastrowid` gives the new id and `cursor.rowcount` tells whether `UPDATE` found a row. The result dicts are built from column positions, so the code works with any `row_factory`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: JOIN queries

**Goal:** Write queries that join `authors` and `books`, filter by author name with a parameter, and list authors that have no books. Practises `JOIN`, `LEFT JOIN` and `GROUP BY`.

**Files:** [`starter.py`]({{ 'modules/21-sqlite/assignments/a2-join-queries/starter.py' | relative_url }}), test file `test_a2_join_queries.py` in the same folder.

```python
{% include_relative assignments/a2-join-queries/starter.py %}
```

Run: `uv run pytest modules/21-sqlite/assignments/a2-join-queries`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-join-queries/solution.py %}
```

An inner `JOIN` drops authors without books. `LEFT JOIN` keeps them, and `COUNT(b.id)` counts only real books, because `COUNT(*)` would count the empty row as 1. `WHERE b.id IS NULL` finds the authors that matched nothing.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Aggregate sales report

**Goal:** Use `SUM`, `GROUP BY`, `ORDER BY` and `LIMIT` to report revenue per customer, totals per month and the best-selling product. Practises aggregates and formatting cents as dollars.

**Files:** [`starter.py`]({{ 'modules/21-sqlite/assignments/a3-sales-report/starter.py' | relative_url }}), test file `test_a3_sales_report.py` in the same folder.

```python
{% include_relative assignments/a3-sales-report/starter.py %}
```

Run: `uv run pytest modules/21-sqlite/assignments/a3-sales-report`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-sales-report/solution.py %}
```

The database does the adding, so Python only formats the result. `substr(ordered_on, 1, 7)` cuts `YYYY-MM` out of an ISO date. Money is kept as integer cents and divided by 100 only for display.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Migrations and upsert

**Goal:** Apply schema migration steps once, using `PRAGMA user_version` as the version counter, and write a settings store that uses `INSERT ... ON CONFLICT DO UPDATE`. Practises schema changes over time and upserts.

**Files:** [`starter.py`]({{ 'modules/21-sqlite/assignments/a4-migrate-upsert/starter.py' | relative_url }}), test file `test_a4_migrate_upsert.py` in the same folder.

```python
{% include_relative assignments/a4-migrate-upsert/starter.py %}
```

Run: `uv run pytest modules/21-sqlite/assignments/a4-migrate-upsert`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-migrate-upsert/solution.py %}
```

`migrations[version:]` is exactly the list of steps not yet run, and `enumerate(..., start=version + 1)` numbers them. After each step the version is saved, so a crash in the middle resumes at the right place. In the upsert, `excluded.value` is the value you tried to insert, and `updates = updates + 1` refers to the stored row.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="21-sqlite:assignments"> I have finished the assignments</label></li>
</ul>
