import asyncio

import pytest

from practice import load

m = load(__file__)


class FakeSleep:
    def __init__(self):
        self.calls = []

    async def __call__(self, seconds):
        self.calls.append(seconds)


async def test_ticker_items_and_sleeps():
    sleep = FakeSleep()
    items = [n async for n in m.ticker(4, interval=0.5, sleep=sleep)]
    assert items == [0, 1, 2, 3]
    assert sleep.calls == [0.5, 0.5, 0.5]   # between items only


async def test_ticker_single_and_empty():
    sleep = FakeSleep()
    assert [n async for n in m.ticker(1, sleep=sleep)] == [0]
    assert [n async for n in m.ticker(0, sleep=sleep)] == []
    assert sleep.calls == []


async def test_ticker_is_lazy():
    sleep = FakeSleep()
    gen = m.ticker(5, interval=2, sleep=sleep)
    assert sleep.calls == []
    assert await anext(gen) == 0
    assert sleep.calls == []         # the wait comes after the item was handed out
    assert await anext(gen) == 1
    assert sleep.calls == [2]
    await gen.aclose()


@pytest.mark.parametrize(
    ("text", "size", "expected"),
    [
        ("abcdefg", 3, ["abc", "def", "g"]),
        ("abcdef", 3, ["abc", "def"]),
        ("ab", 5, ["ab"]),
        ("", 3, []),
        ("héllo", 2, ["hé", "ll", "o"]),
    ],
)
async def test_chunk_text(text, size, expected):
    assert [c async for c in m.chunk_text(text, size)] == expected


async def test_chunk_text_bad_size():
    with pytest.raises(ValueError, match="at least 1"):
        [c async for c in m.chunk_text("abc", 0)]


async def test_chunk_text_yields_to_the_event_loop():
    seen = []

    async def spy():
        for _ in range(3):
            seen.append("spy")
            await asyncio.sleep(0)

    task = asyncio.create_task(spy())
    chunks = []
    async for chunk in m.chunk_text("abcdef", 2):
        chunks.append(chunk)
        seen.append(chunk)
    await task
    assert chunks == ["ab", "cd", "ef"]
    assert "spy" in seen[:3]          # the spy task ran while we were streaming


async def test_collect():
    async def numbers():
        for n in range(4):
            yield n * n

    assert await m.collect(numbers()) == [0, 1, 4, 9]


async def test_collect_empty():
    async def nothing():
        return
        yield

    assert await m.collect(nothing()) == []


def make_source(log):
    async def source():
        try:
            for n in range(100):
                log.append(f"made {n}")
                yield n
        finally:
            log.append("source closed")

    return source()


async def test_take_returns_first_items_and_closes_source():
    log = []
    assert await m.take(make_source(log), 3) == [0, 1, 2]
    assert log == ["made 0", "made 1", "made 2", "source closed"]


async def test_take_more_than_available():
    async def short():
        yield "a"
        yield "b"

    assert await m.take(short(), 10) == ["a", "b"]


async def test_take_zero_closes_without_reading():
    log = []
    assert await m.take(make_source(log), 0) == []
    assert "made 0" not in log


async def test_session_success_and_error():
    log = []
    async with m.session(log, "db") as name:
        assert name == "db"
        log.append("working")
    assert log == ["open db", "working", "close db"]

    log.clear()
    with pytest.raises(RuntimeError):
        async with m.session(log, "api"):
            raise RuntimeError("boom")
    assert log == ["open api", "close api"]
