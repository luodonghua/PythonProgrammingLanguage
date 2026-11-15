import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(("n", "expected"), [(0, 1), (1, 1), (5, 120), (10, 3628800)])
def test_factorial(n, expected):
    assert m.factorial(n) == expected


def test_factorial_negative():
    with pytest.raises(ValueError):
        m.factorial(-1)


@pytest.mark.parametrize(("n", "expected"), [(0, 0), (7, 7), (10, 1), (1234, 10), (999, 27)])
def test_sum_digits(n, expected):
    assert m.sum_digits(n) == expected


@pytest.mark.parametrize(("n", "expected"), [(0, 0), (1, 1), (2, 1), (10, 55)])
def test_fib_small(n, expected):
    assert m.fib(n) == expected


def test_fib_large_is_fast():
    # Without a cache this would need about 10**16 calls.
    assert m.fib(80) == 23416728348467685


def test_fib_uses_the_given_cache():
    cache = {}
    assert m.fib(20, cache) == 6765
    assert cache[20] == 6765
    assert len(cache) >= 10


def test_fib_has_no_shared_default_cache():
    default = m.fib.__defaults__[0]
    assert default is None
    assert m.fib(15) == 610


def test_flatten():
    assert m.flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
    assert m.flatten([]) == []
    assert m.flatten([[], [[]]]) == []
    assert m.flatten(["a", ["b"]]) == ["a", "b"]


def test_flatten_does_not_change_input():
    data = [1, [2, [3]]]
    assert m.flatten(data) == [1, 2, 3]
    assert data == [1, [2, [3]]]


def test_power_set_size():
    assert m.power_set_size([]) == 1
    assert m.power_set_size([1, 2, 3]) == 8
    assert m.power_set_size(list(range(10))) == 1024
