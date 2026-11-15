import inspect
from pathlib import Path

from practice import load

m = load(__file__)

LOG = Path(__file__).parent / "app.log"


def test_read_lines_strips_newlines(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text("one\ntwo\n\nlast", encoding="utf-8")
    assert list(m.read_lines(f)) == ["one", "two", "", "last"]


def test_read_lines_is_lazy_generator(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text("a\nb\n", encoding="utf-8")
    gen = m.read_lines(f)
    assert inspect.isgenerator(gen)
    assert next(gen) == "a"


def test_read_lines_handles_unicode(tmp_path):
    f = tmp_path / "u.txt"
    f.write_text("caf\u00e9\n", encoding="utf-8")
    assert list(m.read_lines(f)) == ["caf\u00e9"]


def test_parse_lines():
    lines = [
        "2024-05-01 12:00:01 INFO server started",
        "",
        "garbage",
        "2024-05-01 12:00:02 warning  two  spaces kept",
        "2024-05-01 12:00:03 ERROR",
    ]
    assert list(m.parse_lines(lines)) == [
        ("INFO", "server started"),
        ("WARNING", "two  spaces kept"),
    ]


def test_parse_lines_is_lazy():
    seen = []

    def source():
        for line in ["d t INFO a", "d t INFO b", "d t INFO c"]:
            seen.append(line)
            yield line

    gen = m.parse_lines(source())
    assert next(gen) == ("INFO", "a")
    assert len(seen) == 1


def test_only_levels():
    records = [("INFO", "a"), ("ERROR", "b"), ("DEBUG", "c"), ("ERROR", "d")]
    assert list(m.only_levels(records, {"ERROR"})) == [("ERROR", "b"), ("ERROR", "d")]
    assert list(m.only_levels(iter(records), ["INFO", "DEBUG"])) == [("INFO", "a"), ("DEBUG", "c")]


def test_only_levels_is_generator():
    assert inspect.isgenerator(m.only_levels([], {"ERROR"}))


def test_count_levels_order_of_first_appearance():
    records = iter([("B", "x"), ("A", "y"), ("B", "z")])
    counts = m.count_levels(records)
    assert counts == {"B": 2, "A": 1}
    assert list(counts) == ["B", "A"]


def test_count_levels_on_data_file():
    counts = m.count_levels(m.parse_lines(m.read_lines(LOG)))
    assert counts == {"INFO": 2, "WARNING": 1, "ERROR": 2, "CRITICAL": 1}


def test_error_report_on_data_file():
    assert m.error_report(LOG) == [
        "cannot open database",
        "disk full",
        "shutting down",
    ]


def test_error_report_tmp_file(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text("d t INFO fine\nd t error bad thing\n", encoding="utf-8")
    assert m.error_report(f) == ["bad thing"]
