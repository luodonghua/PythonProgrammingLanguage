import random

import pytest

from practice import load

m = load(__file__)


def test_chunks():
    assert m.chunks([1, 2, 3, 4, 5], 2) == [(1, 2), (3, 4), (5,)]
    assert m.chunks([], 3) == []
    assert m.chunks("abcd", 2) == [("a", "b"), ("c", "d")]


def test_running_totals():
    assert m.running_totals([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert m.running_totals([]) == []
    assert m.running_totals([2.5]) == [2.5]


def test_pair_count():
    assert m.pair_count(["a", "b", "c", "d"]) == 6
    assert m.pair_count(["a"]) == 0
    assert m.pair_count([]) == 0
    assert m.pair_count(list(range(10))) == 45


def test_distance():
    assert m.distance((0, 0), (3, 4)) == 5.0
    assert m.distance((1, 1), (1, 1)) == 0.0


def test_most_common_word():
    assert m.most_common_word("the cat and the hat") == "the"
    assert m.most_common_word("The the THE a") == "the"
    assert m.most_common_word("") is None


def test_most_common_word_tie_returns_first_seen():
    assert m.most_common_word("b a b a") == "b"
    assert m.most_common_word("x y") == "x"


def test_rolls_are_dice_values():
    result = m.rolls(200, seed=1)
    assert len(result) == 200
    assert set(result) <= {1, 2, 3, 4, 5, 6}
    assert len(set(result)) > 1


def test_rolls_same_seed_same_result():
    assert m.rolls(10, seed=7) == m.rolls(10, seed=7)
    assert m.rolls(10, seed=7) != m.rolls(10, seed=8)


def test_rolls_match_a_private_generator():
    rng = random.Random(123)
    expected = [rng.randint(1, 6) for _ in range(8)]
    assert m.rolls(8, seed=123) == expected


def test_rolls_do_not_touch_global_random_state():
    random.seed(99)
    before = random.getstate()
    assert len(m.rolls(5, seed=1)) == 5
    assert random.getstate() == before


def test_rolls_zero():
    assert m.rolls(0, seed=1) == []


def test_to_json():
    assert m.to_json({"b": 1, "a": [1, 2]}) == '{\n  "a": [\n    1,\n    2\n  ],\n  "b": 1\n}'
    assert m.to_json({}) == "{}"


def test_spread():
    assert m.spread([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(2.13809, abs=1e-4)
    assert m.spread([1, 3]) == pytest.approx(1.41421, abs=1e-4)
    assert m.spread([5]) == 0.0
    assert m.spread([]) == 0.0
