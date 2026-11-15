"""Assignment 4: A page-hit counter with an upsert.

Every function takes an open psycopg connection first.
"""

import psycopg


def create_schema(conn: psycopg.Connection) -> None:
    """Create the table if it does not exist, then commit:

        page_hits(page TEXT PRIMARY KEY, hits INTEGER NOT NULL DEFAULT 0)

    Calling it twice must not fail.
    """
    # TODO: CREATE TABLE IF NOT EXISTS page_hits (...) and commit.
    ...


def hit(conn: psycopg.Connection, page: str, count: int = 1) -> int:
    """Add `count` to the hits of `page` and return the new total.

    A page seen for the first time starts at `count`. Use ONE statement:

        INSERT INTO page_hits (page, hits) VALUES (%s, %s)
        ON CONFLICT (page) DO UPDATE SET hits = page_hits.hits + EXCLUDED.hits
        RETURNING hits

    Commit afterwards. Raise ValueError (before any database work) if count is
    less than 1.
    """
    # TODO: run the upsert, fetch the returned hits, commit.
    ...


def get_hits(conn: psycopg.Connection, page: str) -> int:
    """Return the hits of `page`, or 0 for a page that was never counted."""
    # TODO: SELECT hits FROM page_hits WHERE page = %s
    ...


def top_pages(conn: psycopg.Connection, n: int = 3) -> list[tuple[str, int]]:
    """Return up to `n` (page, hits) pairs, most hits first, ties by page name."""
    # TODO: ORDER BY hits DESC, page LIMIT %s
    ...


def reset(conn: psycopg.Connection, page: str) -> bool:
    """Delete the counter of `page`. Return True if there was one, False if not.
    Commit afterwards."""
    # TODO: DELETE ... WHERE page = %s and look at cursor.rowcount.
    ...


if __name__ == "__main__":
    print("Run the tests: uv run pytest modules/22-postgresql/assignments/a4-upsert-counter")
