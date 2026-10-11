# Erzeugt aus EINER Datenquelle (preise-daten.json): Rechner-Daten js/pakete-daten.js,
# Bereichsleiste + Glossar der Preisseite und Leistungsabschnitte + Leiste + Glossar der Leistungsseite (service/). Preise und Paketinhalte nur in preise-daten.json ändern.
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
weg = ('kurz', 'link', 'karte', 'intro', 'unterseite')
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
# --- Glossar (Preis- und Leistungsseite) ---
def glossar_html():
    zeilen = ''.join(f'    <div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>\n' for a, b in daten['glossar'])
    return ('<section class="glossar" id="glossar" aria-labelledby="glossar-titel">\n  <p class="meta">Begriffe kurz erklärt</p>\n'
            '  <h2 class="preis-h2" id="glossar-titel">Glossar</h2>\n  <dl class="glossar-liste">\n' + zeilen + '  </dl>\n</section>')


def einsetzen(text, name, inhalt):
    return re.sub(rf'<!-- {name}:START -->.*?<!-- {name}:ENDE -->', lambda m: f'<!-- {name}:START -->\n{inhalt}\n<!-- {name}:ENDE -->', text, count=1, flags=re.S)


seite = basis / 'website' / 'preise' / 'index.html'
seite.write_text(einsetzen(seite.read_text(encoding='utf-8'), 'GLOSSAR', glossar_html()), encoding='utf-8')

# --- Leistungsseite: gleiche Bereiche und Reihenfolge wie im Rechner ---
def preis_kurz(e):
    if e.get('anfrage'): return 'auf Anfrage'
    if e.get('anteil'): return f"+{int(e['anteil'] * 100)} %"
    if e.get('monat'): return f"ab {e['monat']} € / Monat"
    return ('ab ' if e.get('ab', True) else '') + f"{e['preis']:,} €".replace(',', '.')


GEFRAGT = ' <span class="wahl-gefragt">gefragt</span>'


def paket_li(e):
    wer = f'<p class="gedaempft">{esc(e["wer"])}</p>' if e.get('wer') else ''
    return f'<li><h3>{esc(e["name"])}{GEFRAGT if e.get("gefragt") else ""}</h3><span class="ls-preis">{preis_kurz(e)}</span>{wer}</li>'


def karte(g):
    ziel = g['unterseite'] or f'../preise/#r-{g["id"]}'
    return (f'<a class="ls-karte" href="{ziel}" id="s-{g["id"]}"><img src="{g["karte"]}" alt="" loading="lazy">'
            f'<span class="ls-karte-titel">{esc(g["name"])}</span><span class="ls-karte-text">{esc(g["intro"])}</span>'
            f'<span class="ls-karte-link">{"Mehr erfahren" if g["unterseite"] else "Kosten berechnen"} →</span></a>')


mit_karte = [g for g in daten['gruppen'] if g.get('karte') and g['id'] != 'print']
reihe1, reihe2 = mit_karte[:2], mit_karte[2:]
druck = [g for g in daten['gruppen'] if g['id'] == 'print']
zusatz_g = [g for g in daten['gruppen'] if g['id'] == 'zusatz']
bloecke = [
    '  <section class="ls-raster" aria-label="Leistungen">\n    <div class="ls-reihe ls-zwei">' + ''.join(karte(g) for g in reihe1) + '</div>\n'
    '    <div class="ls-reihe ls-drei">' + ''.join(karte(g) for g in reihe2) + '</div>\n'
    '    <div class="ls-reihe ls-eins">' + ''.join(karte(g) for g in druck) + '</div>\n  </section>']
for g in zusatz_g:
    pakete = ''.join(paket_li(e) for e in g['pakete'])
    bloecke.append(f'  <section class="leistung ohne-bild" id="s-{g["id"]}" aria-labelledby="s-{g["id"]}-titel">\n    <div class="leistung-text gross"><h2 class="gr-klein" id="s-{g["id"]}-titel">{esc(g["name"])}</h2>'
                   f'<p class="alt-klein">{esc(g["intro"])}</p><ul class="ls-pakete">{pakete}</ul><p class="ls-links"><a class="button" href="../preise/#r-{g["id"]}">Kosten berechnen <span aria-hidden="true">→</span></a></p></div>\n  </section>')
service = basis / 'website' / 'service' / 'index.html'
s = service.read_text(encoding='utf-8')
s = einsetzen(s, 'LEISTUNGEN', '\n\n'.join(bloecke))
s = einsetzen(s, 'GLOSSAR', glossar_html())
service.write_text(s, encoding='utf-8')
print('Rechner-Daten, Leisten, Glossar und Leistungsseite geschrieben')
