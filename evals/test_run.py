"""Tests for the eval runner. They use fake_claude.py; no model is called.

    python -m unittest discover -s evals
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run  # noqa: E402

FAKE = f'"{sys.executable}" "{Path(__file__).resolve().parent / "fake_claude.py"}"'


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = Path(self.tmp.name) / "calls.jsonl"
        self.env = {"EVAL_CLAUDE_CMD": FAKE, "FAKE_LOG": str(self.log)}
        self.old = {k: os.environ.get(k) for k in ("EVAL_CLAUDE_CMD", "FAKE_LOG", "FAKE_GRADE", "FAKE_TOOLS", "FAKE_EXIT", "FAKE_ANSWER")}
        for k in self.old:
            os.environ.pop(k, None)
        os.environ.update(self.env)

    def tearDown(self):
        for k, v in self.old.items():
            os.environ.pop(k, None)
            if v is not None:
                os.environ[k] = v
        self.tmp.cleanup()

    def go(self, *argv):
        out = Path(self.tmp.name) / "out"
        code = run.main(["run.py", "--out", str(out), *argv])
        rows = [json.loads(l) for l in (out / "results.jsonl").read_text(encoding="utf-8").splitlines()]
        return code, rows, (out / "summary.md").read_text(encoding="utf-8")

    def calls(self):
        return [json.loads(l) for l in self.log.read_text(encoding="utf-8").splitlines()]

    def test_both_arms_pass_and_only_the_plugin_arm_loads_the_plugin(self):
        code, rows, text = self.go("--id", "mechanics-001")
        self.assertEqual(code, 0)
        self.assertEqual([(r["arm"], r["status"]) for r in rows], [("plugin", "pass"), ("plain", "pass")])
        answers = [c for c in self.calls() if "<key>" not in c[c.index("-p") + 1]]
        self.assertEqual(["--plugin-dir" in c for c in answers], [True, False])
        self.assertIn("| `mechanics` | 1/1 (100%) | 1/1 (100%) |", text)

    def test_the_grader_gets_no_tools_and_no_plugin(self):
        self.go("--id", "mechanics-001", "--arms", "plugin")
        grader = [c for c in self.calls() if "<key>" in c[c.index("-p") + 1]]
        self.assertEqual(len(grader), 1)
        self.assertNotIn("--plugin-dir", grader[0])
        self.assertEqual(grader[0][grader[0].index("--tools") + 1], "")

    def test_a_failed_must_fails_the_case(self):
        os.environ["FAKE_GRADE"] = "fail"
        code, rows, text = self.go("--id", "traps-001", "--arms", "plugin")
        self.assertEqual(code, 0)
        self.assertEqual(rows[0]["status"], "fail")
        self.assertIn("Cross-game contamination: 100% of trap cases failed (needs 0%): NOT met", text)

    def test_a_grader_reply_that_is_not_json_or_skips_items_is_an_error_not_a_pass(self):
        for mode in ("garbage", "short"):
            os.environ["FAKE_GRADE"] = mode
            code, rows, _ = self.go("--id", "mechanics-001", "--arms", "plain")
            self.assertEqual((code, rows[0]["status"]), (1, "error"), mode)

    def test_app_cases_are_skipped_without_an_app_config(self):
        code, rows, text = self.go("--id", "tool-discipline-001", "--arms", "plugin")
        self.assertEqual((code, rows[0]["status"]), (0, "skipped"))
        self.assertIn("Tool discipline: not measured in this run", text)

    def test_expected_tools_are_checked_from_the_transcript(self):
        cfg = Path(self.tmp.name) / "mcp.json"
        cfg.write_text("{}", encoding="utf-8")
        os.environ["FAKE_TOOLS"] = "mcp__exiled-studio__get_build,mcp__exiled-studio__list_items"
        _, rows, text = self.go("--id", "tool-discipline-001", "--arms", "plugin", "--app-mcp-config", str(cfg))
        self.assertEqual(rows[0]["status"], "fail")
        self.assertEqual(rows[0]["tool_check"]["missing"], ["get_item", "preview_item_edit"])
        self.assertIn("tools not called: get_item, preview_item_edit", text)
        os.environ["FAKE_TOOLS"] += ",mcp__exiled-studio__get_item,mcp__exiled-studio__preview_item_edit"
        _, rows, _ = self.go("--id", "tool-discipline-001", "--arms", "plugin", "--app-mcp-config", str(cfg))
        self.assertEqual(rows[0]["status"], "pass")

    def test_a_failed_model_call_is_an_error(self):
        os.environ["FAKE_EXIT"] = "3"
        code, rows, _ = self.go("--id", "mechanics-001", "--arms", "plain")
        self.assertEqual((code, rows[0]["status"]), (1, "error"))

    def test_dry_run_calls_nothing(self):
        code, rows, _ = self.go("--suite", "diagnosis", "--dry-run")
        self.assertEqual(code, 0)
        self.assertTrue(all(r["status"] == "dry-run" for r in rows))
        self.assertFalse(self.log.exists())


if __name__ == "__main__":
    unittest.main()
