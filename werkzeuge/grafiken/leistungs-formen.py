#!/usr/bin/env python3
"""Leistungs-Icons aus Bauhaus-Grundformen. Seit 13.11.2026 alle in Schwarz, Weiß und Blau (Anna: „Ja, umstellen“, nur noch Akzente mit Farbe); die Spiel-Farben bleiben im Spiel.
 (Anna 12.11.2026: „die Icons müssen wir jetzt überall ersetzen“).

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
    # Markenbildung: blauer Kreis, schwarzer Balken mit Abstand (bis 18.11.2026 Webdesign; Anna: „Icon von Marke und Webdesign tauschen“)
    'brand': f'<circle cx="200" cy="180" r="100" fill="{BLAU}"/><rect x="100" y="300" width="200" height="22" fill="{SCH}"/>',
    # UI/UX: blauer Halbkreis über schwarzem Balken (mit Abstand)
    'ui-ux': f'<path d="M100 236 A100 100 0 0 1 300 236 Z" fill="{BLAU}"/><rect x="100" y="250" width="200" height="22" fill="{SCH}"/>',
    # Webdesign: blaues Quadrat, schwarzer Balken mit Abstand darunter (bis 18.11.2026 Markenbildung)
    'website': f'<rect x="110" y="90" width="180" height="180" fill="{BLAU}"/><rect x="110" y="290" width="180" height="22" fill="{SCH}"/>',
    # Marketing & Vertrieb: schwarzer Halbkreis, blauer Kreis darüber
    'marketing': f'<circle cx="200" cy="120" r="34" fill="{BLAU}"/><path d="M100 300 A100 100 0 0 1 300 300 Z" fill="{SCH}"/>',
    # KI-Beratung: blauer Stern mit vier Spitzen über schwarzem Balken (Anna, 18.11.2026: „KI ist ja immer der Stern … einen vereinfachten, Stern mit 4 Spitzen“)
    'ki': f'<path d="M200 80 L228 152 L300 180 L228 208 L200 280 L172 208 L100 180 L172 152 Z" fill="{BLAU}"/><rect x="100" y="300" width="200" height="22" fill="{SCH}"/>',
    # Retainer (neu 13.11.2026, Anna: „gefällt mir noch nicht“): blauer Kreislauf mit Pfeilspitze, schwarzer Kern mit Abstand –
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

# Tatsächlicher Rand jeder Form (x, y, Breite, Höhe), im Browser gemessen (12.11.2026): viewBox ohne Innenabstand,
# damit das Icon bündig mit dem Text steht (Anna 12.11.2026). Neue Form: hier eintragen.
RAND = {'brand': (100, 80, 200, 242), 'illustration': (81, 56, 239, 267), 'ki': (100, 80, 200, 242), 'marketing': (100, 86, 200, 214),
        'motion': (82, 82, 236, 236), 'print': (100, 110, 200, 202), 'retainer': (58, 80, 262, 240), 'ui-ux': (100, 136, 200, 136),
        'website': (110, 90, 180, 222)}

if __name__ == '__main__':
    os.makedirs(ZIEL, exist_ok=True)
    for name, inhalt in FORMEN.items():
        with open(os.path.join(ZIEL, name + '.svg'), 'w', encoding='utf-8') as f:
            x, y, w, h = RAND[name]
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMinYMin meet" aria-hidden="true">{inhalt}</svg>\n')
        print('geschrieben:', name)
