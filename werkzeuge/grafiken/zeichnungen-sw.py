# Icon-Set „Zeichnungen schwarz-weiß“:
# schwarze Handlinie, weiße Fläche, kein Versatz, keine Farbe. Zitterstrich wie hero-sticker.py.
# Aufruf im Repository-Ordner: python3 werkzeuge/grafiken/zeichnungen-sw.py
import math, pathlib, random

ZIEL = pathlib.Path(__file__).resolve().parents[2] / 'website' / 'bilder' / 'zeichnungen-sw'
SCHWARZ, WEISS, BLAU, GRAU = '#0E1011', '#FFFFFF', '#2A5FE6', '#EEECE7'
# Stil: klare Linie ohne Zittern, eine Strichstärke,
# Schwarz, Weiß, Grau, genau ein blaues Element je Motiv.


def zitter(punkte, staerke, seed):
    r = random.Random(seed)
    return [(x + r.uniform(-staerke, staerke), y + r.uniform(-staerke, staerke)) for x, y in punkte]


def linie(punkte, zu=True):
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in punkte)
    return d + (' Z' if zu else '')


FARBE = {}   # Motiv-Seed -> Füllfarbe (blaues Element je Motiv)


def form(punkte, seed, zu=True, fuellen=True, breite=7, farbe=None):
    """Bauhaus-Stil: eine klare Linie, Fläche weiß (oder farbe)."""
    f = (farbe or WEISS) if (fuellen and zu) else 'none'
    # Mitte zwischen Zeichnung und Bauhaus: klare Form, leicht gezeichnete Linie
    return (f'<path d="{linie(zitter(punkte, 1.1, seed), zu)}" fill="{f}" stroke="{SCHWARZ}" stroke-width="{breite * .85:.1f}" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def strich(x1, y1, x2, y2, seed, breite=7):
    schritte = 6
    p = [(x1 + (x2 - x1) * i / schritte, y1 + (y2 - y1) * i / schritte) for i in range(schritte + 1)]
    return form(p, seed, zu=False, breite=breite)


def kreis(cx, cy, r, seed, n=72, fuellen=True, ry=None, farbe=None):
    ry = ry or r
    p = [(cx + r * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return form(p, seed, fuellen=fuellen, farbe=farbe)


def punkt(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SCHWARZ}"/>'


def svg(inhalt):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">{inhalt}</svg>\n'


# Zwinkern: läuft im SVG selbst, damit es auch als <img> funktioniert. Zweimal kurz nach dem Laden,
# dann Ruhe (unter fünf Sekunden, WCAG 2.2.2); bei „Bewegung reduzieren“ bleibt das Auge offen.
ZWINKERN = ('<style>.o{animation:o 4.6s steps(1) 1 both}.z{opacity:0;animation:z 4.6s steps(1) 1 both}'
            '@keyframes o{0%,30%,82%,100%{opacity:1}26%,78%{opacity:0}}'
            '@keyframes z{0%,30%,82%,100%{opacity:0}26%,78%{opacity:1}}'
            '@media (prefers-reduced-motion:reduce){.o,.z{animation:none}}</style>')


def auge():
    oben = [(60 + 280 * i / 20, 200 - 110 * math.sin(math.pi * i / 20)) for i in range(21)]
    unten = [(340 - 280 * i / 20, 200 + 90 * math.sin(math.pi * i / 20)) for i in range(1, 20)]
    wimpern = ''.join(strich(200 + 150 * math.cos(a), 160 - 130 * math.sin(a), 200 + 185 * math.cos(a), 150 - 165 * math.sin(a), 40 + k)
                      for k, a in enumerate((math.radians(w) for w in (40, 65, 90, 115, 140))))
    offen = form(oben + unten, 1) + kreis(200, 196, 58, 3, farbe=BLAU) + punkt(200, 196, 28) + f'<circle cx="214" cy="182" r="9" fill="{WEISS}"/>'
    lid = [(60 + 280 * i / 20, 200 + 62 * math.sin(math.pi * i / 20)) for i in range(21)]
    zu = form(lid, 11, zu=False)
    return svg(ZWINKERN + f'<g class="o">{offen}</g><g class="z">{zu}</g>' + wimpern)


def bildschirm():
    rahmen = [(70, 80), (330, 80), (330, 260), (70, 260)]
    innen = [(92, 100), (308, 100), (308, 240), (92, 240)]
    fuss = [(170, 260), (230, 260), (244, 316), (156, 316)]
    stern = [(200 + (46 if i % 2 == 0 else 18) * math.cos(math.radians(-90 + 45 * i)), 170 + (46 if i % 2 == 0 else 18) * math.sin(math.radians(-90 + 45 * i))) for i in range(8)]
    return svg(form(fuss, 5) + form(rahmen, 1) + form(innen, 3, breite=5, farbe=GRAU) + form(stern, 7, farbe=BLAU) + strich(120, 324, 280, 324, 9))


def megafon():
    trichter = [(130, 170), (300, 90), (300, 300), (130, 230)]
    griff = [(150, 228), (186, 244), (176, 310), (146, 304)]
    hinten = [(80, 166), (132, 166), (132, 234), (80, 234)]
    wellen = strich(326, 150, 360, 128, 21) + strich(330, 196, 370, 196, 22) + strich(326, 242, 360, 264, 23)
    return svg(form(griff, 5) + form(hinten, 3) + form(trichter, 1, farbe=BLAU) + kreis(300, 195, 16, 9, ry=104, fuellen=True) + wellen)


def gluehbirne():
    glas = [(200 + 92 * math.cos(math.radians(a)), 160 + 92 * math.sin(math.radians(a))) for a in range(150, 391, 10)]
    glas += [(258, 270), (142, 270)]
    sockel = [(150, 270), (250, 270), (244, 316), (156, 316)]
    draht = [(176, 270), (176, 200), (190, 180), (200, 200), (210, 180), (224, 200), (224, 270)]
    strahlen = ''.join(strich(200 + 120 * math.cos(math.radians(a)), 160 + 120 * math.sin(math.radians(a)),
                              200 + 150 * math.cos(math.radians(a)), 160 + 150 * math.sin(math.radians(a)), 30 + k)
                       for k, a in enumerate((-160, -125, -90, -55, -20)))
    return svg(form(glas, 1) + form(sockel, 3, farbe=BLAU) + strich(156, 292, 244, 292, 4, 5) + form(draht, 6, zu=False, breite=5) + strahlen + strich(180, 336, 220, 336, 8))


def blitz():
    p = [(236, 30), (110, 214), (190, 214), (150, 370), (300, 162), (214, 162), (264, 30)]
    return svg(form(p, 1, farbe=BLAU) + strich(86, 124, 60, 108, 11) + strich(82, 156, 52, 156, 12) + strich(326, 252, 352, 268, 13))


def pfeil():
    p = [(184, 50), (216, 50), (216, 250), (270, 250), (200, 350), (130, 250), (184, 250)]
    return svg(form(p, 1, farbe=BLAU))


def stern():
    p = [(200 + (160 if i % 2 == 0 else 50) * math.cos(math.radians(-90 + 45 * i)),
          200 + (160 if i % 2 == 0 else 50) * math.sin(math.radians(-90 + 45 * i))) for i in range(8)]
    return svg(form(p, 1, farbe=BLAU) + strich(318, 70, 330, 58, 3) + strich(86, 330, 72, 344, 4))


def herz():
    p = []
    for i in range(40):
        t = 2 * math.pi * i / 40
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        p.append((200 + 9.5 * x, 190 - 9.5 * y))
    return svg(form(p, 1, farbe=BLAU) + strich(306, 92, 330, 72, 5) + strich(318, 126, 348, 120, 6))


def lupe():
    return svg(strich(246, 246, 344, 344, 7, 12) + kreis(170, 170, 104, 1, farbe=GRAU) + kreis(170, 170, 40, 3, farbe=BLAU))


def sprechblase():
    p = [(60, 90), (340, 90), (340, 256), (196, 256), (128, 330), (140, 256), (60, 256)]
    return svg(form(p, 1) + strich(110, 146, 290, 146, 3, 5) + strich(110, 196, 240, 196, 4, 5) + kreis(282, 196, 14, 6, farbe=BLAU))


def giesskanne():
    """Retainer: betreute Weiterentwicklung – die Gießkanne ist geneigt und gießt die Pflanze."""
    koerper = [(96, 170), (236, 170), (252, 318), (80, 318)]
    henkel = [(236 + 62 * math.cos(math.radians(a)), 220 + 70 * math.sin(math.radians(a))) for a in range(-90, 91, 15)]
    tuelle = [(96, 210), (34, 120), (22, 128), (80, 236)]
    kanne = form(henkel, 5, zu=False) + form(tuelle, 3) + form(koerper, 1, farbe=BLAU) + strich(96, 196, 236, 196, 4, 5)
    wasser = strich(48, 262, 44, 290, 21, 5) + strich(64, 266, 62, 300, 22, 5) + strich(32, 262, 26, 286, 23, 5)
    pflanze = (strich(52, 380, 52, 318, 31) + form([(52, 340), (24, 318), (16, 292), (46, 310)], 32)
               + form([(52, 352), (82, 326), (94, 304), (60, 322)], 33))
    return svg(f'<g transform="translate(78 40) rotate(-32 160 240)">{kanne}</g>' + wasser + pflanze + strich(0, 380, 140, 380, 8))


# Motive nach Zeichnungen von Annas Tochter, nachgezeichnet, ohne Namen
def gesicht_grinsen():
    kopf = kreis(200, 205, 150, 1, ry=140)
    mund = [(92, 190), (140, 262), (200, 290), (262, 262), (310, 190), (262, 232), (200, 246), (140, 232)]
    zaehne = ''.join(strich(x, 236 + abs(x - 200) * -.25 + 8, x + 12, 262 - abs(x - 200) * .25, 70 + i, 4) for i, x in enumerate(range(130, 280, 24)))
    return svg(kopf + form(mund, 3, farbe=BLAU) + zaehne + punkt(150, 140, 9) + punkt(250, 140, 9))


def gesicht_geist():
    kopf = form([(110, 300), (90, 200), (110, 110), (200, 70), (290, 110), (310, 200), (290, 300), (250, 300), (250, 340), (150, 340), (150, 300)], 1)
    augen = kreis(160, 180, 24, 3, ry=30, farbe=BLAU) + kreis(240, 180, 24, 4, ry=30, farbe=BLAU)
    zaehne = ''.join(strich(x, 302, x, 340, 50 + i, 5) for i, x in enumerate((175, 200, 225)))
    return svg(kopf + augen + zaehne)


def gesicht_hut():
    hut = form([(120, 132), (280, 132), (280, 120), (250, 120), (250, 30), (150, 30), (150, 120), (120, 120)], 2, farbe=BLAU)
    kopf = kreis(200, 240, 130, 1, ry=120)
    auge = lambda cx, cy, sd: form([(cx - 52, cy), (cx - 20, cy - 18), (cx + 20, cy - 18), (cx + 52, cy), (cx + 20, cy + 18), (cx - 20, cy + 18)], sd) + punkt(cx, cy, 8)
    mund = form([(110, 300), (200, 336), (300, 260)], 9, zu=False)
    return svg(kopf + hut + auge(160, 220, 5) + auge(240, 220, 6) + mund)


def vogel():
    koerper = kreis(200, 210, 58, 1, farbe=BLAU)
    fluegel = ''.join(strich(200, 200, 200 + 170 * math.cos(math.radians(w)), 200 - 170 * math.sin(math.radians(w)), 20 + i, 6) for i, w in enumerate(range(100, 171, 14)))
    fluegel += ''.join(strich(200, 220, 200 + 180 * math.cos(math.radians(w)), 220 - 180 * math.sin(math.radians(w)), 40 + i, 6) for i, w in enumerate(range(-10, 61, 14)))
    kopf = kreis(150, 190, 34, 3) + punkt(146, 186, 6) + form([(118, 184), (98, 196), (120, 204)], 7)
    return svg(fluegel + koerper + kopf + strich(60, 70, 96, 58, 81, 5) + strich(96, 58, 120, 78, 82, 5))


SET = {'gesicht-grinsen': gesicht_grinsen, 'gesicht-geist': gesicht_geist, 'gesicht-hut': gesicht_hut, 'vogel': vogel, 'giesskanne': giesskanne, 'lupe': lupe, 'sprechblase': sprechblase, 'auge': auge, 'bildschirm': bildschirm, 'megafon': megafon, 'gluehbirne': gluehbirne,
       'blitz': blitz, 'pfeil': pfeil, 'stern': stern, 'herz': herz}

if __name__ == '__main__':
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, fn in SET.items():
        (ZIEL / f'{name}.svg').write_text(fn(), encoding='utf-8')
        print('geschrieben:', ZIEL / f'{name}.svg')
