#!/usr/bin/env python3
"""Leistungs-Icons aus Bauhaus-Grundformen, alle in Schwarz, Weiß und Blau; die Spiel-Farben bleiben im Spiel.
.

Jede Leistung hat ihre Form und Farbe wie im Hero-Spiel (Markenbildung rotes Quadrat, UI/UX pinker Halbkreis,
Webdesign blauer Kreis, Marketing & Vertrieb schwarzer Halbkreis, KI & Digitalisierung gelbes Dreieck), dazu für
die übrigen Leistungen die erweiterten Formen. Jedes Icon hat ein schwarzes Element; Blau berührt nie Schwarz.
Ausgabe: website/bilder/formen/<id>.svg (ids wie in werkzeuge/leistungen-inhalte.json).
Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/leistungs-formen.py
"""
import os

ZIEL = os.path.join(os.path.dirname(__file__), '..', '..', 'website', 'bilder', 'formen')
SCH, ROT, PINK, ROSA, GELB, BLAU = '#0e1011', '#ff3b2f', '#ff4fa3', '#ff8fc8', '#ffe600', '#2a5fe6'


def zacken(cx, cy, r, n=16, rk=None):
    rk = rk or r * .2
    import math
    kreise = ''.join(f'<circle cx="{cx + r * math.cos(2 * math.pi * i / n):.1f}" cy="{cy + r * math.sin(2 * math.pi * i / n):.1f}" r="{rk:.1f}"/>' for i in range(n))
    return kreise


def stern(cx, cy, R, farbe):
    """Stern mit vier Spitzen (Innenradius wie beim KI-Stern: 0,396 × Spitzenradius)."""
    import math
    ri = R * .396
    pkt = []
    for i in range(8):
        w = math.radians(-90 + 45 * i)
        rr = R if i % 2 == 0 else ri
        pkt.append(f'{cx + rr * math.cos(w):.1f} {cy + rr * math.sin(w):.1f}')
    return f'<path d="M{" L".join(pkt)} Z" fill="{farbe}"/>'


FORMEN = {
    # Markenbildung: blauer Kreis, schwarzer Balken mit Abstand
    # wie eine Zielscheibe: weißer Ring trennt Blau und Schwarz
    'brand': f'<circle cx="200" cy="200" r="110" fill="{BLAU}"/><circle cx="200" cy="200" r="46" fill="#ffffff"/><circle cx="200" cy="200" r="30" fill="{SCH}"/>',
    # UI/UX: blauer Halbkreis über schwarzem Balken (mit Abstand)
    'ui-ux': f'<path d="M100 236 A100 100 0 0 1 300 236 Z" fill="{BLAU}"/><rect x="100" y="250" width="200" height="22" fill="{SCH}"/>',
    # Webdesign: blaues Quadrat, schwarzer Balken mit Abstand darunter
    # Abstand zwischen Blau und Schwarz
    'website': f'<rect x="110" y="90" width="180" height="34" fill="{SCH}"/><rect x="110" y="138" width="180" height="124" fill="{BLAU}"/><rect x="110" y="276" width="180" height="34" fill="{SCH}"/>',
    # Marketing & Vertrieb: schwarzer Halbkreis, blauer Kreis darüber
    'marketing': f'<circle cx="200" cy="120" r="34" fill="{BLAU}"/><path d="M100 300 A100 100 0 0 1 300 300 Z" fill="{SCH}"/>',
    # KI-Beratung: blauer Stern mit vier Spitzen über schwarzem Balken
    # Großer blauer Stern, kleiner schwarzer Stern oben rechts, ohne Berührung
    'ki': stern(185, 215, 105, BLAU) + stern(300, 105, 40, SCH),
    # Retainer: blauer Kreislauf mit Pfeilspitze, schwarzer Kern mit Abstand –
    # die Betreuung läuft nach dem Launch weiter
    'retainer': (f'<path d="M200 80 A120 120 0 1 1 80 200 L124 200 A76 76 0 1 0 200 124 Z" fill="{BLAU}"/>'
                 f'<path d="M58 206 L146 206 L102 140 Z" fill="{BLAU}"/><circle cx="200" cy="200" r="30" fill="{SCH}"/>'),
    # Druck: Stapel aus Balken, oben blau
    'print': f'<rect x="100" y="110" width="200" height="40" fill="{BLAU}"/><rect x="100" y="170" width="200" height="40" fill="{SCH}"/><rect x="100" y="230" width="200" height="40" fill="{SCH}"/><rect x="100" y="290" width="140" height="22" fill="{SCH}"/>',
    # Illustration & Infografik: schwarzes Grundform-Herz (Herzen nie blau), blauer Balken mit Abstand
    'illustration': (f'<g transform="translate(200 175)"><rect x="-70" y="-70" width="140" height="140" transform="rotate(45)" fill="{SCH}"/>'
                     f'<circle cx="-49.5" cy="-49.5" r="70" fill="{SCH}"/><circle cx="49.5" cy="-49.5" r="70" fill="{SCH}"/></g>'
                     f'<rect x="110" y="300" width="180" height="22" fill="{BLAU}"/>'),
    # Animation: blauer Zackenkreis, weißer Ring, schwarzer Kern
    'motion': f'<g fill="{BLAU}"><circle cx="200" cy="200" r="96"/>{zacken(200, 200, 100, 16, 18)}</g><circle cx="200" cy="200" r="50" fill="#ffffff"/><circle cx="200" cy="200" r="34" fill="{SCH}"/>',
}

# Tatsächlicher Rand jeder Form (x, y, Breite, Höhe), im Browser gemessen: viewBox ohne Innenabstand,
# damit das Icon bündig mit dem Text steht. Neue Form: hier eintragen.
RAND = {'brand': (90, 90, 220, 220), 'illustration': (81, 56, 239, 267), 'ki': (80, 65, 260, 255), 'marketing': (100, 86, 200, 214),
        'motion': (82, 82, 236, 236), 'print': (100, 110, 200, 202), 'retainer': (58, 80, 262, 240), 'ui-ux': (100, 136, 200, 136),
        'website': (110, 90, 180, 220)}

if __name__ == '__main__':
    os.makedirs(ZIEL, exist_ok=True)
    for name, inhalt in FORMEN.items():
        with open(os.path.join(ZIEL, name + '.svg'), 'w', encoding='utf-8') as f:
            x, y, w, h = RAND[name]
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMinYMin meet" aria-hidden="true">{inhalt}</svg>\n')
        print('geschrieben:', name)
