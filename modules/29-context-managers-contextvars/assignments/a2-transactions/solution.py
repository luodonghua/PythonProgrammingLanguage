"""Assignment 2: rollback on error, and collecting errors.

``transaction(db)`` is a context manager (use ``@contextmanager``) for a dict.
It yields a *working copy* of ``db``. Changes to the copy reach ``db`` only
when the block ends without an exception (commit: ``db`` then has exactly the
contents of the copy, including removed keys). If the block raises, ``db`` is
left unchanged (rollback) and the exception propagates.

``ErrorCollector(*error_types)`` is a context manager class. If the block
raises an exception that is an instance of ``error_types``, the exception is
swallowed and appended to the list ``self.errors``. Any other exception
propagates. With no ``error_types`` it collects ``Exception``. After the
block, ``self.ok`` is ``True`` when no error was collected.
(Hint: ``__exit__`` swallows the exception by returning ``True``.)
"""

from contextlib import contextmanager


@contextmanager
def transaction(db):
    """Yield a copy of ``db``; commit it on success, drop it on error."""
    working = dict(db)
    yield working
    db.clear()
    db.update(working)


class ErrorCollector:
    """Swallow chosen exceptions and keep them in ``errors``."""

    def __init__(self, *error_types):
        self.error_types = error_types or (Exception,)
        self.errors = []

    @property
    def ok(self):
        return not self.errors

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc is not None and isinstance(exc, self.error_types):
            self.errors.append(exc)
            return True
        return False


if __name__ == "__main__":
    accounts = {"ann": 10, "bob": 0}
    try:
        with transaction(accounts) as tx:
            tx["ann"] -= 5
            tx["bob"] += 5
            raise RuntimeError("crash")
    except RuntimeError:
        pass
    print(accounts)
    with ErrorCollector(ValueError) as c:
        int("x")
    print(c.errors, c.ok)
