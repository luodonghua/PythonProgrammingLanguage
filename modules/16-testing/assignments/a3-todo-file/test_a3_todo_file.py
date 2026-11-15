import json

import pytest

from practice import load

m = load(__file__)


@pytest.fixture
def path(tmp_path):
    return tmp_path / "data" / "todos.json"


def test_load_missing_file_gives_empty_list(path):
    assert m.load_todos(path) == []


def test_save_creates_folders_and_load_reads_back(path):
    todos = [{"text": "naïve café", "done": True}]
    m.save_todos(path, todos)
    assert path.exists()
    assert m.load_todos(path) == todos
    assert json.loads(path.read_text(encoding="utf-8")) == todos


def test_save_uses_indent_2(path):
    m.save_todos(path, [{"text": "a", "done": False}])
    assert path.read_text(encoding="utf-8").startswith('[\n  {\n    "text"')


def test_add_todo(path):
    result = m.add_todo(path, "  buy milk ")
    assert result == {"text": "buy milk", "done": False}
    m.add_todo(path, "call mum")
    assert m.load_todos(path) == [
        {"text": "buy milk", "done": False},
        {"text": "call mum", "done": False},
    ]


@pytest.mark.parametrize("text", ["", "   "])
def test_add_empty_todo_is_rejected(path, text):
    m.add_todo(path, "keep")
    before = path.read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        m.add_todo(path, text)
    assert path.read_text(encoding="utf-8") == before


def test_complete_todo(path):
    m.add_todo(path, "a")
    m.add_todo(path, "b")
    m.complete_todo(path, 2)
    assert [t["done"] for t in m.load_todos(path)] == [False, True]


@pytest.mark.parametrize("number", [0, -1, 3])
def test_complete_out_of_range(path, number):
    m.add_todo(path, "a")
    m.add_todo(path, "b")
    before = path.read_text(encoding="utf-8")
    with pytest.raises(IndexError):
        m.complete_todo(path, number)
    assert path.read_text(encoding="utf-8") == before


def test_prompt_add(path, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "  walk the dog ")
    m.prompt_add(path)
    assert capsys.readouterr().out == "Added: walk the dog\n"
    assert m.load_todos(path) == [{"text": "walk the dog", "done": False}]


def test_prompt_add_uses_the_right_prompt(path, monkeypatch):
    seen = []

    def fake_input(prompt=""):
        seen.append(prompt)
        return "x"

    monkeypatch.setattr("builtins.input", fake_input)
    m.prompt_add(path)
    assert seen == ["New to-do: "]


def test_prompt_add_nothing(path, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "   ")
    m.prompt_add(path)
    assert capsys.readouterr().out == "Nothing to add\n"
    assert not path.exists()
