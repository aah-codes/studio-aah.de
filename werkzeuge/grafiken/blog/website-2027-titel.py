# Titel- und Vorschaubild Blog „Was sollte eine Website 2027 können?“ (Reihe Website-Fragen, Teil 2; 19.10.2026)
# Golden Circle aus drei Kreisen (innen Schwarz: Warum, Creme: Wie, Weiß: Was), daneben die Bauhaus-Figur, die auf den Kern zeigt.
# Figur wie in geld-und-zeit-titel.py (Arme am Rumpf, abgespreizter Arm, Beine mit Eckenradius 4, weiße Fugen statt Blau an Schwarz).
# Rendert mit dem installierten Google Chrome (ohne Fenster), Schriften lokal aus website/schriften:
#   website/bilder/blog-website-2027.webp (1200 × 800, Titelbild) und website/bilder/blog-website-2027-og.jpg (1200 × 630, Vorschau für soziale Netzwerke)
# Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/blog/website-2027-titel.py
import base64, pathlib, re, subprocess, tempfile

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent.parent.parent
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# Nur die Figur übernehmen, ohne das Skript auszuführen (es schreibt sonst sein eigenes SVG)
quelle = (HIER / 'geld-und-zeit-titel.py').read_text(encoding='utf-8')
ns = {}
exec(quelle[:quelle.index('linie = ')], ns)
SCH, BL, WS, GR, MG, FUGE, figur = ns['SCH'], ns['BL'], ns['WS'], ns['GR'], ns['MG'], ns['FUGE'], ns['figur']
CREME = '#eeece7'


def kreis(cx, cy, k):
    """Golden Circle, k = Maßstab gegenüber dem Original (Außenradius 250)."""
    t = [f'<g transform="translate({cx} {cy}) scale({k})">',
         f'<circle r="250" fill="{WS}" stroke="{SCH}" stroke-width="{2 / k:.2f}"/>',
         f'<circle r="165" fill="{CREME}" stroke="{SCH}" stroke-width="{2 / k:.2f}"/>',
         f'<circle r="80" fill="{SCH}"/>']
    for y, wort, gr, farbe in ((-198, 'WAS', 34, SCH), (-112, 'WIE', 34, SCH), (13, 'WARUM', 38, WS)):
        t.append(f'<text x="0" y="{y}" font-family="Anton" font-size="{gr}" letter-spacing="1.4" text-anchor="middle" fill="{farbe}">{wort}</text>')
    t.append('</g>')
    return ''.join(t)


def szene(cx, cy, k, fx, fy, fk, boden):
    """Kreis plus Figur, die mit dem linken Arm auf den Kreis zeigt; gestrichelte Linie von der Hand zum Kern."""
    s = [kreis(cx, cy, k)]
    s.append(f'<line x1="{boden[0]}" y1="{fy}" x2="{boden[1]}" y2="{fy}" stroke="{SCH}" stroke-width="2"/>')
    s.append(f'<g transform="translate({fx} {fy}) scale({fk})">' + figur(100, ns['ARM_UNTEN'], 14, -10, blick=-1) + '</g>')
    hx, hy = ns['ende'](-ns['SCHULTER_X'], ns['SCHULTER_Y'], 100, ns['ARM'])
    hx, hy = fx + hx * fk, fy + hy * fk
    s.append(f'<path d="M{hx - 16 * fk:.0f} {hy:.0f} L{cx + 84 * k:.0f} {cy:.0f}" fill="none" stroke="{BL}" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>')
    return ''.join(s)


def schriften():
    css = []
    for name, datei in (('Anton', 'anton-latin.woff2'), ('Manrope', 'manrope-latin.woff2'), ('JetBrains Mono', 'jetbrains-mono-latin.woff2')):
        b64 = base64.b64encode((REPO / 'website' / 'schriften' / datei).read_bytes()).decode()
        css.append(f'@font-face {{ font-family: "{name}"; src: url(data:font/woff2;base64,{b64}) format("woff2"); font-weight: 200 800; }}')
    return '\n'.join(css)


PUNKTE = f'<defs><pattern id="punkte" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1.3" fill="{GR}"/></pattern></defs>'

titel = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">{PUNKTE}'
         f'<rect width="1200" height="800" fill="{WS}"/><rect width="1200" height="800" fill="url(#punkte)"/>'
         + szene(450, 400, 1.2, 1010, 700, 1.0, (850, 1160)) +
         f'<text x="1160" y="740" font-family="JetBrains Mono" font-size="14" fill="{MG}" text-anchor="end" letter-spacing="2">GOLDEN CIRCLE · 2027</text></svg>')

og = f'''<div style="position:relative;width:1200px;height:630px;background:{WS};overflow:hidden">
<svg style="position:absolute;left:0;top:0" width="1200" height="630" viewBox="0 0 1200 630">{PUNKTE}<rect x="700" width="500" height="630" fill="url(#punkte)"/>
{szene(820, 280, 0.5, 1080, 600, 0.72, (980, 1170))}</svg>
<div style="position:absolute;left:64px;top:64px;width:600px;font-family:'JetBrains Mono';font-size:22px;letter-spacing:3px;color:#3a3d3f;display:flex;align-items:center;gap:14px">
<span style="width:18px;height:18px;border-radius:50%;background:{BL};display:inline-block"></span>RATGEBER · TEIL 2</div>
<h1 style="position:absolute;left:64px;top:112px;width:620px;margin:0;font-family:Anton;font-weight:400;font-size:74px;line-height:1.2;letter-spacing:1px;color:{SCH}">WAS SOLLTE EINE WEBSITE 2027 KÖNNEN?</h1>
<p style="position:absolute;left:64px;top:410px;width:600px;margin:0;font-family:Manrope;font-weight:500;font-size:26px;color:{SCH}">Markenidentität, Nutzen, Zukunft</p>
<p style="position:absolute;left:64px;top:540px;margin:0;font-family:Anton;font-size:30px;letter-spacing:1px;color:{SCH}">STUDIO AAH!</p>
</div>'''


def seite(inhalt):
    return f'<!doctype html><meta charset="utf-8"><style>{schriften()} html,body{{margin:0;background:#fff}} svg{{display:block}}</style>{inhalt}'


def aufnahme(html, b, h, ziel_png):
    with tempfile.TemporaryDirectory() as tmp:
        datei = pathlib.Path(tmp) / 'seite.html'; datei.write_text(html, encoding='utf-8')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        f'--window-size={b},{h}', '--virtual-time-budget=3000', f'--screenshot={ziel_png}', datei.as_uri()],
                       check=True, capture_output=True)


def als_webp(png, ziel, qualitaet=0.9):
    """PNG -> WebP über die Canvas-Funktion von Chrome (keine Zusatzprogramme nötig)."""
    b64 = base64.b64encode(pathlib.Path(png).read_bytes()).decode()
    html = (f'<!doctype html><body><img id="b" src="data:image/png;base64,{b64}"><pre id="aus"></pre><script>'
            f'const i=document.getElementById("b");const go=()=>{{const c=document.createElement("canvas");c.width=i.naturalWidth;c.height=i.naturalHeight;'
            f'c.getContext("2d").drawImage(i,0,0);document.getElementById("aus").textContent="WEBP:"+c.toDataURL("image/webp",{qualitaet})+":ENDE";i.remove();}};'
            f'i.complete?go():i.onload=go;</script>')
    with tempfile.TemporaryDirectory() as tmp:
        datei = pathlib.Path(tmp) / 'umwandeln.html'; datei.write_text(html, encoding='utf-8')
        aus = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=5000', '--dump-dom', datei.as_uri()],
                             check=True, capture_output=True, text=True).stdout
    daten = re.search(r'WEBP:data:image/webp;base64,([A-Za-z0-9+/=]+):ENDE', aus)
    if not daten: raise SystemExit('WebP-Umwandlung fehlgeschlagen')
    pathlib.Path(ziel).write_bytes(base64.b64decode(daten.group(1)))


if __name__ == '__main__':
    bilder = REPO / 'website' / 'bilder'
    (HIER / 'website-2027-titel.svg').write_text(titel + '\n', encoding='utf-8')
    with tempfile.TemporaryDirectory() as tmp:
        png = pathlib.Path(tmp) / 'titel.png'
        aufnahme(seite(titel), 1200, 800, png)
        als_webp(png, bilder / 'blog-website-2027.webp')
        png_og = pathlib.Path(tmp) / 'og.png'
        aufnahme(seite(og), 1200, 630, png_og)
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', str(png_og), '--out', str(bilder / 'blog-website-2027-og.jpg')],
                       check=True, capture_output=True)
    for n in ('blog-website-2027.webp', 'blog-website-2027-og.jpg'):
        print(n, (bilder / n).stat().st_size // 1024, 'KB')
