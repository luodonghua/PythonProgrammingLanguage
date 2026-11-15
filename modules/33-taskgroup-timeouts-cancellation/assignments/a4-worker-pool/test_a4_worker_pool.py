import asyncio

import pytest

from practice import load

m = load(__file__)


class Meter:
    def __init__(self):
        self.active = 0
        self.peak = 0
        self.calls = 0

    async def work(self, n):
        self.calls += 1
        self.active += 1
        self.peak = max(self.peak, self.active)
        try:
            for _ in range(3):
                await asyncio.sleep(0)
            return n * n
        finally:
            self.active -= 1


async def test_results_in_input_order():
    meter = Meter()
    assert await m.run_pool(list(range(10)), meter.work, 3) == [n * n for n in range(10)]
    assert meter.calls == 10


@pytest.mark.parametrize(("workers", "items", "expected_peak"), [(1, 6, 1), (2, 6, 2), (4, 6, 4), (10, 3, 3)])
async def test_concurrency_is_limited_but_used(workers, items, expected_peak):
    meter = Meter()
    await m.run_pool(list(range(items)), meter.work, workers)
    assert meter.peak == expected_peak


async def test_errors_become_results():
    async def work(n):
        await asyncio.sleep(0)
        if n % 2:
            raise ValueError(f"odd {n}")
        return n

    result = await m.run_pool([0, 1, 2, 3], work, 2)
    assert result[0] == 0
    assert result[2] == 2
    assert isinstance(result[1], ValueError) and str(result[1]) == "odd 1"
    assert isinstance(result[3], ValueError) and str(result[3]) == "odd 3"


async def test_empty_items():
    meter = Meter()
    assert await m.run_pool([], meter.work, 3) == []


async def test_no_tasks_left_behind():
    before = len(asyncio.all_tasks())
    meter = Meter()
    assert await m.run_pool([1, 2, 3], meter.work, 2) == [1, 4, 9]
    assert len(asyncio.all_tasks()) == before


@pytest.mark.parametrize("workers", [0, -3])
async def test_bad_worker_count(workers):
    meter = Meter()
    with pytest.raises(ValueError, match="at least 1"):
        await m.run_pool([1], meter.work, workers)
