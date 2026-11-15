import inspect

import pytest

from practice import load

m = load(__file__)


def test_fibonacci_start():
    gen = m.fibonacci()
    assert [next(gen) for _ in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_fibonacci_is_a_generator_and_independent():
    assert inspect.isgenerator(m.fibonacci())
    a, b = m.fibonacci(), m.fibonacci()
    next(a)
    next(a)
    assert next(b) == 0


def test_fibonacci_large_value():
    gen = m.fibonacci()
    for _ in range(90):
        next(gen)
    assert next(gen) == 2880067194370816120


def test_take_from_list():
    assert m.take(2, [5, 6, 7]) == [5, 6]


def test_take_more_than_available():
    assert m.take(10, "abc") == ["a", "b", "c"]


def test_take_zero_and_negative():
    assert m.take(0, [1, 2]) == []
    assert m.take(-3, [1, 2]) == []


def test_take_from_endless_generator():
    assert m.take(5, m.fibonacci()) == [0, 1, 1, 2, 3]


def test_take_reads_no_extra_item():
    seen = []

    def source():
        for i in range(10):
            seen.append(i)
            yield i

    assert m.take(3, source()) == [0, 1, 2]
    assert seen == [0, 1, 2]


def test_chunker_basic():
    assert list(m.chunker("abcdefg", 3)) == [["a", "b", "c"], ["d", "e", "f"], ["g"]]


def test_chunker_exact_multiple_and_empty():
    assert list(m.chunker(range(4), 2)) == [[0, 1], [2, 3]]
    assert list(m.chunker([], 3)) == []


def test_chunker_is_lazy_on_endless_input():
    gen = m.chunker(m.fibonacci(), 3)
    assert next(gen) == [0, 1, 1]
    assert next(gen) == [2, 3, 5]


def test_chunker_bad_size():
    with pytest.raises(ValueError):
        list(m.chunker([1, 2], 0))
