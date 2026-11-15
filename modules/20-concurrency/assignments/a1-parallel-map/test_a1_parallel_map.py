import threading

import pytest

from practice import load

m = load(__file__)


def test_results_keep_input_order():
    assert m.parallel_map(lambda x: x * x, range(10)) == [x * x for x in range(10)]


def test_empty():
    assert m.parallel_map(str, []) == []
    assert m.parallel_map(str, [1]) == ["1"]


def test_order_kept_when_first_job_finishes_last():
    # Job 0 waits until job 3 has run, so it finishes last. This only works
    # if the jobs really run at the same time.
    gate = threading.Event()

    def job(n):
        if n == 0:
            assert gate.wait(timeout=5), "job 0 was never released"
        elif n == 3:
            gate.set()
        return n

    assert m.parallel_map(job, [0, 1, 2, 3], workers=4) == [0, 1, 2, 3]


def test_uses_several_threads():
    barrier = threading.Barrier(3, timeout=5)

    def job(_):
        barrier.wait()
        return threading.get_ident()

    idents = m.parallel_map(job, [1, 2, 3], workers=3)
    assert len(set(idents)) == 3


def test_exception_propagates():
    def job(n):
        if n == 2:
            raise KeyError("boom")
        return n

    assert m.parallel_map(job, [1]) == [1]
    with pytest.raises(KeyError):
        m.parallel_map(job, [1, 2, 3])


def test_bad_worker_count():
    assert m.parallel_map(str, [1], workers=1) == ["1"]
    with pytest.raises(ValueError):
        m.parallel_map(str, [1], workers=0)


def test_parallel_lengths():
    assert m.parallel_lengths(["pear", "fig", "banana", "fig"]) == {"pear": 4, "fig": 3, "banana": 6}
    assert list(m.parallel_lengths(["bb", "a"])) == ["bb", "a"]
