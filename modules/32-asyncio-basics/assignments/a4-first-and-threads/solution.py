"""Assignment 4: First result wins, and blocking code in a thread.

Two everyday tools:
  * ask several sources and use whichever answers first, then stop the rest;
  * call ordinary blocking code (file reads, slow libraries) without freezing
    the event loop, by running it in a worker thread with `asyncio.to_thread`.
"""

import asyncio
from collections.abc import Awaitable, Callable
from pathlib import Path


async def first_result(factories: list[Callable[[], Awaitable]]):
    """Run all factories concurrently; return the result of the first to finish.

    - Create one task per factory with `asyncio.create_task`.
    - Wait with `asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)`.
    - Cancel every task that is still pending, and wait until they have
      actually stopped (so their cleanup code has run).
    - If the winner raised an exception, raise it. If several tasks finished
      at the same moment, prefer the one that comes first in `factories`.
    - An empty list raises ValueError("no jobs").
    """
    if not factories:
        raise ValueError("no jobs")
    tasks = [asyncio.create_task(factory()) for factory in factories]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)
    winner = next(task for task in tasks if task in done)
    return winner.result()


async def run_blocking(func: Callable, *args):
    """Run the ordinary (blocking) function `func(*args)` in a worker thread.

    Return its result. The event loop must stay free to run other tasks while
    `func` is working. Use `asyncio.to_thread`.
    """
    return await asyncio.to_thread(func, *args)


async def read_text_async(path: Path) -> str:
    """Read a UTF-8 text file without blocking the event loop.

    `Path.read_text` is blocking, so run it with `run_blocking`/`to_thread`.
    """
    return await run_blocking(Path(path).read_text, "utf-8")


if __name__ == "__main__":
    async def source(name: str, yields: int) -> str:
        for _ in range(yields):
            await asyncio.sleep(0)
        return name

    async def main() -> None:
        print(await first_result([lambda: source("slow", 5), lambda: source("fast", 1)]))

    asyncio.run(main())
