# Erzeugt den Abschnitt „Warum Website“ (Leistungsseiten mit Website-Bezug) als animierte Grafik im Linienstil:
# Die Website in der Mitte, rundherum sechs Kanäle mit Icons; sie erscheinen nacheinander, danach fließen Punkte
# zwischen Website und Kanälen in beide Richtungen. Start beim Scrollen und Ruhe nach dem Aufbau über js/menue.js (.ci-film).
# Aufruf: python3 werkzeuge/grafiken/website-herz.py
import math, pathlib

ZIEL = pathlib.Path(__file__).with_name('website-herz.html')
C, RING, KERN, KNOTEN = 300, 214, 82, 44

ICONS = {
    'Werbung': '<path d="M3 10v4h3l8 4V6l-8 4z" class="ci-l"/><path d="M17 9a4 4 0 0 1 0 6" class="ci-a"/>',
    'Newsletter': '<rect x="3" y="6" width="18" height="13" rx="2" class="ci-l"/><path d="M3.5 7.5l8.5 6 8.5-6" class="ci-a"/>',
    'Blog': '<rect x="5" y="3" width="14" height="18" rx="2" class="ci-l"/><path d="M8 8h8" class="ci-a"/><path d="M8 12h8M8 16h5" class="ci-l"/>',
    'Events': '<rect x="3" y="5" width="18" height="16" rx="2" class="ci-l"/><path d="M3 10h18" class="ci-l"/><path d="M8 3v4M16 3v4" class="ci-a"/><circle cx="12" cy="15.5" r="1.8" class="ci-f"/>',
    'Kundenbindung': '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z" class="ci-a"/>',
    'Wachstum': '<path d="M4 20h16M7 20v-4M12 20v-7M17 20v-10" class="ci-l"/><path d="M5 12l5-5 4 3 6-6" class="ci-a"/>',
}
NAMEN = list(ICONS)


def z(d, art='ein'):
    return f'class="z z-{art}" style="--d:{d}s"'


def p(a, r):
    return C + r * math.cos(math.radians(a)), C + r * math.sin(math.radians(a))


def fluss(pfad, dauer, start, gr=3.6):
    return ''.join(f'<circle r="{gr}" class="ci-f" opacity="0"><animateMotion dur="{dauer}s" begin="{start + i * dauer / 2:.2f}s" repeatCount="indefinite" path="{pfad}"/>'
                   f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.88;1" dur="{dauer}s" begin="{start + i * dauer / 2:.2f}s" repeatCount="indefinite"/></circle>' for i in range(2))


kanten, punkte, knoten = [], [], []
for i, name in enumerate(NAMEN):
    a = -90 + i * 60
    x, y = p(a, RING)
    t0 = 1.0 + i * .55
    s, e = p(a, KERN + 6), p(a, RING - KNOTEN - 6)
    hin, zur = f'M{s[0]:.0f} {s[1]:.0f}L{e[0]:.0f} {e[1]:.0f}', f'M{e[0]:.0f} {e[1]:.0f}L{s[0]:.0f} {s[1]:.0f}'
    kanten.append(f'<g {z(t0 + .3)}><path d="{hin}" class="ci-p"/></g>')
    punkte.append(fluss(hin, 2.4, 5.2 + i * .2) + fluss(zur, 2.4, 6.4 + i * .17, 2.8))
    knoten.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{KNOTEN}" fill="#fff"/>'
                  f'<g transform="translate({x - 26:.0f} {y - 36:.0f}) scale(2.2)"><g class="ci-schweben" style="--s:{i * .6:.1f}s"><g {z(t0, "pop")}>{ICONS[name]}</g></g></g>'
                  f'<text x="{x:.0f}" y="{y + 32:.0f}" text-anchor="middle" class="herz-name z z-ein" style="--d:{t0 + .3}s">{name}</text>')

svg = (f'<svg class="ci-anim herz-svg" viewBox="0 0 600 600" aria-hidden="true">'
       f'<g {z(.2)}><circle cx="{C}" cy="{C}" r="{RING}" class="ci-p"/></g>'
       + ''.join(kanten) + ''.join(punkte)
       + f'<g {z(.1, "pop")}><circle cx="{C}" cy="{C}" r="{KERN}" class="herz-kern"/></g>'
       + f'<text x="{C}" y="{C + 12}" text-anchor="middle" class="herz-kern-t z z-ein" style="--d:.5s">WEBSITE</text>'
       + f'<circle cx="{C}" cy="{C}" r="{KERN}" fill="none" class="ci-a" opacity="0"><animate attributeName="r" values="{KERN};{KERN + 8};{KERN}" dur="3s" begin="5.2s" repeatCount="indefinite"/>'
       + f'<animate attributeName="opacity" values=".5;0;.5" dur="3s" begin="5.2s" repeatCount="indefinite"/></circle>'
       + ''.join(knoten) + '</svg>')

html = f'''  <section class="herz-abschnitt" aria-labelledby="herzstueck-titel">
    <div class="herz-text">
      <p class="meta">Warum Website</p>
      <h2 class="gr-h3" id="herzstueck-titel">Eine gute Website ist kein digitales Schaufenster. Sie ist das Herzstück Ihres Marketings.</h2>
      <p>Von hier aus erklären Sie Ihr Angebot, schärfen Ihr Profil, bauen Vertrauen auf – und werden gefunden. Sie ist das Fundament für alles, was danach kommt.</p>
    </div>
    <figure class="ci-film herz-film" role="img" aria-label="Die Website in der Mitte, verbunden mit Werbung, Newsletter, Blog, Events, Kundenbindung und Wachstum; zwischen allen fließen Informationen in beide Richtungen.">
      {svg}
      <p class="ci-nochmal"><button type="button" class="textlink ci-nochmal-knopf">Noch einmal ansehen <span aria-hidden="true">↻</span></button></p>
    </figure>
  </section>'''
ZIEL.write_text(html, encoding='utf-8')
print('geschrieben:', ZIEL.name, len(html), 'Zeichen')
