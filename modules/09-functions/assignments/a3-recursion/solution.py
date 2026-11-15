"""Assignment 3: Recursion.

A recursive function calls itself on a smaller problem and stops at a
base case. Write each function recursively (no loops unless stated).
"""


def factorial(n: int) -> int:
    """Return n! (1 * 2 * ... * n). factorial(0) is 1.

    factorial(5)  -> 120
    factorial(0)  -> 1

    Raise ValueError for a negative n.
    """
    if n < 0:
        raise ValueError("n must not be negative")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def sum_digits(n: int) -> int:
    """Return the sum of the digits of a non-negative integer.

    sum_digits(1234)  -> 10
    sum_digits(0)     -> 0

    Hint: n % 10 is the last digit and n // 10 is the rest.
    """
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)


def fib(n: int, cache: dict[int, int] | None = None) -> int:
    """Return the n-th Fibonacci number: fib(0)=0, fib(1)=1, fib(n)=fib(n-1)+fib(n-2).

    Store results in the `cache` dict so that fib(80) is fast.
    When `cache` is None, create a new empty dict (never use a mutable
    default value).

    fib(10)  -> 55
    fib(80)  -> 23416728348467685
    """
    if cache is None:
        cache = {}
    if n < 2:
        return n
    if n not in cache:
        cache[n] = fib(n - 1, cache) + fib(n - 2, cache)
    return cache[n]


def flatten(nested: list) -> list:
    """Flatten lists nested to any depth into one flat list.

    flatten([1, [2, [3, 4]], 5])  -> [1, 2, 3, 4, 5]
    flatten([])                   -> []
    flatten([[], [[]]])           -> []

    Do not change the input. Use isinstance(item, list) to detect nesting.
    """
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


def power_set_size(items: list) -> int:
    """Return how many subsets a list of distinct items has (2 ** len(items)),
    computed recursively: the empty list has 1 subset, and each extra item
    doubles the count.

    power_set_size([])         -> 1
    power_set_size([1, 2, 3])  -> 8
    """
    if not items:
        return 1
    return 2 * power_set_size(items[1:])


if __name__ == "__main__":
    print(factorial(5), sum_digits(1234), fib(30))
    print(flatten([1, [2, [3, 4]], 5]))
