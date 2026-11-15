import statistics
import subprocess
import sys
from pathlib import Path

import pytest

from practice import load

m = load(__file__)


def test_parse_numbers():
    assert m.parse_numbers(["1", "2.5", "-3"]) == [1.0, 2.5, -3.0]
    assert m.parse_numbers([]) == []


def test_parse_numbers_reports_the_bad_word():
    with pytest.raises(ValueError, match="not a number: 'x'"):
        m.parse_numbers(["1", "x", "y"])


def test_summary():
    s = m.summary([1, 2, 3, 4])
    assert s["count"] == 4
    assert s["mean"] == 2.5
    assert s["median"] == 2.5
    assert s["stdev"] == pytest.approx(statistics.stdev([1, 2, 3, 4]))


def test_summary_single_number_has_no_stdev():
    assert m.summary([5]) == {"count": 1, "mean": 5, "median": 5, "stdev": None}


def test_summary_empty():
    with pytest.raises(ValueError, match="no numbers"):
        m.summary([])


def test_format_summary():
    assert m.format_summary([1, 2, 3, 4]) == "count=4 mean=2.50 median=2.50"
    assert m.format_summary([10]) == "count=1 mean=10.00 median=10.00"


def test_main_success(capsys):
    assert m.main(["1", "2", "3", "4"]) == 0
    out, err = capsys.readouterr()
    assert out == "count=4 mean=2.50 median=2.50\n"
    assert err == ""


def test_main_without_arguments(capsys):
    assert m.main([]) == 2
    out, err = capsys.readouterr()
    assert out == ""
    assert err.strip() == "usage: numstats NUMBER [NUMBER ...]"


def test_main_bad_number(capsys):
    assert m.main(["1", "oops"]) == 2
    out, err = capsys.readouterr()
    assert out == ""
    assert "not a number: 'oops'" in err


def test_main_reads_sys_argv_by_default(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["numstats", "2", "4"])
    assert m.main() == 0
    assert capsys.readouterr().out == "count=2 mean=3.00 median=3.00\n"


def test_running_as_a_script():
    script = Path(m.__file__)
    result = subprocess.run(
        [sys.executable, str(script), "1", "2", "3"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert result.stdout == "count=3 mean=2.00 median=2.00\n"
