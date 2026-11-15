import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("name", "qty", "price", "expected"),
    [
        ("Tea", 2, 3.5, "Tea             2         7.00"),
        ("Laptop", 1, 1299.99, "Laptop          1     1,299.99"),
        ("Extremely long name", 10, 0.5, "Extremely long 10         5.00"),
        ("Pen", 120, 1.25, "Pen           120       150.00"),
    ],
)
def test_format_line(name, qty, price, expected):
    line = m.format_line(name, qty, price)
    assert line == expected
    assert len(line) == 30


def test_format_receipt_one_item():
    lines = m.format_receipt([("Tea", 2, 3.5)]).split("\n")
    assert lines == [
        " " * 11 + "RECEIPT" + " " * 12,
        "-" * 30,
        "Tea             2         7.00",
        "-" * 30,
        "TOTAL" + " " * 21 + "7.00",
    ]


def test_format_receipt_total_and_widths():
    text = m.format_receipt([("Tea", 2, 3.5), ("Laptop", 1, 1299.99)], title="CAFE")
    lines = text.split("\n")
    assert len(lines) == 6
    assert all(len(line) == 30 for line in lines)
    assert lines[0].strip() == "CAFE"
    assert lines[0] == f"{'CAFE':^30}"
    assert lines[-1] == "TOTAL" + " " * 17 + "1,306.99"
    assert not text.endswith("\n")


def test_format_receipt_empty():
    lines = m.format_receipt([]).split("\n")
    assert len(lines) == 4
    assert lines[-1].endswith(" 0.00")
    assert len(lines[-1]) == 30
