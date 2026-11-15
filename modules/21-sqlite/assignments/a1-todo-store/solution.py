"""Assignment 1: A to-do store on SQLite.

Every function takes an open sqlite3 connection as its first argument. Always
pass values with ? placeholders. Commit your changes (use `with conn:`).
"""

import sqlite3


def init_db(conn: sqlite3.Connection) -> None:
    """Create the table if it does not exist yet:

        todos(id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)

    Calling it twice must not fail (use CREATE TABLE IF NOT EXISTS).
    """
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )


def add_todo(conn: sqlite3.Connection, title: str) -> int:
    """Insert a to-do (not done) and return its new id.

    Raise ValueError if the title is empty after stripping spaces. Store the
    stripped title.
    """
    title = title.strip()
    if not title:
        raise ValueError("title must not be empty")
    with conn:
        cursor = conn.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    return cursor.lastrowid


def list_todos(conn: sqlite3.Connection, only_open: bool = False) -> list[dict]:
    """Return the to-dos ordered by id as dicts {"id": int, "title": str, "done": bool}.

    With only_open=True return only those that are not done.
    """
    sql = "SELECT id, title, done FROM todos"
    if only_open:
        sql += " WHERE done = 0"
    sql += " ORDER BY id"
    return [
        {"id": row[0], "title": row[1], "done": bool(row[2])}
        for row in conn.execute(sql)
    ]


def complete(conn: sqlite3.Connection, todo_id: int) -> bool:
    """Mark a to-do as done. Return True if a row was changed, False if the id
    does not exist."""
    with conn:
        cursor = conn.execute("UPDATE todos SET done = 1 WHERE id = ?", (todo_id,))
    return cursor.rowcount == 1


def delete_done(conn: sqlite3.Connection) -> int:
    """Delete all finished to-dos and return how many were deleted."""
    with conn:
        cursor = conn.execute("DELETE FROM todos WHERE done = 1")
    return cursor.rowcount


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    init_db(db)
    first = add_todo(db, "Write tests")
    add_todo(db, "Ship it")
    complete(db, first)
    print(list_todos(db))
    print(list_todos(db, only_open=True))
