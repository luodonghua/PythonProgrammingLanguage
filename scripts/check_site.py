"""Sanity checks for site content. Run: uv run python scripts/check_site.py"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


modules = yaml.safe_load((ROOT / "_data/modules.yml").read_text())
slugs = [m["slug"] for m in modules]
if len(slugs) != len(set(slugs)):
    err("duplicate slug in _data/modules.yml")

only = set(sys.argv[1:])  # optional: check just these slugs, even if not "ready" yet
for m in modules:
    if (only and m["slug"] not in only) or (not only and m["status"] != "ready"):
        continue
    slug = m["slug"]
    folder = ROOT / "modules" / slug

    for page in ("index.md", "quiz.md", "assignments.md"):
        if not (folder / page).exists():
            err(f"{slug}: missing {page}")

    quiz_file = ROOT / "_data/quizzes" / f"{slug}.yml"
    if not quiz_file.exists():
        err(f"{slug}: missing quiz data")
    else:
        questions = yaml.safe_load(quiz_file.read_text())
        letters = [q.get("answer") for q in questions]
        if max(letters.count(c) for c in "ABCD") > 4:
            err(f"{slug}: answer letters are unbalanced: {''.join(letters)}")
        if len(questions) != 10:
            err(f"{slug}: expected 10 questions, found {len(questions)}")
        for n, q in enumerate(questions, 1):
            opts = q.get("options", [])
            if not 2 <= len(opts) <= 5:
                err(f"{slug} Q{n}: needs 2-5 options")
            if q.get("answer") not in "ABCDE"[: len(opts)]:
                err(f"{slug} Q{n}: answer {q.get('answer')!r} is not a valid option letter")
            if not str(q.get("why", "")).strip():
                err(f"{slug} Q{n}: missing explanation")

    gl = ROOT / "_data/glossary" / f"{slug}.yml"
    if not gl.exists():
        err(f"{slug}: missing glossary file _data/glossary/{slug}.yml")
    else:
        for t in yaml.safe_load(gl.read_text()) or []:
            if not t.get("term") or not t.get("meaning"):
                err(f"{slug}: glossary entry needs term and meaning: {t}")

    assignments = sorted(p for p in (folder / "assignments").glob("a*") if p.is_dir())
    if not 3 <= len(assignments) <= 5:
        err(f"{slug}: expected 3-5 assignments, found {len(assignments)}")
    page_text = (folder / "assignments.md").read_text() if (folder / "assignments.md").exists() else ""
    for a in assignments:
        for name in ("starter.py", "solution.py"):
            if not (a / name).exists():
                err(f"{a.relative_to(ROOT)}: missing {name}")
        if not list(a.glob("test_*.py")):
            err(f"{a.relative_to(ROOT)}: missing test file")
        for name in ("starter.py", "solution.py"):
            if f"assignments/{a.name}/{name}" not in page_text:
                err(f"{slug}/assignments.md does not include {a.name}/{name}")

# Jekyll renders included files with Liquid, so these sequences would break the page.
for py in (ROOT / "modules").rglob("*.py"):
    text = py.read_text()
    if "{{" in text or "{%" in text:
        err(f"{py.relative_to(ROOT)}: contains '{{{{' or '{{%' (breaks Liquid include)")

if errors:
    print("\n".join(f"ERROR: {e}" for e in errors))
    sys.exit(1)
print("site checks passed")
