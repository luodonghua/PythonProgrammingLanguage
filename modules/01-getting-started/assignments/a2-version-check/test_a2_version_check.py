import sys

from practice import load

m = load(__file__)


def test_version_string_matches_interpreter():
    v = sys.version_info
    assert m.version_string() == f"Python {v.major}.{v.minor}.{v.micro}"


def test_old_versions_not_supported():
    assert m.is_supported((3, 13, 9)) is False
    assert m.is_supported((3, 9, 0)) is False


def test_new_versions_supported():
    assert m.is_supported((3, 14, 0)) is True
    assert m.is_supported((3, 15, 1)) is True
    assert m.is_supported((4, 0, 0)) is True


def test_accepts_full_version_info_tuple():
    assert m.is_supported((3, 14, 1, "final", 0)) is True
