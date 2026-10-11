# Erzeugt wiederkehrende Inhalte aus werkzeuge/inhalte/*.json (Projekte, Kundenstimmen, Blogartikel, Kennzahlen)
# und setzt sie zwischen die Marker <!-- NAME:START --> … <!-- NAME:ENDE --> der Seiten.
# Jeder Eintrag hat Schlagworte (tags), z. B. "website", "brand", "ui-ux"; die Leistungsseiten wählen danach aus.
# Neuer Eintrag: in die passende Datei schreiben, dann  python3 werkzeuge/inhalte-erzeugen.py  (und danach leistungsseiten.py)
import html, json, pathlib, re

basis = pathlib.Path(__file__).resolve().parent.parent
lade = lambda n: json.loads((basis / 'werkzeuge' / 'inhalte' / f'{n}.json').read_text(encoding='utf-8'))
esc = lambda s: html.escape(s, quote=False)
PROJEKTE, STIMMEN, BLOG, ZAHLEN = lade('projekte'), lade('stimmen'), lade('blog'), lade('kennzahlen')
BLOG = sorted(BLOG, key=lambda b: b['datum'], reverse=True)
ORT = '<svg class="fakt-ort" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.6 7-12.5A7 7 0 0 0 5 9.5C5 15.4 12 22 12 22z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><circle cx="12" cy="9.5" r="2.6" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>'


def mit_tag(liste, tags):
    if not tags: return liste
    return [x for x in liste if set(x.get('tags', [])) & set(tags)]


def projekte(liste):
    out = []
    for p in liste:
        links = '<br>'.join(f'<a class="textlink" href="{l["url"]}" target="_blank" rel="noopener">{esc(l["text"])} ↗</a>' for l in p.get('links', []))
        web = f'\n    <div><dt>Website</dt><dd>{links}</dd></div>' if links else ''
        out.append(f'''<details class="referenz">
  <summary><span class="referenz-name">{esc(p["name"])}</span><span class="referenz-zeichen" aria-hidden="true"></span></summary>
  <dl class="referenz-fakten">
    <div><dt>Branche</dt><dd>{esc(p["branche"])}</dd></div>
    <div><dt>Zeitraum</dt><dd>{esc(p["zeitraum"])}</dd></div>
    <div><dt>Leistungen</dt><dd>{esc(p["leistungen"])}</dd></div>{web}
  </dl>
</details>''')
    return '\n'.join(out)


def stimmen(liste, pre):
    out = []
    for s in liste:
        ps = ''.join(f'        <p class="gedaempft">{a}</p>\n' for a in s['absaetze_html'])
        bild = f'          <img class="avatar" src="{pre}bilder/{s["bild"]}" alt="{esc(s["name"])}" width="60" height="60" loading="lazy">\n' if s.get('bild') else ''
        out.append(f'''      <article class="stimme {s["hintergrund"]}">
        <img class="stimme-icon" src="{pre}bilder/icon-quote.png" alt="" width="40" height="25" loading="lazy">
        <h3 class="alt-h5">{esc(s["titel"])}</h3>
{ps}        <div class="person">
{bild}          <div>
            <p class="alt-h6">{esc(s["name"])}</p>
            <p class="meta">{s["rolle_html"]}</p>
          </div>
        </div>
      </article>''')
    return '\n'.join(out)


def blog(liste, pre, linkpre, h='h3', einrueck='    '):
    out = []
    for b in liste:
        u = f'{linkpre}{b["slug"]}/'
        out.append(f'''{einrueck}<li>
{einrueck}  <article class="blog-karte">
{einrueck}    <a href="{u}" aria-hidden="true" tabindex="-1"><img src="{pre}bilder/{b["bild"]}" alt="" width="{b["bild_b"]}" height="{b["bild_h"]}" loading="lazy"></a>
{einrueck}    <div class="blog-karte-text">
{einrueck}      <p class="kategorie">{esc(b["kategorie"])}</p>
{einrueck}      <{h}><a href="{u}">{b["titel_html"]}</a></{h}>
{einrueck}      <p class="artikel-meta">Von Anna · <time datetime="{b["datum"]}">{b["datum_text"]}</time></p>
{einrueck}      <p>{b["teaser_html"]}</p>
{einrueck}      <a class="weiterlesen" href="{u}">Weiterlesen →<span class="unsichtbar">: {b["titel_html"]}</span></a>
{einrueck}    </div>
{einrueck}  </article>
{einrueck}</li>''')
    return '\n'.join(out)


def kennzahlen(klasse='fakten hero-fakten', einrueck='    '):
    z = []
    for k in ZAHLEN:
        if k.get('symbol') == 'ort':
            z.append(f'{einrueck}  <div><dt>{ORT}</dt><dd><span class="mit-liebe">{esc(k["text"])}</span></dd></div>')
        else:
            z.append(f'{einrueck}  <div><dt><span data-zaehlen="{k["zahl"]}">{k["zahl"]}</span>{k["zusatz"]}</dt><dd>{esc(k["text"])}</dd></div>')
    return f'{einrueck}<dl class="{klasse}">\n' + '\n'.join(z) + f'\n{einrueck}</dl>'


def einsetzen(text, name, inhalt):
    neu, n = re.subn(rf'<!-- {name}:START -->.*?<!-- {name}:ENDE -->', lambda m: f'<!-- {name}:START -->\n{inhalt}\n<!-- {name}:ENDE -->', text, count=1, flags=re.S)
    if not n: raise SystemExit(f'Marker {name} fehlt')
    return neu


if __name__ == '__main__':
    seiten = {
        'index.html': [('PROJEKTE', lambda: projekte(PROJEKTE)), ('STIMMEN', lambda: stimmen(STIMMEN, '')),
                       ('BLOG', lambda: blog(BLOG[:3], '', 'blog/')), ('KENNZAHLEN', lambda: kennzahlen())],
        'profil/index.html': [('STIMMEN', lambda: stimmen(STIMMEN, '../')), ('BLOG', lambda: blog(BLOG[:3], '../', '../blog/')),
                              ('KENNZAHLEN', lambda: kennzahlen('fakten', '      '))],
        'blog/index.html': [('BLOG', lambda: blog(BLOG, '../', '', 'h2'))],
    }
    for datei, teile in seiten.items():
        p = basis / 'website' / datei
        t = p.read_text(encoding='utf-8')
        for name, f in teile: t = einsetzen(t, name, f())
        p.write_text(t, encoding='utf-8')
    print('Projekte, Stimmen, Blog und Kennzahlen geschrieben')
