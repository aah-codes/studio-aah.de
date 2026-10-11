# Erzeugt aus EINER Datenquelle (preise-daten.json) die Rechner-Daten js/pakete-daten.js
# und die Bereichsleiste in website/preise/index.html. Preise und Paketinhalte nur in preise-daten.json ändern.
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
weg = ('kurz', 'link')
schlank = lambda e: {k: v for k, v in e.items() if k not in weg}
rechner = {'launch': next(x['preis'] for g in daten['gruppen'] for x in g.get('extras', []) if x.get('auto')), 'gruppen': []}
for g in daten['gruppen']:
    r = schlank(g)
    r['pakete'] = [schlank(e) for e in g['pakete']]
    if 'extras' in g: r['extras'] = [schlank(e) for e in g['extras'] if not e.get('auto')]
    rechner['gruppen'].append(r)
(basis / 'website' / 'js' / 'pakete-daten.js').write_text(
    '// Erzeugt von werkzeuge/preise-erzeugen.py aus werkzeuge/preise-daten.json – nicht von Hand ändern\nwindow.PREISE = '
    + json.dumps(rechner, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8')
print('Leiste und Rechner-Daten geschrieben')
