import queue
import threading

import pytest

from practice import load

m = load(__file__)


def test_results_in_input_order():
    assert m.run_pipeline([1, 2, 3, 4, 5], lambda x: x * 10) == [10, 20, 30, 40, 50]


def test_many_items_few_consumers():
    items = list(range(200))
    assert m.run_pipeline(items, lambda x: x + 1, consumers=2) == [x + 1 for x in items]


def test_single_consumer():
    assert m.run_pipeline(["a", "b"], str.upper, consumers=1) == ["A", "B"]


def test_empty_items():
    assert m.run_pipeline([], str, consumers=2) == []
    assert m.run_pipeline([1], str, consumers=2) == ["1"]


def test_consumers_run_in_other_threads():
    seen = set()
    lock = threading.Lock()

    def transform(x):
        with lock:
            seen.add(threading.get_ident())
        return x

    m.run_pipeline(list(range(20)), transform, consumers=3)
    assert threading.get_ident() not in seen
    assert 1 <= len(seen) <= 3


def test_error_becomes_result():
    def transform(x):
        return 10 // x

    result = m.run_pipeline([5, 0, 2], transform)
    assert result[0] == 2
    assert isinstance(result[1], ZeroDivisionError)
    assert result[2] == 5


def test_threads_are_finished_on_return():
    before = threading.active_count()
    assert m.run_pipeline([1, 2, 3], lambda x: x, consumers=4) == [1, 2, 3]
    assert threading.active_count() == before


def test_bad_consumer_count():
    assert m.run_pipeline([1], str, consumers=1) == ["1"]
    with pytest.raises(ValueError):
        m.run_pipeline([1], str, consumers=0)


def test_drain():
    q = queue.Queue()
    assert m.drain(q) == []
    for n in (3, 1, 2):
        q.put(n)
    assert m.drain(q) == [3, 1, 2]
    assert q.empty()
