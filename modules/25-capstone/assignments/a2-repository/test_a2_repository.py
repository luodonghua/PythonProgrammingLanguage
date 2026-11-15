import sqlite3
from datetime import date
from decimal import Decimal

import pytest

from practice import load

m = load(__file__)


def exp(day, category, description, amount):
    return m.Expense(date.fromisoformat(day), category, description, Decimal(amount))


SAMPLE = [
    exp("2024-03-05", "food", "Lunch", "12.25"),
    exp("2024-03-01", "food", "Groceries", "45.50"),
    exp("2024-03-03", "transport", "Bus pass", "30.00"),
    exp("2024-04-02", "fun", "Cinema", "15.00"),
    exp("2024-03-03", "fun", "Game", "30.00"),
]


@pytest.fixture
def repo():
    repository = m.ExpenseRepository()
    for item in SAMPLE:
        repository.add(item)
    yield repository
    repository.close()


def test_add_returns_increasing_ids():
    repo = m.ExpenseRepository()
    first = repo.add(SAMPLE[0])
    second = repo.add(SAMPLE[1])
    assert (first, second) == (1, 2)
    repo.close()


def test_list_is_ordered_by_date_then_insertion(repo):
    descriptions = [e.description for e in repo.list_expenses()]
    assert descriptions == ["Groceries", "Bus pass", "Game", "Lunch", "Cinema"]


def test_list_returns_expense_objects(repo):
    first = repo.list_expenses()[0]
    assert first == exp("2024-03-01", "food", "Groceries", "45.50")
    assert isinstance(first.amount, Decimal)
    assert isinstance(first.date, date)
    assert str(first.amount) == "45.50"


def test_list_by_month(repo):
    assert [e.description for e in repo.list_expenses("2024-04")] == ["Cinema"]
    assert len(repo.list_expenses("2024-03")) == 4
    assert repo.list_expenses("2023-12") == []


def test_totals_by_category(repo):
    totals = repo.totals_by_category()
    assert totals == {
        "food": Decimal("57.75"),
        "fun": Decimal("45.00"),
        "transport": Decimal("30.00"),
    }
    assert list(totals) == ["food", "fun", "transport"]
    assert str(totals["fun"]) == "45.00"


def test_totals_by_category_for_month(repo):
    totals = repo.totals_by_category("2024-03")
    assert totals == {"food": Decimal("57.75"), "transport": Decimal("30.00"), "fun": Decimal("30.00")}
    assert list(totals) == ["food", "fun", "transport"]  # tie broken A-Z


def test_totals_empty_month(repo):
    assert repo.totals_by_category("1999-01") == {}


def test_no_float_rounding_errors():
    repo = m.ExpenseRepository()
    for _ in range(10):
        repo.add(exp("2024-01-01", "x", "dime", "0.10"))
    assert repo.totals_by_category() == {"x": Decimal("1.00")}
    repo.close()


def test_amount_is_stored_as_integer_cents(tmp_path):
    path = tmp_path / "e.db"
    repo = m.ExpenseRepository(str(path))
    repo.add(exp("2024-01-01", "food", "x", "12.34"))
    repo.close()
    raw = sqlite3.connect(path)
    stored = [row[0] for row in raw.execute("SELECT cents FROM expenses")]
    raw.close()
    assert stored == [1234]


def test_data_survives_reopening(tmp_path):
    path = str(tmp_path / "e.db")
    first = m.ExpenseRepository(path)
    first.add(SAMPLE[0])
    first.close()
    second = m.ExpenseRepository(path)
    assert second.list_expenses() == [SAMPLE[0]]
    second.close()


def test_sql_injection_text_is_stored_as_text(repo):
    nasty = exp("2024-05-01", "food", "x'); DROP TABLE expenses; --", "1.00")
    repo.add(nasty)
    assert nasty in repo.list_expenses("2024-05")
    assert len(repo.list_expenses()) == 6
