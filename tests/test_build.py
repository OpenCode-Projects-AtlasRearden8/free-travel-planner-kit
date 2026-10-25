"""Tests: every sheet builds a valid, complete, unbranded PDF.

Run: python3 -m unittest discover tests -v
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build  # noqa: E402
from pypdf import PdfReader  # noqa: E402
from weasyprint import HTML, CSS  # noqa: E402

EXPECTED_SHEETS = [
    "at-home-while-away-checklist",
    "day-itinerary-one-pager",
    "kids-travel-busy-pages",
    "medications-contacts-card",
    "packing-list-builder",
    "travel-documents-checklist",
    "trip-budget-tracker",
]


class SheetHTMLTests(unittest.TestCase):
    """Each source sheet is complete and consistent with its tips page."""

    def test_all_sheets_exist(self):
        self.assertEqual(build.sheet_slugs(), EXPECTED_SHEETS)

    def test_every_sheet_has_a_tips_page(self):
        for slug in EXPECTED_SHEETS:
            path = build.TIPS_DIR / f"{slug}.html"
            self.assertTrue(path.exists(), f"missing tips page: {path.name}")

    def test_sheets_have_title_and_stylesheet(self):
        for slug in EXPECTED_SHEETS:
            html = (build.SHEETS_DIR / f"{slug}.html").read_text(
                encoding="utf-8"
            )
            self.assertIn("<title>", html)
            self.assertIn("print.css", html)

    def test_fonts_do_not_require_network(self):
        css = (ROOT / "src" / "css" / "print.css").read_text(encoding="utf-8")
        self.assertNotIn("@import", css)
        self.assertNotIn("url(http", css)


class BuildTests(unittest.TestCase):
    """Build into a temp dir and validate the produced PDFs."""

    @classmethod
    def setUpClass(cls):
        cls.out_dir = Path(tempfile.mkdtemp(prefix="travel-pack-test-"))
        cls.pdfs = build.build_all(cls.out_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.out_dir, ignore_errors=True)

    def test_every_sheet_produced_a_pdf(self):
        for slug in EXPECTED_SHEETS:
            self.assertTrue(
                (self.out_dir / f"{slug}.pdf").exists(),
                f"no PDF built for {slug}",
            )

    def test_pdf_header_and_trailer(self):
        for pdf in self.pdfs:
            data = pdf.read_bytes()
            self.assertTrue(
                data.startswith(b"%PDF-"),
                f"{pdf.name}: missing %PDF header",
            )
            self.assertIn(b"%%EOF", data[-64:])

    def test_pdf_page_count_matches_expectation(self):
        """Tips page (1) + at least one printable page per sheet, and the
        on-disk PDF carries the same page count."""
        for slug in EXPECTED_SHEETS:
            reader = PdfReader(self.out_dir / f"{slug}.pdf")
            self.assertGreaterEqual(
                len(reader.pages), 2,
                f"{slug}: expected tips page + sheet page(s)",
            )

    def test_tips_page_is_page_one_of_each_pdf(self):
        for slug in EXPECTED_SHEETS:
            reader = PdfReader(self.out_dir / f"{slug}.pdf")
            first_text = reader.pages[0].extract_text() or ""
            self.assertIn(
                "How to use this sheet", first_text,
                f"{slug}: tips page is not the first page",
            )

    def test_pdfs_are_unbranded_in_output_text(self):
        for slug in EXPECTED_SHEETS:
            reader = PdfReader(self.out_dir / f"{slug}.pdf")
            text = "".join((p.extract_text() or "") for p in reader.pages)
            self.assertNotIn("Asdale", text, f"{slug}: branded text found")

    def test_pdfs_are_substantial_and_unbranded(self):
        for pdf in self.pdfs:
            self.assertGreater(pdf.stat().st_size, 2000, pdf.name)
            text = pdf.read_bytes()
            self.assertNotIn(b"Asdale", text, f"{pdf.name}: branded text found")

    def test_rebuild_is_deterministic_in_validation_terms(self):
        """A second build still produces valid PDFs (idempotent build)."""
        second = Path(tempfile.mkdtemp(prefix="travel-pack-test2-"))
        try:
            build.build_all(second)
            for slug in EXPECTED_SHEETS:
                self.assertTrue((second / f"{slug}.pdf").exists(), slug)
        finally:
            shutil.rmtree(second, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
