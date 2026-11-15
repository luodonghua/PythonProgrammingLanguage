"""Assignment 2: Limit how many tasks run at once.

Starting thousands of requests at the same moment can overload a server or hit
a rate limit. An `asyncio.Semaphore` lets only N tasks into a section at once.
"""

import asyncio
from collections.abc import Awaitable, Callable


async def map_limited(func: Callable[[object], Awaitable], items: list, limit: int) -> list:
    """Call `await func(item)` for every item, with at most `limit` calls active.

    Return the results in the order of `items`. All items must be processed
    even when there are more items than `limit`.
    Raise ValueError("limit must be at least 1") if limit < 1.
    Use `asyncio.Semaphore(limit)` with `async with`.
    """
    # TODO: raise ValueError for a bad limit, create a Semaphore, wrap func.
    ...


class ConcurrencyMeter:
    """Counts how many `track()` blocks are active at the same time.

    Attributes:
      active  how many blocks are inside right now
      peak    the highest value `active` has reached

    Use it as an async context manager:
        async with meter.track():
            ...
    """

    def __init__(self) -> None:
        # TODO: start both counters at 0.
        ...

    def track(self) -> "ConcurrencyMeter":
        """Return an async context manager (the meter itself is fine)."""
        # TODO
        ...

    async def __aenter__(self) -> None:
        # TODO: increase `active`, update `peak`.
        ...

    async def __aexit__(self, exc_type, exc, tb) -> None:
        # TODO: decrease `active`.
        ...


if __name__ == "__main__":
    meter = ConcurrencyMeter()

    async def work(n: int) -> int:
        async with meter.track():
            await asyncio.sleep(0)
            return n * 2

    async def main() -> None:
        print(await map_limited(work, list(range(10)), limit=3))
        print("peak:", meter.peak)

    asyncio.run(main())
