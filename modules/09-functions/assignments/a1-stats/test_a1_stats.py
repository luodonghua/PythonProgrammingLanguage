import pytest

from practice import load

m = load(__file__)


def test_min_max():
    assert m.min_max([3, 1, 4, 1, 5]) == (1, 5)
    assert m.min_max([7]) == (7, 7)
    assert m.min_max([-2.5, -1]) == (-2.5, -1)


def test_mean():
    assert m.mean([1, 2, 3, 4]) == 2.5
    assert m.mean([10]) == 10
    assert m.mean([]) is None


def test_median_odd_and_even():
    assert m.median([5, 1, 3]) == 3
    assert m.median([4, 1, 3, 2]) == 2.5
    assert m.median([9]) == 9


def test_median_empty():
    assert m.median([]) is None
    assert m.median([1]) == 1  # not None


def test_median_does_not_sort_the_input():
    data = [3, 1, 2]
    assert m.median(data) == 2
    assert data == [3, 1, 2]


def test_stats():
    assert m.stats([1, 2, 3, 4]) == {
        "count": 4,
        "min": 1,
        "max": 4,
        "mean": 2.5,
        "median": 2.5,
    }


def test_stats_empty():
    assert m.stats([]) == {
        "count": 0,
        "min": None,
        "max": None,
        "mean": None,
        "median": None,
    }


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada Lovelace", ("Ada", "Lovelace")),
        ("  Mary Ann Smith ", ("Mary", "Ann Smith")),
        ("Plato", ("Plato", "")),
        ("", ("", "")),
        ("   ", ("", "")),
    ],
)
def test_split_name(name, expected):
    assert m.split_name(name) == expected
