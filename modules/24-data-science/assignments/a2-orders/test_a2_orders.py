import pandas as pd
import pytest

from practice import load

m = load(__file__)


@pytest.fixture
def orders():
    return pd.read_csv(m.DATA)


def test_add_total_adds_column(orders):
    result = m.add_total(orders)
    assert result["total"].round(2).tolist() == [25.0, 59.99, 29.99, 33.0, 15.0, 29.97, 19.98, 39.0]


def test_add_total_does_not_change_input(orders):
    result = m.add_total(orders)
    assert "total" in result.columns
    assert "total" not in orders.columns


def test_revenue_by_category(orders):
    result = m.revenue_by_category(orders)
    assert isinstance(result, dict)
    assert result == {"Games": 128.98, "Books": 73.0, "Music": 49.95}


def test_revenue_by_category_order_is_largest_first(orders):
    assert list(m.revenue_by_category(orders)) == ["Games", "Books", "Music"]


def test_customer_summary(orders):
    result = m.customer_summary(orders)
    assert result.columns.tolist() == ["customer", "orders", "total_spent"]
    assert result["customer"].tolist() == ["Ben", "Ana", "Cleo", "Dev"]
    assert result["orders"].tolist() == [2, 3, 2, 1]
    assert result["total_spent"].tolist() == [74.99, 74.97, 62.97, 39.0]
    assert result.index.tolist() == [0, 1, 2, 3]


def test_customer_summary_breaks_ties_by_name():
    df = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "customer": ["Zed", "Amy", "Bob"],
            "category": ["x", "x", "x"],
            "quantity": [1, 1, 2],
            "unit_price": [10.0, 10.0, 5.0],
        }
    )
    assert m.customer_summary(df)["customer"].tolist() == ["Amy", "Bob", "Zed"]
