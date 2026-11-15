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
    m.init_db(conn)
    return conn


def test_init_twice_is_fine(conn):
    m.init_db(conn)
    m.init_db(conn)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    assert ("todos",) in tables


def test_add_returns_ids(db):
    assert m.add_todo(db, "a") == 1
    assert m.add_todo(db, "b") == 2


def test_add_strips_and_validates(db):
    m.add_todo(db, "  buy milk  ")
    assert m.list_todos(db)[0]["title"] == "buy milk"
    for bad in ("", "   "):
        with pytest.raises(ValueError):
            m.add_todo(db, bad)
    assert len(m.list_todos(db)) == 1


def test_list_shape(db):
    m.add_todo(db, "x")
    assert m.list_todos(db) == [{"id": 1, "title": "x", "done": False}]
    assert m.list_todos(db)[0]["done"] is False


def test_complete_and_filter(db):
    a = m.add_todo(db, "a")
    b = m.add_todo(db, "b")
    assert m.complete(db, a) is True
    assert m.list_todos(db) == [
        {"id": a, "title": "a", "done": True},
        {"id": b, "title": "b", "done": False},
    ]
    assert m.list_todos(db, only_open=True) == [{"id": b, "title": "b", "done": False}]


def test_complete_unknown_id(db):
    m.add_todo(db, "a")
    assert m.complete(db, 999) is False


def test_delete_done(db):
    ids = [m.add_todo(db, name) for name in "abc"]
    m.complete(db, ids[0])
    m.complete(db, ids[2])
    assert m.delete_done(db) == 2
    assert [t["title"] for t in m.list_todos(db)] == ["b"]
    assert m.delete_done(db) == 0


def test_quotes_in_titles_are_safe(db):
    title = "Robert'); DROP TABLE todos;--"
    m.add_todo(db, title)
    assert m.list_todos(db)[0]["title"] == title


def test_data_is_committed_to_file(tmp_path):
    path = tmp_path / "todos.db"
    first = sqlite3.connect(path)
    m.init_db(first)
    m.add_todo(first, "persist me")
    m.complete(first, 1)
    first.close()
    second = sqlite3.connect(path)
    try:
        assert m.list_todos(second) == [{"id": 1, "title": "persist me", "done": True}]
    finally:
        second.close()


def test_works_with_row_factory(db):
    db.row_factory = sqlite3.Row
    m.add_todo(db, "r")
    assert m.list_todos(db) == [{"id": 1, "title": "r", "done": False}]
