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

    # Seite KI-Arbeits-Setup (Anna 12.11.2026: Clay-Icons durch die kleinen Illustrationen ersetzen)
    # Arbeitsordner: schwarzer Reiter, roter Ordner
    'ki-ordner': f'<rect x="90" y="100" width="100" height="40" fill="{SCH}"/><rect x="90" y="140" width="220" height="170" fill="{ROT}"/>',
    # Arbeitsanleitung: rosa Heft mit schwarzem Rücken und Lesebändchen
    'ki-anleitung': f'<rect x="100" y="80" width="34" height="240" fill="{SCH}"/><rect x="134" y="80" width="170" height="240" fill="{ROSA}"/><path d="M250 80 L280 80 L280 150 L265 135 L250 150 Z" fill="{SCH}"/>',
    # Skills: schwarzer Zauberstab mit gelbem Zackenkreis
    'ki-skills': f'<rect x="80" y="288" width="210" height="24" transform="rotate(-45 80 300)" fill="{SCH}"/><g fill="{GELB}"><circle cx="270" cy="130" r="56"/>{zacken(270, 130, 58, 16, 11)}</g>',
    # Projekt-Cockpit: drei Balken wie ein Diagramm auf schwarzer Grundlinie
    'ki-cockpit': f'<rect x="100" y="200" width="50" height="90" fill="{ROSA}"/><rect x="175" y="150" width="50" height="140" fill="{GELB}"/><rect x="250" y="100" width="50" height="190" fill="{ROT}"/><rect x="90" y="290" width="220" height="22" fill="{SCH}"/>',
    # Kalender, Mail, Projekttool: drei Grundformen an einer schwarzen Linie
    'ki-verbinden': f'<rect x="70" y="190" width="260" height="20" fill="{SCH}"/><rect x="70" y="150" width="80" height="80" fill="{ROT}"/><circle cx="200" cy="200" r="44" fill="{GELB}"/><path d="M290 150 L330 230 L250 230 Z" fill="{ROSA}"/>',
    # Rundgang: blauer Kreis mit weißer Kompassnadel, schwarzer Balken mit Abstand
    'ki-rundgang': f'<circle cx="200" cy="180" r="100" fill="{BLAU}"/><path d="M200 100 L228 180 L200 260 L172 180 Z" fill="#ffffff"/><rect x="100" y="300" width="200" height="22" fill="{SCH}"/>',
    # Wir richten es gemeinsam ein: Bildschirm wie auf der Branchenseite Software & IT (schwarze Seitenleiste, farbige Kacheln, Mauszeiger)
    'ki-bildschirm': (f'<rect x="40" y="70" width="320" height="210" rx="12" fill="#ffffff" stroke="{SCH}" stroke-width="6"/>'
                      f'<path d="M52 73 H112 V277 H52 A9 9 0 0 1 43 268 V82 A9 9 0 0 1 52 73 Z" fill="{SCH}"/>'
                      f'<rect x="60" y="100" width="34" height="9" rx="4.5" fill="#9a9d9e"/><rect x="60" y="126" width="34" height="9" rx="4.5" fill="#9a9d9e"/><rect x="60" y="152" width="34" height="9" rx="4.5" fill="#9a9d9e"/>'
                      f'<rect x="130" y="92" width="210" height="22" rx="6" fill="#d6d8d9"/>'
                      f'<rect x="130" y="128" width="62" height="62" rx="8" fill="{GELB}"/><rect x="204" y="128" width="62" height="62" rx="8" fill="{BLAU}"/><rect x="278" y="128" width="62" height="62" rx="8" fill="{PINK}"/>'
                      f'<rect x="130" y="204" width="210" height="58" rx="8" fill="{ROSA}"/>'
                      f'<path d="M248 168 L248 206 L257 198 L264 214 L271 211 L264 195 L276 195 Z" fill="{SCH}" stroke="#ffffff" stroke-width="3"/>'
                      f'<rect x="178" y="280" width="44" height="34" fill="{SCH}"/><rect x="140" y="314" width="120" height="16" rx="8" fill="{SCH}"/>'),
    # Erst fragen: rosa Umschlag mit schwarzer Klappe
    'ki-mail': f'<rect x="80" y="120" width="240" height="170" fill="{ROSA}"/><path d="M80 120 L320 120 L200 220 Z" fill="{SCH}"/>',
    # Passender Tarif: gelbes Dreieck mit schwarzem Ausrufezeichen
    'ki-tarif': f'<path d="M200 70 L330 320 L70 320 Z" fill="{GELB}"/><rect x="188" y="160" width="24" height="90" fill="{SCH}"/><circle cx="200" cy="282" r="14" fill="{SCH}"/>',
}

if __name__ == '__main__':
    os.makedirs(ZIEL, exist_ok=True)
    for name, inhalt in FORMEN.items():
        with open(os.path.join(ZIEL, name + '.svg'), 'w', encoding='utf-8') as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400" aria-hidden="true">{inhalt}</svg>\n')
        print('geschrieben:', name)
