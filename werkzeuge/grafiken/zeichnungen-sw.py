# Icon-Set „Zeichnungen schwarz-weiß“ (Anna 22.11.2026, Vorbild Strichzeichnungen wie bei farbenmeer.de):
# schwarze Handlinie, weiße Fläche, kein Versatz, keine Farbe. Zitterstrich wie hero-sticker.py.
# Aufruf im Repository-Ordner:  python3 werkzeuge/grafiken/zeichnungen-sw.py
import math, pathlib, random

ZIEL = pathlib.Path(__file__).resolve().parents[2] / 'website' / 'bilder' / 'zeichnungen-sw'
SCHWARZ, WEISS = '#0E1011', '#FFFFFF'


def zitter(punkte, staerke, seed):
    r = random.Random(seed)
    return [(x + r.uniform(-staerke, staerke), y + r.uniform(-staerke, staerke)) for x, y in punkte]


def linie(punkte, zu=True):
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in punkte)
    return d + (' Z' if zu else '')


def form(punkte, seed, zu=True, fuellen=True, breite=7):
    """Fläche weiß, darüber zwei leicht versetzte Handlinien."""
    teile = []
    if fuellen and zu:
        teile.append(f'<path d="{linie(punkte)}" fill="{WEISS}"/>')
    for i, (st, b) in enumerate(((1.6, breite), (2.6, breite * .45))):
        teile.append(f'<path d="{linie(zitter(punkte, st, seed + i), zu)}" stroke="{SCHWARZ}" stroke-width="{b:.1f}" '
                     'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return ''.join(teile)


def strich(x1, y1, x2, y2, seed, breite=7):
    schritte = 6
    p = [(x1 + (x2 - x1) * i / schritte, y1 + (y2 - y1) * i / schritte) for i in range(schritte + 1)]
    return form(p, seed, zu=False, breite=breite)


def kreis(cx, cy, r, seed, n=36, fuellen=True, ry=None):
    ry = ry or r
    p = [(cx + r * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return form(p, seed, fuellen=fuellen)


def punkt(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SCHWARZ}"/>'


def svg(inhalt):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">{inhalt}</svg>\n'


def auge():
    oben = [(60 + 280 * i / 20, 200 - 110 * math.sin(math.pi * i / 20)) for i in range(21)]
    unten = [(340 - 280 * i / 20, 200 + 90 * math.sin(math.pi * i / 20)) for i in range(1, 20)]
    wimpern = ''.join(strich(200 + 150 * math.cos(a), 160 - 130 * math.sin(a), 200 + 185 * math.cos(a), 150 - 165 * math.sin(a), 40 + k)
                      for k, a in enumerate((math.radians(w) for w in (40, 65, 90, 115, 140))))
    return svg(form(oben + unten, 1) + kreis(200, 196, 58, 3) + punkt(200, 196, 28) + f'<circle cx="214" cy="182" r="9" fill="{WEISS}"/>' + wimpern)


def bildschirm():
    rahmen = [(70, 80), (330, 80), (330, 260), (70, 260)]
    innen = [(92, 100), (308, 100), (308, 240), (92, 240)]
    fuss = [(170, 260), (230, 260), (244, 316), (156, 316)]
    stern = [(200 + (46 if i % 2 == 0 else 18) * math.cos(math.radians(-90 + 45 * i)), 170 + (46 if i % 2 == 0 else 18) * math.sin(math.radians(-90 + 45 * i))) for i in range(8)]
    return svg(form(fuss, 5) + form(rahmen, 1) + form(innen, 3, breite=5) + form(stern, 7) + strich(120, 324, 280, 324, 9))


def megafon():
    trichter = [(130, 170), (300, 90), (300, 300), (130, 230)]
    griff = [(150, 228), (186, 244), (176, 310), (146, 304)]
    hinten = [(80, 166), (132, 166), (132, 234), (80, 234)]
    wellen = strich(326, 150, 360, 128, 21) + strich(330, 196, 370, 196, 22) + strich(326, 242, 360, 264, 23)
    return svg(form(griff, 5) + form(hinten, 3) + form(trichter, 1) + kreis(300, 195, 16, 9, ry=104, fuellen=True) + wellen)


def gluehbirne():
    glas = [(200 + 92 * math.cos(math.radians(a)), 160 + 92 * math.sin(math.radians(a))) for a in range(150, 391, 10)]
    glas += [(258, 270), (142, 270)]
    sockel = [(150, 270), (250, 270), (244, 316), (156, 316)]
    draht = [(176, 270), (176, 200), (190, 180), (200, 200), (210, 180), (224, 200), (224, 270)]
    strahlen = ''.join(strich(200 + 120 * math.cos(math.radians(a)), 160 + 120 * math.sin(math.radians(a)),
                              200 + 150 * math.cos(math.radians(a)), 160 + 150 * math.sin(math.radians(a)), 30 + k)
                       for k, a in enumerate((-160, -125, -90, -55, -20)))
    return svg(form(glas, 1) + form(sockel, 3) + strich(156, 292, 244, 292, 4, 5) + form(draht, 6, zu=False, breite=5) + strahlen + strich(180, 336, 220, 336, 8))


def blitz():
    p = [(236, 30), (110, 214), (190, 214), (150, 370), (300, 162), (214, 162), (264, 30)]
    return svg(form(p, 1) + strich(86, 124, 60, 108, 11) + strich(82, 156, 52, 156, 12) + strich(326, 252, 352, 268, 13))


def pfeil():
    p = [(184, 50), (216, 50), (216, 250), (270, 250), (200, 350), (130, 250), (184, 250)]
    return svg(form(p, 1))


def stern():
    p = [(200 + (160 if i % 2 == 0 else 50) * math.cos(math.radians(-90 + 45 * i)),
          200 + (160 if i % 2 == 0 else 50) * math.sin(math.radians(-90 + 45 * i))) for i in range(8)]
    return svg(form(p, 1) + strich(318, 70, 330, 58, 3) + strich(86, 330, 72, 344, 4))


def herz():
    p = []
    for i in range(40):
        t = 2 * math.pi * i / 40
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        p.append((200 + 9.5 * x, 190 - 9.5 * y))
    return svg(form(p, 1) + strich(306, 92, 330, 72, 5) + strich(318, 126, 348, 120, 6))


SET = {'auge': auge, 'bildschirm': bildschirm, 'megafon': megafon, 'gluehbirne': gluehbirne,
       'blitz': blitz, 'pfeil': pfeil, 'stern': stern, 'herz': herz}

if __name__ == '__main__':
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, fn in SET.items():
        (ZIEL / f'{name}.svg').write_text(fn(), encoding='utf-8')
        print('geschrieben:', ZIEL / f'{name}.svg')
