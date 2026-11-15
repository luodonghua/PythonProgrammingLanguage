import asyncio

import pytest

from practice import load

m = load(__file__)


async def test_meter_counts_overlap():
    meter = m.ConcurrencyMeter()
    gate = asyncio.Event()

    async def worker():
        async with meter.track():
            await gate.wait()

    tasks = [asyncio.create_task(worker()) for _ in range(3)]
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    assert meter.active == 3
    gate.set()
    await asyncio.gather(*tasks)
    assert meter.active == 0
    assert meter.peak == 3


async def test_meter_decrements_when_block_raises():
    meter = m.ConcurrencyMeter()
    with pytest.raises(RuntimeError):
        async with meter.track():
            raise RuntimeError("x")
    assert meter.active == 0
    assert meter.peak == 1


async def test_results_in_order_and_all_items_processed():
    async def double(n):
        for _ in range(n % 3):
            await asyncio.sleep(0)
        return n * 2

    assert await m.map_limited(double, list(range(10)), limit=3) == [n * 2 for n in range(10)]


@pytest.mark.parametrize("limit", [1, 2, 3, 5])
async def test_limit_is_respected_and_used(limit):
    meter = m.ConcurrencyMeter()

    async def work(n):
        async with meter.track():
            for _ in range(3):
                await asyncio.sleep(0)
        return n

    result = await m.map_limited(work, list(range(12)), limit)
    assert result == list(range(12))
    assert meter.peak == limit


async def test_limit_larger_than_items():
    meter = m.ConcurrencyMeter()

    async def work(n):
        async with meter.track():
            await asyncio.sleep(0)
        return n

    assert await m.map_limited(work, [1, 2], limit=10) == [1, 2]
    assert meter.peak == 2


async def test_empty_items():
    async def work(n):
        return n

    assert await m.map_limited(work, [], limit=2) == []


@pytest.mark.parametrize("limit", [0, -1])
async def test_bad_limit(limit):
    async def work(n):
        return n

    with pytest.raises(ValueError, match="at least 1"):
        await m.map_limited(work, [1], limit)
