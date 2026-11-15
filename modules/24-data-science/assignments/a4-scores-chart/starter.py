"""Assignment 4: Merge two tables and draw a bar chart.

Data in this folder: scores.csv (student_id, subject, score) and
students.csv (student_id, name, class).
Practise merge, groupby, and matplotlib with the Agg backend.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw to files only; no window is needed
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).parent


def class_averages(scores: pd.DataFrame, students: pd.DataFrame) -> dict[str, float]:
    """Average score per class, as a plain dict sorted by class name.

    Join `scores` to `students` on student_id (an inner merge is fine: every
    score has a student), group by class, take the mean of score and round to
    1 decimal. Example shape: {"7A": 78.8, "7B": 71.3, "7C": 95.0}
    """
    # TODO: scores.merge(students, on="student_id"), then groupby("class").
    ...


def best_subject_per_student(scores: pd.DataFrame, students: pd.DataFrame) -> dict[str, str]:
    """Map each student NAME to the subject where they scored highest.

    Assume no ties inside one student. Use idxmax on the score column of each
    student group, or sort and drop_duplicates.
    Example shape: {"Asha": "Math", "Ben": "Art"}
    """
    # TODO
    ...


def save_bar_chart(data: dict[str, float], path: Path, title: str) -> Path:
    """Draw a bar chart of `data` (labels -> heights) and save it as an image.

    - Raise ValueError if `data` is empty.
    - Set the title and label the y axis "Average score".
    - Save to `path` (a PNG), close the figure with plt.close(fig), and
      return `path`.
    """
    # TODO: fig, ax = plt.subplots(); ax.bar(list(data), list(data.values())); fig.savefig(path)
    ...


if __name__ == "__main__":
    scores = pd.read_csv(HERE / "scores.csv")
    students = pd.read_csv(HERE / "students.csv")
    averages = class_averages(scores, students)
    print(averages)
    print(save_bar_chart(averages, Path("averages.png"), "Average score by class"))
