from pathlib import Path

import pytest

from practice import load

m = load(__file__)
SAMPLE = Path(__file__).parent / "sample.txt"


@pytest.fixture
def make(tmp_path):
    def _make(text: str) -> Path:
        path = tmp_path / "t.txt"
        path.write_bytes(text.encode("utf-8"))
        return path

    return _make


def test_count_lines_sample():
    assert m.count_lines(SAMPLE) == 5


def test_count_lines_edge_cases(make):
    assert m.count_lines(make("")) == 0
    assert m.count_lines(make("one")) == 1
    assert m.count_lines(make("one\n")) == 1
    assert m.count_lines(make("a\n\nb\n")) == 3


def test_count_words(make):
    assert m.count_words(SAMPLE) == 17
    assert m.count_words(make("  a  b\n\tc \n")) == 3
    assert m.count_words(make("")) == 0


def test_count_chars_counts_characters_not_bytes(make):
    assert m.count_chars(make("Café")) == 4
    assert m.count_chars(make("a\nb\n")) == 4
    assert m.count_chars(SAMPLE) == 82


def test_longest_line(make):
    assert m.longest_line(SAMPLE) == "Café au lait costs 3 euros."
    assert m.longest_line(make("aa\nbb\nc\n")) == "aa"
    assert m.longest_line(make("")) == ""
    assert m.longest_line(make("x\nlast line without newline")) == "last line without newline"


def test_report():
    assert m.report(SAMPLE) == "sample.txt: 5 lines, 17 words, 82 chars"


def test_report_uses_file_name_only(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("hello world\n", encoding="utf-8")
    assert m.report(path) == "notes.txt: 1 lines, 2 words, 12 chars"
