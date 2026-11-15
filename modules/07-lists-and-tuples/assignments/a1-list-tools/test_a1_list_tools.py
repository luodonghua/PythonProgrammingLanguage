import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("items", "k", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([1, 2, 3, 4, 5], -1, [2, 3, 4, 5, 1]),
        ([1, 2, 3], 7, [3, 1, 2]),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([1, 2, 3], -4, [2, 3, 1]),
        ([9], 5, [9]),
        ([], 3, []),
    ],
)
def test_rotate(items, k, expected):
    assert m.rotate(items, k) == expected


@pytest.mark.parametrize(
    ("nested", "expected"),
    [
        ([1, [2, 3], [], [4]], [1, 2, 3, 4]),
        ([[1, [2]], 3], [1, [2], 3]),
        ([], []),
        (["ab", ["cd"]], ["ab", "cd"]),
    ],
)
def test_flatten(nested, expected):
    assert m.flatten(nested) == expected


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([3, 1, 3, 2, 1], [3, 1, 2]),
        (["b", "a", "b"], ["b", "a"]),
        ([1, 2, 3], [1, 2, 3]),
        ([5, 5, 5], [5]),
        ([], []),
    ],
)
def test_dedupe(items, expected):
    assert m.dedupe(items) == expected


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [([1, 2, 3, 4], [1, 3, 6, 10]), ([5], [5]), ([], []), ([2.5, -1.5, 1], [2.5, 1.0, 2.0])],
)
def test_running_totals(numbers, expected):
    assert m.running_totals(numbers) == expected


def test_inputs_are_not_changed():
    data = [1, 2, 3, 2]
    nested = [1, [2, 3]]
    results = [m.rotate(data, 1), m.dedupe(data), m.running_totals(data), m.flatten(nested)]
    assert all(isinstance(r, list) for r in results)
    assert data == [1, 2, 3, 2]
    assert nested == [1, [2, 3]]
    # rotating by 0 must return a new list, not the same object
    assert m.rotate(data, 0) is not data
