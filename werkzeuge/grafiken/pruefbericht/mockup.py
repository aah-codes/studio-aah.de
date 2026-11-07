#!/usr/bin/env python3
"""Setzt die gerenderten Seiten des Musterberichts zu einem Papier-Mockup zusammen.

Aufruf (vom Repository-Ordner aus, nach rendern.py):
  python3 werkzeuge/grafiken/pruefbericht/rendern.py /tmp/pruefbericht
  python3 werkzeuge/grafiken/pruefbericht/mockup.py /tmp/pruefbericht

Ergebnis: website/bilder/website-check/pruefbericht-mockup.webp (transparent, 2400 px breit).
Oben das Deckblatt, dahinter Übersicht, Befunde und Rückseite; mit Rand, damit nichts angeschnitten ist.
"""
import pathlib
import sys

from PIL import Image, ImageFilter

QUELLE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/pruefbericht")
REPO = pathlib.Path(__file__).resolve().parents[3]
ZIEL = REPO / "website/bilder/website-check/pruefbericht-mockup.webp"
B, H = 3200, 1800


def blatt(nr, hoehe, winkel):
    s = Image.open(QUELLE / f"seite-{nr}.png").convert("RGBA")
    s = s.resize((round(s.width * hoehe / s.height), hoehe), Image.LANCZOS)
    return s.rotate(winkel, resample=Image.BICUBIC, expand=True)


def legen(leinwand, bild, mitte_x, mitte_y):
    x, y = round(mitte_x - bild.width / 2), round(mitte_y - bild.height / 2)
    maske = bild.split()[3]
    for versatz, radius, deckung in ((26, 38, .20), (6, 6, .16)):
        schatten = Image.new("RGBA", leinwand.size, (0, 0, 0, 0))
        schwarz = Image.new("RGBA", bild.size, (14, 16, 17, round(255 * deckung)))
        schatten.paste(schwarz, (x, y + versatz), maske)
        leinwand.alpha_composite(schatten.filter(ImageFilter.GaussianBlur(radius)))
    leinwand.alpha_composite(bild, (x, y))


leinwand = Image.new("RGBA", (B, H), (0, 0, 0, 0))
legen(leinwand, blatt(3, 1240, -3), 1900, 840)   # Befunde
legen(leinwand, blatt(6, 1240, -7), 2380, 900)   # Rückseite
legen(leinwand, blatt(2, 1300, 2), 1500, 820)    # Übersicht
legen(leinwand, blatt(1, 1400, 4), 860, 830)     # Deckblatt oben drauf
leinwand = leinwand.crop(leinwand.getbbox())
if leinwand.width > 2400:
    leinwand = leinwand.resize((2400, round(leinwand.height * 2400 / leinwand.width)), Image.LANCZOS)
ZIEL.parent.mkdir(parents=True, exist_ok=True)
leinwand.save(ZIEL, "WEBP", quality=84, method=6)
print(ZIEL, leinwand.size, ZIEL.stat().st_size // 1024, "KB")
klein = ZIEL.with_name(ZIEL.stem + "-1200.webp")
leinwand.resize((1200, round(leinwand.height * 1200 / leinwand.width)), Image.LANCZOS).save(klein, "WEBP", quality=84, method=6)
print(klein, klein.stat().st_size // 1024, "KB")
