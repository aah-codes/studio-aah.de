# Neues kleines k für Annas Handschrift-Schrift (Anna 22.11.2026: „das Problem mit dem K“ – das k sah aus wie ein R,
# „Was es Rostet“, „Fangen wir Rlein an“). Aus ihren eigenen Formen gebaut: Punkt zu Pinselstrichen gestreckt
# (wie „1“ und „!“ in schrift-ableiten.py). Arbeitet direkt auf der Web-Schrift.
# Aufruf im Repository-Ordner:  python3 werkzeuge/schrift-k.py   (braucht fontTools und brotli)
import math, pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

DATEI = pathlib.Path(__file__).resolve().parents[1] / 'website' / 'schriften' / 'anna-haertelt-regular.woff2'
f = TTFont(DATEI); gs = f.getGlyphSet(); glyf = f['glyf']; hmtx = f['hmtx']
PX0, PY0 = 89.5, 36   # Mitte des Punkts (wie in schrift-ableiten.py)


def strich(laenge, dicke, winkel, cx, cy):
    sx, sy = laenge / 87, dicke
    a = math.radians(winkel); c, s = math.cos(a), math.sin(a)
    xx, xy, yx, yy = sx * c, sx * s, -sy * s, sy * c
    dx = cx - (xx * PX0 + yx * PY0); dy = cy - (xy * PX0 + yy * PY0)
    return ('period', (xx, xy, yx, yy, dx, dy))


# Anna 22.11.2026 (Skizze): oben Schlaufe wie ihr l, rechts eine kleine Schlaufe, dann das Bein nach rechts unten
teile = [('l', (1, 0, 0, 1, 0, 0)),                    # Stamm mit Schlaufe: ihr eigenes l
         ('o', (.5, 0, 0, .5, 205, 175)),              # kleine Schlaufe rechts auf Höhe der Mitte
         strich(270, 1.2, -50, 345, 95)]               # Bein nach rechts unten
pen = TTGlyphPen(gs)
for basis, t in teile:
    gs[basis].draw(TransformPen(pen, t))
g = pen.glyph(); glyf['k.neu'] = g; g.recalcBounds(glyf)
hmtx['k.neu'] = (int(g.xMax + 70), g.xMin)
if 'k.neu' not in f.getGlyphOrder(): f.setGlyphOrder(f.getGlyphOrder() + ['k.neu'])
for tab in f['cmap'].tables:
    if tab.isUnicode() or tab.platformID == 3: tab.cmap[0x006B] = 'k.neu'
f['maxp'].numGlyphs = len(f.getGlyphOrder())
f.flavor = 'woff2'
f.save(DATEI)
print('k ersetzt:', DATEI.name, (g.xMin, g.yMin, g.xMax, g.yMax))
