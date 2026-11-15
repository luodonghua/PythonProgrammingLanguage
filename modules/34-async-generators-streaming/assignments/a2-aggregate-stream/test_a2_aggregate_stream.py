import asyncio

import pytest

from practice import load

m = load(__file__)


async def stream_of(items, log=None):
    for item in items:
        if log is not None:
            log.append(f"produced {item!r}")
        await asyncio.sleep(0)
        yield item


async def test_running_total():
    assert [t async for t in m.running_total(stream_of([1, 2, 3, 4]))] == [1, 3, 6, 10]


async def test_running_total_floats_and_empty():
    assert [t async for t in m.running_total(stream_of([0.5, 0.25]))] == [0.5, 0.75]
    assert [t async for t in m.running_total(stream_of([]))] == []


async def test_running_total_is_incremental():
    log = []
    gen = m.running_total(stream_of([5, 5, 5], log))
    assert await anext(gen) == 5
    assert log == ["produced 5"]       # only one item was read so far
    await gen.aclose()


async def test_aggregate():
    assert await m.aggregate(stream_of([4, -2, 9, 1])) == {"count": 4, "total": 12, "min": -2, "max": 9}


async def test_aggregate_single_value():
    assert await m.aggregate(stream_of([7])) == {"count": 1, "total": 7, "min": 7, "max": 7}


async def test_aggregate_empty():
    assert await m.aggregate(stream_of([])) == {"count": 0, "total": 0, "min": None, "max": None}


async def test_aggregate_with_zero_and_negative_only():
    result = await m.aggregate(stream_of([0, -5, -1]))
    assert result == {"count": 3, "total": -6, "min": -5, "max": 0}


@pytest.mark.parametrize(
    ("chunks", "expected"),
    [
        (["ab", "c\nde", "f\n\ngh"], ["abc", "def", "", "gh"]),
        (["one\ntwo\n"], ["one", "two"]),
        (["one\ntwo"], ["one", "two"]),
        (["a", "b", "c"], ["abc"]),
        (["\n"], [""]),
        (["\n\n"], ["", ""]),
        ([], []),
        ([""], []),
        (["x\n", "", "y\n"], ["x", "y"]),
    ],
)
async def test_lines_from_chunks(chunks, expected):
    assert [line async for line in m.lines_from_chunks(stream_of(chunks))] == expected


async def test_lines_arrive_before_the_stream_ends():
    log = []
    gen = m.lines_from_chunks(stream_of(["first\nsec", "ond\n", "third"], log))
    assert await anext(gen) == "first"
    assert log == ["produced 'first\\nsec'"]
    assert await anext(gen) == "second"
    assert len(log) == 2
    await gen.aclose()
