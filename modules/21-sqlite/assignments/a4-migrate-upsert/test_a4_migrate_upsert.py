import sqlite3

import pytest

from practice import load

m = load(__file__)


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    yield connection
    connection.close()


@pytest.fixture
def db(conn):
    m.migrate(conn)
    return conn


def columns(conn):
    return [row[1] for row in conn.execute("PRAGMA table_info(settings)")]


def test_new_database_is_version_zero(conn):
    assert m.get_version(conn) == 0


def test_migrate_new_database(conn):
    assert m.migrate(conn) == 3
    assert m.get_version(conn) == 3
    assert columns(conn) == ["key", "value", "updates"]


def test_migrate_twice_does_nothing(conn):
    m.migrate(conn)
    assert m.migrate(conn) == 0
    assert m.get_version(conn) == 3


def test_migrate_from_old_version_keeps_data(conn):
    # A database that only has step 1 and one row of data.
    conn.execute(m.MIGRATIONS[0])
    conn.execute("PRAGMA user_version = 1")
    conn.execute("INSERT INTO settings VALUES ('lang', 'en')")
    conn.commit()
    assert m.migrate(conn) == 2
    assert m.get_version(conn) == 3
    assert m.get_setting(conn, "lang") == "en"
    assert m.setting_updates(conn, "lang") == 0


def test_migrate_with_custom_list(conn):
    steps = ["CREATE TABLE a (x INTEGER)", "CREATE TABLE b (y INTEGER)"]
    assert m.migrate(conn, steps) == 2
    assert m.get_version(conn) == 2
    steps.append("CREATE TABLE c (z INTEGER)")
    assert m.migrate(conn, steps) == 1
    assert m.get_version(conn) == 3


def test_version_is_stored_in_the_file(tmp_path):
    path = tmp_path / "app.db"
    first = sqlite3.connect(path)
    assert m.migrate(first) == 3
    first.close()
    second = sqlite3.connect(path)
    try:
        assert m.get_version(second) == 3
        assert m.migrate(second) == 0
    finally:
        second.close()


def test_upsert_inserts_new_key(db):
    m.upsert_setting(db, "theme", "dark")
    assert m.get_setting(db, "theme") == "dark"
    assert m.setting_updates(db, "theme") == 0


def test_upsert_replaces_and_counts(db):
    m.upsert_setting(db, "theme", "dark")
    m.upsert_setting(db, "theme", "light")
    m.upsert_setting(db, "theme", "blue")
    assert m.get_setting(db, "theme") == "blue"
    assert m.setting_updates(db, "theme") == 2
    assert db.execute("SELECT COUNT(*) FROM settings").fetchone()[0] == 1


def test_upsert_keeps_other_keys(db):
    m.upsert_setting(db, "a", "1")
    m.upsert_setting(db, "b", "2")
    m.upsert_setting(db, "a", "3")
    assert (m.get_setting(db, "a"), m.get_setting(db, "b")) == ("3", "2")


def test_get_setting_default_and_unknown(db):
    m.upsert_setting(db, "a", "1")
    assert m.get_setting(db, "missing") is None
    assert m.get_setting(db, "missing", "fallback") == "fallback"
    assert m.setting_updates(db, "missing") is None


def test_upsert_is_committed(tmp_path):
    path = tmp_path / "s.db"
    first = sqlite3.connect(path)
    m.migrate(first)
    m.upsert_setting(first, "k", "v")
    first.close()
    second = sqlite3.connect(path)
    try:
        assert m.get_setting(second, "k") == "v"
    finally:
        second.close()


def test_quotes_are_safe(db):
    value = "it's \"fine\"; DROP TABLE settings;"
    m.upsert_setting(db, "k", value)
    assert m.get_setting(db, "k") == value
