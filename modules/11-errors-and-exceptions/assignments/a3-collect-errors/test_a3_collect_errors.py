from practice import load

m = load(__file__)


def test_parse_records_example():
    result = m.parse_records(["Ada,36", "", "Bob,x", "Cy"])
    assert result == ([("Ada", 36)], [(3, "age is not a number"), (4, "expected 2 fields")])


def test_parse_records_all_good():
    records, errors = m.parse_records(["Ada, 36", " Bo ,5"])
    assert records == [("Ada", 36), ("Bo", 5)]
    assert errors == []


def test_parse_records_each_reason():
    lines = ["a,b,c", ",5", "Zed,old", "Old,151", "Neg,-1", "Edge,150", "Zero,0"]
    records, errors = m.parse_records(lines)
    assert errors == [
        (1, "expected 2 fields"),
        (2, "empty name"),
        (3, "age is not a number"),
        (4, "age out of range"),
        (5, "age out of range"),
    ]
    assert records == [("Edge", 150), ("Zero", 0)]


def test_parse_records_blank_lines_count_for_numbering():
    records, errors = m.parse_records(["", "   ", "x"])
    assert records == []
    assert errors == [(3, "expected 2 fields")]


def test_parse_records_empty_input():
    assert m.parse_records([]) == ([], [])


def test_read_or_default(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("héllo", encoding="utf-8")
    assert m.read_or_default(p) == "héllo"
    assert m.read_or_default(tmp_path / "missing.txt") == ""
    assert m.read_or_default(tmp_path / "missing.txt", "none") == "none"


def test_read_or_default_bad_encoding(tmp_path):
    p = tmp_path / "bin.dat"
    p.write_bytes(b"\xff\xfe\x00\x80")
    assert m.read_or_default(p, "unreadable") == "unreadable"


def test_sum_numbers():
    assert m.sum_numbers([1, "2.5", "x", None, 4]) == (7.5, ["x", None])
    assert m.sum_numbers([]) == (0, [])
    assert m.sum_numbers(["a", "b"]) == (0, ["a", "b"])
    assert m.sum_numbers([" 3 "]) == (3.0, [])


def test_run_all():
    results = m.run_all([lambda: 1, lambda: 1 / 0, lambda: "x" + 1, lambda: 3])
    assert results[0] == ("ok", 1)
    assert results[1] == ("error", "ZeroDivisionError: division by zero")
    assert results[2][0] == "error"
    assert results[2][1].startswith("TypeError: ")
    assert results[3] == ("ok", 3)


def test_run_all_runs_every_task_in_order():
    seen = []

    def make(n, fail):
        def task():
            seen.append(n)
            if fail:
                raise ValueError(f"bad {n}")
            return n

        return task

    results = m.run_all([make(1, False), make(2, True), make(3, False)])
    assert seen == [1, 2, 3]
    assert results == [("ok", 1), ("error", "ValueError: bad 2"), ("ok", 3)]
    assert m.run_all([]) == []
