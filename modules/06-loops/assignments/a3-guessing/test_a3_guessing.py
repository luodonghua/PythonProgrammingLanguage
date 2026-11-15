import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("secret", "guess", "expected"),
    [(50, 30, "too low"), (50, 80, "too high"), (50, 50, "correct"), (1, 0, "too low")],
)
def test_judge(secret, guess, expected):
    assert m.judge(secret, guess) == expected


def test_play_win():
    assert m.play(7, [3, 9, 7, 1]) == (True, ["too low", "too high", "correct"])


def test_play_stops_at_first_correct():
    won, feedback = m.play(5, [5, 5, 5])
    assert won is True
    assert feedback == ["correct"]


def test_play_out_of_tries():
    assert m.play(7, [1, 2, 3], 2) == (False, ["too low", "too low"])


def test_play_win_on_last_allowed_try():
    assert m.play(7, [1, 2, 7], 3) == (True, ["too low", "too low", "correct"])


def test_play_win_after_limit_does_not_count():
    assert m.play(7, [1, 2, 7], 2) == (False, ["too low", "too low"])


def test_play_no_guesses():
    assert m.play(7, []) == (False, [])


def test_play_ran_out_of_guesses_before_limit():
    assert m.play(7, [1, 9]) == (False, ["too low", "too high"])


def test_play_default_limit_is_seven():
    won, feedback = m.play(100, [1] * 10)
    assert won is False
    assert len(feedback) == 7


@pytest.mark.parametrize(
    ("low", "high", "secret", "expected"),
    [(1, 100, 50, 1), (1, 100, 1, 6), (1, 10, 10, 4), (5, 5, 5, 1)],
)
def test_best_strategy(low, high, secret, expected):
    assert m.best_strategy(low, high, secret) == expected


def test_best_strategy_never_needs_more_than_seven_for_100():
    assert max(m.best_strategy(1, 100, s) for s in range(1, 101)) == 7
