import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(("n", "expected"), [(1, 0), (2, 1), (6, 8), (7, 16), (27, 111)])
def test_collatz_steps(n, expected):
    assert m.collatz_steps(n) == expected


@pytest.mark.parametrize("n", [0, -5])
def test_collatz_steps_invalid(n):
    with pytest.raises(ValueError):
        m.collatz_steps(n)


@pytest.mark.parametrize(("limit", "expected"), [(2, 1), (3, 2), (10, 9), (30, 27), (1000, 871)])
def test_longest_collatz(limit, expected):
    assert m.longest_collatz(limit) == expected


def test_longest_collatz_invalid():
    with pytest.raises(ValueError):
        m.longest_collatz(1)


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (-3, []),
        (0, []),
        (1, []),
        (2, [2]),
        (3, [2, 3]),
        (4, [2, 3]),
        (20, [2, 3, 5, 7, 11, 13, 17, 19]),
    ],
)
def test_primes_up_to(n, expected):
    assert m.primes_up_to(n) == expected


def test_primes_up_to_100():
    primes = m.primes_up_to(100)
    assert len(primes) == 25
    assert primes[-1] == 97


def test_primes_up_to_includes_n_itself():
    assert m.primes_up_to(97)[-1] == 97
    assert m.primes_up_to(96)[-1] == 89
