"""Assignment 3: a retrying fetcher, built so that it is easy to test.

The class takes everything that is slow or random from outside: the client and
the ``sleep`` function. The tests give it fakes, so a retry with a 4-second
backoff takes no time at all.
"""

import asyncio


class RetryingFetcher:
    """Fetch URLs with ``client.get(url)``, retrying temporary failures.

    ``RetryingFetcher(client, *, retries=2, delay=1.0, sleep=asyncio.sleep,
    retry_on=(ConnectionError, TimeoutError))``

    ``await fetcher.fetch(url)``:

    * Call ``await self.client.get(url)`` and return its result.
    * If the call raises an exception that is an instance of ``retry_on``,
      wait with ``await self.sleep(delay * 2 ** n)``, where ``n`` is 0 before
      the first retry, 1 before the second, and so on. Then call again.
    * Make at most ``retries + 1`` calls. When the last call fails too, raise
      its exception.
    * An exception that is not in ``retry_on`` is raised at once, with no retry
      and no sleep.
    * ``self.attempts`` is the total number of ``client.get`` calls made by
      this fetcher so far (over all ``fetch`` calls).
    """

    def __init__(
        self,
        client,
        *,
        retries: int = 2,
        delay: float = 1.0,
        sleep=asyncio.sleep,
        retry_on: tuple[type[BaseException], ...] = (ConnectionError, TimeoutError),
    ):
        self.client = client
        self.retries = retries
        self.delay = delay
        self.sleep = sleep
        self.retry_on = retry_on
        self.attempts = 0

    async def fetch(self, url: str):
        # TODO: loop up to retries + 1 times; count attempts; sleep before retrying.
        ...


if __name__ == "__main__":

    class Flaky:
        def __init__(self):
            self.calls = 0

        async def get(self, url):
            self.calls += 1
            if self.calls < 3:
                raise ConnectionError("down")
            return f"body of {url}"

    async def demo() -> None:
        waits = []

        async def fake_sleep(seconds):
            waits.append(seconds)

        fetcher = RetryingFetcher(Flaky(), sleep=fake_sleep)
        print(await fetcher.fetch("/a"), waits)

    asyncio.run(demo())
