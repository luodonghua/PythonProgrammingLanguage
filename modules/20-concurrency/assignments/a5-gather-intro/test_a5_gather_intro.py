import asyncio

from practice import load

m = load(__file__)


async def test_double_all_keeps_order():
    assert await m.double_all([3, 1, 2]) == [6, 2, 4]


async def test_double_all_empty():
    assert await m.double_all([]) == []
    assert await m.double_all([5]) == [10]


async def test_double_all_returns_list():
    result = await m.double_all([1, 2])
    assert isinstance(result, list)


async def test_jobs_overlap():
    # Each job waits for the other, so this only finishes when both run together.
    a_started = asyncio.Event()
    b_started = asyncio.Event()

    async def job_a():
        a_started.set()
        await asyncio.wait_for(b_started.wait(), timeout=2)
        return "a"

    async def job_b():
        b_started.set()
        await asyncio.wait_for(a_started.wait(), timeout=2)
        return "b"

    assert await m.run_all([job_a, job_b]) == ["a", "b"]


async def test_run_all_order_is_job_order():
    order = []

    async def slow():
        for _ in range(3):
            await asyncio.sleep(0)
        order.append("slow")
        return "slow"

    async def fast():
        order.append("fast")
        return "fast"

    assert await m.run_all([slow, fast]) == ["slow", "fast"]
    assert order == ["fast", "slow"]


async def test_run_all_keeps_errors_as_results():
    async def ok():
        return 1

    async def bad():
        raise ValueError("nope")

    results = await m.run_all([ok, bad, ok])
    assert results[0] == 1
    assert isinstance(results[1], ValueError)
    assert str(results[1]) == "nope"
    assert results[2] == 1


async def test_count_finished():
    async def ok():
        return 1

    async def bad():
        raise RuntimeError

    assert await m.count_finished([ok, bad, bad, ok, ok]) == (3, 2)
    assert await m.count_finished([]) == (0, 0)
    assert await m.count_finished([ok]) == (1, 0)
