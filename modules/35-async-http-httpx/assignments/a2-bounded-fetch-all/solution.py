"""Assignment 2: fetch many URLs at once, but only a few at a time.

Starting hundreds of requests together can overwhelm a server (and get you
blocked). An ``asyncio.Semaphore`` lets at most N tasks run a section of code
at the same moment.
"""

import asyncio

import httpx


async def fetch_all(client: httpx.AsyncClient, urls: list[str], *, limit: int = 5) -> list:
    """GET every URL concurrently and return the JSON bodies in the same order as ``urls``.

    * At most ``limit`` requests may be in progress at the same moment.
    * If one URL fails (a transport error such as ``httpx.ConnectError``, or an
      HTTP status of 400 or more), its entry in the result is ``None``. The
      other URLs are not affected.
    * An empty ``urls`` list gives ``[]``.

    Hint: write a small inner coroutine that does ``async with semaphore:`` and
    one request, then run all of them with ``asyncio.gather``.
    """
    semaphore = asyncio.Semaphore(limit)

    async def fetch_one(url: str):
        async with semaphore:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except (httpx.TransportError, httpx.HTTPStatusError):
                return None

    return await asyncio.gather(*(fetch_one(url) for url in urls))


if __name__ == "__main__":

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"path": request.url.path})

    async def demo() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, base_url="https://x.test") as c:
            print(await fetch_all(c, ["/a", "/b", "/c"], limit=2))

    asyncio.run(demo())
