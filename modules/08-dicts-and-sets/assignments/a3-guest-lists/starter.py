"""Assignment 3: Guest lists with sets.

Two friends each made a guest list. Use set operations to compare them.
Every function returns sorted lists so that the result is predictable.
"""


def both(list_a: list[str], list_b: list[str]) -> list[str]:
    """Guests who are on both lists, sorted.

    both(["Ann", "Bo", "Cy"], ["Bo", "Cy", "Di"])  -> ["Bo", "Cy"]
    """
    # TODO: use the & operator on two sets.
    ...


def either(list_a: list[str], list_b: list[str]) -> list[str]:
    """Guests on at least one list, each name once, sorted.

    either(["Ann", "Bo"], ["Bo", "Di"])  -> ["Ann", "Bo", "Di"]
    """
    # TODO: use the | operator.
    ...


def only_first(list_a: list[str], list_b: list[str]) -> list[str]:
    """Guests who are on `list_a` but not on `list_b`, sorted.

    only_first(["Ann", "Bo"], ["Bo", "Di"])  -> ["Ann"]
    """
    # TODO: use the - operator.
    ...


def on_one_list_only(list_a: list[str], list_b: list[str]) -> list[str]:
    """Guests who are on exactly one of the two lists, sorted.

    on_one_list_only(["Ann", "Bo"], ["Bo", "Di"])  -> ["Ann", "Di"]
    """
    # TODO: use the ^ operator.
    ...


def normalize(names: list[str]) -> set[str]:
    """Return the set of names with outer spaces removed and each name title-cased.
    Empty names are dropped.

    normalize(["  ann ", "BO", "", "ann"])  -> {"Ann", "Bo"}
    """
    # TODO: use a set comprehension.
    ...


def compare(list_a: list[str], list_b: list[str]) -> dict[str, list[str]]:
    """Normalize both lists (see `normalize`) and return a summary dict with
    exactly these keys: "both", "only_a", "only_b", "all".
    Each value is a sorted list.

    compare(["ann", "Bo "], ["BO", "di"])
        -> {"both": ["Bo"], "only_a": ["Ann"], "only_b": ["Di"], "all": ["Ann", "Bo", "Di"]}
    """
    # TODO: normalize first, then use set operations.
    ...


if __name__ == "__main__":
    print(compare(["ann", "Bo "], ["BO", "di"]))
