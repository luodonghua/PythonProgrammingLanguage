from practice import load

m = load(__file__)


def test_loggers_write_to_the_sink_with_level_and_prefix():
    sink = []
    debug, info, error = m.make_loggers(sink, "app: ")
    debug("d")
    info("started")
    error("boom")
    assert sink == ["[DEBUG] app: d", "[INFO] app: started", "[ERROR] app: boom"]


def test_loggers_default_prefix_is_empty():
    sink = []
    _, info, _ = m.make_loggers(sink)
    info("hi")
    assert sink == ["[INFO] hi"]


def test_loggers_use_partial_objects():
    from functools import partial

    debug, info, error = m.make_loggers([], "x")
    assert all(isinstance(f, partial) for f in (debug, info, error))
    assert info.func is m.log


def test_separate_logger_sets_use_separate_sinks():
    a, b = [], []
    _, info_a, _ = m.make_loggers(a)
    _, info_b, _ = m.make_loggers(b)
    info_a("one")
    assert a == ["[INFO] one"] and b == []


def test_parsers():
    parsers = m.make_parsers()
    assert set(parsers) == {"bin", "oct", "hex"}
    assert parsers["bin"]("1010") == 10
    assert parsers["oct"]("17") == 15
    assert parsers["hex"]("ff") == 255


def test_my_partial_positional():
    double = m.my_partial(pow, 2)
    assert double(5) == 32


def test_my_partial_keywords_and_override():
    to_int = m.my_partial(int, base=2)
    assert to_int("101") == 5
    assert to_int("ff", base=16) == 255


def test_my_partial_passes_extra_arguments():
    def join(sep, *parts, end=""):
        return sep.join(parts) + end

    dash = m.my_partial(join, "-", end="!")
    assert dash("a", "b") == "a-b!"
    assert dash("a", end="?") == "a?"


def test_my_partial_is_not_functools_partial():
    from functools import partial

    fn = m.my_partial(int, base=2)
    assert fn("11") == 3
    assert not isinstance(fn, partial)


def test_apply_discount():
    assert m.apply_discount(80, percent=25) == 60.0
    assert m.apply_discount(19.99, percent=10) == 17.99
    assert m.apply_discount(5, percent=90, minimum=2.0) == 2.0


def test_make_discounts():
    discounts = m.make_discounts()
    assert discounts["half"](20) == 10.0
    assert discounts["tenth"](20) == 18.0
    assert discounts["half"](1.5) == 1.0  # minimum price applies
    assert discounts["tenth"].keywords == {"percent": 10, "minimum": 1.0}
