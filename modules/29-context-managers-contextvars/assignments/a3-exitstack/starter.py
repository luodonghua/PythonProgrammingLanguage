"""Assignment 3: ExitStack and redirect_stdout.

``open_all(paths, mode="r")`` is a context manager (use ``@contextmanager``
and ``contextlib.ExitStack``). It opens every path (UTF-8 text) and yields the
list of open files in the same order. When the block ends, every file is
closed. If opening one of the files fails (for example it does not exist), the
files opened so far are closed and the error propagates.

``capture_output(func, *args, **kwargs)`` calls ``func(*args, **kwargs)`` while
everything it prints is captured (use ``contextlib.redirect_stdout`` and
``io.StringIO``). Return the tuple ``(result, printed_text)``. Output printed
by ``func`` must not reach the real stdout.

``close_all(*objects)`` calls ``.close()`` on every object, in REVERSE order,
even if some ``close()`` raises. Use ExitStack with ``closing`` or
``callback``. If a close raises, the other objects are still closed and the
error propagates after that.
"""

import io
from contextlib import ExitStack, closing, contextmanager, redirect_stdout


@contextmanager
def open_all(paths, mode="r"):
    """Open many files at once and close them all at the end."""
    # TODO
    ...


def capture_output(func, *args, **kwargs):
    """Return (result, text printed by func)."""
    # TODO
    ...


def close_all(*objects):
    """Close every object, last one first."""
    # TODO
    ...


if __name__ == "__main__":
    print(capture_output(lambda: print("hi") or 42))
