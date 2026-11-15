import pytest

from practice import load

m = load(__file__)


def test_emails_basic():
    text = "Mail Ann@Example.com or bob@test.org."
    assert m.extract_emails(text) == ["ann@example.com", "bob@test.org"]


def test_emails_unique_in_order():
    text = "b@x.io, a@x.io, B@X.IO and a@x.io"
    assert m.extract_emails(text) == ["b@x.io", "a@x.io"]


def test_emails_plus_and_subdomain():
    assert m.extract_emails("Write to ann.lee+news@mail.example.co.uk now") == [
        "ann.lee+news@mail.example.co.uk"
    ]


def test_emails_none():
    assert m.extract_emails("no address here, just @ and a@b") == []


def test_dates():
    assert m.find_dates("From 2025-01-31 to 2025-02-03.") == [(2025, 1, 31), (2025, 2, 3)]


def test_dates_values_are_ints():
    (y, mo, d), = m.find_dates("on 2024-02-29")
    assert (type(y), type(mo), type(d)) == (int, int, int)


@pytest.mark.parametrize("text", ["12025-01-01", "2025-1-1", "2025-01-011", "20250101"])
def test_dates_rejects_wrong_shapes(text):
    assert m.find_dates(text) == []


def test_dates_do_not_validate():
    assert m.find_dates("2025-13-45") == [(2025, 13, 45)]


def test_log_line():
    line = "2025-03-01 12:30:05 [ERROR] disk full on [sda1]"
    assert m.parse_log_line(line) == {
        "date": "2025-03-01",
        "time": "12:30:05",
        "level": "ERROR",
        "message": "disk full on [sda1]",
    }


@pytest.mark.parametrize(
    "line",
    [
        "",
        "hello",
        "2025-03-01 12:30:05 ERROR no brackets",
        "2025-03-01 12:30 [INFO] short time",
        "2025-03-01 12:30:05 [info] lower case level",
        "x 2025-03-01 12:30:05 [INFO] prefix",
    ],
)
def test_log_line_bad(line):
    assert m.parse_log_line("2025-03-01 12:30:05 [INFO] ok") is not None
    assert m.parse_log_line(line) is None
