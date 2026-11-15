from datetime import date
from decimal import Decimal

from practice import load

m = load(__file__)


def exp(day, category, amount, description="x"):
    return m.Expense(date.fromisoformat(day), category, description, Decimal(amount))


SAMPLE = [
    exp("2024-03-01", "food", "45.50"),
    exp("2024-03-05", "food", "12.25"),
    exp("2024-03-03", "transport", "30.00"),
    exp("2024-04-01", "fun", "99.00"),
    exp("2024-02-28", "rent", "650.00"),
]

EXPECTED_MARCH = "\n".join(
    [
        "Expenses for 2024-03",
        "Category     Count       Total",
        "------------------------------",
        "food             2       57.75",
        "transport        1       30.00",
        "------------------------------",
        "TOTAL            3       87.75",
    ]
)


def test_full_report_text():
    assert m.format_report(SAMPLE, "2024-03") == EXPECTED_MARCH


def test_report_has_no_trailing_newline_and_fixed_width():
    text = m.format_report(SAMPLE, "2024-03")
    assert not text.endswith("\n")
    assert all(len(line) == 30 for line in text.split("\n")[1:])


def test_other_months_are_ignored():
    text = m.format_report(SAMPLE, "2024-04")
    assert "fun" in text and "food" not in text
    assert text.split("\n")[-1] == "TOTAL            1       99.00"


def test_empty_month_message():
    assert m.format_report(SAMPLE, "2023-01") == "No expenses for 2023-01"
    assert m.format_report([], "2024-03") == "No expenses for 2024-03"


def test_rows_sorted_by_total_then_name():
    items = [
        exp("2024-03-01", "zeta", "10.00"),
        exp("2024-03-01", "alpha", "10.00"),
        exp("2024-03-01", "big", "50.00"),
    ]
    rows = m.format_report(items, "2024-03").split("\n")[3:6]
    assert [r[:12].strip() for r in rows] == ["big", "alpha", "zeta"]


def test_thousands_separator_and_rounding():
    items = [exp("2024-03-01", "rent", "1200.50"), exp("2024-03-02", "rent", "34.5")]
    text = m.format_report(items, "2024-03")
    assert "rent             2    1,235.00" in text
    assert text.endswith("TOTAL            2    1,235.00")


def test_long_category_names_are_cut():
    items = [exp("2024-03-01", "entertainment-and-fun", "5.00")]
    rows = m.format_report(items, "2024-03").split("\n")
    assert rows[3] == "entertainmen     1        5.00"


def test_top_category():
    assert m.top_category(SAMPLE, "2024-03") == "food"
    assert m.top_category(SAMPLE, "2024-04") == "fun"


def test_top_category_tie_and_empty():
    items = [exp("2024-03-01", "b", "5.00"), exp("2024-03-01", "a", "5.00")]
    assert m.top_category(items, "2024-03") == "a"
    assert m.top_category(items, "2020-01") is None
