import pytest

from practice import load

m = load(__file__)


def scripted(*answers):
    """Return (input_fn, prompts). input_fn gives the answers one by one."""
    queue = list(answers)
    prompts = []

    def input_fn(prompt=""):
        prompts.append(prompt)
        return queue.pop(0)

    return input_fn, prompts


def test_valid_first_time(capsys):
    fn, prompts = scripted("42")
    assert m.read_int("n: ", fn) == 42
    assert prompts == ["n: "]
    assert capsys.readouterr().out == ""


def test_spaces_and_negative():
    fn, _ = scripted("  -5 ")
    assert m.read_int("n: ", fn) == -5


def test_retries_until_valid(capsys):
    fn, prompts = scripted("x", "", "3.5", "9")
    assert m.read_int("n: ", fn) == 9
    assert prompts == ["n: "] * 4
    assert capsys.readouterr().out.splitlines() == ["Invalid input."] * 3


def test_range(capsys):
    fn, _ = scripted("0", "11", "-3", "10", "7")
    assert m.read_int("n: ", fn, minimum=1, maximum=10) == 10
    assert capsys.readouterr().out.splitlines() == ["Invalid input."] * 3


def test_only_minimum():
    fn, _ = scripted("1", "5")
    assert m.read_int("n: ", fn, minimum=5) == 5


def test_only_maximum():
    fn, _ = scripted("100", "5")
    assert m.read_int("n: ", fn, maximum=50) == 5


def test_max_tries_gives_up(capsys):
    fn, prompts = scripted("a", "b", "c", "5")
    assert m.read_int("n: ", fn, max_tries=3) is None
    assert len(prompts) == 3
    assert capsys.readouterr().out.splitlines() == ["Invalid input."] * 3


def test_max_tries_success_on_last_try():
    fn, prompts = scripted("a", "b", "8")
    assert m.read_int("n: ", fn, max_tries=3) == 8
    assert len(prompts) == 3


@pytest.mark.parametrize(
    ("answer", "expected"),
    [("y", True), ("Y", True), ("yes", True), (" YES ", True), ("n", False), ("No", False), (" no ", False)],
)
def test_yes_no(answer, expected):
    fn, _ = scripted(answer)
    assert m.read_yes_no("ok? ", fn) is expected


def test_yes_no_retries(capsys):
    fn, prompts = scripted("maybe", "", "y")
    assert m.read_yes_no("ok? ", fn) is True
    assert len(prompts) == 3
    assert capsys.readouterr().out.splitlines() == ["Please answer y or n."] * 2
