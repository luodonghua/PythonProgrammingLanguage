from practice import load

m = load(__file__)

A = ["Ann", "Bo", "Cy", "Bo"]
B = ["Bo", "Cy", "Di"]


def test_both():
    assert m.both(A, B) == ["Bo", "Cy"]


def test_either_has_no_duplicates():
    assert m.either(A, B) == ["Ann", "Bo", "Cy", "Di"]


def test_only_first():
    assert m.only_first(A, B) == ["Ann"]
    assert m.only_first(B, A) == ["Di"]


def test_on_one_list_only():
    assert m.on_one_list_only(A, B) == ["Ann", "Di"]


def test_functions_do_not_change_inputs():
    a, b = ["x", "y"], ["y", "z"]
    assert m.both(a, b) == ["y"]
    assert m.either(a, b) == ["x", "y", "z"]
    assert m.only_first(a, b) == ["x"]
    assert m.on_one_list_only(a, b) == ["x", "z"]
    assert a == ["x", "y"] and b == ["y", "z"]


def test_empty_lists():
    assert m.both([], []) == []
    assert m.either([], ["a"]) == ["a"]
    assert m.only_first(["a"], []) == ["a"]


def test_normalize():
    assert m.normalize(["  ann ", "BO", "", "ann", "  "]) == {"Ann", "Bo"}


def test_normalize_returns_set():
    assert isinstance(m.normalize(["a"]), set)


def test_compare():
    assert m.compare(["ann", "Bo "], ["BO", "di"]) == {
        "both": ["Bo"],
        "only_a": ["Ann"],
        "only_b": ["Di"],
        "all": ["Ann", "Bo", "Di"],
    }


def test_compare_keys():
    assert set(m.compare([], [])) == {"both", "only_a", "only_b", "all"}
