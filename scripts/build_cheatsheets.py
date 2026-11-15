"""Verify cheatsheet snippets and build the downloadable PDFs.

Usage:
  python3 scripts/build_cheatsheets.py --check   # run every snippet, compare output
  python3 scripts/build_cheatsheets.py           # check, then write assets/pdf/*.pdf

A snippet with `out:` is executed and its stdout must match. A snippet without
`out:` is only compiled. `check: none` skips it (shell commands, partial code).
PDF building needs WeasyPrint (in the dev dependency group).
"""

import contextlib
import html
import io
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SHEETS = {
    "basic": "python-basic-cheatsheet.pdf",
    "advanced": "python-advanced-cheatsheet.pdf",
}


def load(name: str) -> dict:
    return yaml.safe_load((ROOT / "_data/cheatsheets" / f"{name}.yml").read_text())


def norm(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def check(name: str) -> list[str]:
    errors = []
    for sec in load(name)["sections"]:
        for i, item in enumerate(sec["items"], 1):
            label = f"{name}/{sec['title']}#{i}"
            mode = item.get("check", "run" if "out" in item else "compile")
            if mode == "none":
                continue
            code = item["code"]
            try:
                compiled = compile(code, label, "exec")
            except SyntaxError as exc:
                errors.append(f"{label}: syntax error: {exc}")
                continue
            if mode == "compile":
                continue
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(compiled, {"__name__": "__main__"})
            except Exception as exc:
                errors.append(f"{label}: raised {type(exc).__name__}: {exc}")
                continue
            if norm(buf.getvalue()) != norm(str(item["out"])):
                errors.append(
                    f"{label}: output differs\n--- expected\n{norm(str(item['out']))}"
                    f"\n--- got\n{norm(buf.getvalue())}"
                )
    return errors


def render_html(name: str) -> str:
    data = load(name)
    css = (ROOT / "assets/css/cheatsheet.css").read_text()
    parts = []
    for sec in data["sections"]:
        body = []
        for item in sec["items"]:
            code = html.escape(item["code"].rstrip())
            out = ""
            if "out" in item:
                lines = str(item["out"]).strip().splitlines()
                out = "\n" + "\n".join(html.escape("# " + ln) for ln in lines)
                out = f'<span class="out">{out.lstrip(chr(10))}</span>'
                out = "\n" + out
            body.append(f"<pre><code>{code}{out}</code></pre>")
        parts.append(f'<section class="cs-sec"><h2>{html.escape(sec["title"])}</h2>{"".join(body)}</section>')
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        f"<title>{html.escape(data['title'])}</title><style>{css}</style></head><body class='cs-pdf'>"
        f"<h1>{html.escape(data['title'])}</h1><p class='sub'>{html.escape(data['subtitle'])}</p>"
        f"<div class='cs-grid'>{''.join(parts)}</div></body></html>"
    )


def build(name: str) -> Path:
    from weasyprint import HTML

    target = ROOT / "assets/pdf" / SHEETS[name]
    target.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=render_html(name)).write_pdf(target)
    return target


if __name__ == "__main__":
    problems = []
    for n in SHEETS:
        problems += check(n)
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("cheatsheet snippets verified")
    if "--check" not in sys.argv:
        for n in SHEETS:
            print("wrote", build(n).relative_to(ROOT))
