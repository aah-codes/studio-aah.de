# Erzeugt die animierte Grafik „Corporate Identity“ (Brand-Seite) als SVG in Schwarz-Weiß:
# vier Bereiche mit Icons, Informationsfluss als wandernde Punkte (Culture, Behaviour, Communication → Kern → Design → Image → zurück).
# Zwei Fassungen: quer (Desktop) und hoch (Handy). Aufruf: python3 werkzeuge/grafiken/ci-animation.py
import math, pathlib

ZIEL = pathlib.Path(__file__).with_name('corporate-identity.html')
R, r = 280, 112          # Außen- und Kernradius des Rads

# Strich-Icons (24er-Raster), werden skaliert eingesetzt
ICONS = {
    'culture': '<circle cx="12" cy="12" r="10" class="ci-l"/><circle cx="12" cy="12" r="6.5" class="ci-l"/><circle cx="12" cy="12" r="3" class="ci-a"/>',          # Werte im Kern
    'behaviour': '<circle cx="5" cy="12" r="3.5" class="ci-l"/><circle cx="19" cy="12" r="3.5" class="ci-a"/><path d="M9 12h6" class="ci-p"/>',                  # Beziehung
    'communication': '<path d="M3 5h18v11H10l-5 4v-4H3z" class="ci-l"/><path d="M7 9.5h10" class="ci-a"/><path d="M7 12.5h6" class="ci-l"/>',                  # Sprechblase
    'design': '<path d="M1 20l5-9 5 9z" class="ci-a"/><rect x="12.5" y="11" width="9" height="9" rx="1" class="ci-l"/><circle cx="12" cy="5" r="3.5" class="ci-l"/>',  # Formen
    'image': '<path d="M2 12s4-6.5 10-6.5S22 12 22 12s-4 6.5-10 6.5S2 12 2 12z" class="ci-l"/><circle cx="12" cy="12" r="3" class="ci-a"/>',                     # Blick von außen
}


def icon(name, x, y, gr, farbe):
    s = gr / 24
    return f'<g transform="translate({x - gr / 2:.1f} {y - gr / 2:.1f}) scale({s:.3f})" class="ci-icon">{ICONS[name]}</g>'


def punkt(cx, cy, a, rad):
    return cx + rad * math.cos(math.radians(a)), cy + rad * math.sin(math.radians(a))


def sektor(cx, cy, a1, a2):
    o1, o2, i2, i1 = punkt(cx, cy, a1, R), punkt(cx, cy, a2, R), punkt(cx, cy, a2, r), punkt(cx, cy, a1, r)
    return (f'M{o1[0]:.1f} {o1[1]:.1f}A{R} {R} 0 0 1 {o2[0]:.1f} {o2[1]:.1f}L{i2[0]:.1f} {i2[1]:.1f}'
            f'A{r} {r} 0 0 0 {i1[0]:.1f} {i1[1]:.1f}Z')


BEREICHE = [  # Winkel-Mitte, Name, Unterzeilen, schwarz?
    (-90, 'behaviour', 'Behaviour', ['Service, Verhalten,', 'Beziehungen'], False),
    (0, 'design', 'Design', ['Gestaltung, Logo,', 'Farben, Bildwelt,', 'Typografie'], True),
    (90, 'communication', 'Communication', ['Kanäle, Stimme,', 'Tonalität intern', 'und extern'], False),
    (180, 'culture', 'Culture', ['Leitbild, Werte,', 'Philosophie'], True),
]


def fluss(pfad, dauer, anzahl, versatz=0, gr=4.5, farbe='#0e1011'):
    # Punkte wandern entlang eines Pfads (SMIL); mehrere zeitversetzt ergeben einen stetigen Strom
    return ''.join(f'<circle r="{gr}" fill="{farbe}" opacity="0" class="ci-fluss"><animateMotion dur="{dauer}s" begin="{versatz + i * dauer / anzahl:.2f}s" '
                   f'repeatCount="indefinite" path="{pfad}" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/>'
                   f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="{dauer}s" begin="{versatz + i * dauer / anzahl:.2f}s" repeatCount="indefinite"/></circle>'
                   for i in range(anzahl))


def rad(cx, cy, g=1.0):
    # g: Schriftfaktor (Handy-Fassung größer, damit die Schrift lesbar bleibt)
    teile = []
    for mitte, key, name, unter, schwarz in BEREICHE:
        vorne, hinten = ('#fff', '#0e1011') if schwarz else ('#0e1011', '#fff')
        farbklasse = 'ci-schwarz-t'
        a1, a2 = punkt(cx, cy, mitte - 45, r), punkt(cx, cy, mitte - 45, R)
        teile.append(f'<path d="M{a1[0]:.1f} {a1[1]:.1f}L{a2[0]:.1f} {a2[1]:.1f}" class="ci-p"/>')
        # Block je Bereich: Icon, CORPORATE, Name, Unterzeilen – untereinander, Mitte bei Radius 208
        bx, by = punkt(cx, cy, mitte, 196 if mitte == 90 else (202 if g > 1 and mitte == -90 else 208))
        hoehe = (34 + 10 + 16 + 26 + len(unter) * 19) * g
        y = by - hoehe / 2
        teile.append(icon(key, bx, y + 17 * g, 34 * g, vorne))
        t = [f'<tspan x="{bx:.1f}" y="{y + (34 + 22) * g:.1f}" class="ci-klein" font-size="{12 * g:.0f}">CORPORATE</tspan>',
             f'<tspan x="{bx:.1f}" y="{y + (34 + 46) * g:.1f}" class="ci-t" font-size="{24 * g:.0f}">{name}</tspan>']
        t += [f'<tspan x="{bx:.1f}" y="{y + (34 + 68 + i * 19) * g:.1f}" class="ci-s" font-size="{14 * g:.0f}">{z}</tspan>' for i, z in enumerate(unter)]
        teile.append(f'<text text-anchor="middle" class="{farbklasse}">{"".join(t)}</text>')
    teile.insert(0, f'<circle cx="{cx}" cy="{cy}" r="{R}" class="ci-l"/>')
    # Kern
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 8}" fill="#fff" class="ci-a"/>')
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="ci-l"/>')
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 8}" fill="none" stroke="#0e1011" stroke-width="2" class="ci-puls">'
                 f'<animate attributeName="r" values="{r - 8};{r - 2};{r - 8}" dur="3s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".6;0;.6" dur="3s" repeatCount="indefinite"/></circle>')
    teile.append(f'<text text-anchor="middle" class="ci-kern-t ci-schwarz-t"><tspan x="{cx}" y="{cy - 4}">CORPORATE</tspan><tspan x="{cx}" y="{cy + 36}">IDENTITY</tspan></text>')
    # Fluss: Culture, Behaviour, Communication → Kern; Kern → Design
    for mitte, dauer in ((180, 2.4), (-90, 2.4), (90, 2.4)):
        a, b = punkt(cx, cy, mitte, 140 if g == 1 else 128), punkt(cx, cy, mitte, r - 6)
        farbe = '#0e1011'
        teile.append(fluss(f'M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}', dauer, 3, versatz=0.3 * (mitte % 7), farbe=farbe))
    a, b = punkt(cx, cy, 0, r - 6), punkt(cx, cy, 0, 140 if g == 1 else 128)
    teile.append(fluss(f'M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}', 2.4, 3, versatz=1.2))
    return ''.join(teile)


def image(cx, cy, gr):
    return (f'<circle cx="{cx}" cy="{cy}" r="{gr}" class="ci-l"/><circle cx="{cx}" cy="{cy}" r="{gr - 14}" class="ci-p"/>'
            + icon('image', cx, cy - 44, 44, '#0e1011')
            + f'<text text-anchor="middle" class="ci-kern-t ci-schwarz-t"><tspan x="{cx}" y="{cy + 14}">CORPORATE</tspan><tspan x="{cx}" y="{cy + 54}">IMAGE</tspan></text>')


def quer():
    cx, cy, ix, iy, ig = 300, 330, 870, 330, 120
    hin = f'M{cx + R + 6} {cy}C{cx + R + 90} {cy} {ix - ig - 90} {iy} {ix - ig - 6} {iy}'
    zurueck = f'M{ix} {iy - ig - 6}C{ix} {iy - ig - 150} {cx + 60} {cy - R - 70} {cx} {cy - R - 6}'
    return (f'<svg class="ci-anim ci-quer" viewBox="0 0 1000 660" aria-hidden="true">'
            f'<path d="{hin}" class="ci-pfad" marker-end="url(#ci-spitze-q)"/>'
            f'<path d="{zurueck}" class="ci-p" marker-end="url(#ci-spitze-q)"/>'
            f'<defs><marker id="ci-spitze-q" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5 0 10z" fill="#0e1011"/></marker></defs>'
            + rad(cx, cy) + image(ix, iy, ig)
            + fluss(hin, 2.2, 3, versatz=0.6) + fluss(zurueck, 4, 3, versatz=1.5, gr=4)
            + f'<text x="{cx + R + 16}" y="{cy - 16}" text-anchor="start" class="ci-pfeil-t" font-size="13">wirkt nach außen</text>'
            + f'<text x="{ix + 10}" y="{iy - ig - 60}" text-anchor="start" class="ci-pfeil-t" font-size="13">Rückmeldung</text>'
            + '</svg>')


def hoch():
    cx, cy, ix, iy, ig = 300, 300, 300, 860, 130
    hin = f'M{cx} {cy + R + 6}C{cx} {cy + R + 70} {ix} {iy - ig - 70} {ix} {iy - ig - 6}'
    zurueck = f'M{ix - ig - 6} {iy}C{ix - ig - 140} {iy} {cx - R - 40} {cy + 160} {cx - R - 6} {cy + 40}'
    return (f'<svg class="ci-anim ci-hoch" viewBox="0 0 600 1010" aria-hidden="true">'
            f'<defs><marker id="ci-spitze-h" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5 0 10z" fill="#0e1011"/></marker></defs>'
            f'<path d="{hin}" class="ci-pfad" marker-end="url(#ci-spitze-h)"/>'
            f'<path d="{zurueck}" class="ci-p" marker-end="url(#ci-spitze-h)"/>'
            + rad(cx, cy, 1.12) + image(ix, iy, ig)
            + fluss(hin, 2, 3, versatz=0.6) + fluss(zurueck, 3.5, 3, versatz=1.5, gr=4)
            + f'<text x="{cx + 16}" y="{cy + R + 58}" text-anchor="start" class="ci-pfeil-t" font-size="17">wirkt nach außen</text>'
            + f'<text x="{cx - R}" y="{iy + 70}" text-anchor="start" class="ci-pfeil-t" font-size="17">Rückmeldung</text>'
            + '</svg>')


html = f'''  <figure class="ci-grafik" id="corporate-identity" role="img" aria-label="Corporate Identity: Corporate Culture (Leitbild, Werte, Philosophie), Corporate Communication (Kanäle, Stimme, Tonalität intern und extern) und Corporate Behaviour (Service, Verhalten, Beziehungen) fließen in die Corporate Identity. Daraus entsteht das Corporate Design (Gestaltung, Logo, Farben, Bildwelt, Typografie). Es wirkt nach außen auf das Corporate Image, und das Image wirkt als Rückmeldung zurück.">
    <figcaption class="ci-titel"><span class="ci-titel-gross">Das Corporate Design baut auf Culture, Communication und Behaviour auf.</span><span class="ci-unter">Zusammen ergeben sie die Corporate Identity, die in Wechselwirkung mit dem Corporate Image steht.</span></figcaption>
    {quer()}
    {hoch()}
  </figure>'''
ZIEL.write_text(html, encoding='utf-8')
print('geschrieben:', ZIEL.name, len(html), 'Zeichen')
