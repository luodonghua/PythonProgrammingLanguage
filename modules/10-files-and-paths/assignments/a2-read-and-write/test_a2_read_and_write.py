from practice import load

m = load(__file__)


def test_read_lines(tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("  a \n\n b\n   \n", encoding="utf-8")
    assert m.read_lines(p) == ["a", "b"]


def test_read_lines_empty_file(tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("", encoding="utf-8")
    assert m.read_lines(p) == []


def test_write_report(tmp_path):
    p = tmp_path / "r.txt"
    count = m.write_report(p, [("tea", 3), ("cake", 4.5)])
    assert count == 3
    assert p.read_text(encoding="utf-8") == "tea: 3.00\ncake: 4.50\nTotal: 7.50\n"


def test_write_report_no_rows(tmp_path):
    p = tmp_path / "r.txt"
    assert m.write_report(p, []) == 1
    assert p.read_text(encoding="utf-8") == "Total: 0.00\n"


def test_write_report_overwrites(tmp_path):
    p = tmp_path / "r.txt"
    p.write_text("old content\nmore\n", encoding="utf-8")
    m.write_report(p, [("x", 1)])
    assert p.read_text(encoding="utf-8") == "x: 1.00\nTotal: 1.00\n"


def test_append_log_creates_and_appends(tmp_path):
    p = tmp_path / "app.log"
    m.append_log(p, "first")
    m.append_log(p, "second")
    assert p.read_text(encoding="utf-8") == "first\nsecond\n"


def test_append_log_keeps_existing_text(tmp_path):
    p = tmp_path / "app.log"
    p.write_text("old\n", encoding="utf-8")
    m.append_log(p, "new")
    assert p.read_text(encoding="utf-8") == "old\nnew\n"


def test_copy_uppercase(tmp_path):
    src = tmp_path / "in.txt"
    dst = tmp_path / "out.txt"
    src.write_text("Café\nok\n", encoding="utf-8")
    assert m.copy_uppercase(src, dst) == 2
    assert dst.read_text(encoding="utf-8") == "CAFÉ\nOK\n"
    assert src.read_text(encoding="utf-8") == "Café\nok\n"


def test_copy_uppercase_empty(tmp_path):
    src = tmp_path / "in.txt"
    dst = tmp_path / "out.txt"
    src.write_text("", encoding="utf-8")
    assert m.copy_uppercase(src, dst) == 0
    assert dst.exists()


def test_tail(tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("1\n2\n3\n4\n5\n", encoding="utf-8")
    assert m.tail(p) == ["3", "4", "5"]
    assert m.tail(p, 1) == ["5"]
    assert m.tail(p, 10) == ["1", "2", "3", "4", "5"]
    assert m.tail(p, 0) == []
    assert m.tail(p, -2) == []
