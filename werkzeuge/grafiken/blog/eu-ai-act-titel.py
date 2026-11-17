# Titel- und Vorschaubild Blog „EU AI Act für kleine Unternehmen“ (17.11.2026)
# Anna 17.11.2026: „blaues Bild mit Europakarte, den EU-Ländern, Sternen vorne drauf und in der Mitte steht AI“.
# Blogbild ohne Studio-Branding (Bildregel Blog): EU-Blau, EU-Länder heller, Sternenkranz in EU-Gelb, „AI“ in Weiß.
# Kartendaten: Natural Earth 1:50m Admin 0 Countries (gemeinfrei), liegen nicht im Repository:
#   curl -L -o ne50.geojson https://cdn.jsdelivr.net/gh/nvkelso/natural-earth-vector@v5.1.2/geojson/ne_50m_admin_0_countries.geojson
# Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/blog/eu-ai-act-titel.py PFAD/ne50.geojson
#   → website/bilder/blog-eu-ai-act.webp (1200 × 800) und website/bilder/blog-eu-ai-act-og.jpg (1200 × 630)
import json, math, pathlib, subprocess, sys, tempfile

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent.parent.parent
quelle = (HIER / 'website-2027-titel.py').read_text(encoding='utf-8')
ns = {'__file__': str(HIER / 'website-2027-titel.py')}
exec(quelle[:quelle.index("if __name__ == '__main__':")], ns)
seite, aufnahme, als_webp = ns['seite'], ns['aufnahme'], ns['als_webp']

EU = set('AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX MLT NLD POL PRT ROU SVK SVN ESP SWE'.split())
GRUND, LAND, EULAND, LINIE, GELB = '#0a2a78', '#173c95', '#3d6fe0', '#0a2a78', '#ffcc00'


def karte(geo, b, h, lon0=13.0, lat0=53.5, k=24.0):
    cosb = math.cos(math.radians(lat0))
    def p(lon, lat):
        return (b / 2 + (lon - lon0) * cosb * k, h / 2 + (lat0 - lat) * k)
    teile = []
    for f in geo['features']:
        a3 = f['properties'].get('ADM0_A3')
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        d = []
        for poly in polys:
            for ring in poly:
                pts = [p(x, y) for x, y in ring]
                if all(x < -50 or x > b + 50 or y < -50 or y > h + 50 for x, y in pts):
                    continue
                d.append('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z')
        if d:
            farbe = EULAND if a3 in EU else LAND
            teile.append(f'<path d="{"".join(d)}" fill="{farbe}" stroke="{LINIE}" stroke-width="1.2" stroke-linejoin="round"/>')
    return ''.join(teile)


def stern(cx, cy, r):
    pts = []
    for i in range(10):
        w = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.382
        pts.append(f'{cx + rr * math.cos(w):.1f},{cy + rr * math.sin(w):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{GELB}"/>'


def bild(geo, b, h, k):
    kranz = ''.join(stern(b / 2 + 0.29 * h * math.cos(math.radians(i * 30)), h / 2 + 0.29 * h * math.sin(math.radians(i * 30)), 0.034 * h) for i in range(12))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {b} {h}" width="{b}" height="{h}">'
            f'<defs><radialGradient id="licht" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="{GRUND}" stop-opacity="0"/><stop offset="1" stop-color="#051a52" stop-opacity=".85"/></radialGradient></defs>'
            f'<rect width="{b}" height="{h}" fill="{GRUND}"/>{karte(geo, b, h, k=k)}'
            f'<rect width="{b}" height="{h}" fill="url(#licht)"/>'
            f'<circle cx="{b / 2}" cy="{h / 2}" r="{0.2 * h:.0f}" fill="#051a52" opacity=".55"/>'
            f'{kranz}'
            f'<text x="{b / 2}" y="{h / 2 + 0.085 * h:.0f}" text-anchor="middle" font-family="Manrope" font-weight="800" font-size="{0.24 * h:.0f}" letter-spacing="4" fill="#ffffff">AI</text></svg>')


if __name__ == '__main__':
    geo = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
    bilder = REPO / 'website' / 'bilder'
    with tempfile.TemporaryDirectory() as tmp:
        png = pathlib.Path(tmp) / 'titel.png'
        aufnahme(seite(bild(geo, 1200, 800, 24.0)), 1200, 800, png)
        als_webp(png, bilder / 'blog-eu-ai-act.webp', 0.86)
        png_og = pathlib.Path(tmp) / 'og.png'
        aufnahme(seite(bild(geo, 1200, 630, 19.0)), 1200, 630, png_og)
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '86', str(png_og), '--out', str(bilder / 'blog-eu-ai-act-og.jpg')],
                       check=True, capture_output=True)
    for n in ('blog-eu-ai-act.webp', 'blog-eu-ai-act-og.jpg'):
        print(n, (bilder / n).stat().st_size // 1024, 'KB')
