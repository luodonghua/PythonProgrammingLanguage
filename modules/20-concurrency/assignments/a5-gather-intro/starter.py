"""Assignment 5: A first look at asyncio.gather."""

import asyncio
from collections.abc import Awaitable, Callable


async def double(n: int) -> int:
    """Return n * 2 after one pause (await asyncio.sleep(0)). Already done."""
    await asyncio.sleep(0)
    return n * 2


async def double_all(numbers: list[int]) -> list[int]:
    """Double every number, running all the `double` coroutines together.

    Return the results in the same order as `numbers`. An empty list gives [].
    """
    # TODO: await asyncio.gather(*(double(n) for n in numbers)) and return a list.
    ...


async def run_all(jobs: list[Callable[[], Awaitable]]) -> list:
    """Call every job (a function that takes no arguments and returns an
    awaitable) and run them together with asyncio.gather.

    Return one entry per job, in order. If a job raises an exception, its entry
    is that exception object and the other jobs still finish
    (use return_exceptions=True).
    """
    # TODO: gather the awaitables with return_exceptions=True; return a list.
    ...


async def count_finished(jobs: list[Callable[[], Awaitable]]) -> tuple[int, int]:
    """Run the jobs like run_all and return (succeeded, failed) counts."""
    # TODO: call run_all, then count entries with isinstance(x, BaseException).
    ...


if __name__ == "__main__":
    print(asyncio.run(double_all([1, 2, 3])))
