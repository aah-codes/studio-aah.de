#!/usr/bin/env python3
"""Icon-Set für die ganze Website (Anna 12.11.2026: „ein Icon-Set zur kompletten Website … vereinheitlichen, nicht jedes
Mal was Neues erfinden … maximal 50 Icons … maximal 3 Farben: Schwarz, Weiß und eine Farbe … 60 % aller Icons blau,
vor allem die, die Seriosität und Vertrauen ausstrahlen sollen; die anderen dürfen farbiger sein als Eyecatcher“).

Regeln für jedes Icon:
- Fläche 320 × 320, die Form reicht bis an den Rand (kein Innenabstand) → steht in Karten genau linksbündig.
- Gefüllte Bauhaus-Grundformen (Kreis, Halbkreis, Quadrat, Dreieck, Balken), keine Linienzeichnung.
- Höchstens drei Farben: Schwarz, Weiß und eine Akzentfarbe. Blau berührt nie Schwarz (Abstand statt Fuge).
- Herzen nur als Grundform-Herz und nie blau.
- Neues Icon nur, wenn keins im Set passt; dann hier eintragen und `ZWECK` ergänzen.
Die Leistungs-Icons (`leistungs-formen.py`, Spiel-Farben) gehören zum Set, bleiben aber dort.

Ausgabe: website/bilder/symbole/<name>.svg und die Übersicht website/entwurf-icons/index.html (nur lokal).
Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/symbole.py
"""
import math
import pathlib

SCH, WS, BLAU = '#0e1011', '#ffffff', '#2a5fe6'
ROT, PINK, ROSA, GELB = '#ff3b2f', '#ff4fa3', '#ff8fc8', '#ffe600'
WURZEL = pathlib.Path(__file__).resolve().parent.parent.parent
ZIEL = WURZEL / 'website' / 'bilder' / 'symbole'
UEBERSICHT = WURZEL / 'website' / 'entwurf-icons' / 'index.html'


def stern(cx, cy, r_aussen, r_innen, zacken=8, drehung=-90):
    """Funkelnder Stern mit tiefen Kerben (nicht als Blume aus Kreisen)."""
    punkte = []
    for i in range(zacken * 2):
        r = r_aussen if i % 2 == 0 else r_innen
        w = math.radians(drehung + i * 180 / zacken)
        punkte.append(f'{cx + r * math.cos(w):.1f} {cy + r * math.sin(w):.1f}')
    return 'M' + ' L'.join(punkte) + ' Z'


def herz(cx, cy, a, farbe):
    """Grundform-Herz: gedrehtes Quadrat mit Kantenlänge a und zwei Halbkreisen."""
    d = a / math.sqrt(2)
    return (f'<g transform="translate({cx} {cy})"><rect x="{-a/2}" y="{-a/2}" width="{a}" height="{a}" transform="rotate(45)" fill="{farbe}"/>'
            f'<circle cx="{-d/2:.1f}" cy="{-d/2:.1f}" r="{a/2}" fill="{farbe}"/><circle cx="{d/2:.1f}" cy="{-d/2:.1f}" r="{a/2}" fill="{farbe}"/></g>')


# name: (Farbe, Zweck, SVG-Inhalt)
SET = {
    # ---------- Blau: Vertrauen, Ordnung, Arbeit ----------
    'ordner': (BLAU, 'Arbeitsordner, Ablage, Projekte', f'<rect x="0" y="24" width="128" height="40" fill="{SCH}"/><rect x="0" y="80" width="320" height="216" fill="{BLAU}"/>'),
    'anleitung': (BLAU, 'Arbeitsanleitung, Handbuch, Regeln', f'<rect x="20" y="0" width="40" height="320" fill="{SCH}"/><rect x="76" y="0" width="224" height="320" fill="{BLAU}"/><path d="M220 0 H260 V96 L240 76 L220 96 Z" fill="{WS}"/>'),
    'cockpit': (BLAU, 'Projekt-Cockpit, Übersicht, Kennzahlen', f'<rect x="0" y="152" width="80" height="128" fill="{BLAU}"/><rect x="120" y="88" width="80" height="192" fill="{BLAU}"/><rect x="240" y="0" width="80" height="280" fill="{BLAU}"/><rect x="0" y="296" width="320" height="24" fill="{SCH}"/>'),
    'projekte': (BLAU, 'Projektmanagement, Projekttool, Tickets', ''.join(f'<rect x="{x}" y="{y}" width="96" height="88" rx="10" fill="{f}"/>' for x, y, f in [(0, 0, BLAU), (0, 116, BLAU), (0, 232, BLAU), (112, 0, BLAU), (112, 116, BLAU), (224, 0, SCH)])),
    'kalender': (BLAU, 'Termine, Kalender, Ablauf', f'<rect x="0" y="0" width="320" height="56" fill="{SCH}"/><rect x="0" y="72" width="320" height="248" fill="{BLAU}"/>' + ''.join(f'<rect x="{32+c*96}" y="{108+r*72}" width="64" height="44" fill="{WS}"/>' for c in range(3) for r in range(3))),
    'telefon': (BLAU, 'Telefon, Anruf, Rückruf', f'<path d="M10 200 A150 150 0 0 1 310 200 L310 250 L230 250 L230 200 A70 70 0 0 0 90 200 L90 250 L10 250 Z" fill="{BLAU}"/><path d="M70 272 L250 272 L300 320 L20 320 Z" fill="{SCH}"/>'),
    'mail': (BLAU, 'E-Mail, Postfach, Nachricht', f'<rect x="0" y="72" width="268" height="216" fill="{BLAU}"/><path d="M0 72 L134 184 L268 72" fill="none" stroke="{WS}" stroke-width="18"/><circle cx="292" cy="28" r="28" fill="{SCH}"/>'),
    'bildschirm': (BLAU, 'Computer, Einrichten, Website', f'<rect x="0" y="0" width="320" height="216" rx="16" fill="{SCH}"/><rect x="16" y="16" width="288" height="184" rx="6" fill="{WS}"/><rect x="40" y="40" width="64" height="136" rx="6" fill="{BLAU}"/><rect x="124" y="40" width="156" height="60" rx="6" fill="{BLAU}"/><rect x="124" y="116" width="156" height="60" rx="6" fill="{BLAU}"/><rect x="136" y="216" width="48" height="64" fill="{SCH}"/><rect x="72" y="280" width="176" height="24" fill="{SCH}"/>'),
    'handy': (BLAU, 'Handy, mobile Ansicht', f'<rect x="60" y="0" width="200" height="320" rx="28" fill="{SCH}"/><rect x="76" y="40" width="168" height="240" fill="{WS}"/><rect x="96" y="60" width="128" height="88" rx="6" fill="{BLAU}"/><rect x="96" y="164" width="128" height="96" rx="6" fill="{BLAU}"/>'),
    'kompass': (BLAU, 'Rundgang, Orientierung, Strategie', f'<circle cx="160" cy="160" r="160" fill="{BLAU}"/><path d="M160 24 L200 160 L160 296 L120 160 Z" fill="{WS}"/><circle cx="160" cy="160" r="18" fill="{SCH}"/>'),
    'ziel': (BLAU, 'Website-Check, Ziel, Treffer', f'<circle cx="160" cy="160" r="160" fill="{BLAU}"/><circle cx="160" cy="160" r="112" fill="{WS}"/><circle cx="160" cy="160" r="72" fill="{BLAU}"/><circle cx="160" cy="160" r="38" fill="{WS}"/><circle cx="160" cy="160" r="22" fill="{SCH}"/>'),
    'sprechblase': (BLAU, 'Chat, Gespräch, Stimmen', f'<rect x="0" y="0" width="320" height="232" rx="40" fill="{BLAU}"/><path d="M48 216 L48 320 L152 216 Z" fill="{BLAU}"/>' + ''.join(f'<circle cx="{88+i*72}" cy="116" r="22" fill="{WS}"/>' for i in range(3))),
    'checkliste': (BLAU, 'Checkliste, Prüfung, Enthalten', ''.join(f'<rect x="0" y="{y}" width="64" height="64" fill="{SCH}"/><rect x="96" y="{y+16}" width="224" height="32" fill="{BLAU}"/>' for y in (0, 128, 256))),
    'haken': (BLAU, 'Erledigt, Bestätigt, Vorteil', f'<circle cx="160" cy="160" r="160" fill="{BLAU}"/><path d="M84 164 L140 220 L240 112" fill="none" stroke="{WS}" stroke-width="34" stroke-linecap="square"/>'),
    'schloss': (BLAU, 'Sicherheit, Datenschutz, Zugang', f'<path d="M72 128 V88 A88 88 0 0 1 248 88 V128 H212 V88 A52 52 0 0 0 108 88 V128 Z" fill="{SCH}"/><rect x="24" y="148" width="272" height="172" rx="12" fill="{BLAU}"/><circle cx="160" cy="220" r="24" fill="{WS}"/><rect x="148" y="232" width="24" height="48" fill="{WS}"/>'),
    'uhr': (BLAU, 'Zeit, Dauer, Termin', f'<circle cx="160" cy="160" r="160" fill="{BLAU}"/><rect x="148" y="52" width="24" height="120" fill="{WS}"/><rect x="148" y="148" width="100" height="24" fill="{WS}"/><circle cx="160" cy="160" r="20" fill="{SCH}"/>'),
    'person': (BLAU, 'Ansprechpartnerin, Kund:in, Team', f'<circle cx="160" cy="64" r="64" fill="{SCH}"/><path d="M0 320 A160 160 0 0 1 320 320 Z" fill="{BLAU}"/>'),
    'ort': (BLAU, 'Standort, Leipzig, Einzugsgebiet', f'<path d="M160 320 L44 168 A136 136 0 1 1 276 168 Z" fill="{BLAU}"/><circle cx="160" cy="116" r="52" fill="{WS}"/><circle cx="160" cy="116" r="24" fill="{SCH}"/>'),
    # ---------- Eyecatcher: Gelb, Pink, Rosa, Rot ----------
    'skills': (GELB, 'Skills, feste Abläufe, Automatik', f'<rect x="-30" y="196" width="230" height="40" transform="rotate(-45 85 216)" fill="{SCH}"/><path d="{stern(216, 104, 104, 36)}" fill="{GELB}"/>'),
    'stern': (GELB, 'Highlight, Empfehlung, Neu', f'<path d="{stern(160, 160, 160, 58)}" fill="{GELB}"/><circle cx="160" cy="160" r="26" fill="{SCH}"/>'),
    'idee': (GELB, 'Idee, Lernen, Regel', f'<circle cx="160" cy="124" r="124" fill="{GELB}"/><rect x="100" y="260" width="120" height="24" fill="{SCH}"/><rect x="124" y="296" width="72" height="24" fill="{SCH}"/>'),
    'warnung': (GELB, 'Achtung, Tarif, Grenzen', f'<path d="M160 0 L320 300 L0 300 Z" fill="{GELB}"/><rect x="146" y="96" width="28" height="112" fill="{SCH}"/><circle cx="160" cy="250" r="18" fill="{SCH}"/>'),
    'geld': (GELB, 'Preis, Kosten, Festpreis', f'<rect x="20" y="248" width="280" height="32" fill="{SCH}"/><rect x="40" y="200" width="240" height="32" fill="{SCH}"/><rect x="20" y="152" width="280" height="32" fill="{SCH}"/><circle cx="160" cy="68" r="68" fill="{GELB}"/><rect x="0" y="296" width="320" height="24" fill="{SCH}"/>'),
    'megafon': (PINK, 'Marketing, Kontakt, Ankündigung', f'<rect x="0" y="112" width="64" height="96" fill="{SCH}"/><path d="M80 112 L320 0 L320 320 L80 208 Z" fill="{PINK}"/>'),
    'herz': (ROSA, 'Herzensprojekt, Initiative, Dank', herz(160, 186, 150, ROSA)),
    'palette': (ROSA, 'Gestaltung, Farben, Marke', f'<circle cx="160" cy="160" r="160" fill="{ROSA}"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="28" fill="{WS}"/>' for x, y in [(96, 92), (176, 72), (244, 132)]) + f'<circle cx="112" cy="212" r="40" fill="{SCH}"/>'),
    'geschenk': (ROT, 'Gratis, Bonus, Geschenk', f'<rect x="0" y="96" width="320" height="224" fill="{ROT}"/><rect x="144" y="96" width="32" height="224" fill="{WS}"/><rect x="0" y="176" width="320" height="28" fill="{WS}"/><circle cx="116" cy="52" r="44" fill="{SCH}"/><circle cx="204" cy="52" r="44" fill="{SCH}"/>'),
}


# Tatsächlicher Rand jeder Form (x, y, rechts, unten), im Browser mit getBBox() gemessen (12.11.2026).
# Die Datei bekommt genau diesen Ausschnitt als viewBox und xMinYMin: Das Icon hat keinen Innenabstand und steht
# wirklich bündig mit dem Text (Anna 12.11.2026: „dass die Icons kein Padding haben“). Neues Icon: hier eintragen.
RAND = {
    'anleitung': (20, 0, 300, 320), 'bildschirm': (0, 0, 320, 304), 'geschenk': (0, 8, 320, 320), 'handy': (60, 0, 260, 320),
    'herz': (32, 58, 288, 292), 'idee': (36, 0, 284, 320), 'mail': (0, 0, 320, 288), 'ordner': (0, 24, 320, 296),
    'ort': (24, -39, 296, 320), 'schloss': (24, 0, 296, 320), 'skills': (-10, 0, 320, 311), 'telefon': (10, 50, 310, 320),
    'warnung': (0, 0, 320, 300),
}


def svg(inhalt, name=''):
    x, y, r, u = RAND.get(name, (0, 0, 320, 320))
    w, h = r - x, u - y
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMinYMin meet" aria-hidden="true">{inhalt}</svg>\n')


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, (_, _, inhalt) in SET.items():
        (ZIEL / f'{name}.svg').write_text(svg(inhalt, name), encoding='utf-8')
    blau = sum(1 for f, _, _ in SET.values() if f == BLAU)
    kacheln = ''.join(f'<figure><img src="../bilder/symbole/{n}.svg" alt="" width="96" height="96"><figcaption><b>{n}</b><br>{z}</figcaption></figure>'
                      for n, (_, z, _) in SET.items())
    leistungen = ''.join(f'<figure><img src="../bilder/formen/{n}.svg" alt="" width="96" height="96"><figcaption><b>{n}</b><br>Leistung (Spiel-Farbe)</figcaption></figure>'
                         for n in ['brand', 'ui-ux', 'website', 'marketing', 'ki', 'retainer', 'print', 'illustration', 'motion'])
    UEBERSICHT.parent.mkdir(parents=True, exist_ok=True)
    UEBERSICHT.write_text(f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Icon-Set STUDIO AAH!</title><style>body{{font:15px/1.4 system-ui,sans-serif;margin:40px;color:#0e1011}}h1{{font-size:28px}}
.raster{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:24px;margin:24px 0 48px}}figure{{margin:0;padding:20px;background:#f4f4f2;border-radius:16px}}
img{{display:block;width:72px;height:72px;object-fit:contain;object-position:left top;margin-bottom:12px;outline:1px dashed #ccc}}figcaption{{font-size:13px;color:#555}}figcaption b{{color:#0e1011}}</style></head><body>
<h1>Icon-Set STUDIO AAH! ({len(SET)} + 9 Leistungen)</h1><p>Blau: {blau} von {len(SET)} ({round(100*blau/len(SET))} %). Schwarz, Weiß und eine Farbe; Form bis an den Rand, steht linksbündig.</p>
<div class="raster">{kacheln}</div><h2>Leistungen (bleiben in Spiel-Farben)</h2><div class="raster">{leistungen}</div></body></html>
''', encoding='utf-8')
    print(f'Icons: {len(SET)} geschrieben, davon blau {blau}; Übersicht: website/entwurf-icons/')


if __name__ == '__main__':
    main()
