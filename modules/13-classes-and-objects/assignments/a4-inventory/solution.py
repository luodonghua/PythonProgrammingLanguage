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

    def __init__(self) -> None:
        self._stock: dict[str, int] = {}

    def add(self, name: str, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[name] = self._stock.get(name, 0) + qty

    def remove(self, name: str, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError("qty must be positive")
        have = self._stock.get(name, 0)
        if qty > have:
            raise ValueError(f"only {have} of {name!r} in stock")
        if qty == have:
            del self._stock[name]
        else:
            self._stock[name] = have - qty

    def quantity(self, name: str) -> int:
        return self._stock.get(name, 0)

    @property
    def total(self) -> int:
        return sum(self._stock.values())

    def __contains__(self, name: str) -> bool:
        return name in self._stock

    def __len__(self) -> int:
        return len(self._stock)

    def __iter__(self):
        return iter(sorted(self._stock))

    @classmethod
    def from_text(cls, text: str) -> "Inventory":
        inv = cls()
        for line in text.splitlines():
            if not line.strip():
                continue
            name, sep, count = line.partition(":")
            name, count = name.strip(), count.strip()
            if not sep or not name or not count.isdigit():
                raise ValueError(f"bad line: {line!r}")
            inv.add(name, int(count))
        return inv


if __name__ == "__main__":
    inv = Inventory.from_text("apple: 3\npear: 2\napple: 1")
    inv.remove("pear")
    print(list(inv), inv.total, inv.quantity("apple"))
