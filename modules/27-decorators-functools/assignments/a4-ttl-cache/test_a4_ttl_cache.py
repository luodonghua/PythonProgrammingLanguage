from practice import load

m = load(__file__)


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def make(seconds=10):
    clock = FakeClock()
    calls = []

    @m.ttl_cache(seconds, clock=clock)
    def square(n):
        """Square doc."""
        calls.append(n)
        return n * n

    return square, clock, calls


def test_second_call_uses_cache():
    square, clock, calls = make()
    assert square(4) == 16
    assert square(4) == 16
    assert calls == [4]
    assert (square.hits, square.misses) == (1, 1)


def test_different_arguments_are_separate():
    square, clock, calls = make()
    square(2)
    square(3)
    square(2)
    assert calls == [2, 3]


def test_entry_expires_exactly_at_ttl():
    square, clock, calls = make(10)
    square(5)
    clock.now = 9.9
    square(5)
    assert calls == [5]
    clock.now = 10.0
    square(5)
    assert calls == [5, 5]


def test_expiry_stores_new_time():
    square, clock, calls = make(10)
    square(5)
    clock.now = 12.0
    square(5)
    clock.now = 21.0  # 9 seconds after the refresh
    square(5)
    assert calls == [5, 5]
    clock.now = 22.0
    square(5)
    assert calls == [5, 5, 5]


def test_keyword_arguments_supported():
    clock = FakeClock()
    calls = []

    @m.ttl_cache(5, clock=clock)
    def add(a, b=0):
        calls.append((a, b))
        return a + b

    assert add(1, b=2) == 3
    assert add(1, b=2) == 3
    assert calls == [(1, 2)]


def test_cache_clear_resets_everything():
    square, clock, calls = make()
    square(1)
    square(1)
    square.cache_clear()
    assert (square.hits, square.misses) == (0, 0)
    square(1)
    assert calls == [1, 1]


def test_counters_start_at_zero_and_metadata_kept():
    square, clock, calls = make()
    assert (square.hits, square.misses) == (0, 0)
    assert square.__name__ == "square"
    assert square.__doc__ == "Square doc."


def test_none_result_is_cached():
    clock = FakeClock()
    calls = []

    @m.ttl_cache(5, clock=clock)
    def nothing():
        calls.append(1)

    nothing()
    nothing()
    assert calls == [1]
