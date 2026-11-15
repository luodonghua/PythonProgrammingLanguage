from decimal import Decimal

import psycopg
import pytest
from psycopg import sql

from practice import load, pg_dsn

m = load(__file__)


def committed_count(pg):
    """Count the rows another connection can see (so only committed rows)."""
    schema = pg.execute("SELECT current_schema()").fetchone()[0]
    with psycopg.connect(pg_dsn()) as other:
        other.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema)))
        return other.execute("SELECT count(*) FROM books").fetchone()[0]


@pytest.fixture
def db(pg):
    m.create_schema(pg)
    return pg


def test_create_schema_twice_and_columns(pg):
    m.create_schema(pg)
    m.create_schema(pg)
    rows = pg.execute(
        "SELECT column_name, data_type FROM information_schema.columns "
        "WHERE table_schema = current_schema() AND table_name = 'books' ORDER BY ordinal_position"
    ).fetchall()
    assert rows == [
        ("id", "integer"),
        ("title", "text"),
        ("author", "text"),
        ("price", "numeric"),
        ("added_at", "timestamp with time zone"),
    ]


def test_add_book_returns_id_and_commits(db):
    first = m.add_book(db, "Dune", "Frank Herbert", Decimal("9.99"))
    second = m.add_book(db, "Emma", "Jane Austen", Decimal("5.00"))
    assert first == 1
    assert second == 2
    assert committed_count(db) == 2


def test_add_book_strips_text(db):
    book_id = m.add_book(db, "  Dune ", " Frank Herbert  ", Decimal("9.99"))
    book = m.get_book(db, book_id)
    assert (book["title"], book["author"]) == ("Dune", "Frank Herbert")


@pytest.mark.parametrize(
    ("title", "author", "price"),
    [("", "A", Decimal("1")), ("T", "   ", Decimal("1")), ("T", "A", Decimal("-0.01"))],
)
def test_add_book_validation(db, title, author, price):
    assert m.add_book(db, "ok", "ok", Decimal("1")) == 1
    with pytest.raises(ValueError):
        m.add_book(db, title, author, price)
    assert committed_count(db) == 1


def test_get_book_shape(db):
    book_id = m.add_book(db, "Dune", "Frank Herbert", Decimal("9.99"))
    book = m.get_book(db, book_id)
    assert book == {"id": book_id, "title": "Dune", "author": "Frank Herbert", "price": Decimal("9.99")}
    assert isinstance(book["price"], Decimal)


def test_get_book_missing(db):
    book_id = m.add_book(db, "Dune", "Frank Herbert", Decimal("9.99"))
    assert m.get_book(db, book_id) is not None
    assert m.get_book(db, 12345) is None


def test_add_books_in_order(db):
    ids = m.add_books(
        db,
        [("A", "x", Decimal("1")), ("B", "y", Decimal("2")), ("C", "z", Decimal("3"))],
    )
    assert ids == sorted(ids)
    assert len(set(ids)) == 3
    assert [m.get_book(db, i)["title"] for i in ids] == ["A", "B", "C"]
    assert committed_count(db) == 3


def test_add_books_empty(db):
    assert m.add_books(db, []) == []
    assert m.add_book(db, "x", "y", Decimal("1")) >= 1


def test_add_books_is_all_or_nothing(db):
    m.add_book(db, "Keep", "me", Decimal("1"))
    with pytest.raises(ValueError):
        m.add_books(db, [("Good", "x", Decimal("1")), ("", "x", Decimal("1"))])
    assert committed_count(db) == 1


def test_add_books_database_error_rolls_back(db):
    # 10**8 does not fit NUMERIC(8, 2), so the database rejects the second row.
    with pytest.raises(psycopg.Error):
        m.add_books(db, [("Good", "x", Decimal("1")), ("Huge", "x", Decimal(10**8))])
    # The connection is still usable and nothing from the failed batch is stored.
    assert m.add_book(db, "After", "x", Decimal("1")) >= 1
    assert committed_count(db) == 1


def test_sql_injection_text_is_stored_literally(db):
    title = "x'); DROP TABLE books; --"
    book_id = m.add_book(db, title, "Mallory", Decimal("1"))
    assert m.get_book(db, book_id)["title"] == title
