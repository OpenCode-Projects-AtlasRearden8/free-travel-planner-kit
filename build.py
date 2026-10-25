#!/usr/bin/env python3
"""Build unbranded printable PDFs from HTML/CSS sources.

Usage: python3 build.py [--out DIR]

Reads sheet HTML from src/sheets/, prepends a friendly usage-tips page from
src/tips/, and writes PDFs to printables/. Fully local: no network, no signups,
no branding. Requires WeasyPrint (pip install weasyprint).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "src" / "sheets"
TIPS_DIR = ROOT / "src" / "tips"
PRINTABLES_DIR = ROOT / "printables"
DEFAULT_OUT = PRINTABLES_DIR

try:
    from weasyprint import HTML, CSS
except ImportError:
    sys.stderr.write(
        "WeasyPrint is required: pip install weasyprint\n"
    )
    sys.exit(2)


def sheet_slugs() -> list[str]:
    return sorted(p.stem for p in SHEETS_DIR.glob("*.html"))


def compose_document(slug: str) -> str:
    """Tips page first, then the printable itself."""
    sheet = (SHEETS_DIR / f"{slug}.html").read_text(encoding="utf-8")
    tips = (TIPS_DIR / f"{slug}.html").read_text(encoding="utf-8")
    if "<body>" not in sheet:
        raise ValueError(f"{slug}: sheet HTML has no <body> tag")
    return sheet.replace("<body>", "<body>\n" + tips.strip(), 1)


def build_pdf(slug: str, out_dir: Path, css_path: Path) -> Path:
    document = compose_document(slug)
    if "<title>" not in document:
        raise ValueError(f"{slug}: sheet HTML is missing <title>")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.pdf"
    HTML(string=document, base_url=str(SHEETS_DIR)).write_pdf(
        str(out_path), stylesheets=[CSS(filename=str(css_path))]
    )
    return out_path


def build_all(out_dir: Path = DEFAULT_OUT) -> list[Path]:
    css_path = ROOT / "src" / "css" / "print.css"
    if not css_path.exists():
        sys.stderr.write(f"Missing stylesheet: {css_path}\n")
        sys.exit(2)
    slugs = sheet_slugs()
    if not slugs:
        sys.stderr.write(f"No sheets found in {SHEETS_DIR}\n")
        sys.exit(2)
    outputs = []
    for slug in slugs:
        out = build_pdf(slug, out_dir, css_path)
        try:
            display = out.relative_to(ROOT)
        except ValueError:
            display = out
        print(f"built {display}")
        outputs.append(out)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    build_all(DEFAULT_OUT)


if __name__ == "__main__":
    main()
