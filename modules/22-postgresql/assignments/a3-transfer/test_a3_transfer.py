from decimal import Decimal

import psycopg
import pytest
from psycopg import sql

from practice import load, pg_dsn

m = load(__file__)

SCHEMA = """
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    owner TEXT NOT NULL,
    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0)
)
"""


def D(text):
    return Decimal(text)


@pytest.fixture
def db(pg):
    pg.execute(SCHEMA)
    pg.execute(
        "INSERT INTO accounts (id, owner, balance) VALUES (1, 'ann', 100.00), (2, 'bo', 50.00), (3, 'cy', 0)"
    )
    pg.commit()
    return pg


def balances(conn):
    return conn.execute("SELECT id, balance FROM accounts ORDER BY id").fetchall()


def test_get_balance(db):
    assert m.get_balance(db, 1) == D("100.00")
    assert isinstance(m.get_balance(db, 2), Decimal)


def test_get_balance_unknown(db):
    assert m.get_balance(db, 1) == D("100.00")
    with pytest.raises(LookupError):
        m.get_balance(db, 99)


def test_transfer_moves_money(db):
    m.transfer(db, 1, 2, D("30.25"))
    assert balances(db) == [(1, D("69.75")), (2, D("80.25")), (3, D("0"))]


def test_transfer_whole_balance(db):
    m.transfer(db, 1, 3, D("100.00"))
    assert m.get_balance(db, 1) == D("0")
    assert m.get_balance(db, 3) == D("100.00")


def test_transfer_is_committed(db):
    m.transfer(db, 1, 2, D("10"))
    schema = db.execute("SELECT current_schema()").fetchone()[0]
    with psycopg.connect(pg_dsn()) as other:
        other.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema)))
        assert other.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()[0] == D("60.00")


@pytest.mark.parametrize(
    ("src", "dst", "amount"),
    [(1, 2, "0"), (1, 2, "-5"), (1, 1, "10")],
)
def test_value_errors(db, src, dst, amount):
    m.transfer(db, 1, 2, D("1"))
    with pytest.raises(ValueError):
        m.transfer(db, src, dst, D(amount))
    assert balances(db) == [(1, D("99.00")), (2, D("51.00")), (3, D("0"))]


def test_insufficient_funds(db):
    with pytest.raises(m.InsufficientFunds):
        m.transfer(db, 2, 1, D("50.01"))
    assert balances(db) == [(1, D("100.00")), (2, D("50.00")), (3, D("0"))]


def test_unknown_source(db):
    with pytest.raises(LookupError):
        m.transfer(db, 99, 1, D("5"))
    assert balances(db) == [(1, D("100.00")), (2, D("50.00")), (3, D("0"))]


def test_unknown_target_undoes_the_withdrawal(db):
    with pytest.raises(LookupError):
        m.transfer(db, 1, 99, D("40"))
    assert balances(db) == [(1, D("100.00")), (2, D("50.00")), (3, D("0"))]


def test_connection_usable_after_failure(db):
    with pytest.raises(m.InsufficientFunds):
        m.transfer(db, 3, 1, D("1"))
    m.transfer(db, 1, 3, D("1"))
    assert m.get_balance(db, 3) == D("1.00")


def test_transfer_many(db):
    done = m.transfer_many(db, [(1, 2, D("10")), (2, 3, D("60")), (3, 1, D("5"))])
    assert done == 3
    assert balances(db) == [(1, D("95.00")), (2, D("0.00")), (3, D("55.00"))]


def test_transfer_many_all_or_nothing(db):
    with pytest.raises(m.InsufficientFunds):
        m.transfer_many(db, [(1, 2, D("10")), (3, 1, D("999"))])
    assert balances(db) == [(1, D("100.00")), (2, D("50.00")), (3, D("0"))]


def test_transfer_many_empty(db):
    assert m.transfer_many(db, []) == 0
    assert m.transfer_many(db, [(1, 2, D("1"))]) == 1
