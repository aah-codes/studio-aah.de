#!/usr/bin/env python3
"""Porträts wie im Fotostudio – Entwurf 13.10.2026.

Anna (13.10.2026, Vorbild: Stockfotos vor farbiger Studiowand): Die Wand ist in Markenblau gestrichen,
nicht einfarbig flach, sondern wie im Fotostudio ausgeleuchtet: in der Mitte heller, außen dunkler.
Das Licht auf der Wand passt zum Licht im Gesicht (Bild 1 von links, Bild 2 von vorn), dazu ein weicher
Schatten der Person auf der Wand. Die Kleidung bekommt einen anderen Blauton als die Wand (Website: nur Blau).
Die Person bleibt sonst Schwarz-Weiß, weil es die Fotos nur in Schwarz-Weiß gibt.

Grundlage: die freigestellten Fotos aus freistellen.py (bilder-blau/*-frei-sw.webp).
Die Grenze Kleidung/Haar/Haut ist von Hand als Linie festgelegt (KLEIDUNG_GRENZE, Pixel im Originalbild).
Benötigt: numpy, Pillow. Aufruf vom Repository-Ordner aus: python3 werkzeuge/grafiken/fotostudio.py
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ORDNER = Path("werkzeuge/grafiken/bilder-blau")  # nicht veröffentlicht
WAND = np.array([0x2f, 0x6b, 0xff], dtype=np.float32) / 255  # Markenblau

# Kleidung: Farbverlauf von Schatten über Mitte zu Licht (dunkel → hell)
MARINE = [(0.0, (10, 22, 66)), (0.45, (28, 58, 150)), (1.0, (214, 226, 255))]
EISBLAU = [(0.0, (16, 34, 92)), (0.55, (98, 134, 222)), (1.0, (232, 239, 255))]

BILDER = [
    {
        "quelle": "anna-haertelt-portraet-frei-sw.webp",
        "ziel": "anna-haertelt-portraet-studio-blau",
        "licht": (0.30, 0.38),  # Lichtmitte auf der Wand (Anteil von Breite, Höhe): Licht von links
        "schatten": (58, 18, 0.5),  # Versatz x, y in px, Deckkraft
        "kleidung": MARINE,
        "grenze": [(0, 790), (60, 776), (110, 764), (160, 756), (192, 736), (205, 722), (240, 742), (290, 772), (330, 792),
                   (400, 802), (470, 796), (485, 790), (520, 804), (600, 810), (700, 830), (794, 850)],
        "aussparen": [],
    },
    {
        "quelle": "studio-aah-gruenderin-anna-haertelt-frei-sw.webp",
        "ziel": "studio-aah-gruenderin-anna-haertelt-studio-blau",
        "licht": (0.50, 0.40),  # Licht von vorn
        "schatten": (0, 22, 0.36),
        "kleidung": EISBLAU,
        "grenze": [(0, 690), (100, 652), (200, 606), (232, 626), (262, 640), (272, 586), (330, 600), (380, 640),
                   (420, 660), (450, 640), (468, 600), (500, 630), (560, 650), (600, 626), (680, 690), (768, 720)],
        "aussparen": [(318, 664, 356, 698)],  # Herz-Aufdruck am Kragen: kein blaues Herz
    },
]


def verlauf(grau, stufen):
    """Grauwerte 0..1 auf einen Farbverlauf abbilden."""
    pos = np.array([s[0] for s in stufen])
    farben = np.array([s[1] for s in stufen], dtype=np.float32) / 255
    return np.stack([np.interp(grau, pos, farben[:, k]) for k in range(3)], axis=-1)


def weich(maske, radius):
    return np.asarray(Image.fromarray((maske * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius)),
                      dtype=np.float32) / 255


def wand(b, h, licht):
    yy, xx = np.mgrid[0:h, 0:b].astype(np.float32)
    lx, ly = licht[0] * b, licht[1] * h
    d = np.sqrt(((xx - lx) / b) ** 2 + ((yy - ly) / h) ** 2 * 0.8)
    hell = 1.3 - 1.15 * d ** 1.4  # Mitte hell, außen dunkler
    hell = np.clip(hell, 0.42, 1.3)
    gestrichen = WAND * 0.9 + WAND.mean() * 0.1  # Wandfarbe wirkt im Licht etwas weniger grell als am Bildschirm
    farbe = gestrichen[None, None, :] * np.minimum(hell, 1)[..., None]
    spitze = np.clip(hell - 1, 0, None)[..., None] * 0.8  # Lichtfleck: heller und weniger gesättigt
    return farbe + (1 - farbe) * spitze


def bauen(eintrag):
    rgba = np.asarray(Image.open(ORDNER / eintrag["quelle"]).convert("RGBA"), dtype=np.float32) / 255
    h, b = rgba.shape[:2]
    grau, alpha = rgba[..., 0], rgba[..., 3]

    # Kleidung: unter der Grenzlinie, weich auslaufend, Aussparungen (z. B. Herz) bleiben grau
    m = Image.new("L", (b, h), 0)
    ImageDraw.Draw(m).polygon(eintrag["grenze"] + [(b, h), (0, h)], fill=255)
    for kasten in eintrag["aussparen"]:
        ImageDraw.Draw(m).ellipse(kasten, fill=0)
    kleidung = weich(np.asarray(m, dtype=np.float32) / 255, 3) * alpha

    person = np.repeat(grau[..., None], 3, axis=-1)
    person = person * (1 - kleidung[..., None]) + verlauf(grau, eintrag["kleidung"]) * kleidung[..., None]

    # Rückstrahlung der blauen Wand an den Rändern (Haare, Schultern), sehr leicht
    rand = np.clip(alpha - weich(alpha, 6) * 0 - weich((alpha > 0.98).astype(np.float32), 8), 0, 1)
    person = person * (1 - 0.22 * rand[..., None]) + WAND * 0.22 * rand[..., None]

    hinten = wand(b, h, eintrag["licht"])
    dx, dy, deck = eintrag["schatten"]
    schatten = np.roll(np.roll(alpha, dy, axis=0), dx, axis=1)
    schatten = weich(schatten, 34) * deck
    hinten = hinten * (1 - schatten[..., None])

    bild = hinten * (1 - alpha[..., None]) + person * alpha[..., None]
    rng = np.random.default_rng(13)
    bild = bild + rng.normal(0, 0.012, bild.shape).astype(np.float32)  # Korn wie bei einem Foto
    bild = Image.fromarray((np.clip(bild, 0, 1) * 255 + 0.5).astype(np.uint8))
    for endung, optionen in [("jpg", {"quality": 92}), ("webp", {"quality": 84, "method": 6})]:
        ziel = ORDNER / f"{eintrag['ziel']}.{endung}"
        bild.save(ziel, **optionen)
        print(ziel, ziel.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    for e in BILDER:
        bauen(e)
