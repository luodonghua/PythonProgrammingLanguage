---
layout: module
module: 21-sqlite
kind: learn
title: "Persistence: SQLite"
permalink: /modules/21-sqlite/
---

<div class="box key" markdown="1">

## Key learning points

- SQLite is a database in a single file (or in memory), and the `sqlite3` module in the standard library talks to it. No server is needed.
- `sqlite3.connect("app.db")` opens or creates a file. `sqlite3.connect(":memory:")` makes a temporary database that disappears when the connection closes.
- **Always pass values with `?` placeholders**, never by building SQL text with f-strings. This stops SQL injection.
- Changes are not saved until `conn.commit()`. `with conn:` commits when the block ends normally and rolls back when it raises an exception. It does not close the connection.
- `conn.row_factory = sqlite3.Row` lets you read columns by name.
- `PRAGMA foreign_keys = ON` must be run on every new connection, or SQLite ignores foreign keys.

</div>

## 1. Connect, create a table, insert

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
conn.execute("""
CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)""")
conn.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id),
    year INTEGER,
    price REAL
)""")
```

`INTEGER PRIMARY KEY` makes `id` a unique row number that SQLite fills in for you. `conn.execute` creates a *cursor*, runs the SQL on it and returns the cursor.

```python
cur = conn.execute("INSERT INTO authors (name) VALUES (?)", ("Ursula Le Guin",))
print(cur.lastrowid, cur.rowcount)
conn.execute("INSERT INTO authors (name) VALUES (?)", ("Terry Pratchett",))
```

```text
1 1
```

`cur.lastrowid` is the new row's id. `cur.rowcount` is the number of rows the statement changed. The values go in a tuple, even for a single value.

Insert many rows at once with `executemany`, then save:

```python
conn.executemany(
    "INSERT INTO books (title, author_id, year, price) VALUES (?, ?, ?, ?)",
    [
        ("A Wizard of Earthsea", 1, 1968, 9.5),
        ("The Dispossessed", 1, 1974, 11.0),
        ("Small Gods", 2, 1992, 8.0),
        ("Mort", 2, 1987, 7.5),
        ("Guards! Guards!", 2, 1989, 8.5),
    ],
)
conn.commit()
```

## 2. Query

```python
rows = conn.execute("SELECT * FROM books WHERE year < ? ORDER BY year", (1980,)).fetchall()
print(rows)
```

```text
[(1, 'A Wizard of Earthsea', 1, 1968, 9.5), (2, 'The Dispossessed', 1, 1974, 11.0)]
```

- `fetchall()` returns a list of tuples.
- `fetchone()` returns one row, or `None` when there is none.
- You can also loop over the cursor: `for row in cursor:`.

With `row_factory = sqlite3.Row` each row works like a tuple and like a dict:

```python
conn.row_factory = sqlite3.Row
row = conn.execute("SELECT title, year FROM books WHERE id = ?", (3,)).fetchone()
print(row["title"], row["year"], tuple(row), row.keys())
print(conn.execute("SELECT * FROM books WHERE id = ?", (99,)).fetchone())
```

```text
Small Gods 1992 ('Small Gods', 1992) ['title', 'year']
None
```

## 3. JOIN and GROUP BY

A `JOIN` combines rows from two tables. `GROUP BY` makes one row per group, and aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) work on each group.

```python
query = """
SELECT a.name, COUNT(*) AS n, ROUND(AVG(b.price), 2) AS avg_price
FROM authors a JOIN books b ON b.author_id = a.id
GROUP BY a.id
ORDER BY n DESC
"""
for r in conn.execute(query):
    print(dict(r))
```

```text
{'name': 'Terry Pratchett', 'n': 3, 'avg_price': 8.0}
{'name': 'Ursula Le Guin', 'n': 2, 'avg_price': 10.25}
```

## 4. Update, delete and transactions

```python
cur = conn.execute("UPDATE books SET price = price * 1.1 WHERE author_id = ?", (2,))
print(cur.rowcount)        # 3
cur = conn.execute("DELETE FROM books WHERE year < ?", (1970,))
print(cur.rowcount)        # 1
conn.commit()
```

Forget the `WHERE` and the statement changes **every** row.

A **transaction** groups changes so that they all happen or none do. `with conn:` does this for you. It rolls back everything since the last commit, which is why we committed above first:

```python
try:
    with conn:
        conn.execute("INSERT INTO authors (name) VALUES ('Temp')")
        raise RuntimeError("fail")
except RuntimeError:
    pass
print(conn.execute("SELECT COUNT(*) FROM authors").fetchone()[0])
```

```text
2
```

The insert was rolled back, so the count is still 2. Call `conn.close()` yourself when you are finished, or use `contextlib.closing(conn)`.

## 5. Constraints and foreign keys

`NOT NULL`, `UNIQUE`, `PRIMARY KEY` and `REFERENCES` make the database refuse bad data. A violation raises `sqlite3.IntegrityError`:

```python
try:
    conn.execute("INSERT INTO books (title, author_id) VALUES ('x', 99)")
except sqlite3.IntegrityError as exc:
    print(exc)
```

```text
FOREIGN KEY constraint failed
```

There is no author 99. This check only works because we ran `PRAGMA foreign_keys = ON` after connecting.

## 6. Indexes

An index lets the database find rows without reading the whole table. It speeds up `WHERE`, `JOIN` and `ORDER BY` on that column, and slows down writes a little.

```python
conn.execute("CREATE INDEX idx_books_year ON books(year)")
plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM books WHERE year = 1987").fetchone()
print(plan[3])
```

```text
SEARCH books USING INDEX idx_books_year (year=?)
```

## 7. SQL injection

If you paste user text into SQL, the user can change the query:

```python
name = "x' OR '1'='1"
bad = conn.execute(f"SELECT COUNT(*) FROM authors WHERE name = '{name}'").fetchone()[0]
good = conn.execute("SELECT COUNT(*) FROM authors WHERE name = ?", (name,)).fetchone()[0]
print(bad, good)
```

```text
2 0
```

The f-string version matched every author. The `?` version treats the whole text as a value and found nobody. Placeholders work for values only. Table and column names cannot be parameters. If a name comes from outside, check it against a fixed list of allowed names.

## 8. Upsert and schema versions

An *upsert* inserts a row or updates it if it already exists (needs a `UNIQUE` or primary key column):

```python
conn.execute(
    """INSERT INTO authors (name) VALUES (?)
       ON CONFLICT(name) DO UPDATE SET name = excluded.name""",
    ("Terry Pratchett",),
)
```

`excluded` refers to the row you tried to insert. To change a schema over time, keep a version number in `PRAGMA user_version` (an integer stored in the file) and run only the migration steps newer than that number.

<div class="box warn" markdown="1">

## Common mistakes

- **Building SQL with f-strings or `+`.** Use `?` placeholders.
- **Forgetting `commit()`.** The data is visible on your connection but is lost when the program ends.
- **Passing a bare value** such as `(name)` instead of the tuple `(name,)`. `execute("... ?", "abc")` fails with "Incorrect number of bindings supplied" because a string is a sequence of characters.
- **Forgetting `PRAGMA foreign_keys = ON`.** SQLite then accepts rows that point to nothing.
- **`UPDATE` or `DELETE` without `WHERE`.**
- **Thinking `with conn:` closes the connection.** It only commits or rolls back.
- **Sharing one connection between threads.** By default SQLite connections can be used only in the thread that made them.

</div>

## Try it yourself

1. Create a `todos` table with `id`, `title`, `done` (0 or 1). Add three rows and print the ones that are not done.
2. Write a function `add_todo(conn, title)` that returns the new id. Call it inside `with conn:`.
3. Try the injection example on your own table. Then fix it with a placeholder.

## Further reading

- [sqlite3 docs](https://docs.python.org/3/library/sqlite3.html)
- [SQLite site](https://www.sqlite.org/docs.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="21-sqlite:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/21-sqlite/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/21-sqlite/assignments/' | relative_url }}).
