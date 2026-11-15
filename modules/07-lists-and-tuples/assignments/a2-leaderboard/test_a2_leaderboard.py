import pytest

from practice import load

m = load(__file__)

DATA = [("Ann", 90), ("Bob", 80), ("Cy", 80), ("Di", 70)]


def test_top_n_basic():
    assert m.top_n([("Ann", 70), ("Bob", 90), ("Cy", 70)], 2) == [("Bob", 90), ("Ann", 70)]


def test_top_n_tie_by_name():
    assert m.top_n([("Zed", 50), ("Amy", 50)], 5) == [("Amy", 50), ("Zed", 50)]


@pytest.mark.parametrize(("scores", "n"), [([], 3), ([("Ann", 70)], 0)])
def test_top_n_empty_results(scores, n):
    assert m.top_n(scores, n) == []
    assert isinstance(m.top_n(scores, n), list)


def test_top_n_does_not_change_input():
    scores = [("Cy", 1), ("Ann", 5), ("Bob", 3)]
    original = list(scores)
    assert m.top_n(scores, 3) == [("Ann", 5), ("Bob", 3), ("Cy", 1)]
    assert scores == original


def test_best_and_worst():
    assert m.best_and_worst([("Ann", 70), ("Bob", 90), ("Cy", 55)]) == (("Bob", 90), ("Cy", 55))


def test_best_and_worst_ties_keep_first():
    result = m.best_and_worst([("Ann", 50), ("Bob", 50), ("Cy", 50)])
    assert result == (("Ann", 50), ("Ann", 50))


def test_best_and_worst_single():
    assert m.best_and_worst([("Ann", 1)]) == (("Ann", 1), ("Ann", 1))


def test_best_and_worst_empty():
    with pytest.raises(ValueError):
        m.best_and_worst([])


def test_ranking_with_ties():
    assert m.ranking(DATA) == [(1, "Ann", 90), (2, "Bob", 80), (2, "Cy", 80), (4, "Di", 70)]


def test_ranking_unsorted_input():
    shuffled = [DATA[3], DATA[1], DATA[0], DATA[2]]
    assert m.ranking(shuffled) == [(1, "Ann", 90), (2, "Bob", 80), (2, "Cy", 80), (4, "Di", 70)]


def test_ranking_all_equal():
    assert m.ranking([("B", 1), ("A", 1)]) == [(1, "A", 1), (1, "B", 1)]


def test_ranking_empty():
    assert m.ranking([]) == []
    assert m.ranking([("Ann", 5)]) == [(1, "Ann", 5)]


def test_average():
    assert m.average([("Ann", 70), ("Bob", 91)]) == 80.5
    assert m.average([("Ann", 10), ("Bob", 10), ("Cy", 11)]) == 10.3
    assert m.average([]) == 0.0
