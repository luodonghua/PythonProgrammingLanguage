import pytest

from practice import load

m = load(__file__)


def test_now_and_start():
    assert m.FakeClock().now() == 0.0
    assert m.FakeClock(start=42).now() == 42.0


def test_advance():
    clock = m.FakeClock(10)
    clock.advance(2.5)
    clock.advance(0)
    assert clock.now() == 12.5


def test_advance_rejects_negative():
    clock = m.FakeClock(10)
    with pytest.raises(ValueError):
        clock.advance(-1)
    assert clock.now() == 10


async def test_sleep_records_and_advances_without_waiting():
    clock = m.FakeClock()
    await clock.sleep(3600)  # a real sleep of one hour would hang the test
    await clock.sleep(0.5)
    assert clock.sleeps == [3600, 0.5]
    assert clock.now() == 3600.5


async def test_sleep_rejects_negative_and_records_nothing():
    clock = m.FakeClock()
    with pytest.raises(ValueError):
        await clock.sleep(-1)
    assert clock.sleeps == []
    assert clock.now() == 0


async def test_sleep_lets_other_tasks_run():
    import asyncio

    clock = m.FakeClock()
    order = []

    async def other():
        order.append("other")

    task = asyncio.create_task(other())
    await clock.sleep(1)
    order.append("after sleep")
    await task
    assert order == ["other", "after sleep"]


async def test_ticker():
    clock = m.FakeClock(100)
    assert await m.ticker(clock, 10, 3) == [100, 110, 120]
    assert clock.sleeps == [10, 10]


async def test_ticker_edge_counts():
    clock = m.FakeClock(5)
    assert await m.ticker(clock, 10, 0) == []
    assert await m.ticker(clock, 10, 1) == [5]
    assert clock.sleeps == []
