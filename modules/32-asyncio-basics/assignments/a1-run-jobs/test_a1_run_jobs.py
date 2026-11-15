import asyncio

from practice import load

m = load(__file__)


async def test_results_follow_input_order_not_finish_order():
    async def job(value, yields):
        for _ in range(yields):
            await asyncio.sleep(0)
        return value

    jobs = [lambda: job("slow", 5), lambda: job("fast", 0), lambda: job("medium", 2)]
    assert await m.run_all(jobs) == ["slow", "fast", "medium"]


async def test_jobs_really_run_at_the_same_time():
    started = 0
    all_started = asyncio.Event()

    async def job(n):
        nonlocal started
        started += 1
        if started == 3:
            all_started.set()
        await all_started.wait()   # would wait forever if jobs ran one after another
        return n

    jobs = [lambda n=n: job(n) for n in range(3)]
    assert await asyncio.wait_for(m.run_all(jobs), timeout=2) == [0, 1, 2]


async def test_empty():
    assert await m.run_all([]) == []


async def test_exception_propagates():
    async def good():
        return 1

    async def bad():
        raise ValueError("boom")

    try:
        await m.run_all([good, bad])
    except ValueError as exc:
        assert str(exc) == "boom"
    else:
        raise AssertionError("ValueError expected")


async def test_safe_labels_each_outcome():
    async def good(n):
        await asyncio.sleep(0)
        return n

    async def bad():
        raise KeyError("missing")

    async def worse():
        raise RuntimeError("nope")

    result = await m.run_all_safe([lambda: good(1), bad, lambda: good(2), worse])
    assert result == [("ok", 1), ("error", "'missing'"), ("ok", 2), ("error", "nope")]


async def test_safe_empty_and_all_ok():
    async def one():
        return "x"

    assert await m.run_all_safe([]) == []
    assert await m.run_all_safe([one, one]) == [("ok", "x"), ("ok", "x")]
