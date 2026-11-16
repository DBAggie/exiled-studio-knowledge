"""Tests of validate.py: python -m unittest discover -s tools/validate"""

import unittest

import validate

GOOD = {
    "game": "poe1",
    "patch": "3.30.0",
    "league": "Covens of Umbra",
    "as_of": "2026-11-15",
    "sources": ["https://www.pathofexile.com/forum/view-forum/patch-notes"],
    "verification": "unverified",
}


class FrontMatter(unittest.TestCase):
    def test_should_read_inline_and_dash_lists(self):
        text = "---\ngame: poe1\nsources: [https://a, https://b]\ntags:\n  - x\n  - 'y'\n---\nbody"
        fm = validate.parse_front_matter(text)
        self.assertEqual(fm["sources"], ["https://a", "https://b"])
        self.assertEqual(fm["tags"], ["x", "y"])

    def test_should_return_none_without_front_matter(self):
        self.assertIsNone(validate.parse_front_matter("# title"))


class Header(unittest.TestCase):
    def test_good_header_should_pass(self):
        self.assertEqual(validate.check_header(GOOD), [])

    def test_missing_as_of_should_fail(self):
        h = dict(GOOD)
        del h["as_of"]
        self.assertIn("missing `as_of`", validate.check_header(h))

    def test_unknown_verification_should_fail(self):
        h = dict(GOOD, verification="looks-right")
        self.assertTrue(validate.check_header(h))

    def test_bad_patch_should_fail(self):
        self.assertTrue(validate.check_header(dict(GOOD, patch="3.30")))

    def test_hotfix_patch_should_pass(self):
        self.assertEqual(validate.check_header(dict(GOOD, patch="3.30.0c")), [])

    def test_empty_sources_should_fail(self):
        self.assertTrue(validate.check_header(dict(GOOD, sources=[])))

    def test_http_source_should_fail(self):
        self.assertTrue(validate.check_header(dict(GOOD, sources=["http://example.com"])))

    def test_unknown_key_should_fail(self):
        self.assertTrue(validate.check_header(dict(GOOD, author="x")))


class Repository(unittest.TestCase):
    def test_repository_should_be_clean(self):
        findings = validate.check_headers() + validate.check_links() + validate.check_versions()
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
