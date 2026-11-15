"""Assignment 4: Merge streams and put a time limit on each item.

Real programs often read from several sources at once (several servers,
several log files) and want items in the order they *arrive*. They also need
a way to give up when a source goes quiet.
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import aclosing


async def merge(*streams: AsyncIterator) -> AsyncIterator:
    """Yield the items of all `streams` as they arrive.

    - Items from one stream keep their own order. Items of different streams
      are interleaved by arrival time.
    - Start one background task per stream. Each task reads its stream and
      puts `("item", value)` into one shared `asyncio.Queue`; when the stream
      ends it puts `("done", None)`. If the stream raises an `Exception`, it
      puts `("error", exception)` instead.
    - The generator takes messages from the queue. It yields item values, counts
      the "done" messages, and finishes when every stream is done.
    - On an "error" message, raise that exception.
    - In all cases (finished, error, or the reader stops early) cancel the
      background tasks and wait for them, so no task is left running.
    - Merging zero streams yields nothing.
    Tip: read each stream inside `async with aclosing(stream):` so that its
    cleanup runs when the task is cancelled.
    """
    # TODO: a shared queue, one pump task per stream, cleanup in finally.
    ...


async def with_item_timeout(stream: AsyncIterator, seconds: float) -> AsyncIterator:
    """Yield the items of `stream`, but give each item at most `seconds` to arrive.

    The limit applies to the wait for ONE item, not to the whole stream: a long
    stream whose items arrive quickly never times out.
    If the next item does not arrive in time, raise `TimeoutError`.
    The source stream must be closed when this generator ends for any reason
    (`async with aclosing(stream):`).
    Use `asyncio.timeout(seconds)` around `await anext(iterator)` and catch
    `StopAsyncIteration` to detect the normal end.
    """
    # TODO: loop over anext(iterator) with asyncio.timeout around each call.
    ...


if __name__ == "__main__":
    async def source(name: str, count: int, pause: int) -> AsyncIterator[str]:
        for n in range(count):
            for _ in range(pause):
                await asyncio.sleep(0)
            yield f"{name}{n}"

    async def main() -> None:
        merged = merge(source("a", 3, 1), source("b", 2, 3))
        print([item async for item in merged])

    asyncio.run(main())
