# Free Travel Planner Pack

A free, unbranded pack of printable pages for calmer trips. Everything is built
locally from simple HTML/CSS sources — no signups, no accounts, nothing online,
no data collected. Print the PDFs at home or anywhere you like.

Part of a family of beginner-friendly tools published by
**Asdale Dynamics, LLC**.

## What's inside (`printables/`)

| PDF | What it does |
| --- | --- |
| `packing-list-builder.pdf` | Fill-in packing list organized by use, with a trip-details strip (type, climate, duration) to build a list from |
| `travel-documents-checklist.pdf` | Everything to grab before you leave — passports, cards, confirmations — with a done checkbox |
| `medications-contacts-card.pdf` | A card listing personal medications, doses, allergies and who to call — carry it, leave a copy at home |
| `day-itinerary-one-pager.pdf` | One page per day: plan a day's timing, places and notes on trip overview |
| `trip-budget-tracker.pdf` | Log what you actually spend on the road, as well as estimating overall before you go |
| `at-home-while-away-checklist.pdf` | Pre-departure and return checklist for the home side of travel: pets, mail, security, plants |
| `kids-travel-busy-pages.pdf` | Multi-page pack of travel games for kids — scavenger hunt, I-spy, word puzzles, tally sheets |

Every PDF begins with a friendly "How to use this sheet" page.

## Running it

Requirements: Python 3.10+ and [WeasyPrint](https://weasyprint.org/)
(`pip install weasyprint`). No network access is needed at build time.

```
python3 build.py        # builds every sheet into printables/*.pdf
python3 -m unittest discover tests -v   # builds + validates every PDF
```

The build script reads HTML + CSS from `src/sheets/` and `src/css/print.css`,
prepends a tips page from `src/tips/`, and writes unbranded PDFs to
`printables/`.

## Customizing

Edit any HTML file in `src/sheets/` — it's plain, readable HTML. Save the file,
run `python3 build.py`, and the matching PDF updates. Add your own rows, cities,
or categories; the layout takes care of the rest.

## Privacy

This project is fully local. It reads your HTML, writes your PDFs, and contacts
nothing. No signups, no telemetry, no API keys.

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Asdale Dynamics, LLC
