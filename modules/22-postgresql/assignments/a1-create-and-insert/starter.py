"""Assignment 1: Create a table and insert rows with RETURNING.

Every function takes an open psycopg connection `conn` as its first argument.
The connection does not autocommit, so commit your work (conn.commit() or
`with conn.transaction():`). Pass values with %s placeholders.
"""

from decimal import Decimal

import psycopg
from psycopg.rows import dict_row


def create_schema(conn: psycopg.Connection) -> None:
    """Create the table `books` if it does not exist, then commit:

        id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
        title     TEXT NOT NULL
        author    TEXT NOT NULL
        price     NUMERIC(8, 2) NOT NULL CHECK (price >= 0)
        added_at  TIMESTAMPTZ NOT NULL DEFAULT now()

    Calling it twice must not fail (CREATE TABLE IF NOT EXISTS).
    """
    # TODO: conn.execute("CREATE TABLE IF NOT EXISTS books (...)") and commit.
    ...


def add_book(conn: psycopg.Connection, title: str, author: str, price: Decimal) -> int:
    """Insert one book and return its new id (use RETURNING id), then commit.

    Strip spaces from the title and the author. Raise ValueError (before
    touching the database) if the title or the author is empty after
    stripping, or if the price is negative.
    """
    # TODO: validate, INSERT ... VALUES (%s, %s, %s) RETURNING id, fetchone()[0].
    ...


def add_books(conn: psycopg.Connection, books: list[tuple[str, str, Decimal]]) -> list[int]:
    """Insert several (title, author, price) books in ONE transaction and return
    their ids in the same order. If any row is invalid (same rules as
    add_book, or rejected by the database), none of the books are stored and
    the error propagates. An empty list gives [].
    """
    # TODO: with conn.transaction(): loop over the books, collecting ids.
    ...


def get_book(conn: psycopg.Connection, book_id: int) -> dict | None:
    """Return the book as a dict with the keys id, title, author, price
    (a Decimal), or None if there is no such id. Use dict_row."""
    # TODO: conn.cursor(row_factory=dict_row) and SELECT id, title, author, price.
    ...


if __name__ == "__main__":
    import os

    dsn = os.environ.get(
        "PRACTICE_PG_DSN", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    with psycopg.connect(dsn, row_factory=dict_row) as connection:
        print("connected:", connection.execute("SELECT 1 AS ok").fetchone())
