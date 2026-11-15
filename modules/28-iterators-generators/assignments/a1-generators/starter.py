"""Assignment 1: first generators.

Write three functions.

``fibonacci()`` is a generator that never ends: 0, 1, 1, 2, 3, 5, 8, ...

``take(n, iterable)`` returns a *list* with the first ``n`` items of any
iterable (fewer if it has fewer). ``n <= 0`` returns ``[]``. It must not read
more items than it needs (it works on endless generators).

``chunker(iterable, size)`` is a generator that yields lists of ``size`` items.
The last list may be shorter. It is lazy: it reads from ``iterable`` only when
the next chunk is requested. ``size < 1`` raises ``ValueError`` (when the
generator is first advanced is fine).
"""


def fibonacci():
    """Yield the Fibonacci numbers forever."""
    # TODO
    ...


def take(n, iterable):
    """Return a list of the first ``n`` items of ``iterable``."""
    # TODO
    ...


def chunker(iterable, size):
    """Yield lists of ``size`` items from ``iterable``."""
    # TODO
    ...


if __name__ == "__main__":
    print(take(10, fibonacci()))
    print(list(chunker("abcdefg", 3)))
