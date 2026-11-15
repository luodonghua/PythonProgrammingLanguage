import json
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

from practice import load

m = load(__file__)

DATA = Path(__file__).parent / "products.json"


def test_product_is_a_model_and_coerces():
    assert issubclass(m.Product, BaseModel)
    p = m.Product.model_validate({"sku": "ab-100", "name": " Pencil ", "price": "0.50", "stock": "200"})
    assert p.sku == "AB-100"
    assert p.name == "Pencil"
    assert p.price == 0.5
    assert p.stock == 200
    assert p.tags == []


def test_tags_string_is_split():
    p = m.Product.model_validate({"sku": "AB-100", "name": "x", "price": 1, "tags": " a, b ,, c "})
    assert p.tags == ["a", "b", "c"]


def test_tags_empty_string_and_list():
    base = {"sku": "AB-100", "name": "x", "price": 1}
    assert m.Product.model_validate({**base, "tags": ""}).tags == []
    assert m.Product.model_validate({**base, "tags": ["q", "r"]}).tags == ["q", "r"]


def test_stock_default():
    assert m.Product.model_validate({"sku": "AB-100", "name": "x", "price": 1}).stock == 0


@pytest.mark.parametrize(
    "change",
    [
        {"sku": "A-1"},
        {"sku": "ABC-100"},
        {"sku": "AB-1000"},
        {"name": "   "},
        {"price": 0},
        {"price": -2},
        {"price": "free"},
        {"stock": -1},
        {"stock": "many"},
    ],
)
def test_invalid_product(change):
    row = {"sku": "AB-100", "name": "x", "price": 1, "stock": 1, **change}
    with pytest.raises(ValidationError):
        m.Product.model_validate(row)


def test_load_products_data_file():
    products, errors = m.load_products(DATA)
    assert [p.sku for p in products] == ["AB-100", "AB-101", "EF-300", "GH-400"]
    assert products[0].tags == ["office", "school"]
    assert products[3].tags == ["furniture", "office"]
    assert products[2].stock == 0
    assert errors == [(2, "price: float_parsing"), (3, "stock: greater_than_equal"), (5, "sku: missing")]


def test_load_products_tmp_file(tmp_path):
    f = tmp_path / "p.json"
    f.write_text(
        json.dumps([{"sku": "ZZ-999", "name": "ok", "price": 1}, "not an object", {"sku": "nope"}]),
        encoding="utf-8",
    )
    products, errors = m.load_products(f)
    assert [p.sku for p in products] == ["ZZ-999"]
    assert errors == [(1, "input: model_type"), (2, "sku: value_error")]


def test_load_products_empty_list(tmp_path):
    f = tmp_path / "p.json"
    f.write_text("[]", encoding="utf-8")
    assert m.load_products(f) == ([], [])


def test_stock_value():
    products, _ = m.load_products(DATA)
    assert m.stock_value(products) == 1030.0
    assert m.stock_value([]) == 0
