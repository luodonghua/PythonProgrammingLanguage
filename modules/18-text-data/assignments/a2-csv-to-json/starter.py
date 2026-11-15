"""Assignment 2: Convert a CSV file to JSON.

The file inventory.csv (same folder) has the columns: sku, name, qty, price, note.
"""

import csv
import json
from pathlib import Path


def convert_value(text: str) -> int | float | str | None:
    """Convert one CSV field to the most specific Python value.

    - "" (empty string)            -> None
    - text that int() accepts      -> int      ("120" -> 120)
    - else text float() accepts    -> float    ("1.5" -> 1.5)
    - anything else                -> the text unchanged ("Pen" -> "Pen")

    Do not strip spaces. Try int first, then float.
    """
    # TODO: try int(), then float(), else return the text.
    ...


def csv_to_json(csv_path: str | Path, json_path: str | Path) -> int:
    """Read the CSV file and write a JSON array of objects to `json_path`.

    - One object per data row, keys from the header, values via convert_value.
    - Write with indent=2 and encoding="utf-8".
    - Return the number of rows written.
    """
    # TODO: use csv.DictReader, convert each value, then json.dump.
    ...


if __name__ == "__main__":
    src = Path(__file__).parent / "inventory.csv"
    out = Path(__file__).parent / "inventory.json"
    print(csv_to_json(src, out), "rows written to", out.name)
