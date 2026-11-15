import inspect

from practice import load

m = load(__file__)


def test_countdown_values():
    assert list(m.Countdown(3)) == [3, 2, 1]


def test_countdown_empty():
    assert list(m.Countdown(0)) == []
    assert list(m.Countdown(-2)) == []


def test_countdown_is_its_own_iterator():
    c = m.Countdown(2)
    assert iter(c) is c
    assert next(c) == 2
    assert next(c) == 1


def test_countdown_stays_empty_when_used_up():
    c = m.Countdown(2)
    assert list(c) == [2, 1]
    assert list(c) == []


def test_countdown_raises_stop_iteration():
    c = m.Countdown(1)
    next(c)
    try:
        next(c)
    except StopIteration:
        pass
    else:
        raise AssertionError("StopIteration expected")


def test_countdown_works_in_for_and_unpacking():
    a, b, c = m.Countdown(3)
    assert (a, b, c) == (3, 2, 1)
    assert [x * 2 for x in m.Countdown(2)] == [4, 2]


def test_playlist_can_be_looped_twice():
    p = m.Playlist(["a", "b", "c"])
    assert list(p) == ["a", "b", "c"]
    assert list(p) == ["a", "b", "c"]


def test_playlist_is_not_an_iterator():
    p = m.Playlist(["a"])
    assert not hasattr(p, "__next__")
    assert iter(p) is not p


def test_playlist_len_and_copy():
    titles = ["x", "y"]
    p = m.Playlist(titles)
    titles.append("z")
    assert len(p) == 2
    assert list(p) == ["x", "y"]


def test_playlist_accepts_any_iterable():
    p = m.Playlist(t for t in "ab")
    assert list(p) == ["a", "b"]
    assert list(p) == ["a", "b"]


def test_repeat_is_generator():
    p = m.Playlist(["A", "B", "C"])
    gen = p.repeat(2)
    assert inspect.isgenerator(gen)
    assert list(gen) == ["A", "B", "C", "A", "B", "C"]
    assert list(p.repeat(0)) == []
