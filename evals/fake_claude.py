#!/usr/bin/env python3
"""Stand-in for the `claude` command, used only by test_run.py. No model is called.

Answers a question with FAKE_ANSWER and the tool calls in FAKE_TOOLS (comma separated).
When the prompt is the grader's, replies with a verdict: every `must` met and no
`must_not` violated, unless FAKE_GRADE is `fail`, `garbage` or `short`.
"""
import json
import os
import sys

args = sys.argv[1:]
prompt = args[args.index("-p") + 1]
log = os.environ.get("FAKE_LOG")
if log:
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(args) + "\n")
if os.environ.get("FAKE_EXIT"):
    sys.stderr.write("boom\n")
    sys.exit(int(os.environ["FAKE_EXIT"]))


def emit(text, tools=()):
    content = [{"type": "tool_use", "name": t, "input": {}} for t in tools] + [{"type": "text", "text": text}]
    print(json.dumps({"type": "assistant", "message": {"content": content}}))
    print(json.dumps({"type": "result", "is_error": False, "result": text}))


if "<key>" in prompt:
    key = json.loads(prompt.split("<key>")[1].split("</key>")[0])
    mode = os.environ.get("FAKE_GRADE", "pass")
    if mode == "garbage":
        emit("I cannot grade this.")
    else:
        must = [{"item": i, "met": mode != "fail", "why": "fake"} for i in range(len(key["must"]))]
        if mode == "short":
            must = must[:-1]
        emit(json.dumps({"must": must, "must_not": [{"item": i, "violated": False, "why": "fake"} for i in range(len(key["must_not"]))]}))
else:
    emit(os.environ.get("FAKE_ANSWER", "an answer"), [t for t in os.environ.get("FAKE_TOOLS", "").split(",") if t])
