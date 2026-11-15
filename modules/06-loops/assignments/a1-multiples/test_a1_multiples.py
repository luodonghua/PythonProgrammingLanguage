import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("limit", "divisors", "expected"),
    [
        (10, (3, 5), 23),
        (1000, (3, 5), 233168),
        (20, (4,), 40),
        (1, (3, 5), 0),
        (16, (3, 5), 60),
        (30, (2, 3, 7), 292),
    ],
)
def test_sum_of_multiples(limit, divisors, expected):
    assert m.sum_of_multiples(limit, divisors) == expected


def test_sum_of_multiples_default_divisors():
    assert m.sum_of_multiples(10) == 23


@pytest.mark.parametrize(("n", "expected"), [(0, 1), (1, 1), (5, 120), (10, 3628800), (20, 2432902008176640000)])
def test_factorial(n, expected):
    assert m.factorial(n) == expected


def test_factorial_negative():
    with pytest.raises(ValueError):
        m.factorial(-1)


@pytest.mark.parametrize(("n", "expected"), [(0, 0), (7, 7), (1234, 10), (-905, 14), (2**15, 26)])
def test_digit_sum(n, expected):
    assert m.digit_sum(n) == expected
