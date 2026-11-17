"""Tests for patch-note triage.

    python -m unittest discover -s tools/refresh
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import triage  # noqa: E402

NOTES = """Player Balance
Spell Suppression now prevents 40% of Suppressed Spell Damage (previously 50%).
Fixed a bug where Damage taken Recouped as Life was not recovering Life.
The Marksman notable has been renamed.

Ruthless-specific Changes
Shaper of Flames: Hits always Ignite.

Other
Trapped chests now open faster. This is unrelated to entrapment.
"""

DEF = "poe1-mechanics/references/defences.md"
REC = "poe1-mechanics/references/recovery.md"
AIL = "poe1-mechanics/references/ailments.md"
TTM = "poe1-mechanics/references/totems-traps-mines.md"


class TriageTest(unittest.TestCase):
    def setUp(self):
        self.hits = triage.triage(NOTES, triage.load_keywords())

    def test_lines_reach_the_references_they_name(self):
        self.assertIn("Spell Suppression now prevents", self.hits[DEF][0]["line"])
        self.assertTrue(any("Recouped" in r["line"] for r in self.hits[REC]))

    def test_whole_words_only(self):
        # "Marksman" must not match the curse keyword "mark".
        self.assertFalse(any("Marksman" in r["line"] for rows in self.hits.values() for r in rows))
        # "trap*" matches "Trapped", not "entrapment" alone.
        self.assertEqual(self.hits[TTM][0]["keywords"], ["trapped"])

    def test_lines_under_a_ruthless_heading_are_marked(self):
        row = next(r for r in self.hits[AIL] if "Shaper of Flames" in r["line"])
        self.assertTrue(row["ruthless"])
        self.assertFalse(self.hits[DEF][0]["ruthless"])

    def test_every_keyword_file_exists(self):
        for ref in triage.load_keywords():
            self.assertTrue((triage.SKILLS / ref).exists(), ref)

    def test_every_reference_has_a_keyword_entry(self):
        have = {p.relative_to(triage.SKILLS).as_posix() for p in triage.SKILLS.glob("*/references/*.md") if p.name != "README.md"}
        self.assertEqual(have, set(triage.load_keywords()))

    def test_report_is_written_and_no_reference_is_touched(self):
        before = {p: p.stat().st_mtime_ns for p in triage.SKILLS.rglob("*.md")}
        with tempfile.TemporaryDirectory() as d:
            notes = Path(d) / "n.txt"
            notes.write_text(NOTES, encoding="utf-8")
            code = triage.main(["triage.py", "--title", "3.30.1 test", "--file", str(notes), "--source", "https://example.invalid/notes", "--out", d])
            text = (Path(d) / "3.30.1-test.md").read_text(encoding="utf-8")
        self.assertEqual(code, 0)
        self.assertIn(f"## `{DEF}`", text)
        self.assertIn("Ruthless-only lines", text)
        self.assertIn("https://example.invalid/notes", text)
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in triage.SKILLS.rglob("*.md")})

    def test_long_lines_are_cut(self):
        self.assertLessEqual(len(triage.cut("x" * 1000)), triage.MAX_LINE)

    def test_html_is_stripped(self):
        self.assertEqual(triage.strip_html("<p>Armour &amp; <b>Evasion</b></p><script>x</script>").strip(), "Armour & Evasion")


if __name__ == "__main__":
    unittest.main()
