"""Assignment 1: Create a table and insert rows with RETURNING.

Every function takes an open psycopg connection `conn` as its first argument.
The connection does not autocommit, so commit your work (conn.commit() or
`with conn.transaction():`). Pass values with %s placeholders.
"""

from decimal import Decimal

import psycopg
from psycopg.rows import dict_row

INSERT_BOOK = "INSERT INTO books (title, author, price) VALUES (%s, %s, %s) RETURNING id"


def create_schema(conn: psycopg.Connection) -> None:
    """Create the table `books` if it does not exist, then commit:

        id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
        title     TEXT NOT NULL
        author    TEXT NOT NULL
        price     NUMERIC(8, 2) NOT NULL CHECK (price >= 0)
        added_at  TIMESTAMPTZ NOT NULL DEFAULT now()

    Calling it twice must not fail (CREATE TABLE IF NOT EXISTS).
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price NUMERIC(8, 2) NOT NULL CHECK (price >= 0),
            added_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    conn.commit()


def _clean(title: str, author: str, price: Decimal) -> tuple[str, str, Decimal]:
    title = title.strip()
    author = author.strip()
    if not title:
        raise ValueError("title must not be empty")
    if not author:
        raise ValueError("author must not be empty")
    if price < 0:
        raise ValueError("price must not be negative")
    return title, author, price


def add_book(conn: psycopg.Connection, title: str, author: str, price: Decimal) -> int:
    """Insert one book and return its new id (use RETURNING id), then commit.

    Strip spaces from the title and the author. Raise ValueError (before
    touching the database) if the title or the author is empty after
    stripping, or if the price is negative.
    """
    values = _clean(title, author, price)
    with conn.transaction():
        row = conn.execute(INSERT_BOOK, values).fetchone()
    return row[0]


def add_books(conn: psycopg.Connection, books: list[tuple[str, str, Decimal]]) -> list[int]:
    """Insert several (title, author, price) books in ONE transaction and return
    their ids in the same order. If any row is invalid (same rules as
    add_book, or rejected by the database), none of the books are stored and
    the error propagates. An empty list gives [].
    """
    ids = []
    with conn.transaction():
        for book in books:
            ids.append(conn.execute(INSERT_BOOK, _clean(*book)).fetchone()[0])
    return ids


def get_book(conn: psycopg.Connection, book_id: int) -> dict | None:
    """Return the book as a dict with the keys id, title, author, price
    (a Decimal), or None if there is no such id. Use dict_row."""
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT id, title, author, price FROM books WHERE id = %s", (book_id,))
        return cur.fetchone()


if __name__ == "__main__":
    import os

    dsn = os.environ.get(
        "PRACTICE_PG_DSN", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    with psycopg.connect(dsn, row_factory=dict_row) as connection:
        print("connected:", connection.execute("SELECT 1 AS ok").fetchone())
