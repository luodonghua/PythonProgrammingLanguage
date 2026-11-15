"""Assignment 4: a request id kept in a ContextVar.

``request_id`` is a ContextVar (already created below) with default ``"-"``.

``current_id()`` returns the current value.

``bind_request_id(value)`` is a context manager (use ``@contextmanager``).
Inside the block ``current_id()`` returns ``value``. When the block ends, also
on error, the previous value comes back. Use ``set()`` and ``reset(token)``.
Blocks can be nested.

``log(message)`` returns ``"[<id>] <message>"``, for example ``"[r1] saved"``.

``with_request_id(value)`` is a decorator factory: the decorated function runs
inside ``bind_request_id(value)``. Keep the function's name and docstring.

``run_in_copy(func, *args)`` calls ``func(*args)`` inside a *copy* of the
current context (``contextvars.copy_context().run``), so any ``request_id.set``
done by ``func`` does not affect the caller. Return what ``func`` returns.
"""

import contextvars
import functools
from contextlib import contextmanager

request_id = contextvars.ContextVar("request_id", default="-")


def current_id():
    """Return the current request id."""
    return request_id.get()


@contextmanager
def bind_request_id(value):
    """Set the request id for the length of a block."""
    token = request_id.set(value)
    try:
        yield
    finally:
        request_id.reset(token)


def log(message):
    """Return the message prefixed with the current request id."""
    return f"[{request_id.get()}] {message}"


def with_request_id(value):
    """Decorator factory: run the function with a bound request id."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with bind_request_id(value):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def run_in_copy(func, *args):
    """Call ``func(*args)`` in a copy of the current context."""
    return contextvars.copy_context().run(func, *args)


if __name__ == "__main__":
    with bind_request_id("r1"):
        print(log("started"))
    print(log("after"))
