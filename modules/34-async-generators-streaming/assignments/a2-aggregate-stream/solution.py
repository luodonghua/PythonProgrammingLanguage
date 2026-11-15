"""Assignment 2: Work on a stream while it arrives.

Data from a network or a model often arrives in small pieces. You rarely want
to wait for all of it before you start working. These helpers process a
stream piece by piece. Streams here are async iterators (anything you can
read with `async for`).
"""

from collections.abc import AsyncIterator


async def running_total(stream: AsyncIterator[float]) -> AsyncIterator[float]:
    """Yield the running total of the numbers in `stream`.

    [1, 2, 3, 4] -> 1, 3, 6, 10. Each total is yielded as soon as its number
    arrives. An empty stream yields nothing.
    """
    total = 0
    async for number in stream:
        total += number
        yield total


async def aggregate(stream: AsyncIterator[float]) -> dict:
    """Read the whole stream and summarise it.

    Return {"count": n, "total": sum, "min": smallest, "max": largest}.
    For an empty stream return {"count": 0, "total": 0, "min": None, "max": None}.
    Do not collect the items into a list first; update the numbers as items arrive.
    """
    count = 0
    total = 0
    smallest = None
    largest = None
    async for number in stream:
        count += 1
        total += number
        smallest = number if smallest is None else min(smallest, number)
        largest = number if largest is None else max(largest, number)
    return {"count": count, "total": total, "min": smallest, "max": largest}


async def lines_from_chunks(chunks: AsyncIterator[str]) -> AsyncIterator[str]:
    """Turn a stream of arbitrary text chunks into a stream of complete lines.

    Chunks can split a line anywhere, even in the middle of a word:
        "ab", "c\\nde", "f\\n\\ngh"   ->   "abc", "def", "", "gh"
    Rules:
      - Yield each line without its trailing "\\n".
      - Yield a line as soon as its "\\n" has arrived (do not wait for the end).
      - When the stream ends, yield any leftover text as a final line, but
        only if it is not empty. (A text that ends with "\\n" has no extra line.)
      - Blank lines in the middle are yielded as "".
    """
    buffer = ""
    async for chunk in chunks:
        buffer += chunk
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            yield line
    if buffer:
        yield buffer


if __name__ == "__main__":
    import asyncio

    async def numbers() -> AsyncIterator[int]:
        for n in (4, 8, 15, 16, 23, 42):
            yield n

    async def pieces() -> AsyncIterator[str]:
        for piece in ("hel", "lo\nwor", "ld\n", "bye"):
            yield piece

    async def main() -> None:
        print([t async for t in running_total(numbers())])
        print(await aggregate(numbers()))
        print([line async for line in lines_from_chunks(pieces())])

    asyncio.run(main())
