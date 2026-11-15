import doctest

import pytest

from practice import load

m = load(__file__)


def examples_for(name):
    """Return the doctest object for one function of the module."""
    tests = doctest.DocTestFinder().find(getattr(m, name), name, module=m, globs=vars(m).copy())
    return tests[0]


@pytest.mark.parametrize("name", ["double", "slugify", "safe_div"])
def test_at_least_three_examples_that_call_the_function(name):
    test = examples_for(name)
    assert len(test.examples) >= 3, f"{name} needs at least 3 examples"
    for ex in test.examples:
        assert name in ex.source, f"every example in {name} must call {name}()"


@pytest.mark.parametrize("name", ["double", "slugify", "safe_div"])
def test_examples_pass(name):
    test = examples_for(name)
    assert test.examples, f"{name} has no examples yet"
    runner = doctest.DocTestRunner(verbose=False)
    runner.run(test)
    assert runner.failures == 0


def test_safe_div_documents_the_error():
    test = examples_for("safe_div")
    errors = [ex for ex in test.examples if ex.exc_msg is not None]
    assert errors, "add an example that shows the ValueError"
    assert "ValueError" in errors[0].exc_msg
    assert "cannot divide by zero" in errors[0].exc_msg


def test_functions_still_work():
    assert m.double(4) == 8
    assert m.slugify("  A  b ") == "a-b"
    assert m.safe_div(1, 4) == 0.25
    with pytest.raises(ValueError):
        m.safe_div(1, 0)
    assert len(examples_for("double").examples) >= 1
