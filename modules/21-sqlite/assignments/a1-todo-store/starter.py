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
    # TODO: run the CREATE TABLE statement.
    ...


def add_todo(conn: sqlite3.Connection, title: str) -> int:
    """Insert a to-do (not done) and return its new id.

    Raise ValueError if the title is empty after stripping spaces. Store the
    stripped title.
    """
    # TODO: validate, INSERT with a placeholder, return cursor.lastrowid.
    ...


def list_todos(conn: sqlite3.Connection, only_open: bool = False) -> list[dict]:
    """Return the to-dos ordered by id as dicts {"id": int, "title": str, "done": bool}.

    With only_open=True return only those that are not done.
    """
    # TODO: SELECT, optionally with WHERE done = 0, and build the dicts.
    ...


def complete(conn: sqlite3.Connection, todo_id: int) -> bool:
    """Mark a to-do as done. Return True if a row was changed, False if the id
    does not exist."""
    # TODO: UPDATE ... WHERE id = ? and look at cursor.rowcount.
    ...


def delete_done(conn: sqlite3.Connection) -> int:
    """Delete all finished to-dos and return how many were deleted."""
    # TODO: DELETE ... WHERE done = 1 and return rowcount.
    ...


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    init_db(db)
    first = add_todo(db, "Write tests")
    add_todo(db, "Ship it")
    complete(db, first)
    print(list_todos(db))
    print(list_todos(db, only_open=True))
