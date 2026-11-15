import asyncio
import functools

import pytest

from practice import load

m = load(__file__)


async def numbers(n, pulled=None):
    for i in range(n):
        if pulled is not None:
            pulled.append(i)
        yield i


def guard(test):
    """Fail a test (instead of hanging forever) if it takes more than 5 seconds."""

    @functools.wraps(test)
    async def wrapper(*args, **kwargs):
        async with asyncio.timeout(5):
            return await test(*args, **kwargs)

    return wrapper


async def settle():
    for _ in range(10):
        await asyncio.sleep(0)


@guard
async def test_produce_puts_items_then_done():
    queue = asyncio.Queue()
    await m.produce(numbers(3), queue)
    assert [queue.get_nowait() for _ in range(4)] == [0, 1, 2, m.DONE]
    assert queue.empty()


@guard
async def test_produce_puts_done_when_stream_fails():
    async def broken():
        yield 1
        raise RuntimeError("source died")

    queue = asyncio.Queue()
    with pytest.raises(RuntimeError, match="source died"):
        await m.produce(broken(), queue)
    assert [queue.get_nowait() for _ in range(2)] == [1, m.DONE]


@guard
async def test_consume_stops_at_done():
    queue = asyncio.Queue()
    for item in ["a", "b", m.DONE, "never"]:
        queue.put_nowait(item)
    assert [x async for x in m.consume(queue)] == ["a", "b"]
    assert queue.get_nowait() == "never"


@guard
async def test_buffered_yields_everything_in_order():
    assert [x async for x in m.buffered(numbers(20), maxsize=3)] == list(range(20))


@guard
async def test_buffered_empty_stream():
    assert [x async for x in m.buffered(numbers(0), maxsize=1)] == []


@guard
async def test_backpressure_limits_read_ahead():
    pulled = []
    gen = m.buffered(numbers(1000, pulled), maxsize=2)
    first = await anext(gen)
    await settle()                      # give the producer every chance to run ahead
    assert first == 0
    # 1 item taken + 2 in the queue + at most 2 in the hands of the producer
    assert len(pulled) <= 1 + 2 + 2
    assert len(pulled) >= 3             # but it does read ahead
    await gen.aclose()


@guard
async def test_closing_early_stops_the_producer():
    pulled = []
    before = len(asyncio.all_tasks())
    gen = m.buffered(numbers(1000, pulled), maxsize=2)
    assert await anext(gen) == 0
    await gen.aclose()
    assert len(asyncio.all_tasks()) == before
    count = len(pulled)
    await settle()
    assert len(pulled) == count         # nothing keeps reading


@guard
async def test_source_is_closed_when_reader_stops_early():
    log = []

    async def source():
        try:
            for i in range(100):
                yield i
        finally:
            log.append("source closed")

    gen = m.buffered(source(), maxsize=1)
    assert await anext(gen) == 0
    await gen.aclose()
    assert log == ["source closed"]


@guard
async def test_producer_error_reaches_the_reader_after_queued_items():
    async def broken():
        yield "a"
        yield "b"
        raise RuntimeError("source died")

    seen = []
    with pytest.raises(RuntimeError, match="source died"):
        async for item in m.buffered(broken(), maxsize=5):
            seen.append(item)
    assert seen == ["a", "b"]


@pytest.mark.parametrize("maxsize", [0, -1])
@guard
async def test_bad_maxsize(maxsize):
    with pytest.raises(ValueError, match="at least 1"):
        [x async for x in m.buffered(numbers(1), maxsize)]
