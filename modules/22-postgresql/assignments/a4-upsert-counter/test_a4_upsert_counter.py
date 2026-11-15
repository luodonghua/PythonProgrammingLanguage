import psycopg
import pytest
from psycopg import sql

from practice import load, pg_dsn

m = load(__file__)


@pytest.fixture
def db(pg):
    m.create_schema(pg)
    return pg


def test_create_schema_is_repeatable(pg):
    m.create_schema(pg)
    m.create_schema(pg)
    columns = pg.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema = current_schema() AND table_name = 'page_hits' ORDER BY ordinal_position"
    ).fetchall()
    assert columns == [("page",), ("hits",)]


def test_first_hit_and_next_hits(db):
    assert m.hit(db, "/home") == 1
    assert m.hit(db, "/home") == 2
    assert m.hit(db, "/about") == 1
    assert m.hit(db, "/home") == 3


def test_hit_with_count(db):
    assert m.hit(db, "/a", 5) == 5
    assert m.hit(db, "/a", 10) == 15


def test_hit_validates_count(db):
    assert m.hit(db, "/a") == 1
    for bad in (0, -3):
        with pytest.raises(ValueError):
            m.hit(db, "/a", bad)
    assert m.get_hits(db, "/a") == 1


def test_only_one_row_per_page(db):
    for _ in range(4):
        m.hit(db, "/x")
    assert db.execute("SELECT count(*) FROM page_hits").fetchone()[0] == 1


def test_get_hits(db):
    m.hit(db, "/a", 2)
    assert m.get_hits(db, "/a") == 2
    assert m.get_hits(db, "/never") == 0


def test_top_pages(db):
    for page, count in [("/a", 5), ("/b", 9), ("/c", 5), ("/d", 1)]:
        m.hit(db, page, count)
    assert m.top_pages(db) == [("/b", 9), ("/a", 5), ("/c", 5)]
    assert m.top_pages(db, 1) == [("/b", 9)]
    assert m.top_pages(db, 10) == [("/b", 9), ("/a", 5), ("/c", 5), ("/d", 1)]
    assert m.top_pages(db, 0) == []


def test_top_pages_empty(db):
    assert m.top_pages(db) == []
    m.hit(db, "/a")
    assert m.top_pages(db) == [("/a", 1)]


def test_reset(db):
    m.hit(db, "/a", 3)
    assert m.reset(db, "/a") is True
    assert m.reset(db, "/a") is False
    assert m.get_hits(db, "/a") == 0
    assert m.hit(db, "/a") == 1


def test_changes_are_committed(db):
    m.hit(db, "/a", 2)
    m.hit(db, "/b")
    m.reset(db, "/b")
    schema = db.execute("SELECT current_schema()").fetchone()[0]
    with psycopg.connect(pg_dsn()) as other:
        other.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema)))
        assert other.execute("SELECT page, hits FROM page_hits ORDER BY page").fetchall() == [("/a", 2)]


def test_page_text_is_a_value_not_sql(db):
    page = "/x'); DROP TABLE page_hits; --"
    assert m.hit(db, page) == 1
    assert m.hit(db, page) == 2
    assert m.get_hits(db, page) == 2
