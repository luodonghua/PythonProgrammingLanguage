import asyncio
import threading

import pytest

from practice import load

m = load(__file__)


async def after(yields, value, log=None, name=None):
    try:
        for _ in range(yields):
            await asyncio.sleep(0)
        return value
    except asyncio.CancelledError:
        if log is not None:
            log.append(f"cancelled {name}")
        raise


async def test_first_result_picks_the_fastest():
    result = await m.first_result([lambda: after(6, "slow"), lambda: after(1, "fast"), lambda: after(3, "mid")])
    assert result == "fast"


async def test_losers_are_cancelled_and_finished_before_return():
    log = []

    async def forever():
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            log.append("cancelled forever")
            raise

    result = await m.first_result([forever, lambda: after(2, "winner", log, "b")])
    assert result == "winner"
    assert log == ["cancelled forever"]   # cleanup already ran when we got the result


async def test_no_tasks_left_running():
    before = len(asyncio.all_tasks())
    assert await m.first_result([lambda: after(5, "a"), lambda: after(1, "b")]) == "b"
    assert len(asyncio.all_tasks()) == before


async def test_winner_exception_is_raised():
    async def bad():
        raise ValueError("first failed")

    with pytest.raises(ValueError, match="first failed"):
        await m.first_result([lambda: after(5, "late"), bad])


async def test_tie_prefers_earlier_factory():
    result = await m.first_result([lambda: after(0, "one"), lambda: after(0, "two")])
    assert result == "one"


async def test_empty_list():
    with pytest.raises(ValueError, match="no jobs"):
        await m.first_result([])


async def test_run_blocking_returns_value_with_args():
    assert await m.run_blocking(pow, 2, 10) == 1024


async def test_run_blocking_uses_another_thread():
    main_thread = threading.get_ident()
    worker_thread = await m.run_blocking(threading.get_ident)
    assert isinstance(worker_thread, int)
    assert worker_thread != main_thread


async def test_run_blocking_does_not_block_the_event_loop():
    release = threading.Event()

    def wait_for_release():
        # Returns True only if the event loop ran and set the event meanwhile.
        return release.wait(timeout=5)

    task = asyncio.create_task(m.run_blocking(wait_for_release))
    await asyncio.sleep(0)       # let the worker thread start
    release.set()                # only possible if our loop is still running
    assert await task is True


async def test_read_text_async(tmp_path):
    path = tmp_path / "note.txt"
    path.write_text("héllo\nworld\n", encoding="utf-8")
    assert await m.read_text_async(path) == "héllo\nworld\n"
    assert await m.read_text_async(str(path)) == "héllo\nworld\n"
