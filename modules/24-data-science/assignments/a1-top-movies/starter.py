"""Assignment 1: Top movies with pandas.

Data: movies.csv in this folder (title, year, rating, minutes, votes).
Practise read_csv, sort_values, head and boolean filtering.
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "movies.csv"


def load(path: Path = DATA) -> pd.DataFrame:
    """Read the CSV file at `path` into a DataFrame and return it."""
    # TODO: use pd.read_csv.
    ...


def top_n(df: pd.DataFrame, column: str, n: int = 3) -> pd.DataFrame:
    """Return the `n` rows with the largest values in `column`.

    - Largest first.
    - If two rows tie, keep their original order (sort_values(kind="stable")).
    - The result has a fresh index 0, 1, 2, ... (reset_index(drop=True)).
    - Do not change `df`.
    """
    # TODO: sort_values(column, ascending=False, kind="stable"), head(n), reset_index.
    ...


def long_good_movies(df: pd.DataFrame, min_rating: float, min_minutes: int) -> list[str]:
    """Titles with rating >= min_rating AND minutes >= min_minutes.

    Return a plain list of strings, sorted alphabetically.
    """
    # TODO: combine two conditions with & (each in parentheses).
    ...


if __name__ == "__main__":
    movies = load()
    print(top_n(movies, "rating"))
    print(long_good_movies(movies, 8.0, 150))
