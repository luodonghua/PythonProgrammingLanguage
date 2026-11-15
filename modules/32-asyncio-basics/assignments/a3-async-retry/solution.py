"""Assignment 3: Retry an async call with a growing delay.

Network calls fail now and then. A retry helper tries again after a short wait.
The wait uses `await sleep(...)`, never `time.sleep`, which would freeze the
whole event loop. The `sleep` function is a parameter so tests can replace it
and never wait for real.
"""

import asyncio
from collections.abc import Awaitable, Callable


async def retry_async(
    func: Callable[[], Awaitable],
    attempts: int = 3,
    delay: float = 1.0,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
    sleep: Callable[[float], Awaitable] = asyncio.sleep,
):
    """Call `await func()` up to `attempts` times and return its result.

    - If the call raises an exception listed in `retry_on`, wait and try again.
    - The wait doubles each time: `delay`, then `2 * delay`, then `4 * delay`...
      Call `await sleep(seconds)` between attempts only (no wait after the last
      failure, none after success).
    - After the last attempt fails, re-raise that last exception.
    - An exception that is not in `retry_on` propagates at once, with no retry.
    - Raise ValueError("attempts must be at least 1") if attempts < 1.
    """
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    wait = delay
    for attempt in range(1, attempts + 1):
        try:
            return await func()
        except retry_on:
            if attempt == attempts:
                raise
            await sleep(wait)
            wait *= 2


if __name__ == "__main__":
    calls = 0

    async def flaky() -> str:
        global calls
        calls += 1
        if calls < 3:
            raise ConnectionError("try again")
        return f"ok after {calls} calls"

    async def no_wait(seconds: float) -> None:
        print(f"(would wait {seconds} s)")

    print(asyncio.run(retry_async(flaky, attempts=4, delay=0.5, sleep=no_wait)))
