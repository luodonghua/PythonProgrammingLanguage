from decimal import Decimal

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("value", "expected"),
    [("2.675", "2.68"), ("10", "10.00"), (3, "3.00"), ("0.004", "0.00"), ("0.005", "0.01")],
)
def test_to_money(value, expected):
    result = m.to_money(value)
    assert isinstance(result, Decimal)
    assert str(result) == expected


@pytest.mark.parametrize(
    ("bill", "tip", "expected"),
    [
        ("80.00", "15", "92.00"),
        ("19.99", "10", "21.99"),
        ("50", "0", "50.00"),
        ("33.33", "18", "39.33"),
    ],
)
def test_add_tip(bill, tip, expected):
    assert str(m.add_tip(bill, tip)) == expected


def test_split_even():
    assert [str(s) for s in m.split_bill("10.00", 4)] == ["2.50"] * 4


def test_split_with_leftover():
    shares = m.split_bill("100.00", 3)
    assert [str(s) for s in shares] == ["33.34", "33.33", "33.33"]


def test_split_less_than_a_cent_each():
    assert [str(s) for s in m.split_bill("0.02", 3)] == ["0.01", "0.01", "0.00"]


@pytest.mark.parametrize(("total", "people"), [("99.99", 7), ("1234.56", 5), ("0.01", 2)])
def test_shares_add_up(total, people):
    shares = m.split_bill(total, people)
    assert len(shares) == people
    assert sum(shares) == Decimal(total)
    assert max(shares) - min(shares) <= Decimal("0.01")


def test_one_person():
    assert m.split_bill("12.34", 1) == [Decimal("12.34")]


def test_zero_people():
    with pytest.raises(ValueError):
        m.split_bill("10.00", 0)
