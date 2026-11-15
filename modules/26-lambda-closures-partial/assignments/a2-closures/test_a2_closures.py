from practice import load

m = load(__file__)


def test_counter_defaults():
    c = m.make_counter()
    assert [c(), c(), c()] == [1, 2, 3]


def test_counter_start_and_step():
    c = m.make_counter(10, 5)
    assert [c(), c()] == [15, 20]


def test_counters_are_independent():
    a = m.make_counter()
    b = m.make_counter(100)
    a()
    a()
    assert b() == 101
    assert a() == 3


def test_limiter():
    allow = m.make_limiter(2)
    assert [allow() for _ in range(5)] == [True, True, False, False, False]


def test_limiter_zero_and_independent():
    never = m.make_limiter(0)
    once = m.make_limiter(1)
    assert never() is False
    assert once() is True
    other = m.make_limiter(1)
    assert once() is False
    assert other() is True


def test_adders_fix_late_binding():
    adders = m.make_adders(4)
    assert len(adders) == 4
    assert [f(10) for f in adders] == [10, 11, 12, 13]


def test_history_records_in_order():
    record, history = m.make_history()
    assert history() == []
    assert record("a") == 1
    assert record("b") == 2
    assert history() == ["a", "b"]


def test_history_returns_a_copy():
    record, history = m.make_history()
    record(1)
    snapshot = history()
    snapshot.append(99)
    assert history() == [1]


def test_histories_are_separate():
    record1, history1 = m.make_history()
    record2, history2 = m.make_history()
    record1("x")
    assert history2() == []
    assert history1() == ["x"]
