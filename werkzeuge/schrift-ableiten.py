# Leitet fehlende Zeichen aus Annas Handschrift-Schrift ab (nur aus vorhandenen Formen: Punkt, C, O)
import math, sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
src, out = sys.argv[1], sys.argv[2]
f = TTFont(src); gs = f.getGlyphSet(); glyf = f['glyf']; hmtx = f['hmtx']
PX0, PY0 = 89.5, 36   # Mitte des Punkts

def neu(name, teile, adv, uni):
    pen = TTGlyphPen(gs)
    for basis, t in teile:
        gs[basis].draw(TransformPen(pen, t))
    g = pen.glyph(); glyf[name] = g; g.recalcBounds(glyf)
    hmtx[name] = (adv, g.xMin if g.numberOfContours else 0)
    for tab in f['cmap'].tables:
        if tab.isUnicode() or (tab.platformID == 3): tab.cmap[uni] = name
    if name not in f.getGlyphOrder(): f.setGlyphOrder(f.getGlyphOrder() + [name])

def strich(laenge, dicke, winkel, cx, cy):
    """Punkt zu einem Pinselstrich gestreckt, gedreht um winkel (Grad), Mitte bei cx, cy"""
    sx, sy = laenge / 87, dicke
    a = math.radians(winkel); c, s = math.cos(a), math.sin(a)
    # erst Punkt in den Ursprung, dann strecken, drehen, verschieben
    xx, xy, yx, yy = sx * c, sx * s, -sy * s, sy * c
    dx = cx - (xx * PX0 + yx * PY0); dy = cy - (xy * PX0 + yy * PY0)
    return ('period', (xx, xy, yx, yy, dx, dy))

def punkt(cx, cy, k=1.0):
    return ('period', (k, 0, 0, k, cx - k * PX0, cy - k * PY0))

def komma(cx, cy, dreh=0):
    # Punkt oben plus kurzer, schräger Schwanz nach unten links
    a = punkt(cx, cy)
    b = strich(120, .75, 115 + dreh, cx - 14, cy - 55)
    return [a, b]

neu('periodcentered', [punkt(87, 250)], 175, 0x00B7)
neu('colon', [punkt(87, 36), punkt(87, 300)], 175, 0x003A)
neu('comma', komma(87, 36), 175, 0x002C)
neu('semicolon', [punkt(97, 300)] + komma(97, 36), 195, 0x003B)
neu('hyphen', [strich(230, .8, 4, 160, 230)], 320, 0x002D)
neu('endash', [strich(400, .8, 3, 245, 230)], 490, 0x2013)
neu('slash', [strich(780, .85, 68, 230, 330)], 460, 0x002F)
neu('exclam', [strich(560, 1.0, 84, 120, 430), punkt(92, 36)], 220, 0x0021)
neu('one', [strich(690, 1.0, 82, 150, 345), strich(120, .75, 38, 112, 620)], 300, 0x0031)
neu('quoteright', komma(87, 640), 175, 0x2019)
neu('quotesingle', komma(87, 640), 175, 0x0027)
neu('quoteleft', [('comma', (-1, 0, 0, -1, 175, 600))], 175, 0x2018)
neu('quotedblright', komma(87, 640) + komma(187, 640), 275, 0x201D)
neu('quotedbl', komma(87, 640) + komma(187, 640), 275, 0x0022)
neu('quotedblleft', [('comma', (-1, 0, 0, -1, 175, 600)), ('comma', (-1, 0, 0, -1, 275, 600))], 275, 0x201C)
neu('quotedblbase', komma(87, 36) + komma(187, 36), 275, 0x201E)
neu('quotesinglbase', komma(87, 36), 175, 0x201A)
neu('parenleft', [('C', (.5, 0, 0, 1.35, 10, -130))], 260, 0x0028)
neu('parenright', [('C', (-.5, 0, 0, 1.35, 250, -130))], 260, 0x0029)
neu('zero', [('O', (.72, 0, 0, 1.0, 10, 0))], 480, 0x0030)
f['maxp'].numGlyphs = len(f.getGlyphOrder())
f.save(out)
print('ok', len(f.getBestCmap()))
