# STATUS.md

Last updated: 2026-10-25

## What was built

A free, unbranded printable pack for calmer trips, published and maintained by
Asdale Dynamics, LLC. HTML/CSS sources print to PDF through one local build
script; every PDF starts with a friendly "How to use this sheet" page.

### Sheets (each HTML in `src/sheets/`, tips in `src/tips/`)

1. `packing-list-builder` — trip-details strip, category tables, trip-type quick lists
2. `travel-documents-checklist` — documents, bookings/confirmation numbers, money & access rules
3. `medications-contacts-card` — medications, allergies, who-to-call panel, fold-and-shred guidance (no medical advice)
4. `day-itinerary-one-pager` — time blocks, transport legs, food plan, "if things go sideways" backups
5. `trip-budget-tracker` — Plan A estimator with overshoot bumps, 12-day spend logger, come-home reconciliation table
6. `at-home-while-away-checklist` — before-leaving, helper's visits, and re-entry phases
7. `kids-travel-busy-pages` — 3-page pack: road-trip scavenger hunt, license-plate tally, word play, doodle/rate pages

## How to run

```
python3 build.py                          # build printables/*.pdf from src/
python3 -m unittest discover tests -v     # build + validate every PDF
```

Requires Python 3.10+, WeasyPrint (`pip install weasyprint`) and pypdf (tests
only). Build is fully local: no network calls, no signups, no fonts fetched.

## Verification results

- `python3 build.py` — all 7 PDFs built with exit code 0, no WeasyPrint warnings
- `python3 -m unittest discover tests` — 11/11 tests pass:
  - sheet/tips source consistency checks (titles, stylesheet, no network CSS)
  - every sheet produces a PDF with valid header/trailer
  - tips page verified as page 1 of each PDF via pypdf
  - page counts ≥ 2 (tips + content); kids pack renders 5 pages total
  - PDFs checked unbranded ("Asdale" never appears in built PDFs)
  - idempotent second build into a temp dir also valid
- Page counts: 7 sheets → 2–5 pages each (tips + 1–3 content pages); the
  one-page sheets (documents, itinerary, medications) fit on a single content
  page after spacing tuning

## Design notes

- Unbranded PDFs: no logos, no LLC name inside the printables; branding lives
  in README/LICENSE only (MIT, Copyright (c) 2026 Asdale Dynamics, LLC)
- `keep-together` hooks prevent awkward final-page orphans where it mattered
- DejaVu/system font stack so builds never fetch fonts
- PDF metadata title comes from each HTML `<title>`; build fails if a sheet
  is missing `<title>` or `<body>`, or has no matching tips page

## Known gaps

- Build assumes WeasyPrint's default letter paper; A4 would need an
  `@page` size variant (a one-line CSS change, not yet exposed as an option)
- Budget tracker log table caps at 12 rows per page; longer trips reuse pages
- Tips are English-only; no localization yet
- No page-count assertion per individual sheet beyond "≥ tips + 1 page"; if
  future edits push a sheet to an ugly extra orphan page, tests won't catch it
- Kids doodle box is an empty bordered cell rather than a true drawing canvas
