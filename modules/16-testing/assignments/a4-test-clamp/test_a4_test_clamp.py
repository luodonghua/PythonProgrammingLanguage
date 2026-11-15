import importlib.util
from pathlib import Path

import pytest

from practice import load

m = load(__file__)

_spec = importlib.util.spec_from_file_location(
    "clamp_implementations", Path(__file__).parent / "implementations.py"
)
impl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(impl)

BUGS = sorted(name for name in dir(impl) if name.startswith("bug_"))
assert len(BUGS) >= 5, "implementations.py should contain the buggy versions"


def outcome(function, case):
    """Return the result of function(x, low, high), or the exception class it raised."""
    x, low, high, _ = case
    try:
        return function(x, low, high)
    except Exception as exc:  # the grader needs to see every kind of error
        return type(exc)


def test_cases_are_well_formed():
    cases = m.clamp_cases
    assert isinstance(cases, list)
    assert len(cases) >= 6, "write at least 6 cases"
    for case in cases:
        assert isinstance(case, tuple) and len(case) == 4, f"bad case: {case!r}"
        x, low, high, expected = case
        for number in (x, low, high):
            assert type(number) in (int, float), f"numbers must be int or float: {case!r}"
        assert expected is ValueError or type(expected) in (int, float), f"bad expected: {case!r}"


def test_cases_agree_with_the_correct_function():
    assert m.clamp_cases, "write some cases first"
    for case in m.clamp_cases:
        assert outcome(impl.correct, case) == case[3], f"{case!r} is wrong: check the rules"


def test_cases_include_an_error_case():
    assert any(case[3] is ValueError for case in m.clamp_cases), "add a ValueError case"


@pytest.mark.parametrize("bug", BUGS)
def test_cases_catch_the_bug(bug):
    function = getattr(impl, bug)
    caught = [case for case in m.clamp_cases if outcome(function, case) != case[3]]
    assert caught, f"none of your cases catches {bug}"
