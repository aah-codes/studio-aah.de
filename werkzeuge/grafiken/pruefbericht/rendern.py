#!/usr/bin/env python3
"""Rendert den Musterbericht (musterbericht.html) als PDF und als Einzelseiten-PNG.

Aufruf (vom Repository-Ordner aus):
  python3 werkzeuge/grafiken/pruefbericht/rendern.py [ZIELORDNER]

Ergebnis: ZIELORDNER/musterbericht.pdf und ZIELORDNER/seite-1.png … seite-6.png
(Standard: /tmp/pruefbericht). PDFs gehören nicht ins Repository.
Braucht Playwright mit Chrome (macOS: Google Chrome, Linux: /usr/bin/google-chrome).
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

HIER = pathlib.Path(__file__).resolve().parent
ZIEL = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/pruefbericht")
ZIEL.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    seite = browser.new_page(viewport={"width": 900, "height": 1200}, device_scale_factor=3)
    seite.goto((HIER / "musterbericht.html").as_uri())
    seite.evaluate("document.fonts.ready")
    seite.wait_for_timeout(400)
    for n in range(1, 7):
        seite.locator(f"#s{n}").screenshot(path=str(ZIEL / f"seite-{n}.png"))
    seite.pdf(path=str(ZIEL / "musterbericht.pdf"), format="A4", print_background=True,
              prefer_css_page_size=True)
    browser.close()
print("fertig:", ZIEL)
