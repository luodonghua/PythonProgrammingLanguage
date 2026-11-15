import pytest

from practice import load

m = load(__file__)


def make():
    inv = m.Inventory()
    inv.add("pear", 2)
    inv.add("apple", 3)
    return inv


def test_add_and_quantity():
    inv = make()
    inv.add("apple")
    assert inv.quantity("apple") == 4
    assert inv.quantity("pear") == 2
    assert inv.quantity("plum") == 0


def test_total_len_contains_iter():
    inv = make()
    assert inv.total == 5
    assert len(inv) == 2
    assert "apple" in inv
    assert "plum" not in inv
    assert list(inv) == ["apple", "pear"]


def test_total_is_a_property():
    assert isinstance(m.Inventory.total, property)


def test_remove_some():
    inv = make()
    inv.remove("apple", 2)
    assert inv.quantity("apple") == 1


def test_remove_all_drops_the_item():
    inv = make()
    inv.remove("pear", 2)
    assert "pear" not in inv
    assert list(inv) == ["apple"]
    assert len(inv) == 1


@pytest.mark.parametrize(("name", "qty"), [("apple", 4), ("plum", 1)])
def test_remove_too_many_changes_nothing(name, qty):
    inv = make()
    with pytest.raises(ValueError):
        inv.remove(name, qty)
    assert inv.total == 5


@pytest.mark.parametrize("qty", [0, -1])
def test_non_positive_quantities_rejected(qty):
    inv = make()
    with pytest.raises(ValueError):
        inv.add("apple", qty)
    with pytest.raises(ValueError):
        inv.remove("apple", qty)
    assert inv.total == 5


def test_from_text():
    inv = m.Inventory.from_text("apple: 3\n\n pear :2\napple: 1\n")
    assert inv.quantity("apple") == 4
    assert inv.quantity("pear") == 2
    assert isinstance(inv, m.Inventory)


def test_from_text_empty():
    assert len(m.Inventory.from_text("")) == 0


@pytest.mark.parametrize("text", ["apple", "apple: x", ": 3", "apple: -2", "apple: 1\nbad"])
def test_from_text_bad_lines(text):
    with pytest.raises(ValueError):
        m.Inventory.from_text(text)


def test_from_text_works_for_subclasses():
    class Shop(m.Inventory):
        pass

    assert isinstance(Shop.from_text("a: 1"), Shop)
