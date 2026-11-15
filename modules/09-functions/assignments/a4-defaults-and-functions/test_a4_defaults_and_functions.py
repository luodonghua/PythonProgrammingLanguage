from practice import load

m = load(__file__)


def test_add_item_new_list_each_call():
    assert m.add_item("a") == ["a"]
    assert m.add_item("b") == ["b"]


def test_add_item_uses_given_list():
    existing = ["x"]
    result = m.add_item("c", existing)
    assert result == ["x", "c"]
    assert result is existing


def test_add_item_default_is_not_a_list():
    assert m.add_item("z") == ["z"]
    assert m.add_item.__defaults__ == (None,)


def test_apply_n_times():
    assert m.apply_n_times(lambda v: v * 2, 3, 1) == 8
    assert m.apply_n_times(str.strip, 0, " a ") == " a "
    assert m.apply_n_times(lambda s: s + "!", 2, "hi") == "hi!!"


def test_compose_order():
    inc = lambda v: v + 1  # noqa: E731
    dbl = lambda v: v * 2  # noqa: E731
    assert m.compose(inc, dbl)(5) == 12
    assert m.compose(dbl, inc)(5) == 11


def test_compose_empty_and_single():
    assert m.compose()(5) == 5
    assert m.compose(str.upper)("a") == "A"


def test_compose_returns_a_function():
    assert callable(m.compose(len))


def test_make_counter():
    counter = m.make_counter(10)
    assert counter() == 10
    assert counter() == 11
    assert counter() == 12


def test_make_counter_default_start():
    assert m.make_counter()() == 0


def test_counters_are_independent():
    a = m.make_counter()
    b = m.make_counter(100)
    assert (a(), a(), b(), a(), b()) == (0, 1, 100, 2, 101)


def test_apply_all():
    result = m.apply_all({"upper": str.upper, "length": len}, "abc")
    assert result == {"upper": "ABC", "length": 3}
    assert m.apply_all({}, "abc") == {}
