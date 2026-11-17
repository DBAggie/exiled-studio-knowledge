#!/usr/bin/env python3
"""Patch-note triage (plan D7 rule 4): match the lines of new patch notes to the references
they may touch, and write one review note per reference. It never edits a reference.

    python tools/refresh/triage.py --title "3.30.1" --file notes.txt [--source <url>]
    python tools/refresh/triage.py --title "3.30.1" --url <patch-notes url>
                                   [--open-issues] [--out local/triage]

- Input is the patch notes as plain text (copy the forum post into a file), or --url to
  fetch the page from the workstation and strip its markup.
- Matching is by keyword (tools/refresh/triage-keywords.json), whole words, case-insensitive.
  Stat-ID matching is not done here: stat IDs live in the app's game data, not in this
  repository.
- A line under a "Ruthless" heading, or that names Ruthless, is marked ruthless-only: most
  such lines do not change the references, which describe the standard game.
- Output: local/triage/<title>.md (git ignores local/), grouped by reference, each line cut
  to 240 characters with the source named. With --open-issues, one GitHub issue per
  reference through `gh`, skipped when an open issue with the same title exists.
Standard library only. Exit 0 written, 1 a request or gh call failed, 2 usage.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "plugins" / "poe1-expert" / "skills"
KEYWORDS = Path(__file__).resolve().parent / "triage-keywords.json"
UA = "exiled-studio-knowledge-triage/0.1 (+https://github.com/DBAggie)"
MAX_LINE = 240


def load_keywords(path: Path = KEYWORDS) -> dict[str, list[re.Pattern]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for ref, words in raw.items():
        if ref.startswith("_"):
            continue
        pats = []
        for w in words:
            w = w.strip()
            body = re.escape(w.rstrip("*")).replace(r"\ ", r"\s+")
            pats.append(re.compile(rf"(?<![A-Za-z]){body}" + (r"[A-Za-z']*" if w.endswith("*") else r"(?![A-Za-z])"), re.I))
        out[ref] = pats
    return out


def strip_html(page: str) -> str:
    page = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", page)
    page = re.sub(r"(?i)<(br|/p|/li|/h[1-6]|/div|/tr)\b[^>]*>", "\n", page)
    return html.unescape(re.sub(r"<[^>]+>", "", page))


def split_lines(text: str) -> list[tuple[str, bool]]:
    """(line, ruthless_only). A heading that names Ruthless marks the lines under it,
    until the next heading (a short line with no full stop, or one ending in a colon)."""
    out, in_ruthless = [], False
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip(" \t-*•")
        if len(line) < 4:
            continue
        heading = line.endswith(":") or (len(line) < 60 and "." not in line and not re.search(r"\d", line))
        if heading:
            in_ruthless = "ruthless" in line.lower()
            continue
        out.append((line, in_ruthless or "ruthless" in line.lower()))
    return out


def triage(text: str, keywords: dict[str, list[re.Pattern]]) -> dict[str, list[dict]]:
    hits: dict[str, list[dict]] = {}
    for line, ruthless in split_lines(text):
        for ref, pats in keywords.items():
            found = sorted({m.group(0).lower() for p in pats for m in [p.search(line)] if m})
            if found:
                hits.setdefault(ref, []).append({"line": line, "keywords": found, "ruthless": ruthless})
    return hits


def cut(line: str) -> str:
    return line if len(line) <= MAX_LINE else line[: MAX_LINE - 1].rstrip() + "…"


def issue_body(ref: str, rows: list[dict], title: str, source: str) -> str:
    out = [
        f"Patch-note triage for **{title}** found lines that may touch `plugins/poe1-expert/skills/{ref}`.",
        "",
        f"Source: {source}",
        "",
        "For each line: read it in the official notes, decide whether the reference needs a change, and if so open a PR that cites the notes. This tool only matches keywords; it does not judge and it never edits a reference.",
        "",
    ]
    std = [r for r in rows if not r["ruthless"]]
    ruth = [r for r in rows if r["ruthless"]]
    for name, group in (("Lines", std), ("Ruthless-only lines (usually no change to the reference)", ruth)):
        if group:
            out += [f"### {name}", ""] + [f"- [ ] {cut(r['line'])} _(matched: {', '.join(r['keywords'])})_" for r in group] + [""]
    return "\n".join(out)


def report(hits: dict[str, list[dict]], title: str, source: str, unmatched_refs: list[str]) -> str:
    out = [f"# Patch-note triage: {title}", "", f"Source: {source}", ""]
    if not hits:
        out += ["No line matched any reference keyword.", ""]
    for ref in sorted(hits):
        out += [f"## `{ref}`", "", issue_body(ref, hits[ref], title, source).split("\n\n", 3)[3], ""]
    if unmatched_refs:
        out += ["## References with no matching line", ""] + [f"- `{r}`" for r in unmatched_refs] + [""]
    return "\n".join(out)


def gh(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)


def open_issues(hits: dict[str, list[dict]], title: str, source: str) -> int:
    existing = gh(["issue", "list", "--state", "open", "--limit", "200", "--json", "title"])
    if existing.returncode != 0:
        print(f"gh issue list failed: {existing.stderr.strip()}", file=sys.stderr)
        return 1
    have = {i["title"] for i in json.loads(existing.stdout or "[]")}
    code = 0
    for ref in sorted(hits):
        name = f"Patch triage {title}: {Path(ref).name}"
        if name in have:
            print(f"exists: {name}")
            continue
        made = gh(["issue", "create", "--title", name, "--body", issue_body(ref, hits[ref], title, source)])
        if made.returncode != 0:
            print(f"gh issue create failed for {ref}: {made.stderr.strip()}", file=sys.stderr)
            code = 1
        else:
            print(f"opened: {made.stdout.strip()}")
    return code


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Match patch-note lines to references; write review notes.")
    ap.add_argument("--title", required=True, help='patch name, for example "3.30.1" or "3.30.0b Hotfix 5"')
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="patch notes as plain text")
    src.add_argument("--url", help="patch-notes page to fetch")
    ap.add_argument("--source", help="link to cite when --file is used")
    ap.add_argument("--out", default=str(ROOT / "local" / "triage"))
    ap.add_argument("--open-issues", action="store_true")
    args = ap.parse_args(argv[1:])

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
        source = args.source or f"file {Path(args.file).name} (no link given)"
    else:
        try:
            req = urllib.request.Request(args.url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                text = strip_html(r.read().decode("utf-8", "replace"))
        except (urllib.error.URLError, OSError) as e:
            print(f"request failed: {e}", file=sys.stderr)
            return 1
        source = args.url

    keywords = load_keywords()
    missing = [ref for ref in keywords if not (SKILLS / ref).exists()]
    if missing:
        print(f"triage-keywords.json names files that do not exist: {missing}", file=sys.stderr)
        return 2
    hits = triage(text, keywords)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    target = out / (re.sub(r"[^A-Za-z0-9.]+", "-", args.title).strip("-") + ".md")
    target.write_text(report(hits, args.title, source, sorted(set(keywords) - set(hits))), encoding="utf-8", newline="\n")
    print(json.dumps({"written": str(target), "references": {k: len(v) for k, v in sorted(hits.items())}}))
    return open_issues(hits, args.title, source) if args.open_issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
