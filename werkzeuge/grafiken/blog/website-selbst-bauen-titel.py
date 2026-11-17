# Titel- und Vorschaubild Blog „Website selbst bauen mit KI“ (17.11.2026)
# Browserfenster, in dem eine Website aus Bauhaus-Grundformen entsteht (zwei Formen fliegen noch hinein), daneben die Bauhaus-Figur, die darauf zeigt, und „OHO!“.
# Figur und Rendern wie in website-2027-titel.py (Arme am Rumpf, Beine mit Eckenradius 4, weiße Fugen statt Blau an Schwarz).
#   website/bilder/blog-website-selbst-bauen.webp (1200 × 800) und website/bilder/blog-website-selbst-bauen-og.jpg (1200 × 630)
# Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/blog/website-selbst-bauen-titel.py
import pathlib, subprocess, tempfile

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent.parent.parent
quelle = (HIER / 'website-2027-titel.py').read_text(encoding='utf-8')
ns = {'__file__': str(HIER / 'website-2027-titel.py')}
exec(quelle[:quelle.index("if __name__ == '__main__':")], ns)
SCH, BL, WS, GR, MG, figur, seite, aufnahme, als_webp, PUNKTE = (ns[k] for k in ('SCH', 'BL', 'WS', 'GR', 'MG', 'figur', 'seite', 'aufnahme', 'als_webp', 'PUNKTE'))
CREME = '#eeece7'


def fenster(x, y, k):
    """Browserfenster mit einer Website aus Grundformen; zwei Formen schweben noch außerhalb (Website im Bau)."""
    w, h = 560, 420
    s = [f'<g transform="translate({x} {y}) scale({k})">',
         f'<rect width="{w}" height="{h}" rx="10" fill="{WS}" stroke="{SCH}" stroke-width="2.5"/>',
         f'<path d="M0 10 a10 10 0 0 1 10 -10 h{w - 20} a10 10 0 0 1 10 10 v34 h-{w} z" fill="{SCH}"/>']
    for i in range(3):
        s.append(f'<circle cx="{24 + i * 22}" cy="22" r="6" fill="{WS}"/>')
    s.append(f'<rect x="96" y="13" width="300" height="18" rx="9" fill="{WS}" opacity=".25"/>')
    # Kopfzeile der Website
    s.append(f'<rect x="28" y="70" width="90" height="16" fill="{SCH}"/>')
    for i in range(3):
        s.append(f'<rect x="{300 + i * 56}" y="74" width="40" height="8" fill="{MG}"/>')
    # Hero: große Überschrift als Balken, blauer Button, rechts Kreis und Halbkreis
    s.append(f'<rect x="28" y="120" width="250" height="26" fill="{SCH}"/>')
    s.append(f'<rect x="28" y="156" width="190" height="26" fill="{SCH}"/>')
    s.append(f'<rect x="28" y="200" width="210" height="8" fill="{MG}"/><rect x="28" y="216" width="170" height="8" fill="{MG}"/>')
    s.append(f'<rect x="28" y="242" width="120" height="34" rx="17" fill="{BL}"/>')
    s.append(f'<circle cx="420" cy="190" r="78" fill="{CREME}" stroke="{SCH}" stroke-width="2"/>')
    s.append(f'<path d="M352 268 a68 68 0 0 1 136 0 z" fill="{SCH}"/>')
    # drei Karten unten, die mittlere fehlt noch (gestrichelt)
    s.append(f'<rect x="28" y="310" width="150" height="80" fill="{CREME}" stroke="{SCH}" stroke-width="2"/>')
    s.append(f'<rect x="205" y="310" width="150" height="80" fill="none" stroke="{MG}" stroke-width="2" stroke-dasharray="6 6"/>')
    s.append(f'<rect x="382" y="310" width="150" height="80" fill="{CREME}" stroke="{SCH}" stroke-width="2"/>')
    s.append('</g>')
    return ''.join(s)


def baustelle(x, y, k):
    """Formen, die noch in die Website fliegen: blaues Quadrat (für die leere Karte) und schwarzes Dreieck, mit Punktlinie."""
    s = [f'<g transform="translate({x} {y}) scale({k})">']
    weg = 'M588 345 C530 365 430 368 362 352'
    s.append(f'<path d="{weg}" fill="none" stroke="{BL}" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>')
    s.append(f'<rect x="590" y="300" width="70" height="70" fill="{BL}" transform="rotate(14 625 335)"/>')
    s.append(f'<polygon points="640,140 700,240 580,240" fill="{SCH}" transform="rotate(-12 640 200)"/>')
    s.append('</g>')
    return ''.join(s)


def oho(x, y, gr):
    return f'<text x="{x}" y="{y}" font-family="Anton" font-size="{gr}" letter-spacing="2" fill="{SCH}">OHO!</text>'


titel = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">{PUNKTE}'
         f'<rect width="1200" height="800" fill="{WS}"/><rect width="1200" height="800" fill="url(#punkte)"/>'
         + fenster(90, 170, 1.05) + baustelle(90, 170, 1.05)
         + f'<line x1="860" y1="700" x2="1160" y2="700" stroke="{SCH}" stroke-width="2"/>'
         + f'<g transform="translate(1000 700) scale(1.0)">' + figur(100, ns['ns']['ARM_UNTEN'], 14, -10, blick=-1) + '</g>'
         + oho(905, 150, 120)
         + f'<text x="1160" y="740" font-family="JetBrains Mono" font-size="14" fill="{MG}" text-anchor="end" letter-spacing="2">VIBE-CODING · 2026</text></svg>')

og = f'''<div style="position:relative;width:1200px;height:630px;background:{WS};overflow:hidden">
<svg style="position:absolute;left:0;top:0" width="1200" height="630" viewBox="0 0 1200 630">{PUNKTE}<rect x="700" width="500" height="630" fill="url(#punkte)"/>
{fenster(730, 150, 0.62)}{baustelle(730, 150, 0.62)}{oho(960, 120, 76)}</svg>
<div style="position:absolute;left:64px;top:64px;width:600px;font-family:'JetBrains Mono';font-size:22px;letter-spacing:3px;color:#3a3d3f;display:flex;align-items:center;gap:14px">
<span style="width:18px;height:18px;border-radius:50%;background:{BL};display:inline-block"></span>ANLEITUNG</div>
<h1 style="position:absolute;left:64px;top:112px;width:620px;margin:0;font-family:Anton;font-weight:400;font-size:74px;line-height:1.2;letter-spacing:1px;color:{SCH}">WEBSITE SELBST BAUEN MIT KI</h1>
<p style="position:absolute;left:64px;top:410px;width:600px;margin:0;font-family:Manrope;font-weight:500;font-size:26px;color:{SCH}">Werkzeuge, Kosten, Recht, Livegang</p>
<p style="position:absolute;left:64px;top:540px;margin:0;font-family:Anton;font-size:30px;letter-spacing:1px;color:{SCH}">STUDIO AAH!</p>
</div>'''


if __name__ == '__main__':
    bilder = REPO / 'website' / 'bilder'
    (HIER / 'website-selbst-bauen-titel.svg').write_text(titel + '\n', encoding='utf-8')
    with tempfile.TemporaryDirectory() as tmp:
        png = pathlib.Path(tmp) / 'titel.png'
        aufnahme(seite(titel), 1200, 800, png)
        als_webp(png, bilder / 'blog-website-selbst-bauen.webp')
        png_og = pathlib.Path(tmp) / 'og.png'
        aufnahme(seite(og), 1200, 630, png_og)
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', str(png_og), '--out', str(bilder / 'blog-website-selbst-bauen-og.jpg')],
                       check=True, capture_output=True)
    for n in ('blog-website-selbst-bauen.webp', 'blog-website-selbst-bauen-og.jpg'):
        print(n, (bilder / n).stat().st_size // 1024, 'KB')
