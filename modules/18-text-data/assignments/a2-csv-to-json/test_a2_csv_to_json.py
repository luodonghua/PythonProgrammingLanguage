import json
from pathlib import Path

import pytest

from practice import load

m = load(__file__)
INVENTORY = Path(__file__).parent / "inventory.csv"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("120", 120),
        ("-5", -5),
        ("1.5", 1.5),
        ("12", 12),
        ("Pen", "Pen"),
        ("12abc", "12abc"),
        (" x ", " x "),
    ],
)
def test_convert_value(text, expected):
    result = m.convert_value(text)
    assert result == expected
    assert type(result) is type(expected)


def test_convert_empty_is_none():
    assert m.convert_value("7") == 7
    assert m.convert_value("") is None


def test_csv_to_json(tmp_path):
    out = tmp_path / "out.json"
    count = m.csv_to_json(INVENTORY, out)
    assert count == 3
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data[0] == {"sku": "A1", "name": "Pen", "qty": 120, "price": 1.5, "note": None}
    assert data[1]["name"] == "Notebook, A5"
    assert data[1]["note"] == "fragile"
    assert data[2]["price"] == 12
    assert isinstance(data[2]["price"], int)


def test_output_is_indented(tmp_path):
    out = tmp_path / "out.json"
    m.csv_to_json(INVENTORY, out)
    assert out.read_text(encoding="utf-8").startswith("[\n  {\n")


def test_header_only(tmp_path):
    src = tmp_path / "h.csv"
    src.write_text("a,b\n", encoding="utf-8")
    out = tmp_path / "h.json"
    assert m.csv_to_json(src, out) == 0
    assert json.loads(out.read_text(encoding="utf-8")) == []
