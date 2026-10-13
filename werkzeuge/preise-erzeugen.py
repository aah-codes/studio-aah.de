# Erzeugt aus EINER Datenquelle (preise-daten.json): Rechner-Daten js/pakete-daten.js,
# Bereichsleiste + Glossar der Preisseite und Leistungskarten der Startseite. Preise und Paketinhalte nur in preise-daten.json ändern.
# Aufruf im Repository-Ordner:  python3 werkzeuge/preise-erzeugen.py
import html, json, pathlib, re

basis = pathlib.Path(__file__).resolve().parent.parent
daten = json.loads((basis / 'werkzeuge' / 'preise-daten.json').read_text(encoding='utf-8'))
esc = lambda s: html.escape(s, quote=False)


seite = basis / 'website' / 'preise' / 'index.html'
t = seite.read_text(encoding='utf-8')
leiste = ''.join(f'<a href="#r-{g["id"]}">{esc(g["kurz"])}</a>' for g in daten['gruppen'])
t = re.sub(r'(<nav class="preis-leiste"[^>]*>\n  <a href="#rechner">Kostenrechner</a>).*?(<a href="#glossar">Glossar</a>)',
           lambda m: m.group(1) + leiste + m.group(2), t, count=1, flags=re.S)
seite.write_text(t, encoding='utf-8')

# Rechner bekommt nur, was er braucht; der automatische Launch-Posten wird zur Zahl „launch“
weg = ('kurz', 'link', 'karte', 'intro', 'unterseite', 'startseite')
schlank = lambda e: {k: v for k, v in e.items() if k not in weg}
rechner = {'launch': next(x['preis'] for g in daten['gruppen'] for x in g.get('extras', []) if x.get('auto')), 'gruppen': []}
for g in daten['gruppen']:
    r = schlank(g)
    r['pakete'] = [schlank(e) for e in g['pakete']]
    # nurSeite: steht nur auf der Leistungsseite; im Rechner gibt es die Leistung schon in einer eigenen Gruppe
    if 'extras' in g: r['extras'] = [schlank(e) for e in g['extras'] if not e.get('auto') and not e.get('nurSeite')]
    rechner['gruppen'].append(r)
(basis / 'website' / 'js' / 'pakete-daten.js').write_text(
    '// Erzeugt von werkzeuge/preise-erzeugen.py aus werkzeuge/preise-daten.json – nicht von Hand ändern\nwindow.PREISE = '
    + json.dumps(rechner, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8')
# --- Glossar (Preisseite) ---
def glossar_html():
    zeilen = ''.join(f'    <div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>\n' for a, b in daten['glossar'])
    return ('<section class="glossar" id="glossar" aria-labelledby="glossar-titel">\n  <p class="meta">Begriffe kurz erklärt</p>\n'
            '  <h2 class="preis-h2" id="glossar-titel">Glossar</h2>\n  <dl class="glossar-liste">\n' + zeilen + '  </dl>\n</section>')


def einsetzen(text, name, inhalt):
    return re.sub(rf'<!-- {name}:START -->.*?<!-- {name}:ENDE -->', lambda m: f'<!-- {name}:START -->\n{inhalt}\n<!-- {name}:ENDE -->', text, count=1, flags=re.S)


seite = basis / 'website' / 'preise' / 'index.html'
seite.write_text(einsetzen(seite.read_text(encoding='utf-8'), 'GLOSSAR', glossar_html()), encoding='utf-8')

# --- Startseite: Leistungen als Karten (9 Stück) mit Chips darüber ---
chips = ''.join(f'<a href="#k-{k["id"]}">{esc(k["titel"])}</a>' for k in daten['startseite'])
karten_s = ''.join(f'<a class="ls-karte" href="{k["link"]}" id="k-{k["id"]}"><img src="{k["bild"]}" alt="" loading="lazy">'
                   f'<span class="ls-karte-titel">{esc(k["titel"])}</span><span class="ls-karte-text">{esc(k["text"])}</span></a>' for k in daten['startseite'])
start_html = ('  <section class="start-leistungen" aria-labelledby="leistungen">\n    <div class="sektionskopf"><p class="meta">Was ich mache</p>'
              '<h2 class="gr-xxl" id="leistungen">Leistungen</h2></div>\n'
              f'    <nav class="leistungs-chips" aria-label="Leistungen">{chips}<a href="preise/#rechner">Kostenrechner →</a></nav>\n'
              f'    <div class="ls-raster">{karten_s}</div>\n'
              '    <p class="ls-grundsatz"><a class="textlink" href="service/brand/#corporate-identity">Grundlage für alles, was ich gestalte: die Corporate Identity <span aria-hidden="true">→</span></a></p>\n  </section>')
start = basis / 'website' / 'index.html'
start.write_text(einsetzen(start.read_text(encoding='utf-8'), 'LEISTUNGEN', start_html), encoding='utf-8')
# --- Startseite, Hero: Leistungen als Kategorie-Leiste wie bei Dribbble (Anna 13.10.2026) ---
# Jede Karte führt zur Leistungsseite. Wo es ein echtes Beispiel gibt, steht es als Mockup in der Karte, sonst das Kartenbild der Leistung.
BEISPIELE = {
    # Mobil (Anna 13.10.2026, Vorbild Dribbble „Mobile“): zwei Handys nebeneinander, führt zu UI/UX
    'mobil': '<span class="kb-duo">' + ''.join(f'<span class="band-teil kb-handy"><span class="handy-bildschirm"><img src="bilder/referenzen/{n}" alt="" width="860" height="{h}" decoding="async"></span></span>'
                                              for n, h in [('deinetwegen-handy.jpg', 9000), ('studio-aah-handy.jpg', 9923)]) + '</span>',
    'website': '<span class="band-teil laptop kb-laptop"><span class="laptop-bildschirm"><span class="laptop-seite"><img src="bilder/referenzen/bauer-website.jpg" alt="" width="1440" height="6000"></span></span><span class="laptop-unterteil"></span></span>',
    # Druck: Flyer-Mockup Dr. Simone Goldhammer (Format 4:3 wie die Karte)
    'print': '<img src="bilder/referenzen/goldhammer-flyer.jpg" alt="" loading="lazy">',
    # Markenbildung wie bei Dribbble als Raster: Rebranding Wolfgang Bauer Ingenieurbau (Folien und Markenfarben, aus den Folien gemessen)
    'brand': ('<span class="kb-raster"><img class="kb-r-gross" src="bilder/hero/bauer-praes-01.jpg" alt="" loading="lazy">'
              '<span class="kb-r-farben"><i style="--f:#123261"></i><i style="--f:#f3d557"></i><i style="--f:#fff"></i></span>'
              '<img src="bilder/hero/bauer-praes-04.jpg" alt="" loading="lazy"><img src="bilder/hero/bauer-praes-12.jpg" alt="" loading="lazy"></span>'),
    'motion': '<img src="bilder/film-bauer-vorschau.jpg" alt="" loading="lazy"><span class="kb-play"></span>',
    # Produktdesign wie bei Dribbble: Website von Down to Earth (Kerstin Hack) und daneben ihre Markenfarben ohne Beschriftung
    'ui-ux': ('<span class="kb-produkt"><span class="kb-p-seite"><img src="bilder/referenzen/leben-website.jpg?v=2" alt="" loading="lazy"></span>'
              '<span class="kb-p-farben"><i style="--f:#3f9961"></i><i style="--f:#a88b45"></i><i style="--f:#2d3b42"></i><i style="--f:#f0eadb"></i></span></span>'),
    # Illustration von STUDIO AAH! selbst (Bauhaus-Figur aus dem Blog)
    'illustration': '<img src="bilder/blog-geld-und-zeit.webp" alt="" loading="lazy">',
    # Typografie: Schriftmuster aus den Hausschriften von STUDIO AAH! (Anton, Manrope, JetBrains Mono)
    'typo': '<span class="kb-typo"><span class="kb-typo-aa">Aa</span><span class="kb-typo-text">Manrope</span><span class="kb-typo-meta">Anton · JetBrains Mono</span></span>',
}
# Kategorien oben (Anna 13.10.2026), unabhängig von den Leistungskarten unten; ohne Beispiel steht das Kartenbild der Leistung
KATEGORIEN = [
    {'id': 'brand', 'titel': 'Markenbildung', 'link': 'service/brand/'},
    {'id': 'print', 'titel': 'Druck', 'link': 'service/print/'},
    {'id': 'mobil', 'titel': 'Mobil', 'link': 'service/ui-ux/'},
    {'id': 'motion', 'titel': 'Animation', 'link': 'service/motion-design/'},
    {'id': 'illustration', 'titel': 'Illustration', 'link': 'service/illustration-infografik/'},
    {'id': 'website', 'titel': 'Webdesign', 'link': 'service/website/'},
    {'id': 'ui-ux', 'titel': 'Produktdesign', 'link': 'service/ui-ux/'},
    {'id': 'typo', 'titel': 'Typografie', 'link': 'service/brand/'},
]
def kat_bild(k):
    return BEISPIELE.get(k['id']) or '<img src="' + k['bild'] + '" alt="" loading="lazy">'


kategorien = ''.join('      <a class="kat" href="' + k['link'] + '"><span class="kat-stapel"><span class="kat-bild">' + kat_bild(k)
                     + '</span></span><span class="kat-name">' + esc(k['titel']) + '</span></a>\n' for k in KATEGORIEN)
hero_html = ('  <nav class="hero-band" aria-label="Leistungen im Überblick">\n    <div class="hero-spur">\n' + kategorien + '    </div>\n'
             '    <button type="button" class="band-pause" aria-pressed="false"><span class="unsichtbar">Laufband anhalten</span></button>\n  </nav>')
start.write_text(einsetzen(start.read_text(encoding='utf-8'), 'HEROBAND', hero_html), encoding='utf-8')
print('Rechner-Daten, Leiste, Glossar und Startseite geschrieben')
