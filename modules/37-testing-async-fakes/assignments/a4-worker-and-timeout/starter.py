"""Assignment 4: an async queue worker and a timeout helper, both testable.

Two patterns that need care in tests:

* a worker that reads jobs from an ``asyncio.Queue`` until it sees a stop marker;
* a call that must give up after a time limit.
"""

import asyncio
from collections.abc import Awaitable, Callable


async def run_worker(
    queue: asyncio.Queue,
    handler: Callable[[object], Awaitable[object]],
    results: list,
    errors: list,
) -> None:
    """Take items from ``queue`` and process them until the item ``None`` arrives.

    For every item that is not ``None``:

    * ``await handler(item)`` and append the result to ``results``.
    * If the handler raises an ``Exception``, append the tuple ``(item, exc)``
      to ``errors`` and keep going. One bad item must not stop the worker.

    ``None`` is the stop marker: the worker returns when it takes it.
    Call ``queue.task_done()`` exactly once for every item taken, the stop
    marker included, even when the handler fails.
    """
    # TODO: loop with queue.get(); stop at None; always call queue.task_done().
    ...


async def call_with_timeout(func: Callable[[], Awaitable[object]], timeout: float, default=None):
    """Await ``func()`` and return its result, but give up after ``timeout`` seconds.

    If the time limit passes first, the call is cancelled (so its ``finally``
    blocks run) and ``default`` is returned. Use ``asyncio.timeout``.
    Exceptions raised by ``func`` itself must still propagate.
    """
    # TODO: use "async with asyncio.timeout(timeout):" and catch TimeoutError.
    ...


if __name__ == "__main__":

    async def demo() -> None:
        queue: asyncio.Queue = asyncio.Queue()
        for item in (1, 2, 0, 4, None):
            queue.put_nowait(item)

        async def inverse(x):
            return 1 / x

        results, errors = [], []
        await run_worker(queue, inverse, results, errors)
        print(results, errors)

    asyncio.run(demo())
