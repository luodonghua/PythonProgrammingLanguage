"""Assignment 3: Stream through a bounded queue (backpressure).

A producer reads from a source and puts items into a queue. A consumer takes
items out. If the queue has a `maxsize`, `await queue.put(...)` waits while the
queue is full, so a slow consumer slows the producer down. This is called
**backpressure**. It stops a fast source from filling memory.
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import aclosing

DONE = object()   # marker that means "the stream has ended"


async def produce(stream: AsyncIterator, queue: asyncio.Queue) -> None:
    """Read `stream` to the end, putting every item into `queue`.

    - Use `await queue.put(item)`.
    - When the stream is finished, put the `DONE` marker once.
    - If reading the stream raises an `Exception`, put `DONE` and then
      re-raise, so the consumer is not left waiting.
    - If the task is cancelled, do NOT put `DONE` (the queue may be full, and
      waiting would hang the cancellation). Just let it go.
    - In every case close the stream: wrap the loop in
      `async with aclosing(stream):` (from contextlib).
    """
    try:
        async with aclosing(stream):
            async for item in stream:
                await queue.put(item)
    except Exception:
        await queue.put(DONE)
        raise
    await queue.put(DONE)


async def consume(queue: asyncio.Queue) -> AsyncIterator:
    """Yield items taken from `queue` until the `DONE` marker arrives.

    The marker itself is not yielded. Items come out in the order they went in.
    """
    while True:
        item = await queue.get()
        if item is DONE:
            return
        yield item


async def buffered(stream: AsyncIterator, maxsize: int) -> AsyncIterator:
    """Yield the items of `stream`, while a background task reads ahead.

    - Create an `asyncio.Queue(maxsize=maxsize)`.
    - Start `produce(stream, queue)` as a task with `asyncio.create_task`.
    - Yield everything that `consume(queue)` gives you.
    - When the consumer stops early (the generator is closed or garbage) or
      an error happens, the producer task must be cancelled and awaited, so
      nothing is left running. Use try/finally around the loop.
    - If the producer failed with an exception, that exception must reach the
      reader after the items that were already queued.
    Raise ValueError("maxsize must be at least 1") if maxsize < 1.
    """
    if maxsize < 1:
        raise ValueError("maxsize must be at least 1")
    queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
    producer = asyncio.create_task(produce(stream, queue))
    try:
        async for item in consume(queue):
            yield item
        await producer          # re-raises the producer's exception, if any
    finally:
        if not producer.done():
            producer.cancel()
        await asyncio.gather(producer, return_exceptions=True)


if __name__ == "__main__":
    async def numbers() -> AsyncIterator[int]:
        for n in range(5):
            yield n

    async def main() -> None:
        print([n async for n in buffered(numbers(), maxsize=2)])

    asyncio.run(main())
