# Erzeugt aus EINER Datenquelle (preise-daten.json) die Preisliste in website/preise/index.html
# und die Rechner-Daten js/pakete-daten.js. Preise und Paketinhalte nur in preise-daten.json ändern.
# Aufruf im Repository-Ordner:  python3 werkzeuge/preise-erzeugen.py
import html, json, pathlib, re

basis = pathlib.Path(__file__).resolve().parent.parent
daten = json.loads((basis / 'werkzeuge' / 'preise-daten.json').read_text(encoding='utf-8'))
esc = lambda s: html.escape(s, quote=False)


def preis_text(e):
    if e.get('anfrage'): return 'auf Anfrage'
    if e.get('anteil'): return f"+ {int(e['anteil'] * 100)} %"
    if e.get('stunde'): return f"{e['stunde']} €/h"
    p = f"{e['preis']:,}".replace(',', '.') if 'preis' in e else f"{e['monat']}"
    if e.get('monat'): return f"<small>ab</small> {p}&nbsp;€/Monat"
    return f"<small>ab</small> {p}&nbsp;€" if e.get('ab', True) else f"{p}&nbsp;€"


def chips(e):
    out = []
    if e.get('plus', '').startswith('Alles aus'):
        out.append(f'<li class="chip-plus">+ {esc(e["plus"][0].lower() + e["plus"][1:].rstrip(":").replace(", plus", ""))}</li>')
    out += [f'<li>{esc(i)}</li>' for i in e.get('items', [])]
    return f'<ul class="pl-chips">{"".join(out)}</ul>' if out else (f'<span class="gedaempft">{esc(e.get("kurz", ""))}</span>')


zeilen, anzahl = [], 0
for g in daten['gruppen']:
    mehr = f' <a class="pl-mehr" href="{g["link"]}">Mehr zu {esc(g["name"])} →</a>' if g.get('link') else ''
    zeilen.append(f'<tr class="pl-gruppe" id="pl-{g["id"]}"><th colspan="4" scope="rowgroup"><span>{esc(g["name"])}</span>{mehr}</th></tr>')
    for e in g['pakete'] + g.get('extras', []) + g.get('nur_liste', []):
        anzahl += 1
        badge = ' <span class="abzeichen-rand">Gefragt</span>' if e.get('gefragt') else ''
        zeilen.append(f'<tr><th scope="row"><span class="pl-name">{esc(e["name"])}</span>{badge}</th><td>{chips(e)}</td>'
                      f'<td class="gedaempft pl-wer">{esc(e.get("wer", ""))}</td><td class="pl-preis">{preis_text(e)}</td></tr>')

tabelle = '\n        '.join(zeilen)
seite = basis / 'website' / 'preise' / 'index.html'
t = seite.read_text(encoding='utf-8')
t = re.sub(r'<p class="meta">\d+ Pakete und Leistungen</p>', f'<p class="meta">{anzahl} Pakete und Leistungen</p>', t)
t = re.sub(r'(<tbody>\n).*?(\n\s*</tbody>\s*</table>\s*</div>\s*<p class="gedaempft preis-netto">)',
           lambda m: m.group(1) + '        ' + tabelle + m.group(2), t, count=1, flags=re.S)
leiste = ''.join(f'<a href="#pl-{g["id"]}">{esc(g["kurz"])}</a>' for g in daten['gruppen'])
t = re.sub(r'(<nav class="preis-leiste"[^>]*>\n  <a href="#rechner">Kostenrechner</a>).*?(<a href="#kostenlos-titel">Programm</a>)',
           lambda m: m.group(1) + leiste + m.group(2), t, count=1, flags=re.S)
seite.write_text(t, encoding='utf-8')
(basis / 'website' / 'js' / 'pakete-daten.js').write_text(
    '// Erzeugt von werkzeuge/preise-erzeugen.py aus werkzeuge/preise-daten.json – nicht von Hand ändern\nwindow.PREISE = '
    + json.dumps(daten, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8')
print(f'{anzahl} Zeilen in der Preisliste, Rechner-Daten geschrieben')
