import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("n", "expected"),
    [(1, "1"), (3, "Fizz"), (5, "Buzz"), (7, "7"), (9, "Fizz"), (10, "Buzz"), (15, "FizzBuzz"), (30, "FizzBuzz")],
)
def test_fizzbuzz(n, expected):
    assert m.fizzbuzz(n) == expected


def test_fizzbuzz_up_to():
    assert m.fizzbuzz_up_to(5) == ["1", "2", "Fizz", "4", "Buzz"]


def test_fizzbuzz_up_to_zero():
    assert m.fizzbuzz_up_to(0) == []
