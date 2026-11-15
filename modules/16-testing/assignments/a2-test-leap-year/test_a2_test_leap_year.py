import importlib.util
from pathlib import Path

import pytest

from practice import load

m = load(__file__)

_spec = importlib.util.spec_from_file_location(
    "leap_implementations", Path(__file__).parent / "implementations.py"
)
impl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(impl)

BUGS = sorted(name for name in dir(impl) if name.startswith("bug_"))
assert len(BUGS) >= 5, "implementations.py should contain the buggy versions"


def test_cases_are_well_formed():
    cases = m.leap_year_cases
    assert isinstance(cases, list)
    assert len(cases) >= 5, "write at least 5 cases"
    for case in cases:
        assert isinstance(case, tuple) and len(case) == 2, f"bad case: {case!r}"
        year, expected = case
        assert type(year) is int and year > 0, f"year must be a positive int: {case!r}"
        assert type(expected) is bool, f"expected must be a bool: {case!r}"


def test_cases_agree_with_the_correct_function():
    assert m.leap_year_cases, "write some cases first"
    for year, expected in m.leap_year_cases:
        assert impl.correct(year) == expected, f"({year}, {expected}) is wrong: check the rule"


@pytest.mark.parametrize("bug", BUGS)
def test_cases_catch_the_bug(bug):
    function = getattr(impl, bug)
    caught = [year for year, expected in m.leap_year_cases if function(year) != expected]
    assert caught, f"none of your cases catches {bug}"
