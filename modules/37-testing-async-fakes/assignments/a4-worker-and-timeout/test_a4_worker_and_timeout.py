import asyncio
from unittest.mock import AsyncMock

import pytest

from practice import load

m = load(__file__)


async def test_worker_processes_items_until_stop_marker():
    queue = asyncio.Queue()
    for item in (1, 2, 3, None, 99):
        queue.put_nowait(item)
    handler = AsyncMock(side_effect=lambda x: x * 10)
    results, errors = [], []
    await m.run_worker(queue, handler, results, errors)
    assert results == [10, 20, 30]
    assert errors == []
    assert [c.args for c in handler.await_args_list] == [(1,), (2,), (3,)]
    assert queue.qsize() == 1  # 99 was never taken


async def test_worker_records_errors_and_continues():
    queue = asyncio.Queue()
    for item in (1, 0, 2, None):
        queue.put_nowait(item)

    async def inverse(x):
        return 1 / x

    results, errors = [], []
    await m.run_worker(queue, inverse, results, errors)
    assert results == [1.0, 0.5]
    assert len(errors) == 1
    item, exc = errors[0]
    assert item == 0
    assert isinstance(exc, ZeroDivisionError)


async def test_task_done_is_called_for_every_item_so_join_finishes():
    queue = asyncio.Queue()
    for item in ("ok", "bad", None):
        queue.put_nowait(item)

    async def handler(x):
        if x == "bad":
            raise ValueError(x)
        return x

    results, errors = [], []
    task = asyncio.create_task(m.run_worker(queue, handler, results, errors))
    async with asyncio.timeout(1):  # a safety net: a missing task_done would hang join()
        await queue.join()
    await task
    assert results == ["ok"]
    assert len(errors) == 1


async def test_worker_waits_for_items_that_arrive_later():
    queue = asyncio.Queue()
    results = []

    async def handler(x):
        return x.upper()

    task = asyncio.create_task(m.run_worker(queue, handler, results, []))
    await asyncio.sleep(0)
    assert results == []
    await queue.put("a")
    await queue.put("b")
    await queue.put(None)
    await task
    assert results == ["A", "B"]


async def test_two_workers_share_a_queue():
    queue = asyncio.Queue()
    for i in range(6):
        queue.put_nowait(i)
    queue.put_nowait(None)
    queue.put_nowait(None)

    async def handler(x):
        await asyncio.sleep(0)
        return x

    r1, r2 = [], []
    await asyncio.gather(
        m.run_worker(queue, handler, r1, []),
        m.run_worker(queue, handler, r2, []),
    )
    assert sorted(r1 + r2) == [0, 1, 2, 3, 4, 5]


async def test_call_with_timeout_returns_result_when_fast():
    async def quick():
        return "done"

    assert await m.call_with_timeout(quick, timeout=5) == "done"


async def test_call_with_timeout_returns_default_when_stuck():
    never = asyncio.Event()  # nobody sets it, so waiting on it never ends

    async def stuck():
        await never.wait()

    assert await m.call_with_timeout(stuck, timeout=0.01, default="gave up") == "gave up"


async def test_call_with_timeout_cancels_the_call_and_runs_cleanup():
    never = asyncio.Event()
    cleaned = []

    async def stuck():
        try:
            await never.wait()
        finally:
            cleaned.append("cleanup")

    assert await m.call_with_timeout(stuck, timeout=0.01) is None
    assert cleaned == ["cleanup"]


async def test_call_with_timeout_lets_other_errors_through():
    async def broken():
        raise KeyError("boom")

    with pytest.raises(KeyError):
        await m.call_with_timeout(broken, timeout=5, default="x")
