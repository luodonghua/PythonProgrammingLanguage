import os

import pytest

from practice import load

m = load(__file__)


class FakeClock:
    def __init__(self, *times):
        self.times = list(times)

    def __call__(self):
        return self.times.pop(0)


def test_timer_measures_with_fake_clock():
    with m.Timer(clock=FakeClock(10.0, 12.5)) as t:
        pass
    assert t.elapsed == 2.5


def test_timer_enter_returns_timer_and_elapsed_none_inside():
    with m.Timer(clock=FakeClock(1.0, 2.0)) as t:
        assert isinstance(t, m.Timer)
        assert t.elapsed is None


def test_timer_records_on_error_and_does_not_swallow():
    timer = m.Timer(clock=FakeClock(0.0, 4.0))
    with pytest.raises(ZeroDivisionError):
        with timer:
            1 / 0
    assert timer.elapsed == 4.0


def test_timer_default_clock_gives_non_negative_float():
    with m.Timer() as t:
        pass
    assert isinstance(t.elapsed, float)
    assert t.elapsed >= 0


def test_temporary_env_sets_and_removes(monkeypatch):
    monkeypatch.delenv("PRACTICE_NEW", raising=False)
    with m.temporary_env(PRACTICE_NEW="yes"):
        assert os.environ["PRACTICE_NEW"] == "yes"
    assert "PRACTICE_NEW" not in os.environ


def test_temporary_env_restores_old_value(monkeypatch):
    monkeypatch.setenv("PRACTICE_OLD", "before")
    with m.temporary_env(PRACTICE_OLD="during", PRACTICE_OTHER="x"):
        assert os.environ["PRACTICE_OLD"] == "during"
        assert os.environ["PRACTICE_OTHER"] == "x"
    assert os.environ["PRACTICE_OLD"] == "before"
    assert "PRACTICE_OTHER" not in os.environ


def test_temporary_env_restores_after_error(monkeypatch):
    monkeypatch.setenv("PRACTICE_OLD", "before")
    with pytest.raises(RuntimeError):
        with m.temporary_env(PRACTICE_OLD="during"):
            raise RuntimeError("boom")
    assert os.environ["PRACTICE_OLD"] == "before"


def test_temporary_env_nested(monkeypatch):
    monkeypatch.delenv("PRACTICE_NEST", raising=False)
    with m.temporary_env(PRACTICE_NEST="outer"):
        with m.temporary_env(PRACTICE_NEST="inner"):
            assert os.environ["PRACTICE_NEST"] == "inner"
        assert os.environ["PRACTICE_NEST"] == "outer"
    assert "PRACTICE_NEST" not in os.environ
