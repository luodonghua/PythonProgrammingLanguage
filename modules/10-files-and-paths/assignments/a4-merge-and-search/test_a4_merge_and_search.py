from pathlib import Path

import pytest

from practice import load

m = load(__file__)
NOTES = Path(__file__).parent / "notes"


def test_list_notes_uses_only_txt_files():
    assert [p.name for p in m.list_notes(NOTES)] == [
        "monday.txt",
        "tuesday.txt",
        "wednesday.txt",
    ]


def test_list_notes_ignores_folders(tmp_path):
    (tmp_path / "dir.txt").mkdir()
    (tmp_path / "b.txt").write_text("x", encoding="utf-8")
    (tmp_path / "a.txt").write_text("x", encoding="utf-8")
    assert [p.name for p in m.list_notes(tmp_path)] == ["a.txt", "b.txt"]


def test_merge_notes_small(tmp_path):
    src = tmp_path / "in"
    src.mkdir()
    (src / "a.txt").write_text("x\n", encoding="utf-8")
    (src / "b.txt").write_text("y\nz", encoding="utf-8")  # no final newline
    dest = tmp_path / "out" / "all.txt"
    assert m.merge_notes(src, dest) == 2
    expected = "== a.txt ==\nx\n\n== b.txt ==\ny\nz\n\n"
    assert dest.read_text(encoding="utf-8") == expected


def test_merge_notes_sample_data(tmp_path):
    dest = tmp_path / "all.txt"
    assert m.merge_notes(NOTES, dest) == 3
    text = dest.read_text(encoding="utf-8")
    assert text.startswith("== monday.txt ==\nBuy milk\n")
    assert "== wednesday.txt ==\nWater the plants\n\n" in text
    assert "readme" not in text


def test_merge_notes_empty_folder(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    dest = tmp_path / "all.txt"
    assert m.merge_notes(empty, dest) == 0
    assert dest.read_text(encoding="utf-8") == ""


def test_search_sample_data():
    assert m.search(NOTES, "buy") == [
        ("monday.txt", 1, "Buy milk"),
        ("tuesday.txt", 2, "Buy stamps"),
    ]


def test_search_is_case_insensitive_and_reports_line_numbers():
    assert m.search(NOTES, "TRIP") == [
        ("monday.txt", 2, "Call Ana about the trip"),
        ("tuesday.txt", 4, "Trip plan: book hotel"),
    ]


def test_search_no_match():
    assert m.search(NOTES, "zebra") == []
    assert m.search(NOTES, "water") == [("wednesday.txt", 1, "Water the plants")]


def test_number_lines(tmp_path):
    src = tmp_path / "a.txt"
    dst = tmp_path / "b.txt"
    src.write_text("a\n\nb\n", encoding="utf-8")
    assert m.number_lines(src, dst) == 3
    assert dst.read_text(encoding="utf-8") == "1: a\n2: \n3: b\n"


def test_number_lines_empty(tmp_path):
    src = tmp_path / "a.txt"
    dst = tmp_path / "b.txt"
    src.write_text("", encoding="utf-8")
    assert m.number_lines(src, dst) == 0
    assert dst.read_text(encoding="utf-8") == ""


def test_safe_read(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text("hello", encoding="utf-8")
    assert m.safe_read(p) == "hello"
    assert m.safe_read(tmp_path / "missing.txt") == ""
    assert m.safe_read(tmp_path / "missing.txt", "n/a") == "n/a"


def test_safe_read_does_not_hide_other_errors(tmp_path):
    with pytest.raises(OSError):
        m.safe_read(tmp_path)
