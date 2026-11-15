import pytest

from practice import load

m = load(__file__)


def test_default_value():
    assert m.current_id() == "-"
    assert m.log("hello") == "[-] hello"


def test_bind_and_restore():
    with m.bind_request_id("r1"):
        assert m.current_id() == "r1"
        assert m.log("saved") == "[r1] saved"
    assert m.current_id() == "-"


def test_nested_binds_restore_each_level():
    with m.bind_request_id("outer"):
        with m.bind_request_id("inner"):
            assert m.current_id() == "inner"
        assert m.current_id() == "outer"
    assert m.current_id() == "-"


def test_restored_after_error():
    with pytest.raises(ValueError):
        with m.bind_request_id("r2"):
            raise ValueError
    assert m.current_id() == "-"


def test_uses_a_context_var():
    import contextvars

    assert isinstance(m.request_id, contextvars.ContextVar)
    token = m.request_id.set("manual")
    try:
        assert m.log("x") == "[manual] x"
    finally:
        m.request_id.reset(token)


def test_decorator():
    @m.with_request_id("job-7")
    def work(x):
        """Work doc."""
        return m.log(f"got {x}")

    assert work(3) == "[job-7] got 3"
    assert m.current_id() == "-"
    assert work.__name__ == "work"
    assert work.__doc__ == "Work doc."


def test_run_in_copy_isolates_changes():
    def changer(value):
        m.request_id.set(value)
        return m.current_id()

    assert m.run_in_copy(changer, "inside") == "inside"
    assert m.current_id() == "-"


def test_run_in_copy_sees_current_value():
    with m.bind_request_id("visible"):
        assert m.run_in_copy(m.current_id) == "visible"
