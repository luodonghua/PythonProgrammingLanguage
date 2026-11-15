from practice import load

m = load(__file__)


async def test_handle_records_own_id():
    assert await m.handle("x", 3) == ["x", "x", "x"]


async def test_handle_zero_steps():
    assert await m.handle("x", 0) == []


async def test_tasks_do_not_see_each_other():
    results = await m.handle_all(["r1", "r2", "r3"], steps=4)
    assert results == [["r1"] * 4, ["r2"] * 4, ["r3"] * 4]


async def test_result_order_matches_ids():
    results = await m.handle_all(["b", "a"], steps=1)
    assert results == [["b"], ["a"]]


async def test_caller_context_is_unchanged():
    assert m.request_id.get() == "-"
    assert await m.handle_all(["r1", "r2"], steps=1) == [["r1"], ["r2"]]
    assert m.request_id.get() == "-"


async def test_handle_all_empty():
    assert await m.handle_all([]) == []


async def test_child_inherits_and_isolates():
    assert await m.child_inherits("parent-1") == ("parent-1", "parent-1")
