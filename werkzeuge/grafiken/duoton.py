#!/usr/bin/env python3
"""Färbt Fotos einfarbig in Blau ein (Duoton, duotone) – Entwurf 13.10.2026.

Vorbild laut Anna: Fotos im ganzen Bild, einfarbig eingefärbt, „in Blau, leicht bewegt“.
Zwei Fassungen je Bild:
  -duoton  Schwarz -> Blau            (dunkler, ruhiger)
  -triton  Schwarz -> Blau -> Weiß    (Gesichter bleiben hell)
Aufruf vom Repository-Ordner aus: python3 werkzeuge/grafiken/duoton.py
"""
from pathlib import Path
from PIL import Image, ImageOps

QUELLE = Path("website/bilder")
ZIEL = Path("website/bilder/blau")
BILDER = [  # (Datei, größte Breite in px, Fassungen)
    ("studio-anna-haertelt.jpg", 1600, ["triton"]),
    ("studio-aah-gruenderin-anna-haertelt.webp", 768, ["duoton", "triton"]),
    ("anna-haertelt-portraet.jpg", 794, ["duoton", "triton"]),
]
FARBVERLAEUFE = {
    "duoton": [(0.0, "#0e1011"), (1.0, "#2f6bff")],
    "triton": [(0.0, "#0e1011"), (0.52, "#2f6bff"), (1.0, "#ffffff")],
}


def rgb(hexwert):
    return tuple(int(hexwert[i:i + 2], 16) for i in (1, 3, 5))


def tabelle(stopps):
    """Farbverlauf (gradient map) als Nachschlagetabelle für 256 Grauwerte."""
    werte = []
    for g in range(256):
        t = g / 255
        for (t0, f0), (t1, f1) in zip(stopps, stopps[1:]):
            if t0 <= t <= t1:
                a, b = rgb(f0), rgb(f1)
                k = (t - t0) / (t1 - t0) if t1 > t0 else 0
                werte.append(tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3)))
                break
    return werte


def einfaerben(grau, stopps):
    lut = tabelle(stopps)
    kanaele = [grau.point([lut[g][i] for g in range(256)]) for i in range(3)]
    return Image.merge("RGB", kanaele)


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    for datei, breite, fassungen in BILDER:
        bild = Image.open(QUELLE / datei)
        bild = ImageOps.exif_transpose(bild).convert("L")
        if bild.width > breite:
            bild = bild.resize((breite, round(bild.height * breite / bild.width)), Image.LANCZOS)
        bild = ImageOps.autocontrast(bild, cutoff=1)
        stamm = Path(datei).stem
        for name in fassungen:
            stopps = FARBVERLAEUFE[name]
            ziel = ZIEL / f"{stamm}-{name}.webp"
            einfaerben(bild, stopps).save(ziel, "WEBP", quality=80, method=6)
            print(ziel, ziel.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
