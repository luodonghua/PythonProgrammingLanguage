import itertools

import pytest

from practice import load

m = load(__file__)


def test_running_average():
    gen = m.running_average()
    assert next(gen) is None
    assert gen.send(10) == 10.0
    assert gen.send(20) == 15.0
    assert gen.send(60) == 30.0


def test_running_average_instances_are_independent():
    a, b = m.running_average(), m.running_average()
    next(a)
    next(b)
    a.send(100)
    assert b.send(2) == 2.0


def test_moving_average():
    assert list(m.moving_average([1, 2, 3, 4], 2)) == [1.5, 2.5, 3.5]
    assert list(m.moving_average([1, 2, 3, 4, 5], 3)) == [2.0, 3.0, 4.0]


def test_moving_average_window_one_and_too_short():
    assert list(m.moving_average([4, 8], 1)) == [4.0, 8.0]
    assert list(m.moving_average([1, 2], 3)) == []
    assert list(m.moving_average([], 2)) == []


def test_moving_average_bad_window():
    with pytest.raises(ValueError):
        list(m.moving_average([1, 2, 3], 0))


def test_moving_average_endless_input():
    gen = m.moving_average(itertools.count(1), 2)
    assert list(itertools.islice(gen, 3)) == [1.5, 2.5, 3.5]


def test_dedupe_consecutive():
    assert list(m.dedupe_consecutive("aabbbaa")) == ["a", "b", "a"]
    assert list(m.dedupe_consecutive([])) == []
    assert list(m.dedupe_consecutive([1, 2, 3])) == [1, 2, 3]


def test_dedupe_consecutive_first_item_none():
    assert list(m.dedupe_consecutive([None, None, 0, 0, None])) == [None, 0, None]


def test_dedupe_consecutive_endless_input():
    gen = m.dedupe_consecutive(itertools.cycle([1, 1, 2]))
    assert list(itertools.islice(gen, 4)) == [1, 2, 1, 2]


def test_merge_sorted():
    assert list(m.merge_sorted([1, 4, 9], [2, 3, 10], [0])) == [0, 1, 2, 3, 4, 9, 10]
    assert list(m.merge_sorted()) == []
    assert list(m.merge_sorted([1, 2])) == [1, 2]


def test_merge_sorted_endless_streams():
    gen = m.merge_sorted(itertools.count(0, 2), itertools.count(1, 2))
    assert list(itertools.islice(gen, 6)) == [0, 1, 2, 3, 4, 5]
