"""Assignment 2: a scripted fake client that records every call.

A *fake* is a simple working replacement for a real dependency. This one stands
in for an HTTP client. You give it a script (the answers it must return, in
order). It also remembers how it was called, which makes it a *spy* too.
"""

import asyncio


class FakeClient:
    """Pretend client with a ``get`` method.

    * ``FakeClient(script)``: ``script`` is a list. Each item is either a value
      to return or an exception instance to raise. Copy the list, so the
      caller's list is not changed.
    * ``await client.get(url, **params)``:
        1. record the call as the tuple ``(url, params)`` (``params`` is a
           dict) in ``self.calls``;
        2. let other tasks run with ``await asyncio.sleep(0)``;
        3. take the next item of the script: raise it if it is an exception
           (``isinstance(item, BaseException)``), otherwise return it;
        4. when the script is empty, raise ``AssertionError("script exhausted")``
           (the code under test made more calls than the test expected).
    * ``call_count`` (property) is the number of calls so far, also failed ones.
    * ``assert_all_used()`` raises ``AssertionError`` if script items are left.
    """

    def __init__(self, script: list):
        # TODO: keep a copy of the script and an empty list called calls.
        ...

    @property
    def call_count(self) -> int:
        # TODO
        ...

    async def get(self, url: str, **params):
        # TODO: follow steps 1 to 4 of the class docstring.
        ...

    def assert_all_used(self) -> None:
        # TODO
        ...


if __name__ == "__main__":

    async def demo() -> None:
        client = FakeClient([{"id": 1}, ConnectionError("down")])
        print(await client.get("/a", page=1))
        try:
            await client.get("/b")
        except ConnectionError as exc:
            print("raised:", exc)
        print(client.calls)

    asyncio.run(demo())
