from practice import load

m = load(__file__)


def build(base):
    (base / "docs").mkdir()
    (base / "a.txt").write_text("aaa", encoding="utf-8")
    (base / "B.TXT").write_text("b", encoding="utf-8")
    (base / "run.py").write_text("print()", encoding="utf-8")
    (base / "Makefile").write_text("all:", encoding="utf-8")
    (base / "docs" / "c.txt").write_text("cc", encoding="utf-8")
    (base / "docs" / "d.md").write_text("dddd", encoding="utf-8")


def test_find_files(tmp_path):
    build(tmp_path)
    assert m.find_files(tmp_path, ".txt") == ["a.txt", "docs/c.txt"]
    assert m.find_files(tmp_path, ".md") == ["docs/d.md"]
    assert m.find_files(tmp_path, ".zip") == []


def test_find_files_skips_directories(tmp_path):
    (tmp_path / "folder.txt").mkdir()
    (tmp_path / "real.txt").write_text("x", encoding="utf-8")
    assert m.find_files(tmp_path, ".txt") == ["real.txt"]


def test_count_by_suffix_is_not_recursive_and_lowercases(tmp_path):
    build(tmp_path)
    assert m.count_by_suffix(tmp_path) == {".txt": 2, ".py": 1, "": 1}


def test_count_by_suffix_empty(tmp_path):
    assert m.count_by_suffix(tmp_path) == {}


def test_largest_file(tmp_path):
    build(tmp_path)
    assert m.largest_file(tmp_path) == "run.py"


def test_largest_file_tie_uses_name_order(tmp_path):
    (tmp_path / "b.txt").write_text("xx", encoding="utf-8")
    (tmp_path / "a.txt").write_text("yy", encoding="utf-8")
    assert m.largest_file(tmp_path) == "a.txt"


def test_largest_file_none(tmp_path):
    (tmp_path / "x.txt").write_text("1", encoding="utf-8")
    assert m.largest_file(tmp_path) == "x.txt"
    (tmp_path / "x.txt").unlink()
    assert m.largest_file(tmp_path) is None
    (tmp_path / "only_a_folder").mkdir()
    assert m.largest_file(tmp_path) is None


def test_make_tree(tmp_path):
    assert m.make_tree(tmp_path, ["a.txt", "docs/b.md", "x/y/z.txt"]) is None
    assert (tmp_path / "a.txt").is_file()
    assert (tmp_path / "docs" / "b.md").is_file()
    assert (tmp_path / "x" / "y" / "z.txt").is_file()


def test_make_tree_keeps_existing_content(tmp_path):
    (tmp_path / "a.txt").write_text("keep", encoding="utf-8")
    m.make_tree(tmp_path, ["a.txt", "b.txt"])
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "keep"
    assert (tmp_path / "b.txt").exists()


def test_change_suffix(tmp_path):
    (tmp_path / "a.txt").write_text("1", encoding="utf-8")
    (tmp_path / "b.txt").write_text("2", encoding="utf-8")
    (tmp_path / "c.py").write_text("3", encoding="utf-8")
    assert m.change_suffix(tmp_path, ".txt", ".md") == ["a.md", "b.md"]
    assert sorted(p.name for p in tmp_path.iterdir()) == ["a.md", "b.md", "c.py"]
    assert (tmp_path / "a.md").read_text(encoding="utf-8") == "1"


def test_total_size(tmp_path):
    build(tmp_path)
    assert m.total_size(tmp_path) == 3 + 1 + 7 + 4 + 2 + 4
    assert m.total_size(tmp_path / "docs") == 6
