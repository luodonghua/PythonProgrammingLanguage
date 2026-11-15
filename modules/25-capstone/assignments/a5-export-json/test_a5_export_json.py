import json
from datetime import date
from decimal import Decimal

import pytest

from practice import load

m = load(__file__)


def exp(day, category, description, amount):
    return m.Expense(date.fromisoformat(day), category, description, Decimal(amount))


SAMPLE = [
    exp("2024-03-05", "food", "Café", "12.25"),
    exp("2024-03-01", "food", "Groceries", "45.5"),
    exp("2024-04-02", "fun", "Cinema", "15"),
    exp("2024-03-01", "transport", "Bus", "30.00"),
]


def test_export_structure(tmp_path):
    target = tmp_path / "out.json"
    m.export_json(SAMPLE, target)
    data = json.loads(target.read_text(encoding="utf-8"))
    assert list(data) == ["count", "total", "expenses"]
    assert data["count"] == 4
    assert data["total"] == "102.75"
    assert data["expenses"][0] == {
        "date": "2024-03-01",
        "category": "food",
        "description": "Groceries",
        "amount": "45.50",
    }


def test_export_sorts_by_date_and_is_stable(tmp_path):
    target = tmp_path / "out.json"
    m.export_json(SAMPLE, target)
    items = json.loads(target.read_text(encoding="utf-8"))["expenses"]
    assert [i["description"] for i in items] == ["Groceries", "Bus", "Café", "Cinema"]


def test_export_file_format(tmp_path):
    target = tmp_path / "out.json"
    m.export_json(SAMPLE[:1], target)
    text = target.read_text(encoding="utf-8")
    assert text.endswith("}\n")
    assert '\n  "count": 1,' in text  # indent=2
    assert "Café" in text  # not escaped as \u00e9


def test_export_empty_list(tmp_path):
    target = tmp_path / "out.json"
    m.export_json([], target)
    assert json.loads(target.read_text(encoding="utf-8")) == {"count": 0, "total": "0.00", "expenses": []}


def test_round_trip(tmp_path):
    target = tmp_path / "out.json"
    m.export_json(SAMPLE, target)
    loaded = m.import_json(target)
    assert loaded == sorted(SAMPLE, key=lambda e: e.date)
    assert all(isinstance(e.amount, Decimal) and isinstance(e.date, date) for e in loaded)


def write(tmp_path, content):
    path = tmp_path / "in.json"
    path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
    return path


GOOD_ITEM = {"date": "2024-03-01", "category": "food", "description": "x", "amount": "1.00"}


@pytest.mark.parametrize(
    "content",
    [
        "not json",
        "[]",
        {"count": 0},
        {"expenses": "nope"},
        {"expenses": [5]},
        {"expenses": [{"date": "2024-03-01", "category": "food", "description": "x"}]},
        {"expenses": [{**GOOD_ITEM, "date": "2024-02-30"}]},
        {"expenses": [{**GOOD_ITEM, "amount": "abc"}]},
        {"expenses": [{**GOOD_ITEM, "amount": None}]},
        {"expenses": [{**GOOD_ITEM, "date": 20240301}]},
        {"count": 2, "expenses": [GOOD_ITEM]},
    ],
)
def test_import_rejects_bad_documents(tmp_path, content):
    with pytest.raises(ValueError):
        m.import_json(write(tmp_path, content))


def test_import_without_count_is_fine(tmp_path):
    assert len(m.import_json(write(tmp_path, {"expenses": [GOOD_ITEM]}))) == 1


def test_monthly_totals():
    assert m.monthly_totals(SAMPLE) == {"2024-03": "87.75", "2024-04": "15.00"}
    assert list(m.monthly_totals(reversed(list(SAMPLE)))) == ["2024-03", "2024-04"]
    assert m.monthly_totals([]) == {}
