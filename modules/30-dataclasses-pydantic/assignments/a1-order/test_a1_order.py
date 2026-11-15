import dataclasses

import pytest

from practice import load

m = load(__file__)


def test_line_item_defaults_and_total():
    item = m.LineItem("pen", 150)
    assert item.quantity == 1
    assert item.total_cents == 150
    assert m.LineItem("pen", 150, 4).total_cents == 600


def test_line_item_is_dataclass_frozen_and_comparable():
    assert dataclasses.is_dataclass(m.LineItem)
    item = m.LineItem("pen", 150, 2)
    assert item == m.LineItem("pen", 150, 2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        item.quantity = 5


@pytest.mark.parametrize(("cents", "qty"), [(-1, 1), (100, 0), (100, -3)])
def test_line_item_validation(cents, qty):
    with pytest.raises(ValueError):
        m.LineItem("x", cents, qty)


def test_zero_price_is_allowed():
    assert m.LineItem("gift", 0).total_cents == 0


def test_order_totals():
    order = m.Order("ann", [m.LineItem("pen", 150, 4), m.LineItem("book", 1000)])
    assert order.subtotal_cents == 1600
    assert order.total_cents == 1600


def test_order_discount_uses_integer_arithmetic():
    order = m.Order("ann", [m.LineItem("pen", 150, 4)], discount_percent=10)
    assert order.subtotal_cents == 600
    assert order.total_cents == 540
    odd = m.Order("bob", [m.LineItem("x", 999)], discount_percent=33)
    assert odd.total_cents == 669  # 999 * 67 // 100


def test_empty_order_and_separate_default_lists():
    a, b = m.Order("a"), m.Order("b")
    assert a.total_cents == 0
    a.items.append(m.LineItem("x", 5))
    assert b.items == []


@pytest.mark.parametrize("percent", [-1, 101])
def test_order_discount_validation(percent):
    with pytest.raises(ValueError):
        m.Order("ann", discount_percent=percent)


def test_discount_limits_allowed():
    assert m.Order("a", [m.LineItem("x", 100)], discount_percent=100).total_cents == 0
    assert m.Order("a", [m.LineItem("x", 100)], discount_percent=0).total_cents == 100


def test_with_item_returns_new_order():
    original = m.Order("ann", [m.LineItem("pen", 100)], discount_percent=50)
    bigger = original.with_item(m.LineItem("book", 300))
    assert bigger is not original
    assert len(original.items) == 1
    assert [i.name for i in bigger.items] == ["pen", "book"]
    assert bigger.customer == "ann"
    assert bigger.discount_percent == 50
    assert bigger.total_cents == 200


def test_to_dict():
    order = m.Order("ann", [m.LineItem("pen", 150, 2)], discount_percent=5)
    assert order.to_dict() == {
        "customer": "ann",
        "items": [{"name": "pen", "unit_cents": 150, "quantity": 2}],
        "discount_percent": 5,
    }
