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
    if text == "":
        return None
    for kind in (int, float):
        try:
            return kind(text)
        except ValueError:
            pass
    return text


def csv_to_json(csv_path: str | Path, json_path: str | Path) -> int:
    """Read the CSV file and write a JSON array of objects to `json_path`.

    - One object per data row, keys from the header, values via convert_value.
    - Write with indent=2 and encoding="utf-8".
    - Return the number of rows written.
    """
    with open(csv_path, newline="", encoding="utf-8") as f:
        records = [
            {key: convert_value(value) for key, value in row.items()}
            for row in csv.DictReader(f)
        ]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    return len(records)


if __name__ == "__main__":
    src = Path(__file__).parent / "inventory.csv"
    out = Path(__file__).parent / "inventory.json"
    print(csv_to_json(src, out), "rows written to", out.name)
