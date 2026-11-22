# Sticker für den Hero der Startseite (Anna 22.11.2026): Blitz statt Vogel, Regenbogen statt „AAH!“-Blase, Pfeil nach unten.
# Zeichenstil wie die übrigen Sticker in website/bilder/sticker/: rosa Versatz, Farbfläche, doppelte schwarze Kontur.
# Aufruf im Repository-Ordner:  python3 werkzeuge/grafiken/hero-sticker.py
import pathlib, random

ZIEL = pathlib.Path(__file__).resolve().parents[2] / 'website' / 'bilder' / 'sticker'
ROSA, SCHWARZ, GELB, BLAU, ROT, PINK = '#FF8FC8', '#0E1011', '#FFE600', '#2A5FE6', '#FF3B2F', '#FF4FA3'


def zitter(punkte, staerke, seed):
    r = random.Random(seed)
    return [(x + r.uniform(-staerke, staerke), y + r.uniform(-staerke, staerke)) for x, y in punkte]


def linie(punkte, zu=True):
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in punkte)
    return d + (' Z' if zu else '')


def kontur(d, breite=8):
    return f'<path d="{d}" stroke="{SCHWARZ}" stroke-width="{breite}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def svg(inhalt):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">{inhalt}</svg>\n'


def blitz():
    p = [(236, 26), (104, 214), (188, 214), (146, 374), (304, 158), (214, 158), (266, 26)]
    versatz = [(x + 9, y + 8) for x, y in p]
    return svg(f'<path d="{linie(versatz)}" fill="{ROSA}"/><path d="{linie(p)}" fill="{GELB}"/>'
               + kontur(linie(zitter(p, 2.5, 1))) + kontur(linie(zitter(p, 3.5, 2)), 4)
               # drei kleine Striche wie bei einer Zeichnung
               + kontur('M84 120 L58 104') + kontur('M80 152 L50 152') + kontur('M330 250 L356 266'))


def bogen(cx, cy, R, r, schritte=40):
    import math
    aussen = [(cx - R * math.cos(math.pi * i / schritte), cy - R * math.sin(math.pi * i / schritte)) for i in range(schritte + 1)]
    innen = [(cx + r * math.cos(math.pi * i / schritte), cy - r * math.sin(math.pi * i / schritte)) for i in range(schritte + 1)]
    return aussen + innen


def regenbogen():
    cx, cy = 200, 300
    baender = [(176, 140, ROT), (140, 106, GELB), (106, 74, BLAU)]
    teile = []
    for i, (R, r, farbe) in enumerate(baender):
        p = bogen(cx, cy, R, r)
        teile.append(f'<path d="{linie([(x + 9, y + 8) for x, y in p])}" fill="{ROSA}"/>')
    for i, (R, r, farbe) in enumerate(baender):
        p = bogen(cx, cy, R, r)
        teile.append(f'<path d="{linie(p)}" fill="{farbe}"/>' + kontur(linie(zitter(p, 1.6, 10 + i))) + kontur(linie(zitter(p, 2.4, 20 + i)), 3))
    # zwei kleine Wolken an den Enden
    for x in (cx - 140, cx + 140):
        w = f'M{x - 52} {cy + 6} C{x - 60} {cy - 26}, {x - 22} {cy - 36}, {x - 10} {cy - 18} C{x} {cy - 46}, {x + 44} {cy - 40}, {x + 40} {cy - 10} C{x + 66} {cy - 12}, {x + 66} {cy + 22}, {x + 40} {cy + 22} L{x - 44} {cy + 22} C{x - 62} {cy + 22}, {x - 64} {cy + 8}, {x - 52} {cy + 6} Z'
        teile.append(f'<path d="{w}" fill="#fff"/>' + kontur(w))
    return svg(''.join(teile))


def pfeil():
    # geschwungener Pfeil wie gezeichnet, mit Strich darunter (Anna 22.11.2026)
    schaft = 'M206 24 C176 70, 238 104, 204 150 C176 190, 236 222, 206 266 C196 282, 190 300, 188 318'
    kopf = 'M140 270 C160 296, 176 316, 188 330 C212 314, 238 302, 270 296'
    strich = 'M150 372 C200 368, 246 368, 286 372'
    return svg(kontur(schaft, 12) + kontur('M209 28 C180 74, 241 108, 207 154 C179 194, 239 226, 209 270 C199 286, 193 302, 191 316', 4)
               + kontur(kopf, 12) + kontur('M144 276 C162 300, 178 318, 190 328 C214 312, 238 302, 266 298', 4) + kontur(strich, 10))



def megafon():
    # Megafon für die Fußkarte „Demokratie braucht Sichtbarkeit“ (Anna 22.11.2026: Illustration statt 3D-Icon)
    trichter = [(110, 170), (250, 92), (272, 92), (272, 300), (250, 300), (110, 222)]
    griff = [(150, 226), (182, 226), (196, 300), (164, 300)]
    hinten = [(78, 168), (112, 168), (112, 224), (78, 224)]
    teile = []
    for form, farbe in ((griff, BLAU), (hinten, SCHWARZ), (trichter, ROT)):
        teile.append(f'<path d="{linie([(x + 9, y + 8) for x, y in form])}" fill="{ROSA}"/>')
    for i, (form, farbe) in enumerate(((griff, BLAU), (hinten, SCHWARZ), (trichter, ROT))):
        teile.append(f'<path d="{linie(form)}" fill="{farbe}"/>' + kontur(linie(zitter(form, 2, 30 + i))))
    teile.append(f'<ellipse cx="272" cy="196" rx="20" ry="104" fill="{GELB}"/>' + kontur('M272 92 C300 120, 300 272, 272 300 C244 272, 244 120, 272 92 Z'))
    for d in ('M320 150 L360 126', 'M330 196 L376 196', 'M320 242 L360 266'):   # Schallstriche
        teile.append(kontur(d, 10))
    return svg(''.join(teile))


def sprechblase():
    # Sprechblase für den Abschluss der Branchenseiten (Anna 22.11.2026: „ein gezeichnetes Icon dazu“, „wir sollten ins Gespräch kommen“)
    blase = 'M80 96 C80 62, 108 44, 150 44 L276 44 C322 44, 348 66, 348 104 L348 216 C348 256, 322 276, 276 276 L188 276 L118 348 L132 276 L136 276 C100 276, 80 254, 80 216 Z'
    versatz = blase.replace('M80 96', 'M89 104')
    teile = [f'<path d="{blase}" transform="translate(9 8)" fill="{ROSA}"/>', f'<path d="{blase}" fill="{GELB}"/>', kontur(blase), kontur(blase, 3).replace('<path', '<path transform="translate(3 -2)"')]
    for x in (156, 214, 272):   # drei Punkte wie beim Tippen
        teile.append(f'<circle cx="{x}" cy="162" r="17" fill="{SCHWARZ}"/>')
    return svg(''.join(teile))


for name, f in (('zeichnung-blitz', blitz), ('zeichnung-regenbogen', regenbogen), ('zeichnung-pfeil', pfeil), ('zeichnung-megafon', megafon), ('zeichnung-sprechblase', sprechblase)):
    (ZIEL / f'{name}.svg').write_text(f(), encoding='utf-8')
    print('geschrieben:', f'bilder/sticker/{name}.svg')
