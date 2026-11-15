from pathlib import Path

import pytest

from practice import load

m = load(__file__)
SALES = Path(__file__).parent / "sales.csv"


def test_sum_qty():
    assert m.sum_column(SALES, "qty") == 16.0


def test_sum_price():
    assert m.sum_column(SALES, "price") == pytest.approx(19.15)


def test_unknown_column():
    with pytest.raises(KeyError):
        m.sum_column(SALES, "weight")


def test_header_only_file(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("a,b\n", encoding="utf-8")
    assert m.sum_column(p, "a") == 0.0


def test_completely_empty_file(tmp_path):
    p = tmp_path / "nothing.csv"
    p.write_text("", encoding="utf-8")
    assert m.sum_column(p, "a") == 0.0


def test_revenue():
    assert m.revenue(SALES) == pytest.approx(3 * 1.5 + 2 * 4.25 + 12.0 + 10 * 1.4)


def test_quoted_comma_row_is_one_row(tmp_path):
    p = tmp_path / "q.csv"
    p.write_text('name,n\n"a, b",5\n"c, d",7\n', encoding="utf-8")
    assert m.sum_column(p, "n") == 12.0
