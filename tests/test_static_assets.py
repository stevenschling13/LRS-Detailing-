"""Well-formedness and content checks for the repo's static assets.

These tests intentionally use only the Python standard library so they can
run anywhere without adding a dependency manifest to this zero-build site.
"""

from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"
ROBOTS_PATH = REPO_ROOT / "robots.txt"
ERROR_PAGE_PATH = REPO_ROOT / "404.html"

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


class SitemapTests(unittest.TestCase):
    """Validate that ``sitemap.xml`` is well-formed and conforms to the spec."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = ET.parse(SITEMAP_PATH)
        cls.root = cls.tree.getroot()

    def test_root_element_is_urlset_in_sitemap_namespace(self) -> None:
        self.assertEqual(self.root.tag, f"{{{SITEMAP_NS}}}urlset")

    def test_has_at_least_one_url_entry(self) -> None:
        urls = self.root.findall(f"{{{SITEMAP_NS}}}url")
        self.assertGreaterEqual(len(urls), 1)

    def test_every_url_has_absolute_https_loc(self) -> None:
        urls = self.root.findall(f"{{{SITEMAP_NS}}}url")
        self.assertTrue(urls, "sitemap must contain <url> entries")
        for url in urls:
            loc = url.find(f"{{{SITEMAP_NS}}}loc")
            self.assertIsNotNone(loc, "<url> missing required <loc>")
            self.assertIsNotNone(loc.text, "<loc> must not be empty")
            parsed = urlparse(loc.text.strip())
            self.assertEqual(parsed.scheme, "https", f"non-https loc: {loc.text}")
            self.assertTrue(parsed.netloc, f"loc missing host: {loc.text}")

    def test_lastmod_values_are_valid_iso_dates(self) -> None:
        for lastmod in self.root.iter(f"{{{SITEMAP_NS}}}lastmod"):
            self.assertIsNotNone(lastmod.text)
            # date.fromisoformat raises ValueError for malformed input
            date.fromisoformat(lastmod.text.strip())

    def test_changefreq_values_are_from_spec(self) -> None:
        allowed = {
            "always",
            "hourly",
            "daily",
            "weekly",
            "monthly",
            "yearly",
            "never",
        }
        for cf in self.root.iter(f"{{{SITEMAP_NS}}}changefreq"):
            self.assertIn((cf.text or "").strip(), allowed)


class RobotsTests(unittest.TestCase):
    """Validate that ``robots.txt`` has the expected directives."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = ROBOTS_PATH.read_text(encoding="utf-8")
        cls.lines = [ln.strip() for ln in cls.text.splitlines() if ln.strip()]

    def test_file_is_not_empty(self) -> None:
        self.assertTrue(self.lines, "robots.txt must not be empty")

    def test_declares_user_agent(self) -> None:
        self.assertTrue(
            any(ln.lower().startswith("user-agent:") for ln in self.lines),
            "robots.txt must declare at least one User-agent",
        )

    def test_sitemap_directive_present_and_absolute_https(self) -> None:
        sitemap_lines = [ln for ln in self.lines if ln.lower().startswith("sitemap:")]
        self.assertEqual(
            len(sitemap_lines),
            1,
            "robots.txt must declare exactly one Sitemap line",
        )
        _, _, value = sitemap_lines[0].partition(":")
        url = value.strip()
        parsed = urlparse(url)
        self.assertEqual(parsed.scheme, "https")
        self.assertTrue(parsed.netloc)
        self.assertTrue(parsed.path.endswith("sitemap.xml"))

    def test_only_known_directives_are_used(self) -> None:
        known = {"user-agent", "allow", "disallow", "sitemap", "crawl-delay", "host"}
        for ln in self.lines:
            if ln.startswith("#"):
                continue
            key, sep, _ = ln.partition(":")
            self.assertTrue(sep, f"malformed line in robots.txt: {ln!r}")
            self.assertIn(key.strip().lower(), known, f"unknown directive: {ln!r}")


class ErrorPageTests(unittest.TestCase):
    """Sanity checks for the 404 page that ship without spinning up a browser."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.html = ERROR_PAGE_PATH.read_text(encoding="utf-8")

    def test_has_doctype(self) -> None:
        self.assertRegex(self.html[:64].lower(), r"^\s*<!doctype html>")

    def test_declares_language(self) -> None:
        self.assertRegex(self.html, r"<html[^>]*\blang=")

    def test_has_title_and_viewport(self) -> None:
        self.assertRegex(self.html, r"<title>[^<]+</title>")
        self.assertRegex(
            self.html, r'<meta[^>]+name=["\']viewport["\'][^>]*content=', re.IGNORECASE
        )

    def test_has_noindex_for_error_page(self) -> None:
        self.assertRegex(
            self.html,
            r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
            re.IGNORECASE,
        )

    def test_links_back_to_home(self) -> None:
        self.assertRegex(self.html, r'href=["\']/["\']')


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
