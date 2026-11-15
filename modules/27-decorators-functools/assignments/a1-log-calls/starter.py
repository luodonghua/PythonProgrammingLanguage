"""Assignment 1: count and log function calls.

Write two decorators.

``count_calls(func)`` wraps ``func`` and keeps the number of calls in the
attribute ``wrapper.calls`` (0 before the first call).

``log_calls(log)`` is a decorator factory. ``log`` is a function that takes one
string. Each call of the decorated function sends one message to ``log``:

* on success: ``"add(1, 2) -> 3"``
* when the function raises: ``"add(1, 2) raised ValueError"``, and the
  exception still propagates.

Arguments are shown with ``repr``: positional first, then ``name=value`` for
keyword arguments in the order given, joined by ``", "``.

Both decorators must keep ``__name__`` and ``__doc__`` (use functools.wraps).
"""

import functools


def count_calls(func):
    """Return a wrapper that counts calls in ``wrapper.calls``."""
    # TODO
    ...


def log_calls(log):
    """Return a decorator that reports every call to ``log``."""
    # TODO
    ...


if __name__ == "__main__":
    messages = []

    @log_calls(messages.append)
    def add(a, b=0):
        return a + b

    add(1, b=2)
    print(messages)
