#!/usr/bin/env python3
"""Leistungs-Icons aus Bauhaus-Grundformen (Anna 12.11.2026: „die Icons müssen wir jetzt überall ersetzen“).

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


FORMEN = {
    # Markenbildung: rotes Quadrat, schwarzer Balken darunter
    'brand': f'<rect x="110" y="90" width="180" height="180" fill="{ROT}"/><rect x="110" y="290" width="180" height="22" fill="{SCH}"/>',
    # UI/UX: pinker Halbkreis auf schwarzem Balken
    'ui-ux': f'<path d="M100 250 A100 100 0 0 1 300 250 Z" fill="{PINK}"/><rect x="100" y="250" width="200" height="22" fill="{SCH}"/>',
    # Webdesign: blauer Kreis, schwarzer Balken mit Abstand (Blau berührt kein Schwarz)
    'website': f'<circle cx="200" cy="180" r="100" fill="{BLAU}"/><rect x="100" y="300" width="200" height="22" fill="{SCH}"/>',
    # Marketing & Vertrieb: schwarzer Halbkreis, rosa Kreis darüber
    'marketing': f'<circle cx="200" cy="120" r="34" fill="{ROSA}"/><path d="M100 300 A100 100 0 0 1 300 300 Z" fill="{SCH}"/>',
    # KI & Digitalisierung: gelbes rechtwinkliges Dreieck, schwarzer Kreis
    'ki': f'<path d="M290 90 L290 300 L80 300 Z" fill="{GELB}"/><circle cx="130" cy="140" r="30" fill="{SCH}"/>',
    # Retainer: Kreis in Klammern (rosa Kreis zwischen zwei schwarzen Sicheln) – langfristige Begleitung
    'retainer': (f'<circle cx="200" cy="200" r="70" fill="{ROSA}"/>'
                 f'<path d="M110 90 A130 130 0 0 0 110 310 A110 110 0 0 1 110 90 Z" fill="{SCH}"/>'
                 f'<path d="M290 90 A130 130 0 0 1 290 310 A110 110 0 0 0 290 90 Z" fill="{SCH}"/>'),
    # Druck: Stapel aus Balken, oben rot
    'print': f'<rect x="100" y="110" width="200" height="40" fill="{ROT}"/><rect x="100" y="170" width="200" height="40" fill="{SCH}"/><rect x="100" y="230" width="200" height="40" fill="{SCH}"/><rect x="100" y="290" width="140" height="22" fill="{SCH}"/>',
    # Illustration & Infografik: Grundform-Herz in Rosa (nie blau), schwarzer Balken
    'illustration': (f'<g transform="translate(200 175)"><rect x="-70" y="-70" width="140" height="140" transform="rotate(45)" fill="{ROSA}"/>'
                     f'<circle cx="-49.5" cy="-49.5" r="70" fill="{ROSA}"/><circle cx="49.5" cy="-49.5" r="70" fill="{ROSA}"/></g>'
                     f'<rect x="110" y="300" width="180" height="22" fill="{SCH}"/>'),
    # Animation: gelber Zackenkreis mit schwarzem Kern
    'motion': f'<g fill="{GELB}"><circle cx="200" cy="200" r="96"/>{zacken(200, 200, 100, 16, 18)}</g><circle cx="200" cy="200" r="34" fill="{SCH}"/>',
}

# Tatsächlicher Rand jeder Form (x, y, Breite, Höhe), im Browser gemessen (12.11.2026): viewBox ohne Innenabstand,
# damit das Icon bündig mit dem Text steht (Anna 12.11.2026). Neue Form: hier eintragen.
RAND = {'brand': (110, 90, 180, 222), 'illustration': (81, 56, 239, 267), 'ki': (80, 90, 210, 210), 'marketing': (100, 86, 200, 214),
        'motion': (82, 82, 236, 236), 'print': (100, 110, 200, 202), 'retainer': (49, 90, 302, 220), 'ui-ux': (100, 150, 200, 122),
        'website': (100, 80, 200, 242)}

if __name__ == '__main__':
    os.makedirs(ZIEL, exist_ok=True)
    for name, inhalt in FORMEN.items():
        with open(os.path.join(ZIEL, name + '.svg'), 'w', encoding='utf-8') as f:
            x, y, w, h = RAND[name]
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMinYMin meet" aria-hidden="true">{inhalt}</svg>\n')
        print('geschrieben:', name)
