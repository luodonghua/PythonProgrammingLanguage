"""Assignment 3: parse messy JSON into models.

The file ``products.json`` (same folder) holds a JSON list of product objects
with messy values: numbers written as strings, tags written as one
comma-separated string, missing fields, and some invalid rows.

``Product`` is a ``pydantic.BaseModel``:

* ``sku: str``      upper-cased, must match ``AA-123`` (two letters, a dash,
                    three digits) after upper-casing.
* ``name: str``     stripped, not empty.
* ``price: float``  greater than 0.
* ``stock: int``    0 or more, default 0.
* ``tags: list[str]``  default empty. A string such as ``"a, b"`` is split on
                    commas, each tag stripped, empty tags dropped. A list is
                    kept as it is. (Use ``field_validator("tags", mode="before")``.)

``load_products(path)`` reads the JSON file and returns ``(products, errors)``:
``products`` is the list of valid ``Product`` objects in file order and
``errors`` is a list of ``(index, message)`` tuples for invalid rows, where
``message`` is ``"<field>: <error type>"`` of the FIRST error Pydantic reports,
for example ``"price: float_parsing"``. For an error without a field name use
``"input"``. The index is the position in the JSON list.

``stock_value(products)`` returns the total of ``price * stock`` rounded to 2
decimals.
"""

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError, field_validator


class Product(BaseModel):
    """One product row."""

    # TODO: fields and validators
    ...


def load_products(path):
    """Return (valid products, [(row index, first error), ...])."""
    # TODO
    ...


def stock_value(products):
    """Return the sum of price * stock, rounded to 2 decimals."""
    # TODO
    ...


if __name__ == "__main__":
    products, errors = load_products(Path(__file__).parent / "products.json")
    print(len(products), errors)
