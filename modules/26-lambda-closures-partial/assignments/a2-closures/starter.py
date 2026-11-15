"""Assignment 2: Closures, nonlocal and the late-binding bug."""


def make_counter(start: int = 0, step: int = 1):
    """Return a function `counter()` that counts.

    Each call returns the next number: the first call returns start + step,
    the second start + 2 * step, and so on. Separate counters are independent.

        c = make_counter(10, 5)
        c(), c()   ->  15, 20

    Keep the running value in the enclosing function and use `nonlocal`.
    """
    # TODO
    ...


def make_limiter(max_calls: int):
    """Return a function `allow()` that answers True for the first `max_calls`
    calls and False for every call after that.

    make_limiter(0) never allows anything. Separate limiters are independent.
    """
    # TODO
    ...


def make_adders(n: int) -> list:
    """Return a list of n functions; the function at index i adds i to its argument.

        adders = make_adders(3)
        [f(10) for f in adders]  ->  [10, 11, 12]

    The version below has the late-binding bug: every lambda sees the last i.
    Fix it (bind i with a default argument, or use functools.partial).
    """
    return [lambda x: x + i for i in range(n)]  # TODO: fix this line


def make_history():
    """Return a pair of functions (record, history).

    record(value) remembers the value and returns how many values are stored.
    history() returns a NEW list with the values in the order recorded
    (changing the returned list must not change the stored values).
    Two calls to make_history() give two separate histories.
    """
    # TODO: keep a list in the enclosing scope. No nonlocal is needed to append.
    ...


if __name__ == "__main__":
    c = make_counter(10, 5)
    print(c(), c())
    print([f(10) for f in make_adders(3)])
