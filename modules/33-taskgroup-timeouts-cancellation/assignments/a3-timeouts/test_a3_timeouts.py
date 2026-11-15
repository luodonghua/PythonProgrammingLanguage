import asyncio

import pytest

from practice import load

m = load(__file__)

SHORT = 0.01   # only used for jobs that can never finish, so the outcome is certain
LONG = 30      # only used for jobs that finish at once


async def hang():
    await asyncio.Event().wait()
    return "never"


async def quick(value="fast"):
    await asyncio.sleep(0)
    return value


async def test_returns_result_when_in_time():
    assert await m.fetch_or_default(quick, LONG, default="slow") == "fast"


async def test_returns_default_on_timeout():
    assert await m.fetch_or_default(hang, SHORT, default="slow") == "slow"


async def test_default_is_none_when_not_given():
    assert await m.fetch_or_default(hang, SHORT) is None
    assert await m.fetch_or_default(quick, LONG) == "fast"


async def test_falsy_result_is_not_replaced_by_default():
    assert await m.fetch_or_default(lambda: quick(0), LONG, default="slow") == 0


async def test_job_errors_propagate():
    async def bad():
        raise KeyError("oops")

    with pytest.raises(KeyError):
        await m.fetch_or_default(bad, LONG, default="slow")


async def test_timeout_cancels_the_job():
    log = []

    async def job():
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            log.append("cancelled")
            raise

    await m.fetch_or_default(job, SHORT)
    assert log == ["cancelled"]


async def test_each_with_timeout_mixed_in_input_order():
    jobs = [lambda: quick("a"), hang, lambda: quick("c"), hang]
    assert await m.each_with_timeout(jobs, SHORT) == ["a", None, "c", None]


async def test_each_with_timeout_empty():
    assert await m.each_with_timeout([], SHORT) == []


async def test_cancel_and_wait_on_running_task():
    task = asyncio.create_task(hang())
    await asyncio.sleep(0)
    assert await m.cancel_and_wait(task) is True
    assert task.cancelled()


async def test_cancel_and_wait_on_finished_task():
    task = asyncio.create_task(quick())
    await task
    assert await m.cancel_and_wait(task) is False
    assert task.result() == "fast"


async def test_cancel_and_wait_on_failed_task():
    async def bad():
        raise RuntimeError("x")

    task = asyncio.create_task(bad())
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    assert task.done()
    assert await m.cancel_and_wait(task) is False
    assert isinstance(task.exception(), RuntimeError)


async def test_download_success():
    log = []
    gate = asyncio.Event()
    gate.set()
    assert await m.download(log, gate) == "data"
    assert log == ["open", "done", "close"]


async def test_download_cleans_up_when_cancelled():
    log = []
    task = asyncio.create_task(m.download(log, asyncio.Event()))
    await asyncio.sleep(0)
    assert await m.cancel_and_wait(task) is True
    assert log == ["open", "close"]


async def test_download_cleans_up_on_timeout():
    log = []
    result = await m.fetch_or_default(lambda: m.download(log, asyncio.Event()), SHORT, default="gave up")
    assert result == "gave up"
    assert log == ["open", "close"]
