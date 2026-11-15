import asyncio

import pytest

from practice import load

m = load(__file__)


def tasks(n):
    return [m.ResearchTask(id=f"t{i}", question=f"Question number {i}?") for i in range(1, n + 1)]


def finding_for(task, answer=None):
    return m.Finding(task_id=task.id, answer=answer or f"answer {task.id}", confidence=0.5)


async def test_all_succeed_in_task_order_even_if_they_finish_in_another_order():
    async def worker(task):
        # t1 is the slowest, t3 the fastest
        for _ in range(4 - int(task.id[1:])):
            await asyncio.sleep(0)
        return finding_for(task)

    result = await m.run_all(worker, tasks(3), max_concurrency=3)
    assert [f.task_id for f in result.findings] == ["t1", "t2", "t3"]
    assert result.failures == {}


async def test_partial_failures_are_collected():
    async def worker(task):
        if task.id in ("t2", "t4"):
            raise RuntimeError(f"boom {task.id}")
        return finding_for(task)

    result = await m.run_all(worker, tasks(5))
    assert [f.task_id for f in result.findings] == ["t1", "t3", "t5"]
    assert result.failures == {"t2": "RuntimeError: boom t2", "t4": "RuntimeError: boom t4"}


async def test_all_fail():
    async def worker(task):
        raise ValueError("no")

    result = await m.run_all(worker, tasks(2))
    assert result.findings == []
    assert set(result.failures) == {"t1", "t2"}


async def test_concurrency_limit():
    state = {"active": 0, "peak": 0}

    async def worker(task):
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        for _ in range(5):
            await asyncio.sleep(0)
        state["active"] -= 1
        return finding_for(task)

    result = await m.run_all(worker, tasks(8), max_concurrency=3)
    assert len(result.findings) == 8
    assert state["peak"] == 3


async def test_workers_really_run_together():
    # each worker waits for the other one, so sequential execution would deadlock
    gate_a, gate_b = asyncio.Event(), asyncio.Event()

    async def worker(task):
        mine, other = (gate_a, gate_b) if task.id == "t1" else (gate_b, gate_a)
        mine.set()
        await other.wait()
        return finding_for(task)

    async with asyncio.timeout(2):
        result = await m.run_all(worker, tasks(2), max_concurrency=2)
    assert len(result.findings) == 2


async def test_empty_task_list():
    async def worker(task):
        raise AssertionError("must not be called")

    result = await m.run_all(worker, [])
    assert result.findings == [] and result.failures == {}


async def test_duplicate_ids_are_rejected_before_anything_runs():
    called = []

    async def worker(task):
        called.append(task.id)
        return finding_for(task)

    duplicate = [m.ResearchTask(id="x", question="First question"), m.ResearchTask(id="x", question="Second question")]
    with pytest.raises(ValueError):
        await m.run_all(worker, duplicate)
    assert called == []


async def test_fail_fast_raises_an_exception_group_and_cancels_the_rest():
    cleaned = []
    never = asyncio.Event()

    async def worker(task):
        if task.id == "t1":
            await asyncio.sleep(0)
            raise RuntimeError("fatal")
        try:
            await never.wait()  # would hang forever unless cancelled
        finally:
            cleaned.append(task.id)
        return finding_for(task)

    async with asyncio.timeout(2):
        with pytest.raises(ExceptionGroup) as info:
            await m.run_all(worker, tasks(3), max_concurrency=3, fail_fast=True)
    assert [type(e) for e in info.value.exceptions] == [RuntimeError]
    assert sorted(cleaned) == ["t2", "t3"]


async def test_fail_fast_without_errors_behaves_normally():
    async def worker(task):
        return finding_for(task)

    result = await m.run_all(worker, tasks(3), fail_fast=True)
    assert [f.task_id for f in result.findings] == ["t1", "t2", "t3"]
