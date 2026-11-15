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
    # TODO: INSERT INTO events (kind, payload) VALUES (%s, %s) RETURNING id
    ...


def get_payload(conn: psycopg.Connection, event_id: int) -> dict | None:
    """Return the payload of an event as a Python dict, or None if the id is unknown."""
    # TODO: SELECT payload ...; psycopg already converts JSONB to a dict.
    ...


def events_containing(conn: psycopg.Connection, **fields) -> list[int]:
    """Return the ids (ascending) of the events whose payload contains all the
    given key/value pairs, using the JSONB containment operator @>.

    events_containing(conn, user="ann", ok=True) finds payloads such as
    {"user": "ann", "ok": true, "ms": 12}. No fields at all matches every event.
    """
    # TODO: WHERE payload @> %s with Jsonb(fields).
    ...


def field_text(conn: psycopg.Connection, event_id: int, key: str) -> str | None:
    """Return the value of a top-level payload key as text (the ->> operator),
    or None if the key or the event does not exist. Pass the key as a parameter:
    SELECT payload ->> %s FROM events WHERE id = %s
    """
    # TODO: run the query and return the first column of the row, if any.
    ...


def count_by_kind(conn: psycopg.Connection) -> dict[str, int]:
    """Return {kind: number_of_events}, with kinds in alphabetical order."""
    # TODO: GROUP BY kind ORDER BY kind
    ...


def average_ms(conn: psycopg.Connection, kind: str) -> float | None:
    """Return the average of the numeric payload key "ms" over the events of
    this kind, as a float, or None if no such event has an "ms" value.

    Cast the text value: avg((payload ->> 'ms')::numeric). Events without "ms"
    are ignored by avg() automatically.
    """
    # TODO: SELECT avg(...) FROM events WHERE kind = %s; convert Decimal to float.
    ...


if __name__ == "__main__":
    print("Run the tests: uv run pytest modules/22-postgresql/assignments/a5-jsonb-events")
