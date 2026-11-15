import math
import os

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("numbers", "parts", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2, 3], [4, 5]]),
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),
        ([1, 2], 3, [[1], [2], []]),
        ([], 2, [[], []]),
        ([7, 8, 9], 1, [[7, 8, 9]]),
        (list(range(7)), 3, [[0, 1, 2], [3, 4], [5, 6]]),
    ],
)
def test_split_chunks(numbers, parts, expected):
    assert m.split_chunks(numbers, parts) == expected


def test_split_chunks_bad_parts():
    assert m.split_chunks([1], 1) == [[1]]
    with pytest.raises(ValueError):
        m.split_chunks([1], 0)


def test_process_map_keeps_order():
    assert m.process_map(math.factorial, [5, 3, 10, 0]) == [120, 6, 3628800, 1]


def test_process_map_bad_workers():
    assert m.process_map(abs, [-1], workers=1) == [1]
    with pytest.raises(ValueError):
        m.process_map(abs, [-1], workers=0)


def test_parallel_sum():
    numbers = list(range(1, 1001))
    assert m.parallel_sum(numbers, workers=3) == 500500
    assert m.parallel_sum([], workers=2) == 0
    assert m.parallel_sum([5], workers=4) == 5


def test_jobs_run_in_other_processes():
    pids = m.worker_pids(6, workers=2)
    assert pids
    assert len(pids) <= 2
    assert os.getpid() not in pids
