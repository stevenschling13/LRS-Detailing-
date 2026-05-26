"""Regression checks for ``index.html``.

Guards business-critical content (phone, tagline, prices) and the
production-hardening details (JSON-LD validity, canonical link, favicon,
manifest, skip-link, main landmark, noscript fallback) so a future edit
that accidentally rips one of them out fails CI loudly.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "index.html"

PHONE_DIGITS = "9522559160"
PHONE_E164 = "+19522559160"
TAGLINE = "Cleaner Car"
PRICE_TIERS = ("$60", "$120", "$200")


class IndexContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = INDEX_PATH.read_text(encoding="utf-8")

    def test_doctype_and_lang(self) -> None:
        self.assertRegex(self.html[:64].lower(), r"^\s*<!doctype html>")
        self.assertRegex(self.html, r"<html[^>]*\blang=")

    def test_business_phone_present(self) -> None:
        # Raw digits show up in tel:/sms: hrefs and visible copy.
        self.assertIn(PHONE_DIGITS, self.html)
        self.assertIn(f"tel:{PHONE_E164}", self.html)
        self.assertIn(f"sms:{PHONE_E164}", self.html)

    def test_tagline_present(self) -> None:
        self.assertIn(TAGLINE, self.html)

    def test_price_tiers_present(self) -> None:
        for price in PRICE_TIERS:
            self.assertIn(price, self.html, f"missing price tier: {price}")

    def test_canonical_link(self) -> None:
        self.assertRegex(
            self.html, r'<link[^>]+rel=["\']canonical["\'][^>]*href=', re.IGNORECASE
        )

    def test_favicon_and_manifest_linked(self) -> None:
        self.assertRegex(
            self.html, r'<link[^>]+rel=["\']icon["\'][^>]*href=["\'][^"\']*favicon\.svg',
            re.IGNORECASE,
        )
        self.assertRegex(
            self.html,
            r'<link[^>]+rel=["\']manifest["\'][^>]*href=["\'][^"\']*manifest\.webmanifest',
            re.IGNORECASE,
        )

    def test_open_graph_and_twitter_card(self) -> None:
        self.assertRegex(
            self.html, r'<meta[^>]+property=["\']og:title["\']', re.IGNORECASE
        )
        self.assertRegex(
            self.html, r'<meta[^>]+property=["\']og:url["\']', re.IGNORECASE
        )
        self.assertRegex(
            self.html, r'<meta[^>]+name=["\']twitter:card["\']', re.IGNORECASE
        )

    def test_json_ld_is_valid_local_business(self) -> None:
        m = re.search(
            r'<script\s+type=["\']application/ld\+json["\']\s*>(.+?)</script>',
            self.html,
            flags=re.DOTALL | re.IGNORECASE,
        )
        self.assertIsNotNone(m, "missing JSON-LD <script> block")
        data = json.loads(m.group(1))
        self.assertEqual(data.get("@type"), "AutoDetailing")
        self.assertEqual(data.get("telephone"), "+1-952-255-9160")
        self.assertIn("address", data)
        self.assertIn("areaServed", data)
        self.assertTrue(data["areaServed"], "areaServed must not be empty")

    def test_has_main_landmark_and_skip_link(self) -> None:
        self.assertRegex(self.html, r'<main\b[^>]*id=["\']main["\']', re.IGNORECASE)
        self.assertRegex(
            self.html,
            r'<a[^>]+class=["\']skip-link["\'][^>]*href=["\']#main["\']',
            re.IGNORECASE,
        )

    def test_quote_form_has_required_fields(self) -> None:
        for name in ("name", "vehicle", "service", "city", "notes"):
            self.assertRegex(
                self.html,
                rf'name=["\']{name}["\']',
                f"quote form missing field: {name}",
            )

    def test_noscript_fallback_present(self) -> None:
        pattern = re.compile(
            r"<noscript>.*?(?:9522559160|952-255-9160).*?</noscript>",
            re.DOTALL | re.IGNORECASE,
        )
        self.assertRegex(self.html, pattern)

    def test_theme_color_meta(self) -> None:
        self.assertRegex(
            self.html,
            r'<meta[^>]+name=["\']theme-color["\']',
            re.IGNORECASE,
        )

    def test_service_card_buttons_carry_data_service(self) -> None:
        # The "Book X" buttons on the three service cards should each
        # tag themselves with data-service so the JS pre-fill knows
        # which option to select.
        for value in (
            "Express Wash ($60+)",
            "Interior Detail ($120+)",
            "Full Detail ($200+)",
        ):
            self.assertIn(
                f'data-service="{value}"',
                self.html,
                f"missing data-service for: {value}",
            )

    def test_html_has_scroll_padding_for_sticky_nav(self) -> None:
        self.assertRegex(
            self.html,
            r"html\s*\{[^}]*scroll-padding-top",
            re.IGNORECASE,
        )

    def test_reduced_motion_overrides_present(self) -> None:
        self.assertIn("prefers-reduced-motion: reduce", self.html)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
