import pandas as pd

from practice import load

m = load(__file__)


def test_load_reads_all_rows():
    df = m.load()
    assert df.shape == (8, 5)
    assert df.columns.tolist() == ["title", "year", "rating", "minutes", "votes"]
    assert df["votes"].sum() == 21400


def test_top_n_by_rating_with_tie_order():
    df = m.load()
    top = m.top_n(df, "rating", 3)
    assert top["title"].tolist() == ["The Quiet Harbor", "Long Road Home", "Iron Garden"]
    assert top.index.tolist() == [0, 1, 2]


def test_top_n_default_is_three():
    assert len(m.top_n(m.load(), "votes")) == 3


def test_top_n_other_column():
    top = m.top_n(m.load(), "minutes", 2)
    assert top["title"].tolist() == ["Last Orchard", "Long Road Home"]


def test_top_n_does_not_change_input():
    df = m.load()
    before = df.copy()
    m.top_n(df, "rating", 2)
    pd.testing.assert_frame_equal(df, before)


def test_top_n_larger_than_table():
    assert len(m.top_n(m.load(), "rating", 50)) == 8


def test_long_good_movies():
    assert m.long_good_movies(m.load(), 8.0, 150) == ["Iron Garden", "Last Orchard", "Long Road Home"]


def test_long_good_movies_needs_both_conditions():
    assert m.long_good_movies(m.load(), 8.5, 150) == []
    assert m.long_good_movies(m.load(), 7.0, 160) == ["Last Orchard", "Long Road Home"]


def test_long_good_movies_returns_plain_list():
    result = m.long_good_movies(m.load(), 0, 0)
    assert isinstance(result, list)
    assert result == sorted(result)
    assert len(result) == 8
