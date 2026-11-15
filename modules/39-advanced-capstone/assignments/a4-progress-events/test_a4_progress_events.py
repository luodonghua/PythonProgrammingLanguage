import asyncio

from practice import load

m = load(__file__)


def tasks(n):
    return [m.ResearchTask(id=f"t{i}", question=f"Question number {i}?") for i in range(1, n + 1)]


async def good_worker(task):
    await asyncio.sleep(0)
    return m.Finding(task_id=task.id, answer="ok", confidence=0.8)


async def collect(worker, task_list, **kwargs):
    return [event async for event in m.run_with_events(worker, task_list, **kwargs)]


async def test_sequential_run_has_an_exact_event_order():
    events = await collect(good_worker, tasks(2), trace_id="tid", max_concurrency=1)
    assert events == [
        {"type": "started", "task_id": "t1", "trace_id": "tid"},
        {"type": "finished", "task_id": "t1", "confidence": 0.8, "trace_id": "tid"},
        {"type": "started", "task_id": "t2", "trace_id": "tid"},
        {"type": "finished", "task_id": "t2", "confidence": 0.8, "trace_id": "tid"},
        {"type": "done", "ok": 2, "failed": 0, "trace_id": "tid"},
    ]


async def test_failures_are_events_and_the_run_continues():
    async def worker(task):
        if task.id == "t2":
            raise RuntimeError("model offline")
        return await good_worker(task)

    events = await collect(worker, tasks(3), trace_id="tid", max_concurrency=1)
    failed = [e for e in events if e["type"] == "failed"]
    assert failed == [{"type": "failed", "task_id": "t2", "error": "RuntimeError: model offline", "trace_id": "tid"}]
    assert events[-1] == {"type": "done", "ok": 2, "failed": 1, "trace_id": "tid"}


async def test_concurrent_run_keeps_per_task_order_and_ends_with_done():
    events = await collect(good_worker, tasks(5), trace_id="tid", max_concurrency=5)
    assert events[-1]["type"] == "done"
    assert sum(e["type"] == "done" for e in events) == 1
    for task_id in ("t1", "t2", "t3", "t4", "t5"):
        kinds = [e["type"] for e in events if e.get("task_id") == task_id]
        assert kinds == ["started", "finished"]
    # with 5 slots, every task starts before any task finishes
    kinds_in_order = [e["type"] for e in events[:-1]]
    assert kinds_in_order[:5] == ["started"] * 5


async def test_concurrency_limit_is_respected_in_the_events():
    events = await collect(good_worker, tasks(6), trace_id="tid", max_concurrency=2)
    running = peak = 0
    for event in events:
        if event["type"] == "started":
            running += 1
            peak = max(peak, running)
        elif event["type"] in ("finished", "failed"):
            running -= 1
    assert peak == 2


async def test_workers_can_read_the_trace_id():
    seen = []

    async def worker(task):
        seen.append(m.trace_id_var.get())
        return await good_worker(task)

    await collect(worker, tasks(3), trace_id="abc")
    assert seen == ["abc", "abc", "abc"]


async def test_generated_trace_id_is_used_everywhere():
    events = await collect(good_worker, tasks(2))
    ids = {e["trace_id"] for e in events}
    assert len(ids) == 1
    (generated,) = ids
    assert len(generated) == 8


async def test_context_variable_is_restored():
    assert m.trace_id_var.get() == "-"
    events = await collect(good_worker, tasks(1), trace_id="x")
    assert events[-1]["type"] == "done"
    assert m.trace_id_var.get() == "-"


async def test_no_tasks_gives_only_done():
    events = await collect(good_worker, [], trace_id="t")
    assert events == [{"type": "done", "ok": 0, "failed": 0, "trace_id": "t"}]


async def test_early_close_cancels_running_workers():
    cleaned = []
    never = asyncio.Event()

    async def worker(task):
        try:
            await never.wait()
        finally:
            cleaned.append(task.id)

    stream = m.run_with_events(worker, tasks(2), trace_id="t", max_concurrency=2)
    first = await anext(stream)
    assert first["type"] == "started"
    await stream.aclose()
    assert sorted(cleaned) == ["t1", "t2"]
