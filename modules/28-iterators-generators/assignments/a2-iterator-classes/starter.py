"""Assignment 2: iterator classes.

``Countdown(start)`` is an *iterator*: it counts down ``start, start-1, ..., 1``
and then raises ``StopIteration`` (it stops before 0). A start below 1 gives an
empty countdown. ``iter(c)`` returns ``c`` itself, and once it is used up it
stays empty.

``Playlist(titles)`` is an *iterable*, not an iterator. Looping over the same
playlist twice must give the titles twice. It also supports ``len()``, and
``repeat(times)`` returns a *generator* that yields every title ``times``
times in order (A B C A B C for times=2).

Write ``Countdown`` with ``__iter__`` and ``__next__``. For ``Playlist`` use
``__iter__`` and ``__len__``.
"""


class Countdown:
    """Iterator that counts down to 1."""

    # TODO
    ...


class Playlist:
    """Iterable collection of titles that can be looped over many times."""

    # TODO
    ...


if __name__ == "__main__":
    print(list(Countdown(3)))
    p = Playlist(["a", "b"])
    print(list(p), list(p), len(p), list(p.repeat(2)))
