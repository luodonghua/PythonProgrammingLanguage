from datetime import date
from decimal import Decimal

import pytest

from practice import load

m = load(__file__)


def row(**overrides):
    base = {"date": "2024-03-01", "category": "Food", "description": "Lunch", "amount": "12.50"}
    base.update(overrides)
    return base


def test_parse_row_good():
    expense = m.parse_row(row())
    assert expense == m.Expense(date(2024, 3, 1), "food", "Lunch", Decimal("12.50"))


def test_parse_row_normalises_text():
    expense = m.parse_row(row(category="  Fun ", description="  Cinema  ", amount=" 15 "))
    assert expense.category == "fun"
    assert expense.description == "Cinema"
    assert expense.amount == Decimal("15")


def test_parse_row_empty_description_is_fine():
    assert m.parse_row(row(description="")).description == ""


def test_amount_is_decimal_not_float():
    amount = m.parse_row(row(amount="0.10")).amount
    assert isinstance(amount, Decimal)
    assert amount + Decimal("0.20") == Decimal("0.30")


@pytest.mark.parametrize(
    "bad",
    [
        {"date": "2024-02-30"},
        {"date": "03/01/2024"},
        {"date": ""},
        {"category": ""},
        {"category": "   "},
        {"amount": "abc"},
        {"amount": ""},
        {"amount": "0"},
        {"amount": "-5.00"},
        {"amount": "3.999"},
        {"amount": "NaN"},
        {"amount": "Infinity"},
        {"amount": None},
        {"category": None},
    ],
)
def test_parse_row_rejects_bad_values(bad):
    with pytest.raises(ValueError):
        m.parse_row(row(**bad))


def test_parse_expenses_sample_file():
    expenses, errors = m.parse_expenses()
    assert [e.description for e in expenses] == ["Groceries", "Bus pass", "Lunch", "Cinema", "March rent"]
    assert [e.category for e in expenses] == ["food", "transport", "food", "fun", "rent"]
    assert sum(e.amount for e in expenses) == Decimal("752.75")
    assert len(errors) == 5


def test_error_messages_have_line_numbers():
    _, errors = m.parse_expenses()
    assert [e.split(":")[0] for e in errors] == ["line 6", "line 7", "line 8", "line 9", "line 10"]
    assert all(len(e.split(":", 1)[1].strip()) > 0 for e in errors)


def test_short_row_and_blank_line(tmp_path):
    path = tmp_path / "x.csv"
    path.write_text(
        "date,category,description,amount\n"
        "2024-01-01,food,ok,1.00\n"
        "\n"
        "2024-01-02,food\n"
        "2024-01-03,rent,flat,500\n",
        encoding="utf-8",
    )
    expenses, errors = m.parse_expenses(path)
    assert [e.description for e in expenses] == ["ok", "flat"]
    assert len(errors) == 1 and errors[0].startswith("line 4:")


def test_header_only_file(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("date,category,description,amount\n", encoding="utf-8")
    assert m.parse_expenses(path) == ([], [])


def test_unicode_description(tmp_path):
    path = tmp_path / "u.csv"
    path.write_text("date,category,description,amount\n2024-01-01,food,Café,3.50\n", encoding="utf-8")
    expenses, _ = m.parse_expenses(path)
    assert expenses[0].description == "Café"
