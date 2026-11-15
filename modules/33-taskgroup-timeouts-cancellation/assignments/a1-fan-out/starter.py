"""Assignment 1: Fan out with a TaskGroup.

`asyncio.TaskGroup` starts several tasks and waits for all of them when the
`async with` block ends. If one task fails, the group cancels the others and
raises an `ExceptionGroup`. This is called structured concurrency: no task
outlives the block that created it.
"""

import asyncio
from collections.abc import Awaitable, Callable


async def fetch_all(names: list[str], fetch: Callable[[str], Awaitable]) -> dict:
    """Call `await fetch(name)` for every name at the same time.

    Return a dict {name: result} with the keys in the order of `names`.
    Use `asyncio.TaskGroup`. If any call fails, do NOT catch anything: the
    ExceptionGroup from the TaskGroup must reach the caller, and the still
    running calls must have been cancelled.
    Duplicate names are allowed; the later result wins.
    """
    # TODO: async with asyncio.TaskGroup() as group: group.create_task(...)
    ...


async def fetch_all_partial(
    names: list[str], fetch: Callable[[str], Awaitable]
) -> tuple[dict, dict]:
    """Like fetch_all, but a failing name must not stop the others.

    Return (results, errors):
      results  {name: result} for the names that worked, in input order
      errors   {name: "<ExceptionClassName>: <message>"} for the names that
               raised an `Exception`, in input order
    Hint: catch the error inside a small wrapper coroutine that each task runs,
    so the TaskGroup itself never sees a failure.
    """
    # TODO: wrap `fetch` in a coroutine that catches Exception.
    ...


if __name__ == "__main__":
    async def fetch(name: str) -> str:
        await asyncio.sleep(0)
        if name == "bad":
            raise ValueError("no such item")
        return name.upper()

    async def main() -> None:
        print(await fetch_all(["a", "b"], fetch))
        print(await fetch_all_partial(["a", "bad", "c"], fetch))

    asyncio.run(main())
