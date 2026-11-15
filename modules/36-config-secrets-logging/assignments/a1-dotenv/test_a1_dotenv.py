import pytest

from practice import load

m = load(__file__)


def test_simple_pairs():
    assert m.parse_dotenv("A=1\nB=two\n") == {"A": "1", "B": "two"}


def test_blank_lines_and_comments_are_skipped():
    text = "# comment\n\n   \nA=1\n  # indented comment\n"
    assert m.parse_dotenv(text) == {"A": "1"}


def test_spaces_around_name_and_value_are_stripped():
    assert m.parse_dotenv("  NAME  =  value  \n") == {"NAME": "value"}


def test_export_prefix():
    assert m.parse_dotenv("export A=1\nexport   B=2") == {"A": "1", "B": "2"}


def test_value_may_contain_equals_sign():
    assert m.parse_dotenv("URL=https://x.test/?a=1&b=2") == {"URL": "https://x.test/?a=1&b=2"}


def test_empty_value():
    assert m.parse_dotenv("EMPTY=\nQ=''") == {"EMPTY": "", "Q": ""}


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ('A="hello world"', "hello world"),
        ("A='hello world'", "hello world"),
        ('A="  padded  "', "  padded  "),
        ('A="not # a comment"', "not # a comment"),
        ("A='say \"hi\"'", 'say "hi"'),
        ('A="mismatched\'', "\"mismatched'"),
    ],
)
def test_quotes(line, expected):
    assert m.parse_dotenv(line) == {"A": expected}


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("A=1 # note", "1"),
        ("A=1\t# note", "1"),
        ("A=color#fff", "color#fff"),
        ("A=# all comment", ""),
    ],
)
def test_inline_comments(line, expected):
    assert m.parse_dotenv(line) == {"A": expected}


def test_later_value_wins():
    assert m.parse_dotenv("A=1\nA=2") == {"A": "2"}


def test_missing_equals_reports_line_number():
    with pytest.raises(ValueError, match=r"^line 3:"):
        m.parse_dotenv("A=1\n\nbroken line\n")


@pytest.mark.parametrize("line", ["1A=x", "A-B=x", "=x", "A B=x"])
def test_invalid_names(line):
    with pytest.raises(ValueError, match=r"^line 1:"):
        m.parse_dotenv(line)
