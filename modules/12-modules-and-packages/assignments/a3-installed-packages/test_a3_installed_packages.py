import importlib.metadata
import json
import math
import os.path

import pytest

from practice import load

m = load(__file__)

MISSING = "no-such-package-x"


def test_installed_version_matches_importlib_metadata():
    assert m.installed_version("pytest") == importlib.metadata.version("pytest")


def test_installed_version_is_a_string_with_digits():
    version = m.installed_version("pytest")
    assert isinstance(version, str)
    assert version[0].isdigit()


def test_installed_version_missing():
    assert m.installed_version("pytest") is not None
    assert m.installed_version(MISSING) is None


def test_report_versions():
    expected = importlib.metadata.version("pytest")
    result = m.report_versions(["pytest", MISSING])
    assert result == {"pytest": expected}


def test_report_versions_empty():
    assert m.report_versions([]) == {}
    assert m.report_versions([MISSING]) == {}


def test_format_report():
    version = importlib.metadata.version("pytest")
    text = m.format_report(["pytest", MISSING])
    assert text == f"pytest {version}\n{MISSING} MISSING"


def test_format_report_empty():
    assert m.format_report([]) == ""
    assert m.format_report(["x-" + MISSING]) == f"x-{MISSING} MISSING"


@pytest.mark.parametrize("name", ["json", "json.decoder", "os.path", "pytest"])
def test_can_import_true(name):
    assert m.can_import(name) is True


@pytest.mark.parametrize("name", ["not_a_module_x", "not_a_pkg_x.sub", "json.not_a_submodule_x"])
def test_can_import_false(name):
    assert m.can_import("json") is True
    assert m.can_import(name) is False


def test_load_function():
    assert m.load_function("math.sqrt") is math.sqrt
    assert m.load_function("os.path.join") is os.path.join
    assert m.load_function("json.dumps") is json.dumps
    assert m.load_function("math.sqrt")(16) == 4.0


def test_load_function_without_dot():
    with pytest.raises(ValueError, match="need module.attribute"):
        m.load_function("math")


def test_load_function_bad_names():
    assert m.load_function("math.pi") == math.pi
    with pytest.raises(AttributeError):
        m.load_function("math.not_there_x")
    with pytest.raises(ImportError):
        m.load_function("not_a_module_x.func")
