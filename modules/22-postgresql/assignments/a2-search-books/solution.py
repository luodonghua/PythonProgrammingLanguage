"""Assignment 2: Parameterized search.

The tests create this table and fill it:

    books(id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
          title TEXT NOT NULL, author TEXT NOT NULL, price NUMERIC(8, 2) NOT NULL)

Every function takes an open psycopg connection first. Build the SQL text only
from fixed pieces that you write yourself, and pass every value as a %s
parameter, so user input can never change the meaning of the query.
"""

from decimal import Decimal

import psycopg
from psycopg.rows import dict_row

COLUMNS = "id, title, author, price"


def _escape_like(text: str) -> str:
    """Make `text` safe to use inside a LIKE pattern (backslash is the escape)."""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search_books(
    conn: psycopg.Connection,
    text: str | None = None,
    max_price: Decimal | None = None,
    authors: list[str] | None = None,
) -> list[dict]:
    """Return the matching books as dicts with the keys id, title, author and
    price, ordered by title and then id.

    Each filter that is not None must match (they combine with AND):
    - text: the title contains `text`, ignoring case. The characters % and _
      in `text` are plain characters, not wildcards.
    - max_price: price <= max_price.
    - authors: the author is one of these names (an empty list matches nothing).

    With no filters return every book.
    """
    conditions: list[str] = []
    params: list = []
    if text is not None:
        conditions.append("title ILIKE %s")
        params.append(f"%{_escape_like(text)}%")
    if max_price is not None:
        conditions.append("price <= %s")
        params.append(max_price)
    if authors is not None:
        conditions.append("author = ANY(%s)")
        params.append(authors)
    where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    query = f"SELECT {COLUMNS} FROM books{where} ORDER BY title, id"
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, params)
        return cur.fetchall()


def count_by_author(conn: psycopg.Connection) -> dict[str, int]:
    """Return {author: number_of_books}, with authors in alphabetical order."""
    rows = conn.execute(
        "SELECT author, count(*) FROM books GROUP BY author ORDER BY author"
    ).fetchall()
    return {author: count for author, count in rows}


def cheapest(conn: psycopg.Connection) -> dict | None:
    """Return the cheapest book as a dict (same keys as search_books); on a
    price tie, the lowest title and then id. Return None if the table is empty."""
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(f"SELECT {COLUMNS} FROM books ORDER BY price, title, id LIMIT 1")
        return cur.fetchone()


if __name__ == "__main__":
    print("Run the tests: uv run pytest modules/22-postgresql/assignments/a2-search-books")
