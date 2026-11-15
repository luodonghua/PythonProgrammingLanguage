import asyncio

import pytest

from practice import load

m = load(__file__)


async def fetch(name):
    for _ in range(len(name)):      # longer names finish later
        await asyncio.sleep(0)
    if name.startswith("bad"):
        raise ValueError(f"cannot fetch {name}")
    return name.upper()


async def test_fetch_all_returns_dict_in_input_order():
    result = await m.fetch_all(["ccc", "a", "bb"], fetch)
    assert result == {"ccc": "CCC", "a": "A", "bb": "BB"}
    assert list(result) == ["ccc", "a", "bb"]


async def test_fetch_all_is_concurrent():
    started = 0
    gate = asyncio.Event()

    async def waiting(name):
        nonlocal started
        started += 1
        if started == 3:
            gate.set()
        await gate.wait()
        return name

    result = await asyncio.wait_for(m.fetch_all(["x", "y", "z"], waiting), timeout=2)
    assert list(result) == ["x", "y", "z"]


async def test_fetch_all_empty():
    assert await m.fetch_all([], fetch) == {}


async def test_failure_raises_exception_group():
    with pytest.raises(ExceptionGroup) as info:
        await m.fetch_all(["a", "bad1"], fetch)
    assert [str(e) for e in info.value.exceptions] == ["cannot fetch bad1"]


async def test_failure_cancels_the_other_tasks():
    log = []

    async def mixed(name):
        if name == "slow":
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                log.append("slow cancelled")
                raise
        raise RuntimeError("fast failure")

    with pytest.raises(ExceptionGroup):
        await m.fetch_all(["slow", "fast"], mixed)
    assert log == ["slow cancelled"]


async def test_partial_collects_results_and_errors_in_order():
    results, errors = await m.fetch_all_partial(["a", "bad1", "ccc", "bad22"], fetch)
    assert results == {"a": "A", "ccc": "CCC"}
    assert list(results) == ["a", "ccc"]
    assert errors == {
        "bad1": "ValueError: cannot fetch bad1",
        "bad22": "ValueError: cannot fetch bad22",
    }
    assert list(errors) == ["bad1", "bad22"]


async def test_partial_order_follows_input_not_finish_time():
    results, _ = await m.fetch_all_partial(["dddd", "a", "bb"], fetch)
    assert list(results) == ["dddd", "a", "bb"]


async def test_partial_all_good_and_all_bad():
    assert await m.fetch_all_partial(["a"], fetch) == ({"a": "A"}, {})
    assert await m.fetch_all_partial(["bad"], fetch) == ({}, {"bad": "ValueError: cannot fetch bad"})
