"""Generate quiz.md and assignments.md for a topic from its metadata.

Usage:  python3 scripts/gen_pages.py <slug> [<slug> ...]

Reads  modules/<slug>/assignments/meta.yml  and  _data/modules.yml.
Writes modules/<slug>/quiz.md and modules/<slug>/assignments.md.
Every assignment folder listed in meta.yml must exist.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

QUIZ = """---
layout: module
module: {slug}
kind: quiz
title: {title} - test
permalink: /modules/{slug}/quiz/
---
Pick an answer for each question. You see at once whether it is right and why. No submit button is needed, and you can press **Reset** to try again.

{{% include quiz.html %}}
"""

HEAD = """---
layout: module
module: {slug}
kind: assignments
title: {title} - assignments
permalink: /modules/{slug}/assignments/
---
{intro}

{{% include practice-setup.md %}}
{setup}
Run all tests for this topic:

```bash
uv run pytest modules/{slug}
```

---
"""

ITEM = """
<div class="assignment" markdown="1">

## Assignment {n}: {title}

**Goal:** {goal}

**Files:** [`starter.py`]({{{{ '{base}/starter.py' | relative_url }}}}), test file `{testfile}` in the same folder.{files_note}

```python
{{% include_relative assignments/{d}/starter.py %}}
```

Run: `uv run pytest {base}`
{run_note}
<details markdown="1">
<summary>Show solution</summary>

```python
{{% include_relative assignments/{d}/solution.py %}}
```

{solution_note}
</details>

</div>
"""

TAIL = """
<ul class="checks">
  <li><label><input type="checkbox" data-progress="{slug}:assignments"> I have finished the assignments</label></li>
</ul>
"""


def gen(slug: str) -> None:
    mods = {m["slug"]: m for m in yaml.safe_load((ROOT / "_data/modules.yml").read_text())}
    title = mods[slug]["title"]
    folder = ROOT / "modules" / slug
    meta = yaml.safe_load((folder / "assignments/meta.yml").read_text())
    items = meta["assignments"]
    word = {3: "Three", 4: "Four", 5: "Five"}.get(len(items), str(len(items)))
    intro = meta.get("intro") or (
        f"{word} tasks. Write the code yourself first, run the tests, "
        "and open the solution only after you have tried."
    )
    setup = ("\n" + meta["setup"].strip() + "\n") if meta.get("setup") else ""
    out = HEAD.format(slug=slug, title=title, intro=intro.strip(), setup=setup)
    for n, a in enumerate(items, 1):
        d = a["dir"]
        adir = folder / "assignments" / d
        if not adir.is_dir():
            raise SystemExit(f"{slug}: missing folder {adir}")
        tests = sorted(p.name for p in adir.glob("test_*.py"))
        if not tests:
            raise SystemExit(f"{slug}/{d}: no test file")
        fn = a.get("files_note", "").strip()
        rn = a.get("run_note", "").strip()
        out += ITEM.format(
            n=n, title=a["title"], goal=a["goal"].strip(), d=d,
            base=f"modules/{slug}/assignments/{d}", testfile=tests[0],
            files_note=(" " + fn) if fn else "",
            run_note=("\n" + rn + "\n") if rn else "",
            solution_note=a["solution_note"].strip(),
        )
    out += TAIL.format(slug=slug)
    (folder / "assignments.md").write_text(out)
    (folder / "quiz.md").write_text(QUIZ.format(slug=slug, title=title))
    print(f"{slug}: wrote quiz.md and assignments.md ({len(items)} assignments)")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        gen(s)
