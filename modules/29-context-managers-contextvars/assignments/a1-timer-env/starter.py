"""Assignment 1: a timer and a temporary environment variable.

``Timer(clock=time.perf_counter)`` is a context manager class.

* ``__enter__`` records ``clock()`` as the start time and returns the Timer.
* ``__exit__`` records ``clock()`` again and stores the difference in
  ``self.elapsed`` (a float). It must do this even when the body raised, and
  it must NOT swallow the exception.
* Before the block finishes, ``elapsed`` is ``None``.
* ``clock`` is injected so that tests can use a fake one.

``temporary_env(**values)`` is a context manager (use ``@contextmanager``).
For the length of the block it sets the given environment variables in
``os.environ``. When the block ends (also on error) every variable goes back
to its old value, or is removed if it did not exist before. Values are strings.
"""

import os
import time
from contextlib import contextmanager


class Timer:
    """Measure how long a ``with`` block takes."""

    # TODO
    ...


@contextmanager
def temporary_env(**values):
    """Set environment variables for the length of a block."""
    # TODO
    ...


if __name__ == "__main__":
    with Timer() as t:
        sum(range(1000))
    print(t.elapsed >= 0)
    with temporary_env(DEMO_VALUE="1"):
        print(os.environ["DEMO_VALUE"])
    print("DEMO_VALUE" in os.environ)
