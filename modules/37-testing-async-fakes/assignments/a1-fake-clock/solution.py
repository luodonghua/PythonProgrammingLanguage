"""Assignment 1: a fake clock for tests.

Code that waits (``asyncio.sleep``) or reads the time (``time.monotonic``) is
hard to test: real waiting is slow and the result depends on timing. The fix is
to pass the clock in as an argument and use a fake one in tests. A fake clock
never waits. ``sleep`` only moves the time forward and remembers the request.
"""

import asyncio


class FakeClock:
    """A clock that only moves when told to.

    * ``FakeClock(start=0.0)``: the current time starts at ``start``.
    * ``now()`` returns the current time (a float).
    * ``advance(seconds)`` moves the time forward. A negative number raises
      ``ValueError``.
    * ``await sleep(seconds)`` does NOT really wait. It appends ``seconds`` to
      the list ``self.sleeps``, advances the time by ``seconds``, and then
      gives other tasks a chance to run with ``await asyncio.sleep(0)``.
      A negative number raises ``ValueError`` (and records nothing).
    """

    def __init__(self, start: float = 0.0):
        self._now = float(start)
        self.sleeps: list[float] = []

    def now(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("cannot move time backwards")
        self._now += seconds

    async def sleep(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("cannot sleep a negative time")
        self.sleeps.append(seconds)
        self.advance(seconds)
        await asyncio.sleep(0)


async def ticker(clock, interval: float, count: int) -> list[float]:
    """Read ``clock.now()`` ``count`` times, waiting ``interval`` between reads.

    Use ``await clock.sleep(interval)`` between two reads, but not after the
    last one. Return the list of times that were read. ``count`` of 0 gives ``[]``.

    With a ``FakeClock(100)``, ``ticker(clock, 10, 3)`` returns ``[100, 110, 120]``
    at once, and ``clock.sleeps`` is ``[10, 10]``.
    """
    times: list[float] = []
    for i in range(count):
        if i > 0:
            await clock.sleep(interval)
        times.append(clock.now())
    return times


if __name__ == "__main__":

    async def demo() -> None:
        clock = FakeClock(100)
        print(await ticker(clock, 10, 3), clock.sleeps)

    asyncio.run(demo())
