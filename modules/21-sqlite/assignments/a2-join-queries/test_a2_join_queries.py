import sqlite3

import pytest

from practice import load

m = load(__file__)

SCHEMA = """
CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id),
    year INTEGER NOT NULL
);
"""

AUTHORS = ["Ann Lee", "Bo Chen", "Cy Park", "Di Ruiz"]
BOOKS = [
    ("Tides", 1, 2001),
    ("Anchors", 1, 1999),
    ("Zephyr", 2, 2010),
    ("Moss", 2, 2010),
    ("Lanterns", 3, 2020),
]


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA)
    connection.executemany("INSERT INTO authors (name) VALUES (?)", [(n,) for n in AUTHORS])
    connection.executemany("INSERT INTO books (title, author_id, year) VALUES (?, ?, ?)", BOOKS)
    connection.commit()
    yield connection
    connection.close()


def test_books_with_authors(conn):
    assert m.books_with_authors(conn) == [
        ("Anchors", "Ann Lee"),
        ("Lanterns", "Cy Park"),
        ("Moss", "Bo Chen"),
        ("Tides", "Ann Lee"),
        ("Zephyr", "Bo Chen"),
    ]


def test_books_by_author(conn):
    assert m.books_by_author(conn, "Ann Lee") == ["Anchors", "Tides"]
    assert m.books_by_author(conn, "Bo Chen") == ["Moss", "Zephyr"]  # same year: by title
    assert m.books_by_author(conn, "Di Ruiz") == []
    assert m.books_by_author(conn, "Nobody") == []


def test_books_by_author_is_safe_against_injection(conn):
    assert m.books_by_author(conn, "Ann Lee")  # sanity: the function works at all
    assert m.books_by_author(conn, "x' OR '1'='1") == []


def test_book_counts_includes_authors_without_books(conn):
    assert m.book_counts(conn) == [
        ("Ann Lee", 2),
        ("Bo Chen", 2),
        ("Cy Park", 1),
        ("Di Ruiz", 0),
    ]


def test_authors_without_books(conn):
    assert m.authors_without_books(conn) == ["Di Ruiz"]
    conn.execute("INSERT INTO authors (name) VALUES ('Al Zed')")
    assert m.authors_without_books(conn) == ["Al Zed", "Di Ruiz"]


def test_empty_database():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA)
    assert m.books_with_authors(connection) == []
    assert m.book_counts(connection) == []
    assert m.authors_without_books(connection) == []
    connection.close()
