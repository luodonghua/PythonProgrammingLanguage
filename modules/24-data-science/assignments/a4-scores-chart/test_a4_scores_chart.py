import pandas as pd
import pytest

from practice import load

m = load(__file__)

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@pytest.fixture
def tables():
    return pd.read_csv(m.HERE / "scores.csv"), pd.read_csv(m.HERE / "students.csv")


def test_class_averages(tables):
    result = m.class_averages(*tables)
    assert result == {"7A": 78.8, "7B": 71.3, "7C": 95.0}
    assert list(result) == ["7A", "7B", "7C"]


def test_class_averages_returns_plain_floats(tables):
    result = m.class_averages(*tables)
    assert isinstance(result, dict)
    assert all(type(v) is float for v in result.values())


def test_class_averages_small_tables():
    scores = pd.DataFrame({"student_id": [1, 2], "subject": ["a", "a"], "score": [10, 20]})
    students = pd.DataFrame({"student_id": [1, 2], "name": ["X", "Y"], "class": ["B", "A"]})
    assert m.class_averages(scores, students) == {"A": 20.0, "B": 10.0}


def test_best_subject_per_student(tables):
    assert m.best_subject_per_student(*tables) == {
        "Asha": "Math",
        "Ben": "Art",
        "Chen": "Art",
        "Dara": "Math",
        "Eli": "Art",
    }


def test_save_bar_chart_writes_png(tmp_path):
    target = tmp_path / "chart.png"
    result = m.save_bar_chart({"7A": 78.8, "7B": 71.3}, target, "Averages")
    assert result == target
    assert target.stat().st_size > 0
    assert target.read_bytes().startswith(PNG_SIGNATURE)


def test_save_bar_chart_closes_figure(tmp_path):
    import matplotlib.pyplot as plt

    m.save_bar_chart({"a": 1.0}, tmp_path / "c.png", "My title")
    assert (tmp_path / "c.png").exists()
    assert plt.get_fignums() == []  # the figure was closed


def test_save_bar_chart_rejects_empty_data(tmp_path):
    with pytest.raises(ValueError):
        m.save_bar_chart({}, tmp_path / "empty.png", "Nothing")
    assert not (tmp_path / "empty.png").exists()
