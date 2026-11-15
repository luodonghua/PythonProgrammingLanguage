import pytest

from practice import load

m = load(__file__)


async def test_returns_script_items_in_order():
    client = m.FakeClient([{"a": 1}, "two", 3])
    assert await client.get("/x") == {"a": 1}
    assert await client.get("/x") == "two"
    assert await client.get("/x") == 3


async def test_raises_exception_items():
    client = m.FakeClient([ConnectionError("down"), "ok"])
    with pytest.raises(ConnectionError, match="down"):
        await client.get("/x")
    assert await client.get("/x") == "ok"


async def test_records_calls_with_params():
    client = m.FakeClient(["a", "b"])
    await client.get("/users", page=2, size=10)
    await client.get("/items")
    assert client.calls == [("/users", {"page": 2, "size": 10}), ("/items", {})]
    assert client.call_count == 2


async def test_failed_calls_are_counted_too():
    client = m.FakeClient([TimeoutError()])
    with pytest.raises(TimeoutError):
        await client.get("/x")
    assert client.call_count == 1


async def test_exhausted_script_raises_assertion_error():
    client = m.FakeClient(["only"])
    await client.get("/x")
    with pytest.raises(AssertionError, match="exhausted"):
        await client.get("/x")
    assert client.call_count == 2


async def test_script_list_is_copied():
    script = ["a", "b"]
    client = m.FakeClient(script)
    assert await client.get("/x") == "a"
    assert script == ["a", "b"]


async def test_assert_all_used():
    client = m.FakeClient(["a", "b"])
    await client.get("/x")
    with pytest.raises(AssertionError):
        client.assert_all_used()
    await client.get("/x")
    client.assert_all_used()  # does not raise now


async def test_get_yields_to_other_tasks():
    import asyncio

    client = m.FakeClient(["a"])
    seen = []

    async def other():
        seen.append("other ran")

    task = asyncio.create_task(other())
    await client.get("/x")
    assert seen == ["other ran"]
    await task
