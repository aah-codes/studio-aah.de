# Erzeugt die Infografik „Corporate Identity“ als kurzen Erklärfilm (Brand-Seite), am Ende als Netz statt Rad:
# Die Bereiche erscheinen nacheinander, jeder mit einer kleinen gezeichneten Animation ohne Worte;
# danach entsteht der Kern, das Design wirkt nach außen auf das Image, die Rückmeldung fließt zurück.
# Schwarz-Weiß im Linienstil. Der Film startet, wenn die Grafik ins Bild kommt (js/menue.js), und lässt sich wiederholen.
# Zwei Fassungen: quer (Desktop) und hoch (Handy). Aufruf: python3 werkzeuge/grafiken/ci-film.py
import math, pathlib

ZIEL = pathlib.Path(__file__).with_name('corporate-identity.html')
R, r = 280, 112


def p(cx, cy, a, rad):
    return cx + rad * math.cos(math.radians(a)), cy + rad * math.sin(math.radians(a))


def z(d, art='ein'):
    # Element im Film: Animationsart und Startzeit (Sekunden)
    return f'class="z z-{art}" style="--d:{d}s"'


# Kleine Zeichnungen je Bereich (Mitte 0,0; etwa 64 × 56), mit Startzeit t0
def zeichnung(key, t0):
    # Bauhaus-Grundformen, gefüllt (Anna 11.10.2026): Kreis, Halbkreis, Quadrat, Dreieck in Schwarz, Grau, Blau – kein Herz
    if key == 'culture':   # Werte wachsen von innen, oben die Fahne als Leitbild
        return (f'<g {z(t0)}><circle cy="6" r="21" class="ci-grau"/></g>'
                f'<g {z(t0 + .25)}><circle cy="6" r="12" class="ci-f"/></g>'
                f'<g {z(t0 + .5)}><circle cy="6" r="4" class="ci-weiss"/></g>'
                f'<g {z(t0 + .8, "hoch")}><rect x="-1.5" y="-28" width="3" height="20" class="ci-f"/><path d="M1.5 -28h15l-15 11z" class="ci-blau"/></g>')
    if key == 'communication':   # Sprechblasen im Wechsel
        return (f'<g {z(t0, "pop")}><rect x="-32" y="-22" width="30" height="18" class="ci-grau"/><path d="M-27 -4v7l7-7z" class="ci-grau"/></g>'
                f'<g {z(t0 + .3)}><rect x="-27" y="-17" width="18" height="3" class="ci-weiss"/><rect x="-27" y="-11" width="10" height="3" class="ci-blau"/></g>'
                f'<g {z(t0 + .6, "pop")}><rect x="2" y="0" width="30" height="18" class="ci-f"/><path d="M27 18v7l-7-7z" class="ci-f"/></g>'
                f'<g {z(t0 + .9)}><rect x="7" y="5" width="18" height="3" class="ci-weiss"/><rect x="7" y="11" width="11" height="3" class="ci-weiss"/></g>')
    if key == 'behaviour':   # zwei Menschen kommen zusammen, Verbindung entsteht
        figur = lambda x, k: f'<circle cx="{x}" cy="-8" r="6.5" class="{k}"/><path d="M{x - 10} 18a10 10 0 0 1 20 0z" class="{k}"/>'
        return (f'<g {z(t0, "links")}>{figur(-20, "ci-grau")}</g><g {z(t0, "rechts")}>{figur(20, "ci-f")}</g>'
                f'<g {z(t0 + .7)}><path d="M-10 10h20" class="ci-p"/></g>'
                f'<g {z(t0 + 1, "pop")}><circle cy="10" r="4.5" class="ci-blau"/></g>')
    if key == 'design':   # Formen fallen an ihren Platz, darunter entsteht eine Linie
        return (f'<g {z(t0, "fallen")}><path d="M-30 14l10-18 10 18z" class="ci-f"/></g>'
                f'<g {z(t0 + .2, "fallen")}><rect x="-7" y="-4" width="14" height="18" class="ci-grau"/></g>'
                f'<g {z(t0 + .4, "fallen")}><circle cx="22" cy="5" r="9" class="ci-blau"/></g>'
                f'<g {z(t0 + .7)}><rect x="-32" y="20" width="64" height="3" class="ci-f"/></g>')
    if key == 'image':   # das Auge öffnet sich
        return (f'<g {z(t0, "blick")}><path d="M-22 0s9-13 22-13S22 0 22 0 13 13 0 13-22 0-22 0z" class="ci-grau"/></g>'
                f'<g {z(t0 + .25, "pop")}><circle r="8.5" class="ci-blau"/></g>'
                f'<g {z(t0 + .45, "pop")}><circle r="3.5" class="ci-f"/></g>')
    return ''


# Knoten: Schlüssel, Name, Unterzeilen, Startzeit, Lage des Texts (unten, links, rechts)
KNOTEN = {
    'culture': ('Culture', ['Leitbild, Werte,', 'Philosophie'], 0.6),
    'communication': ('Communication', ['Kanäle, Stimme,', 'Tonalität intern', 'und extern'], 2.4),
    'behaviour': ('Behaviour', ['Service, Verhalten,', 'Beziehungen'], 4.2),
    'design': ('Design', ['Gestaltung, Logo,', 'Farben, Bildwelt,', 'Typografie'], 6.0),
}
KERN, NETZ, BILD, FLUSS = 7.9, 8.8, 10.4, 11.4
# Wer mit wem Informationen austauscht (in beide Richtungen)
KANTEN = [('culture', 'behaviour'), ('culture', 'communication'), ('culture', 'kern'), ('behaviour', 'kern'),
          ('communication', 'kern'), ('kern', 'design'), ('design', 'image'), ('behaviour', 'image'), ('communication', 'image')]
LAGEN = {
    'quer': dict(vb='0 0 1000 700', g=1.0, kr=46, fs=13,
                 pos={'culture': (130, 340), 'behaviour': (330, 120), 'communication': (330, 560), 'kern': (520, 340),
                      'design': (720, 340), 'image': (895, 340)},
                 text={'culture': 'unten', 'behaviour': 'links', 'communication': 'links', 'design': 'unten'},
                 bogen={('behaviour', 'image'): (690, 70), ('communication', 'image'): (690, 610)}),
    'hoch': dict(vb='0 0 600 1120', g=1.15, kr=50, fs=17,
                 pos={'culture': (300, 90), 'behaviour': (120, 300), 'communication': (480, 300), 'kern': (300, 500),
                      'design': (300, 730), 'image': (300, 960)},
                 text={'culture': 'rechts', 'behaviour': 'unten', 'communication': 'unten', 'design': 'rechts'},
                 bogen={('behaviour', 'image'): (20, 820), ('communication', 'image'): (580, 820)}),
}
RADIUS = {'kern': 96, 'image': 82}


def fluss(pfad, dauer, anzahl, start, gr=4, klasse='ci-f'):
    # Punkte wandern entlang eines Pfads (SMIL, Zeit ab Filmstart – js/menue.js setzt die Uhr beim Start auf 0)
    return ''.join(f'<circle r="{gr}" class="{klasse}" opacity="0"><animateMotion dur="{dauer}s" begin="{start + i * dauer / anzahl:.2f}s" repeatCount="indefinite" path="{pfad}"/>'
                   f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.88;1" dur="{dauer}s" begin="{start + i * dauer / anzahl:.2f}s" repeatCount="indefinite"/></circle>'
                   for i in range(anzahl))


def rand(a, b, ra, rb):
    # Linie zwischen zwei Kreisen, Endpunkte am Rand
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return (x1 + ux * (ra + 6), y1 + uy * (ra + 6)), (x2 - ux * (rb + 6), y2 - uy * (rb + 6))


def bild(art):
    L = LAGEN[art]; pos, g, kr = L['pos'], L['g'], L['kr']
    rad_von = lambda k: RADIUS.get(k, kr)
    teile, punkte = [], []
    # Verbindungen: erst zeichnen, dann Austausch in beide Richtungen
    for i, (a, b) in enumerate(KANTEN):
        pa, pb = pos[a], pos[b]
        if (a, b) in L['bogen']:
            kx, ky = L['bogen'][(a, b)]
            s, e = rand(pa, (kx, ky), rad_von(a), 0)[0], rand((kx, ky), pb, 0, rad_von(b))[1]
            hin, zur = f'M{s[0]:.0f} {s[1]:.0f}Q{kx} {ky} {e[0]:.0f} {e[1]:.0f}', f'M{e[0]:.0f} {e[1]:.0f}Q{kx} {ky} {s[0]:.0f} {s[1]:.0f}'
        else:
            s, e = rand(pa, pb, rad_von(a), rad_von(b))
            hin, zur = f'M{s[0]:.0f} {s[1]:.0f}L{e[0]:.0f} {e[1]:.0f}', f'M{e[0]:.0f} {e[1]:.0f}L{s[0]:.0f} {s[1]:.0f}'
        d = (BILD + .6) if 'image' in (a, b) else (NETZ + i * .12)
        teile.append(f'<g {z(d)} data-kante><path d="{hin}" class="ci-p"/></g>')
        lang = 2.6 if 'image' not in (a, b) else 3.2
        # je Linie nur ein Punkt pro Richtung, der Rückweg in Blau (Anna 11.10.2026: zu viele Punkte)
        punkte.append(fluss(hin, lang, 1, FLUSS + i * .21) + fluss(zur, lang, 1, FLUSS + 1.6 + i * .17, gr=3, klasse='ci-blau'))
    # Knoten der vier Bereiche
    for key, (name, unter, t0) in KNOTEN.items():
        x, y = pos[key]
        teile.append(f'<circle cx="{x}" cy="{y}" r="{kr}" fill="#fff"/>')
        teile.append(f'<g transform="translate({x} {y}) scale({1.2 * kr / 46:.2f})"><g class="ci-schweben" style="--s:{t0 * .7:.1f}s">{zeichnung(key, t0 + .2)}</g></g>')
        lage = L['text'][key]
        n = 2 + len(unter)
        if lage == 'unten': tx, ty, anker = x, y + kr + 22 * g, 'middle'
        elif lage == 'links': tx, ty, anker = x - kr - 16, y - (n * 20 * g) / 2 + 12 * g, 'end'
        else: tx, ty, anker = x + kr + 16, y - (n * 20 * g) / 2 + 12 * g, 'start'
        zeilen = [f'<tspan x="{tx:.0f}" y="{ty:.0f}" class="ci-klein" font-size="{12 * g:.0f}">CORPORATE</tspan>',
                  f'<tspan x="{tx:.0f}" y="{ty + 25 * g:.0f}" class="ci-t" font-size="{23 * g:.0f}">{name}</tspan>']
        schritt = 16 if g == 1 else 22  # Unterzeilen so groß wie die Dachzeile (12 px am Desktop), mehr Abstand zur Überschrift
        zeilen += [f'<tspan x="{tx:.0f}" y="{ty + 54 * g + i * schritt:.0f}" class="ci-s">{s}</tspan>' for i, s in enumerate(unter)]
        teile.append(f'<text text-anchor="{anker}" class="ci-schwarz-t z z-ein" style="--d:{t0 + 1}s">{"".join(zeilen)}</text>')
    # Kern: entsteht, wenn alle vier da sind
    x, y = pos['kern']
    teile.append(f'<g {z(KERN, "pop")}><circle cx="{x}" cy="{y}" r="{RADIUS["kern"]}" fill="#fff" class="ci-a"/><circle cx="{x}" cy="{y}" r="{RADIUS["kern"] + 8}" class="ci-l"/></g>')
    teile.append(f'<text text-anchor="middle" class="ci-kern-t ci-schwarz-t z z-ein" style="--d:{KERN + .3}s"><tspan x="{x}" y="{y - 4}">CORPORATE</tspan><tspan x="{x}" y="{y + 34}">IDENTITY</tspan></text>')
    teile.append(f'<circle cx="{x}" cy="{y}" r="{RADIUS["kern"]}" fill="none" class="ci-a" opacity="0"><animate attributeName="r" values="{RADIUS["kern"]};{RADIUS["kern"] + 7};{RADIUS["kern"]}" dur="3s" begin="{FLUSS}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".5;0;.5" dur="3s" begin="{FLUSS}s" repeatCount="indefinite"/></circle>')
    # Image: kommt zuletzt, das Auge öffnet sich
    x, y = pos['image']; gr = RADIUS['image']
    teile.append(f'<g {z(BILD, "pop")}><circle cx="{x}" cy="{y}" r="{gr}" fill="#fff" class="ci-l"/><circle cx="{x}" cy="{y}" r="{gr - 12}" class="ci-p"/></g>')
    teile.append(f'<g transform="translate({x} {y - 36})">{zeichnung("image", BILD + .4)}</g>')
    teile.append(f'<text text-anchor="middle" class="ci-kern-t ci-image-t ci-schwarz-t z z-ein" style="--d:{BILD + .7}s"><tspan x="{x}" y="{y + 14}">CORPORATE</tspan><tspan x="{x}" y="{y + 46}">IMAGE</tspan></text>')
    # Linien und Punkte liegen unter den Knoten
    return (f'<svg class="ci-anim ci-{art}" viewBox="{L["vb"]}" aria-hidden="true">'
            + ''.join(t for t in teile if 'data-kante' in t) + ''.join(punkte)
            + ''.join(t for t in teile if 'data-kante' not in t) + '</svg>')


html = f'''  <figure class="ci-grafik ci-film" id="corporate-identity" aria-describedby="ci-beschreibung">
    <figcaption class="ci-titel"><span class="ci-titel-gross">Das Corporate Design baut auf Culture, Communication und Behaviour auf.</span><span class="ci-unter">Zusammen ergeben sie die Corporate Identity, die in Wechselwirkung mit dem Corporate Image steht.</span></figcaption>
    <p class="unsichtbar" id="ci-beschreibung">Erklärfilm Corporate Identity: Nacheinander erscheinen Corporate Culture (Leitbild, Werte, Philosophie), Corporate Communication (Kanäle, Stimme, Tonalität intern und extern), Corporate Behaviour (Service, Verhalten, Beziehungen) und Corporate Design (Gestaltung, Logo, Farben, Bildwelt, Typografie). Zusammen bilden sie die Corporate Identity. Zum Schluss steht das ganze System: Alle Bereiche tauschen Informationen untereinander und mit dem Corporate Image aus.</p>
    {bild('quer')}
    {bild('hoch')}
    <p class="ci-nochmal"><button type="button" class="textlink ci-pause-knopf" hidden>Anhalten <span aria-hidden="true">❚❚</span></button><button type="button" class="textlink ci-nochmal-knopf">Noch einmal ansehen <span aria-hidden="true">↻</span></button></p>
  </figure>'''
ZIEL.write_text(html, encoding='utf-8')
print('geschrieben:', ZIEL.name, len(html), 'Zeichen')
