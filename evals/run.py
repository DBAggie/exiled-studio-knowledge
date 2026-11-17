#!/usr/bin/env python3
"""Eval runner (plan D8, REVIEW-QUEUE Q5): run by hand on the workstation, never in CI.

    python evals/run.py [--suite mechanics ...] [--id mechanics-001 ...] [--arms plugin plain]
                        [--app-mcp-config <file>] [--model <name>] [--grader-model <name>]
                        [--out local/eval-runs/<name>] [--limit N] [--dry-run]

For every approved case, and for each arm:
  plugin   Claude Code in print mode with this repository's `poe1-expert` plugin loaded
  plain    the same call with no plugin
the answer is saved, then graded by a second, separate model call that sees only the
prompt, the answer, the tool names the answer called and the maintainer's key. Tool
discipline (`expect_tools`) is checked from the transcript, not by the grader.

How Claude is called: the `claude` command line (Claude Code), `-p` with
`--output-format stream-json`, in an empty working directory so no project instructions
leak in. Set EVAL_CLAUDE_CMD to use another command (the tests use a fake one); it gets the
same arguments.

A case whose setup needs the app MCP is skipped unless --app-mcp-config names an MCP config
file for a running Exiled Studio. A diagnosis case whose build fixture is still "TBD" runs
from its prompt alone and is marked `no-fixture`.

Output (under local/, which git ignores): results.jsonl (one line per case and arm) and
summary.md (pass rates per suite and arm, and the v1 gates). Nothing is committed.
Standard library only. Exit 0 ran, 1 a call failed, 2 usage.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITES = ROOT / "evals" / "suites"
PLUGIN = ROOT / "plugins" / "poe1-expert"
ARMS = ("plugin", "plain")

GRADER_PROMPT = """You are grading one answer about Path of Exile against a key written by the project's maintainer.
Judge only against the key. Do not use your own knowledge of the game to add or waive requirements.

Question:
<question>
{prompt}
</question>

Answer being graded:
<answer>
{answer}
</answer>

Tools the answer called, in order: {tools}

Key. Each "must" item has to be clearly present in the answer (same meaning, any wording).
Each "must_not" item has to be absent.
<key>
{key}
</key>

Reply with one JSON object and nothing else:
{{"must": [{{"item": <index from 0>, "met": true|false, "why": "<short>"}}, ...],
  "must_not": [{{"item": <index from 0>, "violated": true|false, "why": "<short>"}}, ...]}}
"""


def load_cases(suites: list[str] | None, ids: list[str] | None) -> list[dict]:
    cases = []
    for f in sorted(SUITES.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                cases.append(json.loads(line))
    if suites:
        cases = [c for c in cases if c["suite"] in suites]
    if ids:
        cases = [c for c in cases if c["id"] in ids]
    return cases


def claude_cmd() -> list[str]:
    return shlex.split(os.environ.get("EVAL_CLAUDE_CMD", "claude"), posix=os.name != "nt")


def call_claude(prompt: str, extra: list[str], model: str | None, timeout: int) -> dict:
    """One print-mode call. Returns {"text", "tools", "error"}."""
    cmd = claude_cmd() + ["-p", prompt, "--output-format", "stream-json", "--verbose", "--no-session-persistence"]
    if model:
        cmd += ["--model", model]
    cmd += extra
    with tempfile.TemporaryDirectory(prefix="eval-cwd-") as cwd:
        try:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"text": "", "tools": [], "error": f"timeout after {timeout}s"}
        except OSError as e:
            return {"text": "", "tools": [], "error": f"cannot run {cmd[0]!r}: {e}"}
    return parse_stream(p.stdout, p.returncode, p.stderr)


def parse_stream(stdout: str, code: int, stderr: str = "") -> dict:
    text, tools, final = [], [], None
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            for block in (ev.get("message") or {}).get("content") or []:
                if block.get("type") == "text":
                    text.append(block.get("text", ""))
                elif block.get("type") == "tool_use":
                    tools.append(block.get("name", ""))
        elif ev.get("type") == "result":
            final = ev
    answer = (final or {}).get("result") or "\n".join(t for t in text if t)
    error = None
    if code != 0 or (final or {}).get("is_error"):
        error = (stderr.strip() or str((final or {}).get("result")) or f"exit {code}")[:500]
    elif not answer:
        error = "no answer in the output"
    return {"text": answer or "", "tools": tools, "error": error}


def short_tool(name: str) -> str:
    """mcp__server__tool -> tool, so keys can name tools without the server prefix."""
    return name.rsplit("__", 1)[-1]


def check_tools(case: dict, tools: list[str]) -> dict | None:
    want = case.get("expect_tools")
    if not want:
        return None
    called = {short_tool(t) for t in tools}
    missing = [t for t in want if t not in called]
    return {"expected": want, "missing": missing, "ok": not missing}


def extract_json(text: str) -> dict | None:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


def grade(case: dict, answer: dict, model: str | None, timeout: int) -> dict:
    key = case["key"]
    prompt = GRADER_PROMPT.format(
        prompt=case["prompt"],
        answer=answer["text"],
        tools=", ".join(short_tool(t) for t in answer["tools"]) or "none",
        key=json.dumps({"must": key.get("must", []), "must_not": key.get("must_not", [])}, ensure_ascii=False, indent=1),
    )
    # The grader gets no tools and no plugin: it only reads.
    out = call_claude(prompt, ["--tools", ""], model, timeout)
    if out["error"]:
        return {"error": f"grader: {out['error']}"}
    verdict = extract_json(out["text"])
    if verdict is None:
        return {"error": "grader: reply was not JSON"}
    must = verdict.get("must") or []
    must_not = verdict.get("must_not") or []
    if len(must) != len(key.get("must", [])) or len(must_not) != len(key.get("must_not", [])):
        return {"error": "grader: verdict does not cover every key item"}
    return {
        "must": must,
        "must_not": must_not,
        "must_met": sum(1 for m in must if m.get("met") is True),
        "must_total": len(must),
        "violations": sum(1 for m in must_not if m.get("violated") is True),
    }


def run_case(case: dict, arm: str, args: argparse.Namespace) -> dict:
    row = {"id": case["id"], "suite": case["suite"], "arm": arm, "notes": []}
    if case.get("key_status") != "maintainer-approved" or not case.get("key"):
        return row | {"status": "skipped", "reason": "no approved key"}
    setup = case.get("setup") or {}
    extra: list[str] = []
    if setup.get("app_mcp"):
        if not args.app_mcp_config:
            return row | {"status": "skipped", "reason": "needs the app MCP (--app-mcp-config)"}
        extra += ["--mcp-config", str(Path(args.app_mcp_config).resolve())]
    if arm == "plugin":
        extra += ["--plugin-dir", str(PLUGIN)]
    if str(setup.get("build", "")).startswith("fixture: TBD"):
        row["notes"].append("no-fixture")
    if args.dry_run:
        return row | {"status": "dry-run"}

    answer = call_claude(case["prompt"], extra, args.model, args.timeout)
    row |= {"answer": answer["text"], "tools": answer["tools"]}
    if answer["error"]:
        return row | {"status": "error", "reason": answer["error"]}
    verdict = grade(case, answer, args.grader_model or args.model, args.timeout)
    if "error" in verdict:
        return row | {"status": "error", "reason": verdict["error"]}
    tools = check_tools(case, answer["tools"])
    passed = verdict["must_met"] == verdict["must_total"] and verdict["violations"] == 0 and (tools is None or tools["ok"])
    return row | {"status": "pass" if passed else "fail", "grade": verdict, "tool_check": tools}


def rate(rows: list[dict]) -> str:
    done = [r for r in rows if r["status"] in ("pass", "fail")]
    if not done:
        return "n/a"
    ok = sum(1 for r in done if r["status"] == "pass")
    return f"{ok}/{len(done)} ({100 * ok / len(done):.0f}%)"


def pct(rows: list[dict]) -> float | None:
    done = [r for r in rows if r["status"] in ("pass", "fail")]
    return 100 * sum(1 for r in done if r["status"] == "pass") / len(done) if done else None


def summary(rows: list[dict], arms: list[str], started: str) -> str:
    suites = sorted({r["suite"] for r in rows})
    by = lambda s, a: [r for r in rows if r["suite"] == s and r["arm"] == a]  # noqa: E731
    out = [f"# Eval run {started}", "", "Run by hand with `evals/run.py`. Pass = every `must` met, no `must_not` violated, and every expected tool called.", ""]
    out += ["| Suite | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for s in suites:
        out.append(f"| `{s}` | " + " | ".join(rate(by(s, a)) for a in arms) + " |")
    out.append("")

    if "plugin" in arms:
        def gate(name: str, value: float | None, need: float) -> str:
            if value is None:
                return f"- {name}: not measured in this run"
            return f"- {name}: {value:.0f}% (needs {need:.0f}%): {'met' if value >= need else 'NOT met'}"

        out += ["## v1 gates (plugin arm)", ""]
        traps = pct(by("traps", "plugin"))
        out.append("- Cross-game contamination: not measured in this run" if traps is None else
                   f"- Cross-game contamination: {100 - traps:.0f}% of trap cases failed (needs 0%): {'met' if traps == 100 else 'NOT met'}")
        out.append(gate("Date disclosure on snapshot answers", pct(by("snapshot-honesty", "plugin")), 100))
        out.append(gate("Tool discipline", pct(by("tool-discipline", "plugin")), 95))
        out.append(gate("Mechanics accuracy", pct(by("mechanics", "plugin")), 90))
        d_plugin, d_plain = pct(by("diagnosis", "plugin")), pct(by("diagnosis", "plain"))
        if d_plugin is None or d_plain is None:
            out.append("- Gain over plain Claude on build diagnosis: not measured in this run (needs both arms)")
        else:
            out.append(f"- Gain over plain Claude on build diagnosis: {d_plugin:.0f}% with the plugin, {d_plain:.0f}% without. Whether that is a clear gain is the maintainer's call.")
        out.append("")

    other = [r for r in rows if r["status"] not in ("pass", "fail")]
    if other:
        out += ["## Not graded", ""] + [f"- `{r['id']}` ({r['arm']}): {r['status']}, {r.get('reason', '')}" for r in other] + [""]
    failed = [r for r in rows if r["status"] == "fail"]
    if failed:
        out += ["## Failed", ""]
        for r in failed:
            g = r["grade"]
            why = [f"must {m['item']}: {m.get('why', '')}" for m in g["must"] if m.get("met") is not True]
            why += [f"must_not {m['item']}: {m.get('why', '')}" for m in g["must_not"] if m.get("violated") is True]
            if r.get("tool_check") and not r["tool_check"]["ok"]:
                why.append("tools not called: " + ", ".join(r["tool_check"]["missing"]))
            out.append(f"- `{r['id']}` ({r['arm']}): " + "; ".join(why))
        out.append("")
    if any("no-fixture" in r["notes"] for r in rows):
        out += ["Diagnosis cases marked `no-fixture` ran from the prompt alone; their build fixtures are not written yet.", ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Run the eval suites with and without the plugin, then grade.")
    ap.add_argument("--suite", nargs="*")
    ap.add_argument("--id", nargs="*")
    ap.add_argument("--arms", nargs="*", default=list(ARMS), choices=ARMS)
    ap.add_argument("--app-mcp-config", help="MCP config file for a running Exiled Studio (cases with setup.app_mcp)")
    ap.add_argument("--model")
    ap.add_argument("--grader-model")
    ap.add_argument("--out")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--timeout", type=int, default=600, help="seconds per model call")
    ap.add_argument("--dry-run", action="store_true", help="list what would run; no model calls")
    args = ap.parse_args(argv[1:])

    cases = load_cases(args.suite, args.id)
    if args.limit:
        cases = cases[: args.limit]
    if not cases:
        print("no cases match", file=sys.stderr)
        return 2
    started = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    out = Path(args.out) if args.out else ROOT / "local" / "eval-runs" / started
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    with (out / "results.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for case in cases:
            for arm in args.arms:
                row = run_case(case, arm, args)
                rows.append(row)
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                print(f"{row['id']:24} {arm:7} {row['status']}" + (f"  ({row['reason']})" if row.get("reason") else ""))
    (out / "summary.md").write_text(summary(rows, args.arms, started), encoding="utf-8", newline="\n")
    print(f"\nwrote {out / 'summary.md'}")
    return 1 if any(r["status"] == "error" for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
