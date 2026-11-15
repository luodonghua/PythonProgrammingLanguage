# Adding a topic

1. Set `status: ready` for the topic in `_data/modules.yml`.
2. Create `modules/<slug>/index.md`. Copy an existing topic and change the `module:` and `permalink:` values.
3. Create `_data/quizzes/<slug>.yml` with exactly 10 questions: `q`, `options` (2 to 5), `answer` (a letter, balanced across A-D) and `why`. Create `_data/glossary/<slug>.yml`.
4. Create 3 to 5 folders `modules/<slug>/assignments/aN-name/` with `starter.py`, `solution.py` and `test_*.py`. Tests use `from practice import load` and `m = load(__file__)`. Describe the assignments in `modules/<slug>/assignments/meta.yml`.
5. Generate the other two pages: `python3 scripts/gen_pages.py <slug>`.
6. Cheatsheets: edit `_data/cheatsheets/*.yml`, then run `python3 scripts/build_cheatsheets.py` to verify the snippets and rebuild the PDFs (commit them).
7. Check locally:

   ```bash
   uv run python scripts/check_site.py
   PRACTICE_TARGET=solution uv run pytest     # must pass
   uv run pytest                              # starters should fail until completed
   ```

Do not write `{{` or `{%` in any `.py` file under `modules/`. Jekyll includes the files through Liquid and would break the page.
