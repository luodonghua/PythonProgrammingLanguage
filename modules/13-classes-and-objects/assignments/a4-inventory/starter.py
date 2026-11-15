"""Assignment 4: A shop inventory with an alternative constructor."""


class Inventory:
    """Counts how many of each item are in stock.

    Inventory()                 starts empty.
    .add(name, qty=1)           add qty items. qty must be > 0, else ValueError.
    .remove(name, qty=1)        remove qty items. qty must be > 0, else ValueError.
                                Removing more than are in stock (or an unknown item)
                                raises ValueError and changes nothing.
                                When the count reaches 0 the item is no longer listed.
    .quantity(name)             how many are in stock (0 if unknown).
    .total                      property: the total number of items (sum of all counts).
    name in inv                 True when quantity(name) > 0.
    len(inv)                    number of distinct item names in stock.
    iter(inv)                   item names in alphabetical order.
    Inventory.from_text(text)   class method: build an inventory from lines like
                                "apple: 3" (name, a colon, a whole number).
                                Blank lines are ignored. Repeated names are added up.
                                A line that does not match raises ValueError.
    """

    def __init__(self):
        # TODO: create the dict that maps names to counts.
        ...

    def add(self, name, qty=1):
        # TODO
        ...

    def remove(self, name, qty=1):
        # TODO
        ...

    def quantity(self, name):
        # TODO
        ...

    # TODO: add the `total` property, __contains__, __len__ and __iter__.

    @classmethod
    def from_text(cls, text):
        # TODO: build an Inventory with cls() and add each line.
        ...


if __name__ == "__main__":
    inv = Inventory.from_text("apple: 3\npear: 2\napple: 1")
    inv.remove("pear")
    print(list(inv), inv.total, inv.quantity("apple"))
