# Python Programming

**Live site: <https://luodonghua.github.io/PythonProgrammingLanguage/>**

A free, self-paced Python 3 course published with GitHub Pages. It has 39 topics in two parts: basics (1-25) and advanced Python for modern applications (26-39). Each topic has:

1. **Learn**: key points, examples and common mistakes.
2. **Test**: 10 multiple-choice questions with instant right/wrong feedback and an explanation.
3. **Assignments**: 3 to 5 coding tasks with starter code, tests and a collapsible solution.

There are also two printable cheatsheets (basic and advanced) with PDF downloads.

The course uses **Python 3.14 or later** and [uv](https://docs.astral.sh/uv/).

## Practise locally

```bash
git clone https://github.com/luodonghua/PythonProgrammingLanguage.git
cd PythonProgrammingLanguage
uv sync
uv run pytest modules/01-getting-started          # runs your starter.py files
```

Topic 22 (PostgreSQL) needs a database: `docker compose up -d`. Its tests skip when no server is running.

## Preview the site locally

```bash
docker run --rm -p 4000:4000 -p 35729:35729 -v "$PWD:/srv/jekyll" \
  jekyll/jekyll jekyll serve --host 0.0.0.0 --livereload
```

## Repo layout

```
index.md, glossary.md          home page and glossary
cheatsheets/                   cheatsheet pages (data in _data/cheatsheets/)
assets/pdf/                    generated cheatsheet PDFs
_data/modules.yml              topic list and status
_data/quizzes/<topic>.yml      the 10 questions for each topic
_data/glossary/<topic>.yml     glossary terms for each topic
_layouts/, _includes/          page templates and the quiz renderer
modules/<topic>/               index.md (learn), quiz.md, assignments.md
modules/<topic>/assignments/   aN-name/ with starter.py, solution.py, test_*.py, meta.yml
scripts/                       check_site.py, gen_pages.py, build_cheatsheets.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add or change a topic.
