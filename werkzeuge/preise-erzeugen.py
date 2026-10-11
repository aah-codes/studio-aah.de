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
              '    <p class="ls-grundsatz"><a class="textlink" href="service/brand/#corporate-identity">Grundlage für alles, was ich gestalte: das Rad der Corporate Identity <span aria-hidden="true">→</span></a></p>\n  </section>')
start = basis / 'website' / 'index.html'
start.write_text(einsetzen(start.read_text(encoding='utf-8'), 'LEISTUNGEN', start_html), encoding='utf-8')
print('Rechner-Daten, Leiste, Glossar und Startseite geschrieben')
