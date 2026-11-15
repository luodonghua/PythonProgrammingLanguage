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
    # TODO: build a list of WHERE fragments and a list of params, then run one query.
    # Hints: ILIKE %s with the value "%" + escaped + "%"; escape \, % and _ in `text`
    # with a backslash; author = ANY(%s) with the Python list as the parameter.
    ...


def count_by_author(conn: psycopg.Connection) -> dict[str, int]:
    """Return {author: number_of_books}, with authors in alphabetical order."""
    # TODO: SELECT author, count(*) ... GROUP BY author ORDER BY author.
    ...


def cheapest(conn: psycopg.Connection) -> dict | None:
    """Return the cheapest book as a dict (same keys as search_books); on a
    price tie, the lowest title and then id. Return None if the table is empty."""
    # TODO: ORDER BY price, title, id LIMIT 1.
    ...


if __name__ == "__main__":
    print("Run the tests: uv run pytest modules/22-postgresql/assignments/a2-search-books")
