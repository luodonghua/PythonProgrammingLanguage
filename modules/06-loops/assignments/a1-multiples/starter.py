"""Assignment 1: Loops and accumulators.

Three small functions that each build a result step by step in a loop.
"""


def sum_of_multiples(limit: int, divisors: tuple[int, ...] = (3, 5)) -> int:
    """Sum all numbers from 1 up to but NOT including `limit` that are
    multiples of at least one of the divisors. Count each number once.

    sum_of_multiples(10)          -> 23     (3 + 5 + 6 + 9)
    sum_of_multiples(1000)        -> 233168
    sum_of_multiples(20, (4,))    -> 40     (4 + 8 + 12 + 16)
    sum_of_multiples(1)           -> 0
    """
    # TODO: total = 0, loop over range(1, limit), add matching numbers.
    ...


def factorial(n: int) -> int:
    """Return n! = 1 * 2 * ... * n, with 0! = 1. Use a loop, not recursion.

    factorial(0) -> 1
    factorial(5) -> 120

    Raise ValueError if n is negative.
    """
    # TODO: result = 1, multiply by every factor from 2 to n.
    ...


def digit_sum(n: int) -> int:
    """Return the sum of the decimal digits of n. Ignore the sign.

    digit_sum(0)      -> 0
    digit_sum(1234)   -> 10
    digit_sum(-905)   -> 14
    """
    # TODO: loop over the characters of str(abs(n)).
    ...


if __name__ == "__main__":
    print(sum_of_multiples(1000))
    print(factorial(10))
    print(digit_sum(2**15))
