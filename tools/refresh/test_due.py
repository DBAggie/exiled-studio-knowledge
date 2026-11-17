"""Tests for the refresh-due check.

    python -m unittest discover -s tools/refresh
"""
import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import due  # noqa: E402


class DueTest(unittest.TestCase):
    def test_age_and_due(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "covens").mkdir()
            (root / "covens" / "2026-11-10.json").write_text('{"header": {"status": "current"}}', encoding="utf-8")
            (root / "covens" / "2026-11-16.json").write_text('{"header": {"status": "current"}}', encoding="utf-8")
            (root / "old-league").mkdir()
            (root / "old-league" / "2026-07-01.json").write_text('{"header": {"status": "historical"}}', encoding="utf-8")
            rows = {r["league"]: r for r in due.leagues(root, dt.date(2026, 11, 20), 2)}
            self.assertEqual((rows["covens"]["newest"], rows["covens"]["age_days"], rows["covens"]["due"]), ("2026-11-16", 4, True))
            self.assertFalse(rows["old-league"]["due"])
            self.assertFalse(due.leagues(root, dt.date(2026, 11, 17), 2)[0]["due"])
            self.assertEqual(due.main(["due.py", "--root", d, "--today", "2026-11-20", "--max-age", "2"]), 1)
            self.assertEqual(due.main(["due.py", "--root", d, "--today", "2026-11-17", "--max-age", "2"]), 0)

    def test_the_real_snapshot_folder_is_read(self):
        self.assertTrue(any(r["league"] == "covens" for r in due.leagues(due.SNAPSHOTS, dt.date(2026, 11, 17), 7)))


if __name__ == "__main__":
    unittest.main()
