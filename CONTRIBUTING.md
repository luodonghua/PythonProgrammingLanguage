# Adding a topic

1. Set `status: ready` for the topic in `_data/modules.yml`.
2. Create `modules/<slug>/index.md`, `quiz.md` and `assignments.md`. Copy an existing topic and change the `module:` and `permalink:` values.
3. Create `_data/quizzes/<slug>.yml` with exactly 10 questions: `q`, `options` (2 to 5), `answer` (a letter) and `why`.
4. Create 3 to 5 folders `modules/<slug>/assignments/aN-name/` with `starter.py`, `solution.py` and `test_*.py`. Tests use `from practice import load` and `m = load(__file__)`.
5. Include each starter and solution in `assignments.md` with `{% include_relative assignments/aN-name/starter.py %}`.
6. Check locally:

   ```bash
   uv run python scripts/check_site.py
   PRACTICE_TARGET=solution uv run pytest     # must pass
   uv run pytest                              # starters should fail until completed
   ```

Do not write `{{` or `{%` in any `.py` file under `modules/`. Jekyll includes the files through Liquid and would break the page.
