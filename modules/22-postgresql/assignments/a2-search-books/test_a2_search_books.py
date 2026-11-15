from decimal import Decimal

import pytest

from practice import load

m = load(__file__)

SCHEMA = """
CREATE TABLE books (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price NUMERIC(8, 2) NOT NULL
)
"""

BOOKS = [
    ("Dune", "Frank Herbert", "9.99"),
    ("Dune Messiah", "Frank Herbert", "7.50"),
    ("Emma", "Jane Austen", "5.00"),
    ("Persuasion", "Jane Austen", "6.25"),
    ("100% Wool", "Ann Knit", "12.00"),
    ("Snake_Case", "Ann Knit", "3.00"),
    ("Shakecase", "Ann Knit", "3.00"),
]


@pytest.fixture
def db(pg):
    pg.execute(SCHEMA)
    for title, author, price in BOOKS:
        pg.execute(
            "INSERT INTO books (title, author, price) VALUES (%s, %s, %s)",
            (title, author, Decimal(price)),
        )
    pg.commit()
    return pg


def titles(rows):
    return [row["title"] for row in rows]


def test_no_filters_returns_everything_ordered(db):
    rows = m.search_books(db)
    assert titles(rows) == [
        "100% Wool", "Dune", "Dune Messiah", "Emma", "Persuasion", "Shakecase", "Snake_Case",
    ]
    assert set(rows[0]) == {"id", "title", "author", "price"}
    assert isinstance(rows[0]["price"], Decimal)


def test_text_filter_ignores_case(db):
    assert titles(m.search_books(db, text="dUNe")) == ["Dune", "Dune Messiah"]
    assert titles(m.search_books(db, text="zzz")) == []


def test_percent_is_a_plain_character(db):
    assert titles(m.search_books(db, text="%")) == ["100% Wool"]
    assert titles(m.search_books(db, text="100%")) == ["100% Wool"]


def test_underscore_is_a_plain_character(db):
    assert titles(m.search_books(db, text="e_c")) == ["Snake_Case"]


def test_max_price(db):
    assert titles(m.search_books(db, max_price=Decimal("5.00"))) == ["Emma", "Shakecase", "Snake_Case"]


def test_authors_filter(db):
    assert titles(m.search_books(db, authors=["Jane Austen"])) == ["Emma", "Persuasion"]
    assert titles(m.search_books(db, authors=["Jane Austen", "Frank Herbert"])) == [
        "Dune", "Dune Messiah", "Emma", "Persuasion",
    ]
    assert m.search_books(db, authors=[]) == []


def test_filters_combine_with_and(db):
    rows = m.search_books(db, text="dune", max_price=Decimal("8"), authors=["Frank Herbert"])
    assert titles(rows) == ["Dune Messiah"]


def test_injection_text_matches_nothing_and_breaks_nothing(db):
    assert titles(m.search_books(db, text="Dune")) == ["Dune", "Dune Messiah"]
    assert m.search_books(db, text="'; DROP TABLE books; --") == []
    assert m.search_books(db, authors=["x' OR '1'='1"]) == []
    assert len(m.search_books(db)) == len(BOOKS)


def test_count_by_author(db):
    result = m.count_by_author(db)
    assert result == {"Ann Knit": 3, "Frank Herbert": 2, "Jane Austen": 2}
    assert list(result) == ["Ann Knit", "Frank Herbert", "Jane Austen"]


def test_cheapest_with_tie(db):
    book = m.cheapest(db)
    assert book["title"] == "Shakecase"
    assert book["price"] == Decimal("3.00")


def test_empty_table(pg):
    pg.execute(SCHEMA)
    pg.commit()
    assert m.search_books(pg) == []
    assert m.count_by_author(pg) == {}
    assert m.cheapest(pg) is None
