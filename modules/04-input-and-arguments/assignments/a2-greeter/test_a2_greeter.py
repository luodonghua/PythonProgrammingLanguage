import pytest

from practice import load

m = load(__file__)


def test_simple(capsys):
    assert m.main(["Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada!\n"
    assert captured.err == ""


def test_several_words_and_shout(capsys):
    assert m.main(["Ada", "Lovelace", "--shout"]) == 0
    assert capsys.readouterr().out == "HELLO, ADA LOVELACE!\n"


def test_times_and_greeting(capsys):
    assert m.main(["Ada", "--times", "2", "--greeting", "Hi"]) == 0
    assert capsys.readouterr().out == "Hi, Ada!\nHi, Ada!\n"


def test_options_before_name(capsys):
    assert m.main(["--times", "3", "Bob"]) == 0
    assert capsys.readouterr().out == "Hello, Bob!\n" * 3


@pytest.mark.parametrize("times", ["0", "-2"])
def test_bad_times_value(capsys, times):
    assert m.main(["Ada", "--times", times]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == "error: --times must be at least 1"


def test_missing_name_exits_with_2(capsys):
    with pytest.raises(SystemExit) as info:
        m.main([])
    assert info.value.code == 2
    assert "usage" in capsys.readouterr().err.lower()


def test_times_not_a_number(capsys):
    with pytest.raises(SystemExit) as info:
        m.main(["Ada", "--times", "x"])
    assert info.value.code == 2


def test_parser_defaults():
    args = m.build_parser().parse_args(["Ada"])
    assert args.name == ["Ada"]
    assert args.times == 1
    assert args.shout is False
    assert args.greeting == "Hello"
