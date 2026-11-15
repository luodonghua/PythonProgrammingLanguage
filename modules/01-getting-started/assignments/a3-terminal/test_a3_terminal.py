from pathlib import Path

from practice import load

m = load(__file__)


def test_where_am_i(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert m.where_am_i() == str(Path.cwd())


def test_lists_only_python_files_sorted(tmp_path):
    (tmp_path / "b.py").write_text("")
    (tmp_path / "a.py").write_text("")
    (tmp_path / "notes.txt").write_text("")
    assert m.list_python_files(tmp_path) == ["a.py", "b.py"]


def test_ignores_subfolders_and_folders_named_like_files(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "deep.py").write_text("")
    (tmp_path / "weird.py").mkdir()
    (tmp_path / "ok.py").write_text("")
    assert m.list_python_files(tmp_path) == ["ok.py"]


def test_empty_folder(tmp_path):
    assert m.list_python_files(tmp_path) == []
