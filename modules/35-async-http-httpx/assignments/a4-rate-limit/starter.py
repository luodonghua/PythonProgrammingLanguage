"""Assignment 4: obey "429 Too Many Requests" and the Retry-After header.

When you send requests too fast, many APIs answer with status 429 and a
``Retry-After`` header that says how many seconds to wait. A polite client
waits that long and tries again.
"""

import asyncio

import httpx


class RateLimitError(Exception):
    """Raised when the server keeps answering 429 after every allowed attempt."""


def retry_after_seconds(response: httpx.Response, default: float = 1.0, maximum: float = 30.0) -> float:
    """Return how long to wait, in seconds, according to the ``Retry-After`` header.

    * A header such as ``"3"`` or ``"2.5"`` gives that number as a float.
    * A missing header, text that is not a number, or a negative number gives ``default``.
    * Never return more than ``maximum``.
    """
    # TODO: read response.headers.get("Retry-After") and convert it carefully.
    ...


async def get_with_rate_limit(
    client: httpx.AsyncClient,
    url: str,
    *,
    max_attempts: int = 4,
    sleep=asyncio.sleep,
) -> httpx.Response:
    """GET ``url``. Wait and retry while the server answers 429.

    * Make at most ``max_attempts`` requests.
    * After a 429 response (and only if attempts remain), call
      ``await sleep(retry_after_seconds(response))`` and try again.
    * If the last allowed attempt is also 429, raise ``RateLimitError``.
    * Any other response is returned after ``response.raise_for_status()``, so a
      404 or 500 raises ``httpx.HTTPStatusError`` and is not retried here.
    """
    # TODO: write the loop.
    ...


if __name__ == "__main__":
    answers = [httpx.Response(429, headers={"Retry-After": "2"}), httpx.Response(200, json={"ok": 1})]

    def handler(request: httpx.Request) -> httpx.Response:
        return answers.pop(0)

    async def demo() -> None:
        async def fake_sleep(seconds: float) -> None:
            print("would sleep", seconds)

        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, base_url="https://x.test") as c:
            response = await get_with_rate_limit(c, "/x", sleep=fake_sleep)
            print(response.json())

    asyncio.run(demo())
