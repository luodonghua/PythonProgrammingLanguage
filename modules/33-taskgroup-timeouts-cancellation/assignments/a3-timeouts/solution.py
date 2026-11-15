"""Assignment 3: Timeouts and cancellation.

`asyncio.timeout(seconds)` cancels the code inside the block when time runs
out, and the block then raises `TimeoutError`. A cancelled coroutine receives
`asyncio.CancelledError` at its current `await`. It should clean up in a
`finally` block and let the error go on.
"""

import asyncio
from collections.abc import Awaitable, Callable


async def fetch_or_default(factory: Callable[[], Awaitable], seconds: float, default=None):
    """Return `await factory()`, or `default` if it takes longer than `seconds`.

    Use `async with asyncio.timeout(seconds):` and catch `TimeoutError`.
    Other exceptions raised by the job propagate unchanged.
    """
    try:
        async with asyncio.timeout(seconds):
            return await factory()
    except TimeoutError:
        return default


async def each_with_timeout(
    factories: list[Callable[[], Awaitable]], seconds: float
) -> list:
    """Run all jobs concurrently, each with its own time limit.

    Return a list in input order. A job that finishes in time gives its
    result. A job that times out gives None. Use `fetch_or_default` and
    `asyncio.gather`.
    """
    return list(
        await asyncio.gather(*(fetch_or_default(f, seconds, None) for f in factories))
    )


async def cancel_and_wait(task: asyncio.Task) -> bool:
    """Cancel `task`, wait until it has stopped, and report what happened.

    Return True if the task ended because of the cancellation, False if it had
    already finished (with a result or an error) before we cancelled it.
    A task that already failed with an error must not raise from here.
    Steps: `task.cancel()`, then `await task` inside try/except CancelledError,
    then look at `task.cancelled()`.
    """
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    except Exception:
        pass
    return task.cancelled()


async def download(log: list[str], gate: asyncio.Event) -> str:
    """A pretend download that always cleans up.

    Append "open" to `log`, then wait for `gate` to be set, then append
    "done" and return "data". Whatever happens (success, error or
    cancellation), append "close" last. Use try/finally.
    """
    log.append("open")
    try:
        await gate.wait()
        log.append("done")
        return "data"
    finally:
        log.append("close")


if __name__ == "__main__":
    async def hang() -> str:
        await asyncio.Event().wait()
        return "never"

    async def quick() -> str:
        return "fast"

    async def main() -> None:
        print(await fetch_or_default(hang, 0.01, default="timed out"))
        print(await each_with_timeout([quick, hang], 0.01))

    asyncio.run(main())
