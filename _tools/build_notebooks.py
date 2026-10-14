#!/usr/bin/env python3
"""Turn Jupyter notebooks (*.ipynb) into Jekyll blog posts at build time.

Drop a notebook anywhere in the repo (ideally in notebooks/) and push. The
GitHub Actions workflow runs this script before Jekyll, which writes one post
per notebook into _posts/. Those generated posts are NOT meant to be committed.

Optional notebook metadata (Edit > Edit Notebook Metadata in Jupyter):
    {"title": "...", "description": "...", "date": "2026-06-02",
     "tags": ["ml", "ann"], "category": "Class"}

Without metadata:
    title        first '# Heading' of the notebook, else the file name
    description  a line "Summary: ..." in one of the first markdown cells
                 (the line is hidden from the post), else the first full
                 sentence-like paragraph, else a generic line
    date         YYYY-MM-DD prefix of the file name, else git first-commit date
    tags         ["jupyter"]

Cell tags understood: remove_cell, hide_input, hide_output
(with either "_" or "-").

Requires:  pip install markdown-it-py pygments
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
SYNTAX_CSS = ROOT / "assets" / "css" / "notebook-syntax.css"
SKIP_DIRS = {"_site", "node_modules", "vendor", ".git", ".bundle", ".jekyll-cache", ".ipynb_checkpoints"}

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
MATH_BLOCK = re.compile(r"\$\$(.+?)\$\$", re.S)
MATH_INLINE = re.compile(r"(?<![\\$])\$(?!\s)([^$\n]+?)(?<![\s\\])\$(?!\d)")
PLACEHOLDER = re.compile(r"MATHPLACEHOLDER(\d+)END")
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})[-_ ]+(.+)$")

MD = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
PRIORITY = ["text/html", "image/svg+xml", "image/png", "image/jpeg", "text/latex", "text/markdown", "text/plain"]
TAG_REMOVE = {"remove_cell", "remove-cell"}
TAG_HIDE_IN = {"hide_input", "hide-input", "remove_input", "remove-input"}
TAG_HIDE_OUT = {"hide_output", "hide-output", "remove_output", "remove-output"}


# ----------------------------------------------------------------- helpers
def text_of(value) -> str:
    return "".join(value) if isinstance(value, list) else (value or "")


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def q(value: str) -> str:
    """YAML-safe double-quoted scalar (JSON strings are valid YAML)."""
    return json.dumps(value, ensure_ascii=False)


def clean_stream(text: str) -> str:
    text = ANSI.sub("", text.replace("\r\n", "\n"))
    return "\n".join(line.split("\r")[-1] for line in text.split("\n"))


def find_notebooks() -> list[Path]:
    found = []
    for path in sorted(ROOT.rglob("*.ipynb")):
        folders = path.relative_to(ROOT).parts[:-1]
        if any(part in SKIP_DIRS or part.startswith((".", "_")) for part in folders):
            continue
        found.append(path)
    return found


def clear_generated() -> None:
    if not POSTS.is_dir():
        return
    for old in POSTS.glob("*.html"):
        try:
            if "generated_from:" in old.read_text(encoding="utf-8")[:800]:
                old.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------- markdown
def render_markdown(md_text: str, attachments: dict | None = None) -> str:
    for name, mimes in (attachments or {}).items():
        for mime, data in mimes.items():
            uri = f"data:{mime};base64,{text_of(data).replace(chr(10), '').strip()}"
            md_text = md_text.replace(f"attachment:{name}", uri)

    stash: list[str] = []

    def keep(match: re.Match) -> str:
        stash.append(match.group(0))
        return f"MATHPLACEHOLDER{len(stash) - 1}END"

    protected = MATH_INLINE.sub(keep, MATH_BLOCK.sub(keep, md_text))
    rendered = MD.render(protected)
    return PLACEHOLDER.sub(lambda m: esc(stash[int(m.group(1))]), rendered)


# -------------------------------------------------------------------- code
def render_code(source: str, lang: str) -> str:
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        lexer = TextLexer()
    return highlight(source.rstrip("\n"), lexer, HtmlFormatter(cssclass="highlight"))


def render_data(data: dict) -> str:
    if "application/vnd.jupyter.widget-view+json" in data and "text/html" not in data:
        return ""  # interactive widgets cannot run on a static page
    for mime in PRIORITY:
        if mime not in data:
            continue
        value = text_of(data[mime])
        if mime == "text/html":
            return f'<div class="nb-html">{value}</div>'
        if mime == "image/svg+xml":
            return f'<div class="nb-image">{value}</div>'
        if mime in ("image/png", "image/jpeg"):
            b64 = value.replace("\n", "").strip()
            return f'<div class="nb-image"><img alt="Notebook output" loading="lazy" src="data:{mime};base64,{b64}"></div>'
        if mime == "text/latex":
            body = value.strip()
            if not body.startswith("$") and not body.startswith("\\["):
                body = f"$${body}$$"
            return f'<div class="nb-latex">{esc(body)}</div>'
        if mime == "text/markdown":
            return f'<div class="nb-markdown-out">{render_markdown(value)}</div>'
        return f'<pre class="nb-text">{esc(clean_stream(value))}</pre>'
    return ""


def render_output(out: dict) -> str:
    kind = out.get("output_type")
    if kind == "stream":
        cls = "nb-stderr" if out.get("name") == "stderr" else "nb-stdout"
        return f'<pre class="nb-stream {cls}">{esc(clean_stream(text_of(out.get("text"))))}</pre>'
    if kind == "error":
        trace = clean_stream("\n".join(out.get("traceback", [])) or f'{out.get("ename")}: {out.get("evalue")}')
        return f'<pre class="nb-error">{esc(trace)}</pre>'
    if kind in ("display_data", "execute_result"):
        return render_data(out.get("data", {}))
    return ""


def render_cell(cell: dict, lang: str) -> str:
    tags = set(cell.get("metadata", {}).get("tags", []))
    if tags & TAG_REMOVE:
        return ""
    kind = cell.get("cell_type")
    source = text_of(cell.get("source"))
    if kind == "markdown":
        if not source.strip():
            return ""
        return f'<div class="nb-cell nb-markdown">{render_markdown(source, cell.get("attachments"))}</div>'
    if kind != "code":
        return ""
    parts = []
    if source.strip() and not tags & TAG_HIDE_IN:
        parts.append(render_code(source, lang))
    outputs = "" if tags & TAG_HIDE_OUT else "".join(render_output(o) for o in cell.get("outputs", []))
    if outputs.strip():
        parts.append(f'<div class="nb-outputs">{outputs}</div>')
    return f'<div class="nb-cell nb-code">{"".join(parts)}</div>' if parts else ""


# ---------------------------------------------------------------- metadata
def plain(md: str) -> str:
    md = MATH_INLINE.sub("", MATH_BLOCK.sub("", md))
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"<[^>]+>", "", md)
    md = re.sub(r"[*_`>#~]", "", md)
    return re.sub(r"\s+", " ", md).strip()


def first_heading(cells: list[dict]) -> str | None:
    """Return the title from the first '# Heading' and remove it from the cell."""
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            if text_of(cell.get("source")).strip():
                return None
            continue
        lines = text_of(cell.get("source")).split("\n")
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            match = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
            if match:
                cell["source"] = "\n".join(lines[:i] + lines[i + 1:]).lstrip("\n")
                return plain(match.group(1))
            return None
    return None


SUMMARY_LINE = re.compile(r"^\s*(?:summary|description|abstract)\s*:\s*(.+?)\s*$", re.I)


def explicit_summary(cells: list[dict]) -> str | None:
    """A line 'Summary: ...' in the first few cells becomes the description."""
    for cell in cells[:3]:
        if cell.get("cell_type") != "markdown":
            continue
        lines = text_of(cell.get("source")).split("\n")
        for i, line in enumerate(lines):
            match = SUMMARY_LINE.match(line)
            if match:
                cell["source"] = "\n".join(lines[:i] + lines[i + 1:]).strip("\n")
                return plain(match.group(1))
    return None


def first_paragraph(cells: list[dict]) -> str:
    """First paragraph that reads like a sentence (not a label or a bullet fragment)."""
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        for block in re.split(r"\n\s*\n", text_of(cell.get("source"))):
            block = block.strip()
            if not block or block.startswith(("#", "```", "|", "![", "<", "---")):
                continue
            text = plain(block)
            if text.endswith(":") or len(text) < 60 or len(text.split()) < 8:
                continue
            return text if len(text) <= 160 else text[:157].rsplit(" ", 1)[0] + "…"
    return ""


def git_first_date(path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%as", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        return out[-1] if out else None
    except Exception:
        return None


def pick_date_and_stem(path: Path, meta: dict) -> tuple[str, str]:
    match = DATE_PREFIX.match(path.stem)
    if match:
        return match.group(1), match.group(2)
    for candidate in (str(meta.get("date", ""))[:10], git_first_date(path) or ""):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", candidate):
            return candidate, path.stem
    return dt.date.today().isoformat(), path.stem


def read_minutes(cells: list[dict]) -> int:
    prose = sum(len(text_of(c.get("source")).split()) for c in cells if c.get("cell_type") == "markdown")
    code = sum(len(text_of(c.get("source")).split()) for c in cells if c.get("cell_type") == "code")
    return max(1, round(prose / 200 + code / 400))


# ------------------------------------------------------------------ convert
def convert(path: Path) -> str:
    nb = json.loads(path.read_text(encoding="utf-8"))
    if int(nb.get("nbformat", 4)) < 4:
        raise ValueError("only nbformat 4 notebooks are supported (re-save in a recent Jupyter)")
    meta = nb.get("metadata", {})
    cells = nb.get("cells", [])

    date, stem = pick_date_and_stem(path, meta)
    title = meta.get("title") or first_heading(cells) or re.sub(r"[_-]+", " ", stem).strip()
    description = (
        meta.get("description")
        or explicit_summary(cells)
        or first_paragraph(cells)
        or f"{title} — a Jupyter notebook with code, results and notes."
    )
    tags = meta.get("tags") or meta.get("keywords") or ["jupyter"]
    category = meta.get("category") or "Notebook"
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "notebook"
    lang = (meta.get("language_info", {}).get("name") or meta.get("kernelspec", {}).get("language") or "python").lower()

    body = "\n".join(filter(None, (render_cell(c, lang) for c in cells)))
    body = re.sub(r"\{(%-?\s*endraw)", r"&#123;\1", body)  # never let content end the raw block
    rel = path.relative_to(ROOT).as_posix()

    front = [
        "---",
        "layout: post",
        f"title: {q(title)}",
        f"description: {q(description)}",
        f"excerpt: {q(description)}",
        f"date: {date} 00:00:00 +0000",
        f"permalink: /blog/{slug}/",
        f"categories: {json.dumps([category], ensure_ascii=False)}",
        f"tags: {json.dumps(list(tags), ensure_ascii=False)}",
        "notebook: true",
        f"notebook_path: {q(quote(rel))}",
        f"read_time: {read_minutes(cells)}",
        f"generated_from: {q(rel)}",
        "---",
    ]
    post = POSTS / f"{date}-{slug}.html"
    post.write_text("\n".join(front) + '\n{% raw %}\n<div class="notebook">\n' + body + "\n</div>\n{% endraw %}\n", encoding="utf-8")
    return f"{rel} -> {post.relative_to(ROOT).as_posix()}"


def write_syntax_css() -> None:
    SYNTAX_CSS.parent.mkdir(parents=True, exist_ok=True)
    css = HtmlFormatter(style="monokai").get_style_defs(".notebook .highlight")
    SYNTAX_CSS.write_text("/* generated by _tools/build_notebooks.py */\n" + css + "\n", encoding="utf-8")


def main() -> int:
    clear_generated()
    notebooks = find_notebooks()
    if not notebooks:
        print("No notebooks found - nothing to convert.")
        return 0
    POSTS.mkdir(exist_ok=True)
    done = 0
    for nb_path in notebooks:
        try:
            print("Converted", convert(nb_path))
            done += 1
        except Exception as exc:  # a bad notebook must never break the whole site
            print(f"::warning file={nb_path.relative_to(ROOT).as_posix()}::Could not convert notebook: {exc}")
    if done:
        write_syntax_css()
    print(f"{done} of {len(notebooks)} notebook(s) converted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
