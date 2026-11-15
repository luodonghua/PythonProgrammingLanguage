import asyncio

from practice import load

m = load(__file__)


def call(name, arguments, id):
    return {"id": id, "name": name, "arguments": arguments}


async def test_results_are_in_call_order():
    reg = m.ToolRegistry()

    @reg.tool
    async def pause(rounds: int, label: str) -> str:
        for _ in range(rounds):
            await asyncio.sleep(0)  # the first call is the slowest
        return label

    calls = [
        call("pause", '{"rounds": 5, "label": "slow"}', "a"),
        call("pause", '{"rounds": 2, "label": "medium"}', "b"),
        call("pause", '{"rounds": 0, "label": "fast"}', "c"),
    ]
    results = await m.dispatch_all(reg, calls)
    assert [(r["tool_call_id"], r["content"]) for r in results] == [("a", "slow"), ("b", "medium"), ("c", "fast")]


async def test_calls_really_run_at_the_same_time():
    # Each tool waits for the other one. Run one after the other, they would wait forever.
    reg = m.ToolRegistry()
    event_a, event_b = asyncio.Event(), asyncio.Event()

    @reg.tool
    async def first() -> str:
        event_a.set()
        await event_b.wait()
        return "first done"

    @reg.tool
    async def second() -> str:
        event_b.set()
        await event_a.wait()
        return "second done"

    calls = [call("first", "{}", "1"), call("second", "{}", "2")]
    async with asyncio.timeout(2):  # a safety net: fail instead of hanging
        results = await m.dispatch_all(reg, calls)
    assert [r["content"] for r in results] == ["first done", "second done"]


async def test_one_failure_does_not_cancel_the_others():
    reg = m.ToolRegistry()
    finished = []

    @reg.tool
    async def good(x: int) -> int:
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        finished.append(x)
        return x

    @reg.tool
    def bad() -> str:
        raise RuntimeError("tool crashed")

    calls = [call("good", '{"x": 1}', "a"), call("bad", "{}", "b"), call("good", '{"x": 3}', "c"), call("missing", "{}", "d")]
    results = await m.dispatch_all(reg, calls)
    assert results[0]["content"] == "1"
    assert results[1]["content"].startswith("error:") and "tool crashed" in results[1]["content"]
    assert results[2]["content"] == "3"
    assert results[3]["content"].startswith("error:")
    assert sorted(finished) == [1, 3]


async def test_limit_bounds_the_concurrency():
    reg = m.ToolRegistry()
    state = {"active": 0, "peak": 0}

    @reg.tool
    async def work() -> str:
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        for _ in range(4):
            await asyncio.sleep(0)
        state["active"] -= 1
        return "ok"

    calls = [call("work", "{}", str(i)) for i in range(7)]
    results = await m.dispatch_all(reg, calls, limit=2)
    assert len(results) == 7
    assert all(r["content"] == "ok" for r in results)
    assert state["peak"] == 2


async def test_without_limit_everything_runs_together():
    reg = m.ToolRegistry()
    state = {"active": 0, "peak": 0}

    @reg.tool
    async def work() -> str:
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        for _ in range(4):
            await asyncio.sleep(0)
        state["active"] -= 1
        return "ok"

    await m.dispatch_all(reg, [call("work", "{}", str(i)) for i in range(5)])
    assert state["peak"] == 5


async def test_empty_list():
    assert await m.dispatch_all(m.ToolRegistry(), []) == []
