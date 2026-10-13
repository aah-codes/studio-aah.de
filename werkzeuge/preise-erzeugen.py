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
# Leistungskarten ohne Kundenbilder (Anna 13.10.2026: Kunden stehen in den Success Stories): nur das Clay-Icon, ohne Formen
ICONS = {k: v['icon'] for k, v in json.loads((basis / 'werkzeuge' / 'leistungen-inhalte.json').read_text(encoding='utf-8')).items() if isinstance(v, dict) and 'icon' in v}
def ls_bild(i, k):
    return f'<span class="ls-bild"><img src="{ICONS[k["id"]]}" alt="" width="400" height="400" loading="lazy"></span>'


karten_s = ''.join(f'<a class="ls-karte" href="{k["link"]}" id="k-{k["id"]}">{ls_bild(i, k)}'
                   f'<span class="ls-karte-titel">{esc(k["titel"])}</span><span class="ls-karte-text">{esc(k["text"])}</span></a>' for i, k in enumerate(daten['startseite']))
start_html = ('  <section class="start-leistungen" aria-labelledby="leistungen">\n    <div class="sektionskopf"><p class="meta">Was ich mache</p>'
              '<h2 class="gr-xxl" id="leistungen">Leistungen</h2></div>\n'
              f'    <nav class="leistungs-chips" aria-label="Leistungen">{chips}<a href="preise/#rechner">Kostenrechner →</a></nav>\n'
              f'    <div class="ls-raster">{karten_s}</div>\n'
              '    <p class="ls-grundsatz"><a class="textlink" href="service/markenbildung/#corporate-identity">Grundlage für alles, was ich gestalte: die Corporate Identity <span aria-hidden="true">→</span></a></p>\n  </section>')
start = basis / 'website' / 'index.html'
start.write_text(einsetzen(start.read_text(encoding='utf-8'), 'LEISTUNGEN', start_html), encoding='utf-8')
# --- Startseite, Hero: Leistungen als Kategorie-Leiste wie bei Dribbble (Anna 13.10.2026) ---
# Jede Karte führt zur Leistungsseite. Wo es ein echtes Beispiel gibt, steht es als Mockup in der Karte, sonst das Kartenbild der Leistung.
BEISPIELE = {
    # Mobil (Anna 13.10.2026, Vorbild Dribbble „Mobile“): zwei Handys nebeneinander, führt zu UI/UX
    # Mobil wie bei Dribbble: zwei Handys mit dünnem schwarzem Rahmen, heller Grund mit Lichtkante, eine große Form dahinter (Anna 13.10.2026)
    'mobil': ('<span class="kb-mobil"><i class="kb-form-gross"></i>'
              + ''.join(f'<span class="kb-phone"><span class="kb-phone-screen"><img src="bilder/referenzen/{n}" alt="" width="860" height="{h}" decoding="async"></span></span>'
                        for n, h in [('deinetwegen-handy.jpg', 9000), ('studio-aah-handy.jpg', 9923)]) + '</span>'),
    # Webdesign: Foto-Mockup Laptop auf Podest (Vorlage von Anna, Mockuptree, 13.10.2026); die Website sitzt per matrix3d
    # genau im Bildschirm (Ecken im 2000 × 1500 px großen Foto: 530|440, 1248|401, 1334|926, 615|1012) und scrollt wie bisher
    'website': ('<span class="kb-szene" style="--sb:2000;--sh:1500"><img class="kb-szene-bild" src="bilder/mockups/laptop-podest.webp" alt="" width="1000" height="750" loading="lazy">'
                '<span class="kb-szene-schirm" style="transform:matrix3d(0.5768583309,-0.002993487456,0,6.037555358e-05,0.08645866767,0.6267902485,0,-1.30273683e-05,0,0,1,0,528,438,0,1)">'
                '<span class="laptop-seite"><img src="bilder/referenzen/bauer-website.jpg" alt="" width="1440" height="6000" loading="lazy"></span></span></span>'),
    # Druck: Visitenkarten von Dr. Simone Goldhammer auf dem Schreibtisch (werkzeuge/grafiken/druck-mockup.py)
    'print': '<img src="bilder/mockups/druck-schreibtisch.webp" alt="" width="1200" height="900" loading="lazy">',
    # Markenbildung: STUDIO AAH! als eigenes Beispiel (Anna 13.10.2026: ein Kunde, ein Platz; Bauer steht bei Webdesign):
    # Logo auf Creme, Markenfarben, Kreis auf Blau, „AAH!“ auf Schwarz
    'brand': ('<span class="kb-raster kb-eigen"><span class="kb-e-logo"><img src="bilder/logo-studio-aah.svg" alt="" width="180" height="33"></span>'
              '<span class="kb-r-farben"><i style="--f:#0e1011"></i><i style="--f:#2f6bff"></i><i style="--f:#eeece7"></i><i style="--f:#d6d8d9"></i></span>'
              '<span class="kb-e-blau"><i></i></span><span class="kb-e-schwarz">AAH!</span></span>'),
    # Animation: Foto-Mockup Laptop in Händen vor Wolken (Bendito Mockup); im Bildschirm der eigene Erklärfilm Corporate Identity
    # als kurze Animation (einmal 4,7 s, dann Standbild; beim Darüberfahren neu, js/hero.js); bei „Bewegung reduzieren“ nur das Standbild
    'motion': ('<span class="kb-szene" style="--sb:1777;--sh:1333"><img class="kb-szene-bild" src="bilder/mockups/laptop-wolken.webp" alt="" width="1000" height="750" loading="lazy">'
               '<span class="kb-szene-schirm" style="transform:matrix3d(0.4712927933,-0.01449482037,0,-2.30025695e-05,0.01573352095,0.5063413888,0,1.697912788e-05,0,0,1,0,528,455,0,1)">'
               '<picture><source media="(prefers-reduced-motion: reduce)" srcset="bilder/mockups/ci-animation-still.webp">'
               '<img class="kb-anim" src="bilder/mockups/ci-animation.webp" alt="" width="720" height="450"></picture></span></span>'),
    # Produktdesign wie bei Dribbble: Website von Down to Earth (Kerstin Hack) und daneben ihre Markenfarben ohne Beschriftung
    'ui-ux': ('<span class="kb-produkt"><span class="kb-p-buehne"><span class="kb-p-seite"><img src="bilder/referenzen/leben-website.jpg?v=2" alt="" loading="lazy"></span></span>'
              '<span class="kb-p-farben">' + ''.join(f'<i style="--f:{f};--t:{t}">{f.upper()}</i>' for f, t in
                  [('#2d3b42', '#fff'), ('#3f9961', '#fff'), ('#a88b45', '#fff'), ('#f0eadb', '#2d3b42'), ('#ffffff', '#2d3b42')]) + '</span></span>'),
    # Illustration von STUDIO AAH! selbst (Bauhaus-Figur aus dem Blog)
    'illustration': '<img src="bilder/blog-geld-und-zeit.webp" alt="" loading="lazy">',
    # Typografie: Schriftmuster aus den Hausschriften von STUDIO AAH! (Anton, Manrope, JetBrains Mono)
    'typo': '<span class="kb-typo"><span class="kb-typo-aa">Aa</span><span class="kb-typo-text">Manrope</span><span class="kb-typo-meta">Anton · JetBrains Mono</span></span>',
}
# Kategorien oben (Anna 13.10.2026), unabhängig von den Leistungskarten unten; ohne Beispiel steht das Kartenbild der Leistung
KATEGORIEN = [
    {'id': 'brand', 'titel': 'Markenbildung', 'link': 'service/markenbildung/'},
    {'id': 'print', 'titel': 'Druck', 'link': 'service/druck/'},
    {'id': 'mobil', 'titel': 'Mobil', 'link': 'service/ui-ux/'},
    {'id': 'motion', 'titel': 'Animation', 'link': 'service/animation/'},
    {'id': 'illustration', 'titel': 'Illustration', 'link': 'service/illustration-infografik/'},
    {'id': 'website', 'titel': 'Webdesign', 'link': 'service/webdesign/'},
    {'id': 'ui-ux', 'titel': 'Produktdesign', 'link': 'service/ui-ux/'},
    {'id': 'typo', 'titel': 'Typografie', 'link': 'service/markenbildung/'},
]
def kat_bild(k):
    return BEISPIELE.get(k['id']) or '<img src="' + k['bild'] + '" alt="" loading="lazy">'


kategorien = ''.join('      <a class="kat" href="' + k['link'] + '"><span class="kat-stapel"><span class="kat-bild">' + kat_bild(k)
                     + '</span></span><span class="kat-name">' + esc(k['titel']) + '</span></a>\n' for k in KATEGORIEN)
hero_html = ('  <nav class="hero-band" aria-label="Leistungen im Überblick">\n    <div class="hero-spur">\n' + kategorien + '    </div>\n'
             '    <button type="button" class="band-pause" aria-pressed="false"><span class="unsichtbar">Laufband anhalten</span></button>\n  </nav>')
start.write_text(einsetzen(start.read_text(encoding='utf-8'), 'HEROBAND', hero_html), encoding='utf-8')
print('Rechner-Daten, Leiste, Glossar und Startseite geschrieben')
