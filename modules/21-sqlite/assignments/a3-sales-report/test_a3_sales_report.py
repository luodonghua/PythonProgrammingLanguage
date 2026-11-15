import sqlite3

import pytest

from practice import load

m = load(__file__)

SCHEMA = """
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    product TEXT NOT NULL,
    qty INTEGER NOT NULL,
    unit_price_cents INTEGER NOT NULL,
    ordered_on TEXT NOT NULL
)
"""

ROWS = [
    # id, customer, product, qty, unit price (cents), date
    (1, "Ann", "pen", 10, 150, "2025-01-15"),    # 1500
    (2, "Bo", "ink", 2, 1200, "2025-01-20"),     # 2400
    (3, "Ann", "ink", 1, 1200, "2025-02-03"),    # 1200
    (4, "Cy", "pen", 4, 150, "2025-02-10"),      # 600
    (5, "Bo", "cap", 1, 900, "2025-03-01"),      # 900
    (6, "Ann", "cap", 3, 900, "2025-03-05"),     # 2700
]


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    connection.execute(SCHEMA)
    connection.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", ROWS)
    connection.commit()
    yield connection
    connection.close()


@pytest.fixture
def empty():
    connection = sqlite3.connect(":memory:")
    connection.execute(SCHEMA)
    yield connection
    connection.close()


def test_revenue_by_customer(conn):
    assert m.revenue_by_customer(conn) == [("Ann", 5400), ("Bo", 3300), ("Cy", 600)]


def test_revenue_ties_sorted_by_name(empty):
    empty.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
        [(1, "Zed", "x", 1, 100, "2025-01-01"), (2, "Amy", "x", 1, 100, "2025-01-02")],
    )
    assert m.revenue_by_customer(empty) == [("Amy", 100), ("Zed", 100)]


def test_monthly_totals(conn):
    result = m.monthly_totals(conn)
    assert result == {"2025-01": 3900, "2025-02": 1800, "2025-03": 3600}
    assert list(result) == ["2025-01", "2025-02", "2025-03"]


def test_best_product(conn):
    assert m.best_product(conn) == "pen"  # 14 units; ink 3, cap 4


def test_best_product_tie_is_alphabetical(empty):
    empty.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
        [(1, "A", "zip", 3, 100, "2025-01-01"), (2, "A", "bar", 3, 100, "2025-01-02")],
    )
    assert m.best_product(empty) == "bar"


def test_best_product_empty(empty):
    assert m.best_product(empty) is None
    empty.execute("INSERT INTO orders VALUES (1, 'A', 'only', 1, 100, '2025-01-01')")
    assert m.best_product(empty) == "only"


@pytest.mark.parametrize(
    ("minimum", "ids"),
    [(0, [1, 2, 3, 4, 5, 6]), (1200, [1, 2, 3, 6]), (1500, [1, 2, 6]), (2700, [6]), (2701, [])],
)
def test_orders_above(conn, minimum, ids):
    assert m.orders_above(conn, minimum) == ids


def test_format_report(conn):
    assert m.format_report(conn) == "Ann: 54.00\nBo: 33.00\nCy: 6.00"


def test_format_report_empty(empty):
    assert m.format_report(empty) == "No orders"


def test_format_report_cents(empty):
    empty.execute("INSERT INTO orders VALUES (1, 'Ann', 'pen', 5, 251, '2025-01-01')")
    assert m.format_report(empty) == "Ann: 12.55"
