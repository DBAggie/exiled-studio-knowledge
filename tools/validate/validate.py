#!/usr/bin/env python3
"""Validate the knowledge pack (standard library only).

Checks:
  1. headers: every knowledge file has a header matching schema/knowledge-header.schema.json
     (references/*.md and snapshots/**/*.md front matter; snapshots/**/*.json `header` object).
  2. game separation: files under plugins/poe1-expert say game poe1; poe2-expert, poe2.
  3. links: relative Markdown links resolve to files in the repo.
  4. versions: each plugin's plugin.json version equals its marketplace entry; poe1-expert's
     version is `<patch>-kb.<n>`.

Exit 0 when clean, 1 with findings (one per line), 2 on usage error.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "schema" / "knowledge-header.schema.json").read_text(encoding="utf-8"))
LINK = re.compile(r"\]\(([^)\s]+)\)")
KB_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+-kb\.[0-9]+$")


def parse_front_matter(text: str) -> dict | None:
    """Flat YAML subset: `key: value`, `key: [a, b]`, or `key:` followed by `- item` lines."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    out: dict = {}
    key = None
    for raw in text[4:end].splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- ") and key is not None:
            out.setdefault(key, [])
            if isinstance(out[key], list):
                out[key].append(_scalar(line.lstrip()[2:]))
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not m:
            raise ValueError(f"cannot read front matter line: {line!r}")
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            out[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            out[key] = [_scalar(v) for v in inner.split(",")] if inner else []
        else:
            out[key] = _scalar(value)
    return out


def _scalar(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        return v[1:-1]
    return v


def check_header(header: object, schema: dict = SCHEMA) -> list[str]:
    errs: list[str] = []
    if not isinstance(header, dict):
        return ["header is not an object"]
    for k in schema["required"]:
        if k not in header:
            errs.append(f"missing `{k}`")
    for k, v in header.items():
        spec = schema["properties"].get(k)
        if spec is None:
            errs.append(f"unknown key `{k}`")
            continue
        errs += [f"`{k}`: {e}" for e in _check(v, spec)]
    return errs


def _check(v: object, spec: dict) -> list[str]:
    t = spec.get("type")
    if t == "string":
        if not isinstance(v, str):
            return [f"expected a string, got {v!r}"]
        if "enum" in spec and v not in spec["enum"]:
            return [f"{v!r} not one of {spec['enum']}"]
        if "pattern" in spec and not re.search(spec["pattern"], v):
            return [f"{v!r} does not match {spec['pattern']}"]
        if len(v) < spec.get("minLength", 0):
            return ["empty"]
        return []
    if t == "array":
        if not isinstance(v, list):
            return [f"expected a list, got {v!r}"]
        if len(v) < spec.get("minItems", 0):
            return [f"needs at least {spec['minItems']} item(s)"]
        out: list[str] = []
        for item in v:
            out += _check(item, spec.get("items", {}))
        return out
    return []


def expected_game(path: Path) -> str | None:
    parts = path.relative_to(ROOT).parts
    if len(parts) > 1 and parts[0] == "plugins":
        return {"poe1-expert": "poe1", "poe2-expert": "poe2"}.get(parts[1])
    return None


def knowledge_files() -> list[Path]:
    files = []
    for p in sorted((ROOT / "plugins").rglob("*")):
        rel = p.relative_to(ROOT).parts
        if not p.is_file() or p.name == "README.md":
            continue
        if ("references" in rel and p.suffix == ".md") or ("snapshots" in rel and p.suffix in (".md", ".json")):
            files.append(p)
    return files


def check_headers() -> list[str]:
    findings = []
    for p in knowledge_files():
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        try:
            header = json.loads(text).get("header") if p.suffix == ".json" else parse_front_matter(text)
        except (ValueError, AttributeError) as e:
            findings.append(f"{rel}: {e}")
            continue
        if header is None:
            findings.append(f"{rel}: no header")
            continue
        findings += [f"{rel}: {e}" for e in check_header(header)]
        game = expected_game(p)
        if game and isinstance(header, dict) and header.get("game") not in (None, game):
            findings.append(f"{rel}: game {header.get('game')!r} in the {game} plugin (cross-game contamination)")
    return findings


def check_links() -> list[str]:
    findings = []
    for p in sorted(ROOT.rglob("*.md")):
        if any(part.startswith(".") and part not in (".claude-plugin",) for part in p.relative_to(ROOT).parts):
            continue
        for target in LINK.findall(p.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            dest = (p.parent / target.split("#", 1)[0]).resolve()
            if not dest.exists():
                findings.append(f"{p.relative_to(ROOT).as_posix()}: broken link {target}")
    return findings


def check_versions() -> list[str]:
    findings = []
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    for entry in market["plugins"]:
        src = (ROOT / entry["source"]).resolve()
        manifest = src / ".claude-plugin" / "plugin.json"
        if not manifest.exists():
            findings.append(f"marketplace: {entry['name']} has no {manifest.relative_to(ROOT).as_posix()}")
            continue
        plugin = json.loads(manifest.read_text(encoding="utf-8"))
        if plugin.get("name") != entry["name"]:
            findings.append(f"marketplace: name {entry['name']} != plugin.json {plugin.get('name')}")
        if plugin.get("version") != entry.get("version"):
            findings.append(f"marketplace: {entry['name']} version {entry.get('version')} != plugin.json {plugin.get('version')}")
        if entry["name"] == "poe1-expert" and not KB_VERSION.match(plugin.get("version", "")):
            findings.append(f"plugin.json: poe1-expert version {plugin.get('version')} is not <patch>-kb.<n>")
        for skill in sorted((src / "skills").glob("*/SKILL.md")):
            fm = parse_front_matter(skill.read_text(encoding="utf-8")) or {}
            if fm.get("name") != skill.parent.name:
                findings.append(f"{skill.relative_to(ROOT).as_posix()}: name {fm.get('name')!r} != folder {skill.parent.name}")
            if not fm.get("description"):
                findings.append(f"{skill.relative_to(ROOT).as_posix()}: no description")
    return findings


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        print("usage: validate.py", file=sys.stderr)
        return 2
    findings = check_headers() + check_links() + check_versions()
    for f in findings:
        print(f)
    print(f"{len(findings)} finding(s)", file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
