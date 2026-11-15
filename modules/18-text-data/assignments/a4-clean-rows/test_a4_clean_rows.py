from pathlib import Path

import pytest

from practice import load

m = load(__file__)
PEOPLE = Path(__file__).parent / "people.csv"


def test_good_rows():
    good, _ = m.clean_rows(PEOPLE)
    assert good == [
        {"name": "Ada Lovelace", "age": 36, "email": "ada@example.com"},
        {"name": "Eve, Jr.", "age": 52, "email": "eve@example.org"},
    ]


def test_errors():
    _, errors = m.clean_rows(PEOPLE)
    assert errors == [
        (3, "missing name"),
        (4, "bad age"),
        (5, "bad age"),
        (6, "bad email"),
        (8, "wrong field count"),
        (9, "wrong field count"),
    ]


def test_cleaning_and_first_error_wins(tmp_path):
    p = tmp_path / "p.csv"
    p.write_text(
        "name,age,email\n"
        "  Zed  , 7 ,ZED@Example.COM\n"
        "  ,abc,bad\n"
        "Amy,131,amy@x.org\n"
        "Bo,0,bo@x.org\n"
        "Cat,30,c at@x.org\n"
        "Dan,30,dan@x\n",
        encoding="utf-8",
    )
    good, errors = m.clean_rows(p)
    assert good == [
        {"name": "Zed", "age": 7, "email": "zed@example.com"},
        {"name": "Bo", "age": 0, "email": "bo@x.org"},
    ]
    assert errors == [(3, "missing name"), (4, "bad age"), (6, "bad email"), (7, "bad email")]


def test_empty_data(tmp_path):
    p = tmp_path / "e.csv"
    p.write_text("name,age,email\n", encoding="utf-8")
    assert m.clean_rows(p) == ([], [])


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("", "0 good rows, 0 errors"),
        ("A,1,a@b.co\n", "1 good row, 0 errors"),
        ("A,1,a@b.co\nB,2,b@b.co\n,3,c@b.co\n", "2 good rows, 1 error"),
        ("A,x,a@b.co\n,x,a@b.co\n", "0 good rows, 2 errors"),
    ],
)
def test_summarize(tmp_path, body, expected):
    p = tmp_path / "s.csv"
    p.write_text("name,age,email\n" + body, encoding="utf-8")
    assert m.summarize(p) == expected
