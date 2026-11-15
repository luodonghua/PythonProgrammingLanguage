import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("matrix", "expected"),
    [
        ([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]),
        ([[7]], [[7]]),
        ([[1, 2], [3, 4]], [[1, 3], [2, 4]]),
        ([[1], [2], [3]], [[1, 2, 3]]),
        ([], []),
    ],
)
def test_transpose(matrix, expected):
    result = m.transpose(matrix)
    assert result == expected
    assert all(isinstance(row, list) for row in result)


def test_identity():
    assert m.identity(3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert m.identity(1) == [[1]]
    assert m.identity(0) == []


def test_identity_rows_are_separate_lists():
    matrix = m.identity(3)
    matrix[0][1] = 99
    assert matrix[1][1] == 1
    assert matrix[2][1] == 0
    assert len({id(row) for row in matrix}) == 3


def test_multiply():
    assert m.multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
    assert m.multiply([[1, 2, 3]], [[1], [1], [1]]) == [[6]]
    assert m.multiply([[1], [2]], [[3, 4]]) == [[3, 4], [6, 8]]


def test_multiply_by_identity():
    a = [[2, 3, 4], [5, 6, 7]]
    assert m.multiply(a, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == a


def test_multiply_shape_mismatch():
    with pytest.raises(ValueError):
        m.multiply([[1, 2]], [[1, 2]])


def test_rotate_clockwise():
    assert m.rotate_clockwise([[1, 2, 3], [4, 5, 6]]) == [[4, 1], [5, 2], [6, 3]]
    assert m.rotate_clockwise([[1, 2], [3, 4]]) == [[3, 1], [4, 2]]
    assert m.rotate_clockwise([[5]]) == [[5]]


def test_four_rotations_give_the_original():
    start = [[1, 2, 3], [4, 5, 6]]
    turned = start
    for _ in range(4):
        turned = m.rotate_clockwise(turned)
    assert turned == start


def test_arguments_are_not_changed():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    assert m.multiply(a, b) == [[19, 22], [43, 50]]
    assert m.rotate_clockwise(a) == [[3, 1], [4, 2]]
    assert a == [[1, 2], [3, 4]]
    assert b == [[5, 6], [7, 8]]
