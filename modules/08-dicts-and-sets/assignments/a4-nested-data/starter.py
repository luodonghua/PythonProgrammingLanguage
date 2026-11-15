"""Assignment 4: Nested data and inventories.

Real data often arrives as dicts inside dicts (think JSON). These helpers
read and combine such data without crashing on missing keys.
"""

from collections import Counter


def get_path(data: dict, path: str, default=None):
    """Follow a dotted path through nested dicts.

    Return `default` if any key on the way is missing, or if you reach
    something that is not a dict before the path ends. Never raise.

    config = {"db": {"host": "localhost", "port": 5432}}
    get_path(config, "db.host")            -> "localhost"
    get_path(config, "db.user", "admin")   -> "admin"
    get_path(config, "db.host.name")       -> None   (a str is not a dict)
    get_path(config, "")                   -> None   (no key is named "")
    """
    # TODO: split the path on "." and walk down one key at a time.
    ...


def set_path(data: dict, path: str, value) -> None:
    """Set a value at a dotted path, creating missing dicts on the way.
    Change `data` in place and return None.

    d = {}
    set_path(d, "a.b.c", 1)   # d is now {"a": {"b": {"c": 1}}}
    """
    # TODO: walk down with setdefault(key, {}), then assign the last key.
    ...


def merge_inventories(*inventories: dict[str, int]) -> dict[str, int]:
    """Add up item counts from any number of inventories.

    merge_inventories({"apple": 2, "pear": 1}, {"apple": 3})
        -> {"apple": 5, "pear": 1}
    merge_inventories()  -> {}

    Return a plain dict. Do not change the arguments.
    """
    # TODO: Counter objects can be added together, or loop and use .get.
    ...


def low_stock(inventory: dict[str, int], threshold: int = 2) -> list[str]:
    """Return the sorted names of items whose count is below `threshold`.

    low_stock({"apple": 5, "pear": 1, "fig": 0})  -> ["fig", "pear"]
    """
    # TODO: use a comprehension.
    ...


def count_by_field(records: list[dict], field: str) -> dict:
    """Count how many records have each value of `field`.
    Records that do not have the field are counted under the key None.

    count_by_field([{"c": "red"}, {"c": "red"}, {"c": "blue"}, {}], "c")
        -> {"red": 2, "blue": 1, None: 1}
    """
    # TODO: use Counter and record.get(field).
    ...


if __name__ == "__main__":
    cfg = {"db": {"host": "localhost"}}
    print(get_path(cfg, "db.host"), get_path(cfg, "db.port", 5432))
    print(merge_inventories({"apple": 2}, {"apple": 3, "fig": 1}))
