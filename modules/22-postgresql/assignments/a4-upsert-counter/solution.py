"""Assignment 4: A page-hit counter with an upsert.

Every function takes an open psycopg connection first.
"""

import psycopg


def create_schema(conn: psycopg.Connection) -> None:
    """Create the table if it does not exist, then commit:

        page_hits(page TEXT PRIMARY KEY, hits INTEGER NOT NULL DEFAULT 0)

    Calling it twice must not fail.
    """
    conn.execute(
        "CREATE TABLE IF NOT EXISTS page_hits "
        "(page TEXT PRIMARY KEY, hits INTEGER NOT NULL DEFAULT 0)"
    )
    conn.commit()


def hit(conn: psycopg.Connection, page: str, count: int = 1) -> int:
    """Add `count` to the hits of `page` and return the new total.

    A page seen for the first time starts at `count`. Use ONE statement:

        INSERT INTO page_hits (page, hits) VALUES (%s, %s)
        ON CONFLICT (page) DO UPDATE SET hits = page_hits.hits + EXCLUDED.hits
        RETURNING hits

    Commit afterwards. Raise ValueError (before any database work) if count is
    less than 1.
    """
    if count < 1:
        raise ValueError("count must be at least 1")
    row = conn.execute(
        """
        INSERT INTO page_hits (page, hits) VALUES (%s, %s)
        ON CONFLICT (page) DO UPDATE SET hits = page_hits.hits + EXCLUDED.hits
        RETURNING hits
        """,
        (page, count),
    ).fetchone()
    conn.commit()
    return row[0]


def get_hits(conn: psycopg.Connection, page: str) -> int:
    """Return the hits of `page`, or 0 for a page that was never counted."""
    row = conn.execute("SELECT hits FROM page_hits WHERE page = %s", (page,)).fetchone()
    return 0 if row is None else row[0]


def top_pages(conn: psycopg.Connection, n: int = 3) -> list[tuple[str, int]]:
    """Return up to `n` (page, hits) pairs, most hits first, ties by page name."""
    rows = conn.execute(
        "SELECT page, hits FROM page_hits ORDER BY hits DESC, page LIMIT %s", (n,)
    ).fetchall()
    return [(page, hits) for page, hits in rows]


def reset(conn: psycopg.Connection, page: str) -> bool:
    """Delete the counter of `page`. Return True if there was one, False if not.
    Commit afterwards."""
    cursor = conn.execute("DELETE FROM page_hits WHERE page = %s", (page,))
    conn.commit()
    return cursor.rowcount == 1


if __name__ == "__main__":
    print("Run the tests: uv run pytest modules/22-postgresql/assignments/a4-upsert-counter")
