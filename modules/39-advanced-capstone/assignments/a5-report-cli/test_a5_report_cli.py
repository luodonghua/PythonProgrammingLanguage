import json
from pathlib import Path

import pytest

from practice import load

m = load(__file__)

HERE = Path(__file__).parent


def make_result():
    tasks = [
        m.ResearchTask(id="q1", question="What causes the tides?"),
        m.ResearchTask(id="q2", question="Is the unreachable server up?"),
        m.ResearchTask(id="q3", question="Why is the sky blue?"),
    ]
    result = m.RunResult(
        findings=[
            m.Finding(task_id="q1", answer="The Moon.", confidence=0.8, sources=["wiki", "book"]),
            m.Finding(task_id="q3", answer="Scattering.", confidence=0.555),
        ],
        failures={"q2": "WorkerFailed: task q2 failed: ConnectionError: model offline"},
    )
    return tasks, result


def test_load_tasks_skips_blank_and_comment_lines(tmp_path):
    path = tmp_path / "q.txt"
    path.write_text("# header\n\n  First question?  \n   \n# another\nSecond question?\n", encoding="utf-8")
    tasks = m.load_tasks(path)
    assert [(t.id, t.question) for t in tasks] == [("q1", "First question?"), ("q2", "Second question?")]


def test_load_tasks_on_the_bundled_file():
    tasks = m.load_tasks(HERE / "questions.txt")
    assert [t.id for t in tasks] == ["q1", "q2", "q3"]
    assert tasks[2].question == "Is the unreachable server up?"


def test_load_tasks_empty_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("# only a comment\n", encoding="utf-8")
    assert m.load_tasks(path) == []


def test_load_tasks_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        m.load_tasks(tmp_path / "nope.txt")


def test_build_report_exact_text():
    tasks, result = make_result()
    assert m.build_report(tasks, result) == (
        "# Research report\n"
        "Questions: 3 | answered: 2 | failed: 1\n"
        "\n"
        "## q1: What causes the tides?\n"
        "The Moon.\n"
        "Confidence: 80%\n"
        "Sources: wiki, book\n"
        "\n"
        "## q2: Is the unreachable server up?\n"
        "FAILED: WorkerFailed: task q2 failed: ConnectionError: model offline\n"
        "\n"
        "## q3: Why is the sky blue?\n"
        "Scattering.\n"
        "Confidence: 56%\n"
    )


def test_build_report_with_no_failures_and_one_task():
    task = m.ResearchTask(id="q1", question="One question")
    result = m.RunResult(findings=[m.Finding(task_id="q1", answer="Yes", confidence=1)])
    text = m.build_report([task], result)
    assert text.startswith("# Research report\nQuestions: 1 | answered: 1 | failed: 0\n")
    assert text.endswith("Confidence: 100%\n")
    assert "FAILED" not in text and "Sources" not in text


def write_questions(tmp_path, text):
    path = tmp_path / "questions.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_main_success_prints_the_report_and_returns_0(tmp_path, capsys):
    path = write_questions(tmp_path, "What causes the tides?\nWhy is the sky blue?\n")
    assert m.main([str(path)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("# Research report\nQuestions: 2 | answered: 2 | failed: 0\n")
    assert "## q1: What causes the tides?" in out
    assert "Notes about: Why is the sky blue?" in out
    assert "Confidence: 80%" in out
    assert "Sources: demo://notes" in out


def test_main_returns_1_when_a_task_fails(capsys):
    assert m.main([str(HERE / "questions.txt")]) == 1
    out = capsys.readouterr().out
    assert "answered: 2 | failed: 1" in out
    assert "## q3: Is the unreachable server up?" in out
    assert "FAILED: WorkerFailed" in out


def test_main_json_format(tmp_path, capsys):
    path = write_questions(tmp_path, "What causes the tides?\nIs the unreachable server up?\n")
    assert m.main([str(path), "--format", "json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert [f["task_id"] for f in data["findings"]] == ["q1"]
    assert data["findings"][0]["confidence"] == 0.8
    assert list(data["failures"]) == ["q2"]


def test_main_output_file(tmp_path, capsys):
    path = write_questions(tmp_path, "What causes the tides?\n")
    target = tmp_path / "report.md"
    assert m.main([str(path), "-o", str(target)]) == 0
    assert capsys.readouterr().out == f"Report written to {target}\n"
    assert target.read_text(encoding="utf-8").startswith("# Research report\n")


def test_main_uses_the_llm_that_is_passed_in(tmp_path, capsys):
    class OneLiner:
        async def ask(self, prompt):
            return json.dumps({"answer": "custom answer", "confidence": 0.1})

    path = write_questions(tmp_path, "Any question?\n")
    assert m.main([str(path)], llm=OneLiner()) == 0
    out = capsys.readouterr().out
    assert "custom answer" in out
    assert "Confidence: 10%" in out


def test_main_missing_file(tmp_path, capsys):
    assert m.main([str(tmp_path / "missing.txt")]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "error: cannot read" in captured.err


def test_main_no_questions(tmp_path, capsys):
    path = write_questions(tmp_path, "# nothing here\n\n")
    assert m.main([str(path)]) == 2
    assert "error: no questions found" in capsys.readouterr().err


def test_main_concurrency_must_be_positive(tmp_path, capsys):
    path = write_questions(tmp_path, "Any question?\n")
    assert m.main([str(path), "--concurrency", "0"]) == 2
    assert "--concurrency must be at least 1" in capsys.readouterr().err


def test_main_bad_option_exits_with_2(tmp_path, capsys):
    path = write_questions(tmp_path, "Any question?\n")
    with pytest.raises(SystemExit) as info:
        m.main([str(path), "--format", "xml"])
    assert info.value.code == 2
