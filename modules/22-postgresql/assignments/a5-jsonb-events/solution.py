"""Assignment 5: Store and query JSON documents with JSONB.

The tests create this table:

    events(id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
           kind TEXT NOT NULL,
           payload JSONB NOT NULL,
           created_at TIMESTAMPTZ NOT NULL DEFAULT now())

Every function takes an open psycopg connection first.
"""

import psycopg
from psycopg.types.json import Jsonb


def add_event(conn: psycopg.Connection, kind: str, payload: dict) -> int:
    """Insert an event and return its id (RETURNING id), then commit.

    Wrap the payload in Jsonb(...) so psycopg sends it as JSONB.
    """
    row = conn.execute(
        "INSERT INTO events (kind, payload) VALUES (%s, %s) RETURNING id",
        (kind, Jsonb(payload)),
    ).fetchone()
    conn.commit()
    return row[0]


def get_payload(conn: psycopg.Connection, event_id: int) -> dict | None:
    """Return the payload of an event as a Python dict, or None if the id is unknown."""
    row = conn.execute("SELECT payload FROM events WHERE id = %s", (event_id,)).fetchone()
    return None if row is None else row[0]


def events_containing(conn: psycopg.Connection, **fields) -> list[int]:
    """Return the ids (ascending) of the events whose payload contains all the
    given key/value pairs, using the JSONB containment operator @>.

    events_containing(conn, user="ann", ok=True) finds payloads such as
    {"user": "ann", "ok": true, "ms": 12}. No fields at all matches every event.
    """
    rows = conn.execute(
        "SELECT id FROM events WHERE payload @> %s ORDER BY id", (Jsonb(fields),)
    ).fetchall()
    return [row[0] for row in rows]


def field_text(conn: psycopg.Connection, event_id: int, key: str) -> str | None:
    """Return the value of a top-level payload key as text (the ->> operator),
    or None if the key or the event does not exist. Pass the key as a parameter:
    SELECT payload ->> %s FROM events WHERE id = %s
    """
    row = conn.execute(
        "SELECT payload ->> %s FROM events WHERE id = %s", (key, event_id)
    ).fetchone()
    return None if row is None else row[0]


def count_by_kind(conn: psycopg.Connection) -> dict[str, int]:
    """Return {kind: number_of_events}, with kinds in alphabetical order."""
    rows = conn.execute(
        "SELECT kind, count(*) FROM events GROUP BY kind ORDER BY kind"
    ).fetchall()
    return {kind: count for kind, count in rows}


def average_ms(conn: psycopg.Connection, kind: str) -> float | None:
    """Return the average of the numeric payload key "ms" over the events of
    this kind, as a float, or None if no such event has an "ms" value.

    Cast the text value: avg((payload ->> 'ms')::numeric). Events without "ms"
    are ignored by avg() automatically.
    """
    row = conn.execute(
        "SELECT avg((payload ->> 'ms')::numeric) FROM events WHERE kind = %s", (kind,)
    ).fetchone()
    return None if row[0] is None else float(row[0])


if __name__ == "__main__":
    print("Run the tests: uv run pytest modules/22-postgresql/assignments/a5-jsonb-events")
