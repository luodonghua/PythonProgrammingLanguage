"""Assignment 1: fetch JSON with retries and exponential backoff.

Network calls fail in two ways. Some failures are temporary (a dropped
connection, a 503 from an overloaded server), so trying again can work. Others
are permanent (404 Not Found), so retrying only wastes time.
"""

import asyncio

import httpx


async def fetch_json(
    client: httpx.AsyncClient,
    url: str,
    *,
    retries: int = 3,
    base_delay: float = 0.5,
    sleep=asyncio.sleep,
):
    """GET ``url`` with ``client`` and return the decoded JSON body.

    ``retries`` is the number of extra attempts after the first one, so the
    function makes at most ``retries + 1`` requests.

    * A transport problem (``httpx.TransportError``, which includes timeouts and
      connection errors) is temporary: retry.
    * An HTTP status of 500 or more is temporary: retry.
    * A status of 400-499 is permanent: raise ``httpx.HTTPStatusError`` at once
      (use ``response.raise_for_status()``) and do not retry.
    * Before retry number n (n = 1, 2, 3 ...) call ``await sleep(delay)`` with
      ``delay = base_delay * 2 ** (n - 1)``. Do not sleep before the first try.
    * When all attempts fail, raise the last error.

    ``sleep`` is a parameter so that tests can pass a fake and not wait.
    """
    # TODO: write the retry loop.
    ...


if __name__ == "__main__":

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"path": request.url.path})

    async def demo() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, base_url="https://x.test") as c:
            print(await fetch_json(c, "/hello"))

    asyncio.run(demo())
