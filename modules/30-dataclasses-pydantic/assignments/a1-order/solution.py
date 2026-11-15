"""Assignment 1: dataclasses for an order.

All money is in whole cents (``int``) to avoid float rounding.

``LineItem`` is a frozen dataclass with fields ``name: str``,
``unit_cents: int`` and ``quantity: int = 1``.
* ``unit_cents`` must be >= 0 and ``quantity`` >= 1, otherwise
  ``__post_init__`` raises ``ValueError``.
* property ``total_cents`` is ``unit_cents * quantity``.

``Order`` is a dataclass with fields ``customer: str``,
``items: list[LineItem]`` (default: a new empty list for each order) and
``discount_percent: int = 0``.
* ``discount_percent`` must be between 0 and 100 (inclusive), otherwise
  ``ValueError`` in ``__post_init__``.
* property ``subtotal_cents``: sum of the item totals.
* property ``total_cents``: the subtotal minus the discount, using integer
  arithmetic: ``subtotal * (100 - discount_percent) // 100``.
* method ``with_item(item)`` returns a NEW Order with the item added at the
  end. The original order is not changed (use ``dataclasses.replace``).
* method ``to_dict()`` returns the order as nested plain dicts and lists
  (use ``dataclasses.asdict``).
"""

from dataclasses import asdict, dataclass, field, replace


@dataclass(frozen=True)
class LineItem:
    """One product line of an order."""

    name: str
    unit_cents: int
    quantity: int = 1

    def __post_init__(self):
        if self.unit_cents < 0:
            raise ValueError("unit_cents must be >= 0")
        if self.quantity < 1:
            raise ValueError("quantity must be >= 1")

    @property
    def total_cents(self):
        return self.unit_cents * self.quantity


@dataclass
class Order:
    """A customer order."""

    customer: str
    items: list[LineItem] = field(default_factory=list)
    discount_percent: int = 0

    def __post_init__(self):
        if not 0 <= self.discount_percent <= 100:
            raise ValueError("discount_percent must be between 0 and 100")

    @property
    def subtotal_cents(self):
        return sum(item.total_cents for item in self.items)

    @property
    def total_cents(self):
        return self.subtotal_cents * (100 - self.discount_percent) // 100

    def with_item(self, item):
        return replace(self, items=[*self.items, item])

    def to_dict(self):
        return asdict(self)


if __name__ == "__main__":
    order = Order("ann", [LineItem("pen", 150, 4)], discount_percent=10)
    print(order.total_cents)
    print(order.with_item(LineItem("book", 1000)).total_cents)
