# Python Programming

A free, self-paced Python 3 course published with GitHub Pages. Each topic has:

1. **Learn**: key points, examples and common mistakes.
2. **Test**: 10 multiple-choice questions with instant right/wrong feedback and an explanation.
3. **Assignments**: 3 to 5 coding tasks with starter code, tests and a collapsible solution.

The course uses **Python 3.14 or later** and [uv](https://docs.astral.sh/uv/). The topic order follows *Introducing Python* (3rd ed.), and the practice style follows *Learn Python the Hard Way*.

## Practise locally

```bash
git clone https://github.com/luodonghua/PythonProgrammingLanguage.git
cd PythonProgrammingLanguage
uv sync
uv run pytest modules/01-getting-started          # your starter.py files
```

## Repo layout

```
index.md, glossary.md       home page and glossary
_data/modules.yml           topic list and status (ready / soon)
_data/quizzes/<topic>.yml   the 10 questions for each topic
_layouts/, _includes/       page templates and the quiz renderer
assets/                     CSS and JavaScript (quiz and progress tracking)
modules/<topic>/            index.md (learn), quiz.md, assignments.md
modules/<topic>/assignments/aN-name/   starter.py, solution.py, test_*.py
scripts/check_site.py       content checks used by CI
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a topic.
