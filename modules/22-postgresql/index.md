---
layout: module
module: 22-postgresql
kind: learn
title: "Persistence: PostgreSQL"
permalink: /modules/22-postgresql/
---

<div class="box key" markdown="1">

## Key learning points

- PostgreSQL is a **database server**. Your program connects to it over the network as a client, and many clients can read and write at the same time.
- Start a practice server with `docker compose up -d`. The default connection string is `postgresql://postgres:postgres@localhost:5432/postgres`.
- `psycopg` (version 3) is the Python driver. `psycopg.connect(dsn)` opens a connection, `conn.execute(sql, params)` runs a query.
- Pass values with **`%s` placeholders** and a tuple. Never build SQL with f-strings.
- A transaction starts automatically with your first statement. Nothing is saved until `commit()`. An error aborts the transaction until you call `rollback()`.
- `conn.transaction()` wraps a block: commit on success, rollback on an exception. `RETURNING` gives back the rows you changed, and `ON CONFLICT` does an upsert.

</div>

## 1. Why PostgreSQL after SQLite

SQLite is a file that one program opens. PostgreSQL is a separate server process that many programs talk to.

| | SQLite | PostgreSQL |
|---|---|---|
| Runs as | a library inside your program | a server (own process) |
| Many writers at once | limited | built for it (MVCC: readers do not block writers) |
| Types | few, loose | strict, many (`NUMERIC`, `TIMESTAMPTZ`, `JSONB`, arrays, ...) |
| Users and permissions | none | roles and grants |
| Typical use | local apps, tests, small tools | web back ends, shared data |

The SQL you learned in topic 21 mostly carries over. The differences are in types, placeholders and transactions.

## 2. Start a server

The repository has a `compose.yaml` file. With Docker installed, run this in the project folder:

```bash
docker compose up -d
```

This starts PostgreSQL 17 on port 5432 with the user `postgres` and the password `postgres`. That is fine for practice on your own computer. A real database needs a strong password and no public port.

- Stop it with `docker compose down`. The practice data is not kept.
- To use another server, set the environment variable `PRACTICE_PG_DSN`. A DSN (data source name) looks like `postgresql://user:password@host:port/database`.
- In a real program, read the DSN from the environment and never write passwords in your code.

Install the driver with `uv add "psycopg[binary]"`. The course project already includes it.

## 3. Connect and create a table

```python
from decimal import Decimal

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

DSN = "postgresql://postgres:postgres@localhost:5432/postgres"

with psycopg.connect(DSN) as conn:
    conn.execute("DROP TABLE IF EXISTS products")
    conn.execute("""
        CREATE TABLE products (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            attrs JSONB NOT NULL DEFAULT '{}'
        )
    """)
    ...
```

The rest of this page runs inside this `with` block. Used as a context manager, a psycopg connection **commits** when the block ends normally, **rolls back** if it ends with an exception, and then **closes**. This differs from `sqlite3`, where `with conn:` does not close.

Useful column types:

| Type | Python value | Note |
|---|---|---|
| `INTEGER`, `BIGINT` | `int` | `GENERATED ALWAYS AS IDENTITY` numbers rows for you |
| `TEXT` | `str` | no length limit needed |
| `NUMERIC(10, 2)` | `Decimal` | exact decimals, use it for money |
| `TIMESTAMPTZ` | aware `datetime` | stores the moment in UTC (see topic 19) |
| `JSONB` | `dict` / `list` | JSON you can query |
| `BOOLEAN` | `bool` | |

## 4. Insert with parameters and RETURNING

```python
    cur = conn.execute(
        "INSERT INTO products (name, price, attrs) VALUES (%s, %s, %s) RETURNING id",
        ("pen", Decimal("1.50"), Jsonb({"color": "blue", "tags": ["a", "b"]})),
    )
    print(cur.fetchone())
```

```text
(1,)
```

- `%s` is the placeholder for every type, not only strings. Write `%%` for a literal percent sign.
- `RETURNING` sends back columns of the inserted (or updated, or deleted) rows, so you do not need a second query for the new `id`.
- `Jsonb(...)` tells psycopg to send a Python value as JSONB.

Placeholders hold **values** only. Table and column names cannot be parameters.

## 5. Read rows

```python
    conn.execute("INSERT INTO products (name, price) VALUES (%s, %s)", ("book", Decimal("12.00")))
    print(conn.execute("SELECT id, name, price FROM products ORDER BY id").fetchall())
```

```text
[(1, 'pen', Decimal('1.50')), (2, 'book', Decimal('12.00'))]
```

`NUMERIC` comes back as `Decimal`, not `float`. For dict rows, use `row_factory=dict_row`:

```python
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT id, name, price FROM products WHERE price > %s ORDER BY id", (Decimal("2"),))
        print(cur.fetchall())
```

```text
[{'id': 2, 'name': 'book', 'price': Decimal('12.00')}]
```

You can also set it for the whole connection: `psycopg.connect(DSN, row_factory=dict_row)`. `fetchone()` returns `None` when there is no row.

```python
    print(conn.execute("SELECT name FROM products WHERE name LIKE %s ORDER BY name", ("p%",)).fetchall())
    print(conn.execute("SELECT name FROM products WHERE name = ANY(%s) ORDER BY name", (["pen", "book", "x"],)).fetchall())
```

```text
[('pen',)]
[('book',), ('pen',)]
```

Put the `%` of a `LIKE` pattern inside the *value*, as above. A Python list becomes a PostgreSQL array, and `= ANY(%s)` is the safe way to match a list of values.

## 6. Upsert

`ON CONFLICT` inserts a row or, if a unique rule is hit, updates the existing row:

```python
    upsert = """
        INSERT INTO products (name, price) VALUES (%s, %s)
        ON CONFLICT (name) DO UPDATE SET price = EXCLUDED.price
        RETURNING id, price
    """
    print(conn.execute(upsert, ("pen", Decimal("1.75"))).fetchone())
    print(conn.execute(upsert, ("ink", Decimal("3.00"))).fetchone())
```

```text
(1, Decimal('1.75'))
(4, Decimal('3.00'))
```

`EXCLUDED` is the row you tried to insert. The new row got id 4, not 3: an identity counter moves forward even when the insert ends up as an update, so ids can have gaps. Do not rely on ids being consecutive.

## 7. JSONB

`JSONB` stores JSON in a binary form that can be searched. Operators: `->` gets a value as JSON, `->>` gets it as text, `@>` tests whether the left side contains the right side.

```python
    print(conn.execute(
        "SELECT attrs->>'color', attrs->'tags'->>0 FROM products WHERE attrs @> %s",
        (Jsonb({"color": "blue"}),),
    ).fetchall())
    attrs = conn.execute("SELECT attrs FROM products WHERE name = 'pen'").fetchone()[0]
    print(type(attrs).__name__, attrs["tags"])
    conn.commit()
```

```text
[('blue', 'a')]
dict ['a', 'b']
```

A `JSONB` column comes back as a normal Python `dict` or `list`. JSONB does not keep key order. Use it for flexible extra data. Keep fields you filter and join on in normal columns.

## 8. Transactions

psycopg does **not** autocommit. The first statement opens a transaction, and `conn.commit()` or `conn.rollback()` ends it. The `conn.commit()` above saved the table and the rows.

When a statement fails, PostgreSQL marks the whole transaction as failed. Every later statement is refused until you roll back:

```python
    try:
        conn.execute("INSERT INTO products (name, price) VALUES (%s, %s)", ("bad", -1))
    except psycopg.errors.CheckViolation as exc:
        print(type(exc).__name__)
    try:
        conn.execute("SELECT 1")
    except psycopg.errors.InFailedSqlTransaction as exc:
        print(type(exc).__name__)
    conn.rollback()
    print(conn.execute("SELECT count(*) FROM products").fetchone())
```

```text
CheckViolation
InFailedSqlTransaction
(3,)
```

The rollback undid only the failed work. The three rows were committed before. `conn.transaction()` makes this tidy:

```python
    with conn.transaction():
        conn.execute("UPDATE products SET price = price + 1")
    try:
        with conn.transaction():
            conn.execute("UPDATE products SET price = 0")
            raise RuntimeError("stop")
    except RuntimeError:
        pass
    print(conn.execute("SELECT name, price FROM products ORDER BY id").fetchall())
```

```text
[('pen', Decimal('2.75')), ('book', Decimal('13.00')), ('ink', Decimal('4.00'))]
```

The first block committed (+1 on every price). The second block raised an error, so its `UPDATE ... SET price = 0` was rolled back. Nested `conn.transaction()` blocks use savepoints.

**Isolation.** Isolation says what one transaction can see of another's work. The default level is `READ COMMITTED`: each statement sees only data that was committed before it started.

```python
    print(conn.execute("SHOW transaction_isolation").fetchone())
```

```text
('read committed',)
```

Two transactions that read, then write, the same row can still collide. For "read, then update" logic, use `SELECT ... FOR UPDATE` to lock the row, or do the change in one statement (`UPDATE accounts SET balance = balance - %s ...`). Other levels (`REPEATABLE READ`, `SERIALIZABLE`) exist; see the PostgreSQL manual.

## 9. Connection pools

Opening a connection takes time (a network round trip, authentication). Web servers keep a few connections open and share them. The separate package `psycopg_pool` provides `ConnectionPool` for this. You do not need it for this course.

<div class="box warn" markdown="1">

## Common mistakes

- **Building SQL with f-strings or `%`.** Use `%s` placeholders. It is the only protection against SQL injection.
- **Forgetting to commit.** Your changes are visible to you but lost when the connection closes without a commit.
- **Ignoring the aborted transaction.** After an error you must `rollback()` (or use `conn.transaction()`), or every later statement fails.
- **Using `float` for money.** Use `NUMERIC` and `Decimal`.
- **Naive datetimes with `TIMESTAMPTZ`.** Pass aware datetimes, preferably in UTC.
- **Passing a single value as a bare string.** Write `(name,)`, a tuple with a comma.
- **Leaving the server running with a weak password and an open port.** The practice setup is for your own machine only.

</div>

## Try it yourself

1. Start the server, connect with `psycopg.connect`, and run `SELECT version()`. Print the result.
2. Create a `notes` table with an identity `id`, a `TEXT` body and a `TIMESTAMPTZ` column with default `now()`. Insert two notes and print them with `RETURNING`.
3. Write a function `transfer(conn, from_id, to_id, amount)` that moves money between two rows of an `accounts` table inside `with conn.transaction():`. Make it raise an error halfway and check that nothing changed.

## Further reading

- [psycopg 3 docs](https://www.psycopg.org/psycopg3/docs/)
- [PostgreSQL manual](https://www.postgresql.org/docs/17/index.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="22-postgresql:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/22-postgresql/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/22-postgresql/assignments/' | relative_url }}).
