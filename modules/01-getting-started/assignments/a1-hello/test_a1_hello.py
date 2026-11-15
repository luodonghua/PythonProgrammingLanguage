from practice import load

m = load(__file__)


def test_greet_name():
    assert m.greet("Ada") == "Hello, Ada!"


def test_greet_strips_spaces():
    assert m.greet("  Ada ") == "Hello, Ada!"


def test_greet_empty_means_world():
    assert m.greet("") == "Hello, world!"
    assert m.greet("   ") == "Hello, world!"


def test_main_prints_greeting(capsys):
    m.main()
    assert capsys.readouterr().out == "Hello, Python!\n"
