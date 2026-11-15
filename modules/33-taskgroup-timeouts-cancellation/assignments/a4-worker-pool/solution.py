"""Assignment 4: A pool of workers fed by an asyncio.Queue.

A pool keeps the number of concurrent jobs fixed. Items go into a queue, and
a set of worker tasks takes items out one at a time until the queue is empty.
"""

import asyncio
from collections.abc import Awaitable, Callable


async def run_pool(
    items: list, worker: Callable[[object], Awaitable], num_workers: int
) -> list:
    """Process `items` with `num_workers` worker tasks and return the results.

    - Put `(index, item)` pairs into an `asyncio.Queue`.
    - Start `num_workers` tasks inside an `asyncio.TaskGroup`. Each task loops:
      `await queue.get()`, run `await worker(item)`, store the result,
      then `queue.task_done()`.
    - The result list follows the order of `items`.
    - If `worker(item)` raises an `Exception`, store that exception object as
      the result for the item (do not raise) and keep going.
    - When `await queue.join()` returns, all items are done. Cancel the
      workers so the TaskGroup can finish.
    - Never run more than `num_workers` calls of `worker` at the same time.
    - Raise ValueError("num_workers must be at least 1") if num_workers < 1.
    """
    if num_workers < 1:
        raise ValueError("num_workers must be at least 1")
    queue: asyncio.Queue = asyncio.Queue()
    for index, item in enumerate(items):
        queue.put_nowait((index, item))
    results: list = [None] * len(items)

    async def run_worker() -> None:
        while True:
            index, item = await queue.get()
            try:
                results[index] = await worker(item)
            except Exception as exc:
                results[index] = exc
            finally:
                queue.task_done()

    async with asyncio.TaskGroup() as group:
        workers = [group.create_task(run_worker()) for _ in range(num_workers)]
        await queue.join()
        for task in workers:
            task.cancel()
    return results


if __name__ == "__main__":
    async def square(n: int) -> int:
        await asyncio.sleep(0)
        if n == 3:
            raise ValueError("three is unlucky")
        return n * n

    print(asyncio.run(run_pool(list(range(6)), square, num_workers=2)))
