#!/usr/bin/env python3
"""Check every eval case in evals/suites/*.jsonl (standard library only).

A case is one JSON object per line:
  id            unique, `<suite>-<nnn>`
  suite         mechanics | traps | diagnosis | tool-discipline | snapshot-honesty
  game          poe1 | poe2
  patch         e.g. 3.30.0
  prompt        what the user asks
  setup         {"app_mcp": bool, "knowledge_mcp": bool, "build": optional fixture path}
  key_status    draft-question | maintainer-approved
  key           null until the maintainer writes it; then
                {"must": [..], "must_not": [..], "sources": [..]} or {"rubric": [..]}
  expect_tools  optional list of tool names the answer must call (tool-discipline)

Rules (plan D8): answer keys are written or approved by the maintainer, never by the
sessions that write the knowledge. A case with key_status `draft-question` must have
key null; a `maintainer-approved` case must have a key.
Exit 0 clean, 1 findings.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUITES = {"mechanics", "traps", "diagnosis", "tool-discipline", "snapshot-honesty"}
REQUIRED = ("id", "suite", "game", "patch", "prompt", "setup", "key_status", "key")


def check_case(case: dict) -> list[str]:
    errs = [f"missing `{k}`" for k in REQUIRED if k not in case]
    if errs:
        return errs
    if case["suite"] not in SUITES:
        errs.append(f"unknown suite {case['suite']!r}")
    if not re.match(rf"^{re.escape(case['suite'])}-[0-9]{{3}}$", case["id"]):
        errs.append(f"id {case['id']!r} is not <suite>-<nnn>")
    if case["game"] not in ("poe1", "poe2"):
        errs.append(f"unknown game {case['game']!r}")
    if not isinstance(case["setup"], dict) or not {"app_mcp", "knowledge_mcp"} <= case["setup"].keys():
        errs.append("setup needs app_mcp and knowledge_mcp")
    if case["key_status"] == "draft-question" and case["key"] is not None:
        errs.append("a draft question must not carry a key (keys are the maintainer's)")
    elif case["key_status"] == "maintainer-approved" and not case["key"]:
        errs.append("an approved case needs a key")
    elif case["key_status"] not in ("draft-question", "maintainer-approved"):
        errs.append(f"unknown key_status {case['key_status']!r}")
    if case["suite"] == "tool-discipline" and not case.get("expect_tools"):
        errs.append("a tool-discipline case needs expect_tools")
    return errs


def main() -> int:
    findings: list[str] = []
    seen: set[str] = set()
    for f in sorted((ROOT / "suites").glob("*.jsonl")):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            where = f"{f.name}:{n}"
            try:
                case = json.loads(line)
            except json.JSONDecodeError as e:
                findings.append(f"{where}: {e}")
                continue
            findings += [f"{where}: {e}" for e in check_case(case)]
            if case.get("id") in seen:
                findings.append(f"{where}: duplicate id {case.get('id')}")
            seen.add(case.get("id"))
    for x in findings:
        print(x)
    print(f"{len(seen)} case(s), {len(findings)} finding(s)", file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
