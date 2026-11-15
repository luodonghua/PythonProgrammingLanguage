"""Assignment 4: stream tools.

Write four generator functions. All of them must be lazy, so each one also
works on an endless input.

``running_average()``
    A generator you drive with ``send``. After priming it with ``next(gen)``
    (which yields ``None``), every ``gen.send(x)`` returns the average of all
    numbers sent so far.

``moving_average(values, window)``
    Yield the average of each run of ``window`` consecutive values, starting
    when the first full window is available. ``[1, 2, 3, 4]`` with window 2
    gives ``1.5, 2.5, 3.5``. Fewer values than the window yield nothing.
    ``window < 1`` raises ``ValueError``.

``dedupe_consecutive(iterable)``
    Yield items, skipping an item equal to the one just before it.
    ``"aabbbaa"`` gives ``a, b, a``.

``merge_sorted(*streams)``
    Merge any number of already sorted iterables into one sorted stream
    (use ``heapq.merge``).
"""


def running_average():
    """Coroutine-style generator: send numbers, receive the running average."""
    # TODO
    ...


def moving_average(values, window):
    """Yield the average of each full window of ``window`` values."""
    # TODO
    ...


def dedupe_consecutive(iterable):
    """Yield items, dropping repeats that follow each other."""
    # TODO
    ...


def merge_sorted(*streams):
    """Merge sorted iterables into one sorted stream."""
    # TODO
    ...


if __name__ == "__main__":
    print(list(moving_average([1, 2, 3, 4], 2)))
    print(list(dedupe_consecutive("aabbbaa")))
    print(list(merge_sorted([1, 4], [2, 3])))
