# Illustration „Eine Website geht zum Arzt“ für /website-check/.
# Eine Website (Browserfenster mit Kopfzeile, Bildfläche mit Herz und Pulslinie, Textbalken, Button) sitzt als Patientin
# auf der Liege; eine Ärztin (weißes Kreuz auf dem Rumpf) hört sie mit dem Stethoskop ab und hält ein Klemmbrett mit Häkchen.
# Bausteine (Figur, Browser, Button, Zeilen) aus werkzeuge/grafiken/fuer-wen-hero.py, Grundlage dort „gesundheit“.
# Blau berührt nie Schwarz (weiße Fugen); Herz nie blau.
# Format 1200 × 730, wird mit object-fit: cover / object-position: top gezeigt: Wichtiges in der Mitte, nichts am Rand.
# Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/website-beim-arzt.py → website/bilder/website-check/website-beim-arzt.svg
import importlib.util, pathlib

HIER = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('fuer_wen_hero', HIER / 'fuer-wen-hero.py')
hero = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hero)  # schreibt nichts (Ausgabe nur unter __main__)
SCH, BL, WS, GR, FUGE = hero.SCH, hero.BL, hero.WS, hero.GR, hero.FUGE
CR = '#eeece7'
ZIEL = HIER.parent.parent / 'website' / 'bilder' / 'website-check' / 'website-beim-arzt.svg'
B, H, BODEN = 1200, 730, 640
TITEL = 'Eine Website sitzt als Patientin auf der Liege; eine Ärztin hört sie mit dem Stethoskop ab und hält ein Klemmbrett mit Häkchen'


def herz(cx, cy, g, farbe=SCH):
    """Gedrehtes Quadrat + zwei Halbkreise (gestaltung.md), Spitze unten."""
    h = g / 2
    return (f'<g transform="translate({cx} {cy}) rotate(45)"><rect x="{-h}" y="{-h}" width="{g}" height="{g}" fill="{farbe}"/>'
            f'<circle cx="0" cy="{-h}" r="{h}" fill="{farbe}"/><circle cx="{-h}" cy="0" r="{h}" fill="{farbe}"/></g>')


def fuge_linie(d, breite=7):
    """Schwarze Linie mit weißer Fuge, damit sie auf schwarzen Flächen sichtbar bleibt."""
    return (f'<path d="{d}" fill="none" stroke="{WS}" stroke-width="{breite+10}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{SCH}" stroke-width="{breite}" stroke-linecap="round" stroke-linejoin="round"/>')


t = f'<line x1="60" y1="{BODEN}" x2="{B-60}" y2="{BODEN}" stroke="{SCH}" stroke-width="3"/>'

# Liege: Platte und zwei Beine
lx1, lx2, ly = 500, 950, 470
t += f'<rect x="{lx1}" y="{ly}" width="{lx2-lx1}" height="22" rx="4" fill="{SCH}"/>'
t += f'<rect x="{lx1+30}" y="{ly+22}" width="16" height="{BODEN-ly-22}" fill="{SCH}"/><rect x="{lx2-46}" y="{ly+22}" width="16" height="{BODEN-ly-22}" fill="{SCH}"/>'

# Website als Patientin: Beine baumeln vor der Liege (Balken mit Eckenradius 4, weiße Fuge zur schwarzen Platte)
bx, by, bw, bh = 550, 140, 360, 330
for fx, w in ((bx + 120, 14), (bx + 240, 4)):
    t += (f'<g transform="translate({fx} {by+bh-10}) rotate({w})"><rect x="-9" y="0" width="18" height="128" rx="4" fill="{SCH}" '
          f'stroke="{WS}" stroke-width="8" paint-order="stroke"/></g>')
inhalt = f'<rect x="{bx+30}" y="{by+66}" width="170" height="18" rx="4" fill="{SCH}"/>'
inhalt += hero.zeilen(bx + 30, by + 100, [260, 210])
# Bildfläche in Creme mit Herz und blauer Pulslinie
fx, fy, fw, fh = bx + 30, by + 146, bw - 60, 100
inhalt += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="8" fill="{CR}"/>'
inhalt += herz(fx + 56, fy + fh / 2 + 4, 30)
m = fy + fh / 2
puls = f'M{fx+100} {m} H{fx+150} L{fx+166} {m-34} L{fx+186} {m+30} L{fx+202} {m-14} L{fx+212} {m} H{fx+fw-24}'
inhalt += f'<path d="{puls}" fill="none" stroke="{BL}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
inhalt += hero.knopf(bx + 30, by + bh - 66, 150, 42)
t += hero.browser(bx, by, bw, bh, inhalt)

# Ärztin: rechter Arm hält das Bruststück an die Website, linker Arm hält das Klemmbrett
ax, s = 397, 0.95
arm_r, arm_l = -75, 34
t += hero.figur(ax, BODEN, s, arm_l, arm_r, 8, -6, blick=1)
# weißes Kreuz auf dem Rumpf (Kittel-Zeichen, kein Rot)
kx, ky = ax, BODEN - 254 * s
t += f'<rect x="{kx-20*s}" y="{ky-6*s}" width="{40*s}" height="{12*s}" fill="{WS}"/><rect x="{kx-6*s}" y="{ky-20*s}" width="{12*s}" height="{40*s}" fill="{WS}"/>'
# Hände (gleiche Rechnung wie hero.balken: Länge 132 + 4)
hrx = ax + (30 - hero.math.sin(hero.math.radians(arm_r)) * 136) * s
hry = BODEN + (-290 + hero.math.cos(hero.math.radians(arm_r)) * 136) * s
hlx = ax + (-30 - hero.math.sin(hero.math.radians(arm_l)) * 136) * s
hly = BODEN + (-290 + hero.math.cos(hero.math.radians(arm_l)) * 136) * s
# Stethoskop: Schlauch vom Bruststück in einem Bogen zum Hals, Ohrbügel als kleiner Bogen am Kopf
brust_x, brust_y = hrx + 14, hry
t += fuge_linie(f'M{brust_x-6} {brust_y+14} C {brust_x-30} {brust_y+120}, {ax+80} {brust_y+130}, {ax+30*s} {BODEN-300*s}')
t += f'<circle cx="{brust_x}" cy="{brust_y}" r="22" fill="{SCH}" stroke="{WS}" stroke-width="8" paint-order="stroke"/><circle cx="{brust_x}" cy="{brust_y}" r="8" fill="{WS}"/>'
t += f'<circle cx="{hrx}" cy="{hry}" r="{11*s}" fill="{SCH}"/>'
# Klemmbrett mit drei blauen Häkchen
cw, ch = 96, 128
cx0, cy0 = hlx - cw + 18, hly - 40
klemm = f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="8" fill="{WS}" stroke="{SCH}" stroke-width="4"/>'
klemm += f'<rect x="{cx0+cw/2-22}" y="{cy0-10}" width="44" height="18" rx="5" fill="{SCH}"/>'
for i in range(3):
    zy = cy0 + 34 + i * 30
    klemm += (f'<path d="M{cx0+14} {zy} l7 8 l13 -16" fill="none" stroke="{BL}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<rect x="{cx0+44}" y="{zy-4}" width="{36-i*6}" height="8" rx="4" fill="{GR}"/>')
t += klemm + f'<circle cx="{hlx}" cy="{hly}" r="{11*s}" fill="{SCH}" stroke="{WS}" stroke-width="6" paint-order="stroke"/>'

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {B} {H}" width="{B}" height="{H}" role="img"><title>{TITEL}</title>'
       f'{t}</svg>')

if __name__ == '__main__':
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(svg, encoding='utf-8')
    print('geschrieben:', ZIEL.relative_to(HIER.parent.parent))
