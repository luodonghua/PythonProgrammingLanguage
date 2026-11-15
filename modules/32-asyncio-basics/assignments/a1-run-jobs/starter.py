"""Assignment 1: Run jobs at the same time and keep the results in order.

A "job" here is a function that takes no arguments and returns a coroutine,
for example `lambda: fetch("a")`. Passing factories (not coroutine objects)
means nothing starts until you decide to start it.
"""

import asyncio
from collections.abc import Awaitable, Callable

Job = Callable[[], Awaitable]


async def run_all(jobs: list[Job]) -> list:
    """Run every job concurrently and return the results in the order of `jobs`.

    The result order must follow the order of the input list, not the order in
    which the jobs finish. If a job raises, the exception propagates.
    An empty list returns [].
    """
    # TODO: call each job to get a coroutine, then gather them.
    ...


async def run_all_safe(jobs: list[Job]) -> list[tuple[str, object]]:
    """Like run_all, but one failing job does not hide the others.

    Return one tuple per job, in input order:
      ("ok", result)             when the job returned normally
      ("error", "<message>")     when it raised; the message is str(exception)
    Use `asyncio.gather(..., return_exceptions=True)`.
    """
    # TODO: gather with return_exceptions=True, then label each outcome.
    ...


if __name__ == "__main__":
    async def square(n: int) -> int:
        await asyncio.sleep(0)
        return n * n

    async def main() -> None:
        print(await run_all([lambda n=n: square(n) for n in range(5)]))

    asyncio.run(main())
