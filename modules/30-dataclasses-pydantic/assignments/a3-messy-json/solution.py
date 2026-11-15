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
import re
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

SKU_PATTERN = re.compile(r"[A-Z]{2}-[0-9]{3}")


class Product(BaseModel):
    """One product row."""

    model_config = ConfigDict(str_strip_whitespace=True)

    sku: str
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    tags: list[str] = []

    @field_validator("sku")
    @classmethod
    def check_sku(cls, value):
        value = value.upper()
        if not SKU_PATTERN.fullmatch(value):
            raise ValueError("sku must look like AA-123")
        return value

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, value):
        if isinstance(value, str):
            parts = (part.strip() for part in value.split(","))
            return [part for part in parts if part]
        return value


def load_products(path):
    """Return (valid products, [(row index, first error), ...])."""
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    products = []
    errors = []
    for index, row in enumerate(rows):
        try:
            products.append(Product.model_validate(row))
        except ValidationError as exc:
            first = exc.errors()[0]
            field = ".".join(str(part) for part in first["loc"]) or "input"
            errors.append((index, f"{field}: {first['type']}"))
    return products, errors


def stock_value(products):
    """Return the sum of price * stock, rounded to 2 decimals."""
    return round(sum(p.price * p.stock for p in products), 2)


if __name__ == "__main__":
    products, errors = load_products(Path(__file__).parent / "products.json")
    print(len(products), errors)
