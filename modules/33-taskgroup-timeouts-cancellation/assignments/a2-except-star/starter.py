"""Assignment 2: Handle several failures at once with `except*`.

When more than one task of a TaskGroup fails, Python raises an
`ExceptionGroup` that holds all the errors. A normal `except ValueError`
does not match a group. `except* ValueError` does: it takes the ValueErrors
out of the group and leaves the rest.

Note: `return`, `break` and `continue` are not allowed inside an `except*`
block. Store what you need in variables and return after the `try` statement.
"""

import asyncio
from collections.abc import Awaitable, Callable


def flatten_exceptions(exc: BaseException) -> list[BaseException]:
    """Return the "leaf" exceptions inside `exc`, in order.

    - A normal exception returns a list with just itself.
    - An ExceptionGroup returns the leaves of all its members, in order.
      Groups can be nested, so use recursion.
    - The groups themselves are not included.
    """
    # TODO: recurse into exc.exceptions when exc is a BaseExceptionGroup.
    ...


async def summarize_failures(job: Callable[[], Awaitable]) -> dict:
    """Run `await job()` and sort any failures by type.

    Return a dict with these keys:
      "ok"            True if the job raised nothing, else False
      "value_errors"  the str() of every ValueError that was raised
      "key_errors"    the str() of every KeyError that was raised
    Use `try:` with `except* ValueError` and `except* KeyError`. Keep the
    order in which the errors appear in the group. The job usually runs a
    TaskGroup, so its errors arrive wrapped in an ExceptionGroup.
    Any other exception type is NOT handled: it must still propagate.
    """
    # TODO: try: await job()  except* ValueError as group: ...
    # Remember: no `return` inside an except* block.
    ...


if __name__ == "__main__":
    async def fail(exc: Exception) -> None:
        raise exc

    async def job() -> None:
        async with asyncio.TaskGroup() as group:
            group.create_task(fail(ValueError("bad number")))
            group.create_task(fail(KeyError("name")))

    print(asyncio.run(summarize_failures(job)))
