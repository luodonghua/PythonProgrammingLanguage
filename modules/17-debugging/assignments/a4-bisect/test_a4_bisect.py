import pytest

from practice import load

m = load(__file__)


def make_is_bad(first, log):
    def is_bad(version):
        log.append(version)
        return version >= first

    return is_bad


@pytest.mark.parametrize("n", [1, 2, 3, 7, 10, 64, 100])
def test_finds_every_possible_position(n):
    for first in range(n):
        log = []
        assert m.first_bad(n, make_is_bad(first, log)) == first


def test_none_when_no_version_is_bad():
    log = []
    assert m.first_bad(10, make_is_bad(2, [])) == 2
    assert m.first_bad(10, make_is_bad(99, log)) is None
    assert m.first_bad(0, lambda k: True) is None


def test_example_from_the_docstring():
    assert m.first_bad(10, lambda k: k >= 6) == 6
    assert m.first_bad(10, lambda k: False) is None


def test_everything_is_bad():
    log = []
    assert m.first_bad(50, make_is_bad(0, log)) == 0


def test_number_of_calls_is_logarithmic():
    for n in (1, 2, 5, 16, 100, 1000, 12345):
        for first in {0, 1, n // 2, n - 1, n}:
            log = []
            result = m.first_bad(n, make_is_bad(first, log))
            assert result == (first if first < n else None)
            assert len(log) <= n.bit_length() + 1, f"n={n} first={first}: {len(log)} calls"


def test_never_asks_about_a_missing_version():
    log = []
    m.first_bad(37, make_is_bad(20, log))
    assert log
    assert all(0 <= v < 37 for v in log)


def test_bisect_report():
    report = m.bisect_report(1000, lambda k: k >= 618)
    assert report["first_bad"] == 618
    assert 1 <= report["calls"] <= 11


def test_bisect_report_counts_exact_calls():
    seen = []

    def is_bad(k):
        seen.append(k)
        return k >= 3

    report = m.bisect_report(8, is_bad)
    assert report == {"first_bad": 3, "calls": len(seen)}


def test_bisect_report_with_nothing_bad():
    report = m.bisect_report(8, lambda k: False)
    assert report["first_bad"] is None
    assert report["calls"] >= 1
