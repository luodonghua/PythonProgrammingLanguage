"""Shared pytest fixtures."""

import os
import uuid

import pytest

from practice import pg_dsn


@pytest.fixture
def pg():
    """A psycopg connection whose search_path is a fresh, temporary schema.

    The test is skipped (not failed) when PostgreSQL is not running, unless
    PRACTICE_REQUIRE_PG=1 (set in CI). Start a server with:
        docker compose up -d
    """
    psycopg = pytest.importorskip("psycopg")
    try:
        conn = psycopg.connect(pg_dsn(), connect_timeout=3)
    except psycopg.OperationalError as exc:
        if os.environ.get("PRACTICE_REQUIRE_PG") == "1":
            raise
        pytest.skip(f"PostgreSQL is not available ({exc}). Run: docker compose up -d")
    schema = f"practice_{uuid.uuid4().hex[:10]}"
    conn.execute(f"CREATE SCHEMA {schema}")
    conn.execute(f"SET search_path TO {schema}")
    conn.commit()
    try:
        yield conn
    finally:
        conn.rollback()
        conn.execute(f"DROP SCHEMA {schema} CASCADE")
        conn.commit()
        conn.close()
