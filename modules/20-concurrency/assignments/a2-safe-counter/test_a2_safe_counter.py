import sys
import threading

import pytest

from practice import load

m = load(__file__)


@pytest.fixture
def frequent_switching():
    """Ask the interpreter to switch threads very often, to expose races."""
    old = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    yield
    sys.setswitchinterval(old)


def test_basic_use():
    c = m.SafeCounter()
    assert c.value == 0
    c.increment()
    c.increment(5)
    assert c.value == 6
    c.reset()
    assert c.value == 0


def test_start_value():
    assert m.SafeCounter(10).value == 10


def test_value_is_read_only():
    c = m.SafeCounter()
    c.increment()
    assert c.value == 1
    with pytest.raises(AttributeError):
        c.value = 99


def test_run_in_threads_runs_task_each_time():
    calls = []
    lock = threading.Lock()
    barrier = threading.Barrier(5, timeout=5)  # all 5 threads must be alive together

    def task():
        barrier.wait()
        with lock:
            calls.append(threading.get_ident())

    m.run_in_threads(task, 5)
    assert len(calls) == 5
    assert len(set(calls)) == 5  # each call ran in its own thread


def test_run_in_threads_waits_for_all():
    done = []
    m.run_in_threads(lambda: done.append(1), 3)
    assert done == [1, 1, 1]


def test_run_in_threads_bad_count():
    m.run_in_threads(lambda: None, 1)
    with pytest.raises(ValueError):
        m.run_in_threads(lambda: None, 0)


def test_no_lost_updates(frequent_switching):
    counter = m.SafeCounter()

    def task():
        for _ in range(5000):
            counter.increment()

    m.run_in_threads(task, 8)
    assert counter.value == 40_000


def test_increment_by_amount_under_threads(frequent_switching):
    counter = m.SafeCounter(100)
    m.run_in_threads(lambda: [counter.increment(3) for _ in range(2000)], 4)
    assert counter.value == 100 + 4 * 2000 * 3


class RecordingLock:
    """Stands in for threading.Lock and counts how often it is taken."""

    def __init__(self):
        self.acquired = 0
        self.depth = 0

    def __enter__(self):
        self.acquired += 1
        self.depth += 1
        return self

    def __exit__(self, *exc_info):
        self.depth -= 1

    def acquire(self, *args, **kwargs):
        self.__enter__()
        return True

    def release(self):
        self.__exit__()


def test_changes_are_made_while_holding_a_lock(monkeypatch):
    locks = []

    def make_lock():
        lock = RecordingLock()
        locks.append(lock)
        return lock

    monkeypatch.setattr(m.threading, "Lock", make_lock)
    counter = m.SafeCounter()
    assert len(locks) == 1, "create exactly one lock with threading.Lock()"
    lock = locks[0]
    counter.increment()
    after_increment = lock.acquired
    counter.increment(2)
    assert lock.acquired > after_increment >= 1
    before_reset = lock.acquired
    counter.reset()
    assert lock.acquired > before_reset
    assert counter.value == 0
    assert lock.depth == 0
