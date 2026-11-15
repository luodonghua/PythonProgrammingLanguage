import importlib
import sys

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize("name", ["utils", "my_tools2", "a", "_private"])
def test_valid_names(name):
    assert m.is_valid_module_name(name) is True


@pytest.mark.parametrize("name", ["2fast", "my-tools", "class", "Utils", "", "with space", "import"])
def test_invalid_names(name):
    assert m.is_valid_module_name("utils") is True
    assert m.is_valid_module_name(name) is False


def test_create_package_returns_sorted_relative_paths(tmp_path):
    created = m.create_package(tmp_path, "pkg", ["util", "helpers"])
    assert created == ["pkg/__init__.py", "pkg/helpers.py", "pkg/util.py"]
    for rel in created:
        assert (tmp_path / rel).is_file()


def test_create_package_file_contents(tmp_path):
    m.create_package(tmp_path, "pkg", ["util"])
    assert (tmp_path / "pkg" / "__init__.py").read_text(encoding="utf-8") == '"""Package pkg."""\n'
    module_text = (tmp_path / "pkg" / "util.py").read_text(encoding="utf-8")
    assert module_text.startswith('"""Module util."""\n')
    assert "def hello():" in module_text


def test_create_package_without_modules(tmp_path):
    assert m.create_package(tmp_path, "empty_pkg", []) == ["empty_pkg/__init__.py"]


def test_create_package_validates_before_writing(tmp_path):
    with pytest.raises(ValueError, match="invalid module name: 'bad-name'"):
        m.create_package(tmp_path, "pkg", ["ok", "bad-name"])
    assert not (tmp_path / "pkg").exists()
    with pytest.raises(ValueError, match="invalid module name: 'Pkg'"):
        m.create_package(tmp_path, "Pkg", [])


def test_generated_package_can_be_imported(tmp_path, monkeypatch):
    name = "generated_pkg_for_test"
    m.create_package(tmp_path, name, ["util", "helpers"])
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    try:
        package = importlib.import_module(name)
        util = importlib.import_module(f"{name}.util")
        assert package.__doc__ == f"Package {name}."
        assert util.hello() == f"{name}.util"
    finally:
        for key in [k for k in sys.modules if k == name or k.startswith(name + ".")]:
            del sys.modules[key]


def test_list_modules(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    for file_name in ("__init__.py", "util.py", "helpers.py", "notes.txt"):
        (pkg / file_name).write_text("", encoding="utf-8")
    (pkg / "sub").mkdir()
    (pkg / "sub" / "deep.py").write_text("", encoding="utf-8")
    (pkg / "folder.py").mkdir()
    assert m.list_modules(pkg) == ["helpers", "util"]


def test_list_modules_skips_init(tmp_path):
    (tmp_path / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "x.py").write_text("", encoding="utf-8")
    assert m.list_modules(tmp_path) == ["x"]


def test_find_missing_init(tmp_path):
    (tmp_path / "good").mkdir()
    (tmp_path / "good" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "good" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "bad" / "inner").mkdir(parents=True)
    (tmp_path / "bad" / "inner" / "b.py").write_text("", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "readme.txt").write_text("", encoding="utf-8")
    (tmp_path / "top.py").write_text("", encoding="utf-8")
    assert m.find_missing_init(tmp_path) == ["bad/inner"]


def test_find_missing_init_all_fine(tmp_path):
    assert m.find_missing_init(tmp_path) == []
    m.create_package(tmp_path, "pkg", ["a"])
    assert m.find_missing_init(tmp_path) == []
    (tmp_path / "pkg" / "__init__.py").unlink()
    assert m.find_missing_init(tmp_path) == ["pkg"]
