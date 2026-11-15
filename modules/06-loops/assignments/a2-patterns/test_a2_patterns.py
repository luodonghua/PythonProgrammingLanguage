import pytest

from practice import load

m = load(__file__)


def test_multiplication_table_3():
    assert m.multiplication_table(3) == ["   1   2   3", "   2   4   6", "   3   6   9"]


def test_multiplication_table_row_widths():
    table = m.multiplication_table(10)
    assert len(table) == 10
    assert all(len(row) == 40 for row in table)
    assert table[-1].endswith(" 100")
    assert table[1].split()[:3] == ["2", "4", "6"]


def test_multiplication_table_zero():
    assert m.multiplication_table(0) == []
    assert m.multiplication_table(1) == ["   1"]


@pytest.mark.parametrize(
    ("height", "expected"),
    [(0, []), (1, ["*"]), (3, ["*", "**", "***"])],
)
def test_triangle(height, expected):
    assert m.triangle(height) == expected


@pytest.mark.parametrize(
    ("height", "expected"),
    [
        (0, []),
        (1, ["*"]),
        (3, ["  *", " ***", "*****"]),
        (4, ["   *", "  ***", " *****", "*******"]),
    ],
)
def test_pyramid(height, expected):
    assert m.pyramid(height) == expected


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (0, []),
        (1, ["#"]),
        (3, ["#.#", ".#.", "#.#"]),
        (4, ["#.#.", ".#.#", "#.#.", ".#.#"]),
    ],
)
def test_checkerboard(size, expected):
    assert m.checkerboard(size) == expected
