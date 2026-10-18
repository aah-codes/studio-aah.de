#!/usr/bin/env python3
"""Druck-Mockup für die Startseite (Anna 13.10.2026): Visitenkarten von Dr. Simone Goldhammer auf einem Schreibtisch.

Zwei Karten, leicht gedreht und gestapelt, mit weichem Schatten, Kontaktschatten, Papierkante und dem Korn des Fotos.
Die Karte wird nur verkleinert, nie vergrößert, damit sie scharf bleibt.
Schreibtisch-Foto (lizenzfrei, von Anna, 2000 × 1333 px) liegt nicht im Repository; Pfad als Argument.
Aufruf vom Repository-Ordner aus: python3 werkzeuge/grafiken/druck-mockup.py PFAD/schreibtisch.jpg
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

KARTE = 'website/bilder/hero/goldhammer-visitenkarte.webp'
ZIEL = 'website/bilder/mockups/druck-schreibtisch.webp'
K = 2  # Überabtastung für saubere Kanten
BREITE = 440  # Kartenbreite im Foto (Tasse ≈ 9 cm ≈ 470 px → 85 mm ≈ 440 px)
LAGEN = [(-9, (1180, 560), -0.02), (7, (1300, 640), 0.0)]  # Drehung, Mitte im Foto, Helligkeit
AUSSCHNITT = (640, 150, 1840, 1050)  # 4:3 wie die Karten der Leiste


def kartenbild(karte, hell):
    b = BREITE * K
    h = round(b * 55 / 85)
    a = np.asarray(karte.resize((b, h), Image.LANCZOS).convert('RGBA')).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:b]
    licht = 1 + 0.035 * (1 - (xx / b + yy / h) / 2) - 0.02 + hell  # oben links etwas heller
    a[..., :3] = np.clip(a[..., :3] * licht[..., None], 0, 255)
    k = Image.fromarray(a.astype(np.uint8))
    d = ImageDraw.Draw(k)  # Papierkante unten und rechts
    d.line([(0, h - 1), (b - 1, h - 1)], fill=(205, 205, 200, 255), width=2 * K)
    d.line([(b - 1, 0), (b - 1, h - 1)], fill=(215, 215, 210, 255), width=2 * K)
    return k


def main():
    tisch = Image.open(sys.argv[1]).convert('RGB')
    karte = Image.open(KARTE).convert('RGB')
    w, h = tisch.size
    gross = tisch.convert('RGBA').resize((w * K, h * K), Image.LANCZOS)
    schatten = np.zeros((h * K, w * K), np.float32)
    karten = []
    for winkel, (cx, cy), hell in LAGEN:
        k = kartenbild(karte, hell).rotate(winkel, resample=Image.BICUBIC, expand=True)
        karten.append((k, int(cx * K - k.width / 2), int(cy * K - k.height / 2)))
    for k, x, y in karten:
        for dx, dy, weich, staerke in [(6, 10, 14, 1.0), (1, 2, 2, 0.8)]:  # weicher Schatten, Kontaktschatten
            m = Image.new('L', gross.size, 0)
            m.paste(k.split()[3], (x + dx * K, y + dy * K))
            schatten = np.maximum(schatten, np.asarray(m.filter(ImageFilter.GaussianBlur(weich * K)), np.float32) / 255 * staerke)
    g = np.asarray(gross).astype(np.float32)
    g[..., :3] *= 1 - schatten[..., None] * 0.28
    gross = Image.fromarray(g.astype(np.uint8))
    for k, x, y in karten:
        gross.alpha_composite(k, (x, y))
    bild = np.asarray(gross.resize((w, h), Image.LANCZOS).convert('RGB')).astype(np.float32)
    bild += np.random.default_rng(3).normal(0, 1.6, (h, w, 1))  # Korn wie im Foto
    aus = Image.fromarray(np.clip(bild, 0, 255).astype(np.uint8)).crop(AUSSCHNITT)
    aus.save(ZIEL, quality=86, method=6)
    print(ZIEL, aus.size)


if __name__ == '__main__':
    main()
