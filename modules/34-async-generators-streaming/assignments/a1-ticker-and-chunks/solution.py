"""Assignment 1: Your first async generators.

An async generator is an `async def` function that contains `yield`. You read
it with `async for`. Between two items it may `await`, for example to wait for
a timer or a network packet.
"""

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager


async def ticker(
    count: int,
    interval: float = 1.0,
    sleep: Callable[[float], Awaitable] = asyncio.sleep,
) -> AsyncIterator[int]:
    """Yield 0, 1, ..., count - 1, waiting `interval` seconds between items.

    Call `await sleep(interval)` after every item except the last one.
    (The `sleep` parameter lets tests replace the real clock.)
    count == 0 yields nothing and never sleeps.
    """
    for number in range(count):
        yield number
        if number < count - 1:
            await sleep(interval)


async def chunk_text(text: str, size: int) -> AsyncIterator[str]:
    """Yield `text` in pieces of at most `size` characters.

    Call `await asyncio.sleep(0)` after each piece so other tasks can run.
    The pieces joined together must equal `text`. An empty text yields nothing.
    Raise ValueError("size must be at least 1") when the generator is first
    iterated with size < 1.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    for start in range(0, len(text), size):
        yield text[start : start + size]
        await asyncio.sleep(0)


async def collect(stream: AsyncIterator) -> list:
    """Read an async iterator to the end and return all items as a list.

    Use `async for` or an async comprehension: `[x async for x in stream]`.
    """
    return [item async for item in stream]


async def take(stream: AsyncIterator, n: int) -> list:
    """Return the first `n` items of `stream`, then stop reading.

    The source generator must be closed when you are done, so that its
    `finally` block runs at once. Call `await stream.aclose()`. If the
    stream is shorter than `n`, return everything it has. n <= 0 returns []
    (and also closes the stream).
    """
    items: list = []
    try:
        if n > 0:
            async for item in stream:
                items.append(item)
                if len(items) >= n:
                    break
    finally:
        await stream.aclose()
    return items


@asynccontextmanager
async def session(log: list[str], name: str):
    """An async context manager that records when it opens and closes.

    On entering: append f"open {name}" to `log` and give `name` to the
    `with` block. On leaving, even when the block raises: append
    f"close {name}". Build it with `@asynccontextmanager` (already applied)
    using try/finally around a single `yield`.
    """
    log.append(f"open {name}")
    try:
        yield name
    finally:
        log.append(f"close {name}")


if __name__ == "__main__":
    async def no_wait(seconds: float) -> None:
        pass

    async def main() -> None:
        print(await collect(ticker(4, sleep=no_wait)))
        print(await collect(chunk_text("streaming", 4)))

    asyncio.run(main())
