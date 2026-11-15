"""Assignment 3: Clean messy sensor data.

Data: sensors.csv in this folder (station, date, temp_c, humidity).
It has a missing station, missing numbers and a duplicate row.
Practise isna, dropna, fillna, drop_duplicates and groupby().transform.
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "sensors.csv"


def missing_report(df: pd.DataFrame) -> dict[str, int]:
    """Count missing values per column.

    Return a dict with only the columns that have at least one missing value,
    e.g. {"temp_c": 2}. Values are plain ints. Return {} if nothing is missing.
    """
    counts = df.isna().sum()
    return {str(name): int(count) for name, count in counts.items() if count > 0}


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of `df`. Apply these steps in this order:

    1. Drop rows with no station.
    2. Drop exact duplicate rows (keep the first).
    3. Fill missing temp_c with the mean temp_c of the SAME station,
       computed from the rows that are left after steps 1 and 2.
    4. Fill missing humidity with the median humidity of the whole table
       (again, after steps 1 and 2 and ignoring missing values).
    5. Reset the index to 0, 1, 2, ... (drop the old one).

    The input must not change.
    """
    result = df.dropna(subset=["station"]).drop_duplicates().copy()
    station_mean = result.groupby("station")["temp_c"].transform("mean")
    result["temp_c"] = result["temp_c"].fillna(station_mean)
    result["humidity"] = result["humidity"].fillna(result["humidity"].median())
    return result.reset_index(drop=True)


if __name__ == "__main__":
    raw = pd.read_csv(DATA)
    print(missing_report(raw))
    print(clean(raw))
