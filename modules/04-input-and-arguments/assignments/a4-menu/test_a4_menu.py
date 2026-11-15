from practice import load

m = load(__file__)


def run(*commands):
    """Run the menu with scripted commands. Return (tasks_left, output_lines)."""
    queue = list(commands)
    prompts = []

    def input_fn(prompt=""):
        prompts.append(prompt)
        if not queue:
            raise EOFError
        return queue.pop(0)

    out = []
    tasks = m.run_menu(input_fn, out.append)
    assert set(prompts) <= {"> "}
    return tasks, out


def test_add_list_quit():
    tasks, out = run("add buy milk", "add call Bob", "list", "quit")
    assert out == ["Added: buy milk", "Added: call Bob", "1. buy milk", "2. call Bob", "Bye!"]
    assert tasks == ["buy milk", "call Bob"]


def test_empty_list():
    tasks, out = run("list", "quit")
    assert out == ["No tasks.", "Bye!"]
    assert tasks == []


def test_done_removes_and_renumbers():
    tasks, out = run("add a", "add b", "add c", "done 2", "list", "quit")
    assert out == ["Added: a", "Added: b", "Added: c", "Done: b", "1. a", "2. c", "Bye!"]
    assert tasks == ["a", "c"]


def test_done_errors():
    _, out = run("add a", "done 0", "done 2", "done x", "done", "done 1 2", "done -1", "quit")
    assert out == ["Added: a"] + ["No such task."] * 6 + ["Bye!"]


def test_add_without_text():
    tasks, out = run("add", "add   ", "quit")
    assert out == ["Usage: add <text>", "Usage: add <text>", "Bye!"]
    assert tasks == []


def test_unknown_and_empty_lines():
    _, out = run("", "   ", "Dance now", "quit")
    assert out == ["Unknown command: Dance", "Bye!"]


def test_case_and_spaces():
    tasks, out = run("  ADD   water   the plants ", "LIST", "Quit")
    assert out == ["Added: water the plants", "1. water the plants", "Bye!"]
    assert tasks == ["water the plants"]


def test_stops_at_quit():
    queue = ["add x", "quit", "add y"]
    seen = []

    def input_fn(prompt=""):
        seen.append(prompt)
        return queue.pop(0)

    out = []
    assert m.run_menu(input_fn, out.append) == ["x"]
    assert queue == ["add y"]


def test_eof_acts_like_quit():
    tasks, out = run("add one")
    assert out == ["Added: one", "Bye!"]
    assert tasks == ["one"]
