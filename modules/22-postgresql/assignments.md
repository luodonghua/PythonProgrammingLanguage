---
layout: module
module: 22-postgresql
kind: assignments
title: "Persistence: PostgreSQL - assignments"
permalink: /modules/22-postgresql/assignments/
---
Five tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

These tasks need a running PostgreSQL server. The repository includes a `compose.yaml` for one. With Docker installed, run this in the project folder:

```bash
docker compose up -d
```

This starts PostgreSQL 17 on port 5432. The tests connect with the default DSN `postgresql://postgres:postgres@localhost:5432/postgres`. To use a different server, set the environment variable `PRACTICE_PG_DSN` to its DSN.

Each test gets a fresh temporary schema (a private set of tables), and the schema is dropped afterwards. Your tables never collide with each other or with other data in the database.

**If no database is running, the tests are skipped, not failed.** A skipped test proves nothing, so start the server before you judge your solution. When you are done, stop it with:

```bash
docker compose down
```

The `psycopg` driver is already part of the course environment (`uv sync`). Every function takes the open connection `conn` as its first argument. The connection does not autocommit, so commit your changes.

Run all tests for this topic:

```bash
uv run pytest modules/22-postgresql
```

---

<div class="assignment" markdown="1">

## Assignment 1: Create a table and insert with RETURNING

**Goal:** Create a `books` table with an identity key, `NUMERIC` and `TIMESTAMPTZ` columns, insert books with `RETURNING id`, insert a batch in one transaction, and read a book back as a dict. Practises `%s` parameters, `dict_row` and `conn.transaction()`.

**Files:** [`starter.py`]({{ 'modules/22-postgresql/assignments/a1-create-and-insert/starter.py' | relative_url }}), test file `test_a1_create_and_insert.py` in the same folder.

```python
{% include_relative assignments/a1-create-and-insert/starter.py %}
```

Run: `uv run pytest modules/22-postgresql/assignments/a1-create-and-insert`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-create-and-insert/solution.py %}
```

`RETURNING id` gives the new key without a second query. `add_books` runs inside one `with conn.transaction():`, so a bad row (rejected by Python or by the database) undoes the whole batch. Validation happens before the SQL runs, so the connection never enters an aborted transaction.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Parameterized search

**Goal:** Write a search that combines optional filters (title text, maximum price, a list of authors) into one query, using only `%s` parameters. Practises dynamic `WHERE` clauses without SQL injection, `ILIKE`, `= ANY(%s)` and `GROUP BY`.

**Files:** [`starter.py`]({{ 'modules/22-postgresql/assignments/a2-search-books/starter.py' | relative_url }}), test file `test_a2_search_books.py` in the same folder.

```python
{% include_relative assignments/a2-search-books/starter.py %}
```

Run: `uv run pytest modules/22-postgresql/assignments/a2-search-books`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-search-books/solution.py %}
```

The SQL text is assembled only from fixed fragments (`title ILIKE %s`, `price <= %s`, `author = ANY(%s)`). All user values go into the `params` list. The `%` and `_` in the search text are escaped with a backslash, so they match themselves instead of acting as wildcards. A Python list passed to `ANY(%s)` becomes a PostgreSQL array.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Money transfer with rollback

**Goal:** Move money between two accounts so that the withdrawal and the deposit happen together or not at all. Practises `conn.transaction()`, `SELECT ... FOR UPDATE`, custom exceptions and nested transactions (savepoints).

**Files:** [`starter.py`]({{ 'modules/22-postgresql/assignments/a3-transfer/starter.py' | relative_url }}), test file `test_a3_transfer.py` in the same folder.

```python
{% include_relative assignments/a3-transfer/starter.py %}
```

Run: `uv run pytest modules/22-postgresql/assignments/a3-transfer`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-transfer/solution.py %}
```

The whole transfer runs inside `with conn.transaction():`. If the target account does not exist, the `LookupError` leaves the block and the withdrawal is rolled back. `FOR UPDATE` locks the source row, so a second transfer must wait until the first one commits. In `transfer_many`, each inner `transaction()` becomes a savepoint inside the outer one.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Upsert counter

**Goal:** Build a page-hit counter with one `INSERT ... ON CONFLICT DO UPDATE ... RETURNING` statement. Practises upserts, `EXCLUDED`, `LIMIT` with a parameter and `rowcount`.

**Files:** [`starter.py`]({{ 'modules/22-postgresql/assignments/a4-upsert-counter/starter.py' | relative_url }}), test file `test_a4_upsert_counter.py` in the same folder.

```python
{% include_relative assignments/a4-upsert-counter/starter.py %}
```

Run: `uv run pytest modules/22-postgresql/assignments/a4-upsert-counter`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-upsert-counter/solution.py %}
```

One statement both inserts a new page and adds to an existing one, so two programs counting at the same time cannot lose a hit. A read followed by a write could. `EXCLUDED.hits` is the value you tried to insert, and `page_hits.hits` is the stored value.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 5: JSONB events

**Goal:** Store event payloads as JSONB and query them with `@>`, `->>` and a cast. Practises `Jsonb(...)`, containment queries and aggregates over JSON fields.

**Files:** [`starter.py`]({{ 'modules/22-postgresql/assignments/a5-jsonb-events/starter.py' | relative_url }}), test file `test_a5_jsonb_events.py` in the same folder.

```python
{% include_relative assignments/a5-jsonb-events/starter.py %}
```

Run: `uv run pytest modules/22-postgresql/assignments/a5-jsonb-events`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a5-jsonb-events/solution.py %}
```

`Jsonb(payload)` sends a Python dict as JSONB, and a JSONB column comes back as a dict. `payload @> %s` finds rows that contain all the given pairs, and an empty dict matches every row. `->>` returns text, so `average_ms` casts it with `::numeric` before `avg`, and `avg` skips rows where the key is missing.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="22-postgresql:assignments"> I have finished the assignments</label></li>
</ul>
