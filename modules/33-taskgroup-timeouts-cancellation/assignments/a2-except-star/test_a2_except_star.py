import asyncio

import pytest

from practice import load

m = load(__file__)


async def fail(exc):
    raise exc


def test_flatten_plain_exception():
    err = ValueError("x")
    assert m.flatten_exceptions(err) == [err]


def test_flatten_nested_groups():
    a, b, c = ValueError("a"), KeyError("b"), TypeError("c")
    group = ExceptionGroup("outer", [a, ExceptionGroup("inner", [b, c])])
    assert m.flatten_exceptions(group) == [a, b, c]


def test_flatten_keeps_order():
    a, b = ValueError("a"), ValueError("b")
    assert m.flatten_exceptions(ExceptionGroup("g", [b, a])) == [b, a]


async def test_ok_when_nothing_fails():
    async def job():
        await asyncio.sleep(0)

    assert await m.summarize_failures(job) == {"ok": True, "value_errors": [], "key_errors": []}


async def test_sorts_errors_from_a_task_group():
    async def job():
        async with asyncio.TaskGroup() as group:
            group.create_task(fail(ValueError("v1")))
            group.create_task(fail(KeyError("k1")))
            group.create_task(fail(ValueError("v2")))

    assert await m.summarize_failures(job) == {
        "ok": False,
        "value_errors": ["v1", "v2"],
        "key_errors": ["'k1'"],
    }


async def test_single_error_type():
    async def job():
        async with asyncio.TaskGroup() as group:
            group.create_task(fail(KeyError("only")))

    result = await m.summarize_failures(job)
    assert result == {"ok": False, "value_errors": [], "key_errors": ["'only'"]}


async def test_plain_exception_not_in_a_group_is_also_handled():
    async def job():
        raise ValueError("direct")

    result = await m.summarize_failures(job)
    assert result["value_errors"] == ["direct"]
    assert result["ok"] is False


async def test_other_exception_types_propagate():
    async def job():
        async with asyncio.TaskGroup() as group:
            group.create_task(fail(ValueError("handled")))
            group.create_task(fail(RuntimeError("not handled")))

    with pytest.raises(ExceptionGroup) as info:
        await m.summarize_failures(job)
    assert [type(e) for e in info.value.exceptions] == [RuntimeError]
