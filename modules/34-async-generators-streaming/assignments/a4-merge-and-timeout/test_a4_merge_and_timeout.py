import asyncio
import functools

import pytest

from practice import load

m = load(__file__)


def guard(test):
    """Fail a test (instead of hanging forever) if it takes more than 5 seconds."""

    @functools.wraps(test)
    async def wrapper(*args, **kwargs):
        async with asyncio.timeout(5):
            return await test(*args, **kwargs)

    return wrapper


async def source(items, pause=1, log=None, name=""):
    try:
        for item in items:
            for _ in range(pause):
                await asyncio.sleep(0)
            yield item
    finally:
        if log is not None:
            log.append(f"{name} closed")


@guard
async def test_merge_keeps_every_item_and_each_streams_order():
    merged = [x async for x in m.merge(source(["a1", "a2", "a3"], 1), source(["b1", "b2"], 3))]
    assert sorted(merged) == ["a1", "a2", "a3", "b1", "b2"]
    assert [x for x in merged if x.startswith("a")] == ["a1", "a2", "a3"]
    assert [x for x in merged if x.startswith("b")] == ["b1", "b2"]


@guard
async def test_merge_orders_by_arrival():
    fast = source(["fast1", "fast2", "fast3"], pause=1)
    slow = source(["slow1"], pause=20)
    merged = [x async for x in m.merge(slow, fast)]
    assert merged[-1] == "slow1"                  # the slow stream's only item arrives last
    assert merged[:3] == ["fast1", "fast2", "fast3"]


@guard
async def test_merge_single_and_empty():
    assert [x async for x in m.merge(source([1, 2, 3]))] == [1, 2, 3]
    assert [x async for x in m.merge()] == []
    assert [x async for x in m.merge(source([]), source([]))] == []


@guard
async def test_merge_error_reaches_reader_and_others_are_closed():
    log = []

    async def broken():
        yield "ok"
        raise RuntimeError("stream failed")

    seen = []
    with pytest.raises(RuntimeError, match="stream failed"):
        async for item in m.merge(broken(), source(range(1000), pause=1, log=log, name="other")):
            seen.append(item)
    assert "ok" in seen
    assert log == ["other closed"]


@guard
async def test_merge_closed_early_cancels_everything():
    log = []
    before = len(asyncio.all_tasks())
    gen = m.merge(source(range(1000), log=log, name="one"), source(range(1000), log=log, name="two"))
    await anext(gen)
    await gen.aclose()
    assert sorted(log) == ["one closed", "two closed"]
    assert len(asyncio.all_tasks()) == before


@guard
async def test_item_timeout_passes_fast_stream_through():
    result = [x async for x in m.with_item_timeout(source(range(50), pause=3), seconds=30)]
    assert result == list(range(50))


@guard
async def test_item_timeout_empty_stream():
    assert [x async for x in m.with_item_timeout(source([]), seconds=30)] == []


@guard
async def test_item_timeout_raises_when_stream_goes_quiet():
    log = []

    async def stalls():
        try:
            yield "first"
            await asyncio.Event().wait()       # never produces a second item
            yield "second"
        finally:
            log.append("closed")

    seen = []
    with pytest.raises(TimeoutError):
        async for item in m.with_item_timeout(stalls(), seconds=0.01):
            seen.append(item)
    assert seen == ["first"]
    assert log == ["closed"]


@guard
async def test_item_timeout_closes_source_when_reader_stops_early():
    log = []
    gen = m.with_item_timeout(source(range(100), log=log, name="src"), seconds=30)
    assert await anext(gen) == 0
    await gen.aclose()
    assert log == ["src closed"]

