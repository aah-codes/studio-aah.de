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


def projekte(liste, pre=''):
    out = []
    for p in liste:
        links = '<br>'.join(f'<a class="textlink" href="{l["url"]}" target="_blank" rel="noopener">{esc(l["text"])} ↗</a>' for l in p.get('links', []))
        web = f'\n    <div><dt>Website</dt><dd>{links}</dd></div>' if links else ''
        f = p.get('film')
        film = (f'\n    <div class="referenz-film"><dt class="unsichtbar">Film</dt><dd><button type="button" class="film-knopf" data-film="{pre}{f["datei"]}" data-titel="{html.escape(f["titel"])}" aria-label="{html.escape(f["titel"])} ansehen">'
                f'<img src="{pre}{f["vorschau"]}" alt="" width="960" height="540" loading="lazy"><span class="film-play" aria-hidden="true"></span></button></dd></div>') if f else ''
        out.append(f'''<details class="referenz">
  <summary><span class="referenz-name">{esc(p["name"])}</span><span class="referenz-zeichen" aria-hidden="true"></span></summary>
  <dl class="referenz-fakten{' mit-film' if p.get('film') else ''}">{film}
    <div><dt>Branche</dt><dd>{esc(p["branche"])}</dd></div>
    <div><dt>Zeitraum</dt><dd>{esc(p["zeitraum"])}</dd></div>
    <div><dt>Leistungen</dt><dd>{esc(p["leistungen"])}</dd></div>{web}
  </dl>
</details>''')
    return '\n'.join(out)



# --- Referenzkarten (Vorbild Google Business Profile, Mockups wie Behance/Dribbble): Text links, Mockup rechts,
#     schwebende Karte (Launch-Film oder Kundenstimme) über dem Rand; Kartenfarbe = Hausfarbe des Projekts ---
def _chips(p):
    teile = [x.strip() for s in p['leistungen'].split(', ') for x in s.split(' & ')]
    return ''.join(f'<li>{esc(x)}</li>' for x in teile if x)


def _mockup(p, pre):
    m, h = p.get('mockup', {}), []
    if m.get('browser'):
        h.append(f'<div class="rk-browser"><img src="{pre}{m["browser"]}" alt="Website von {esc(p["kurzname"])}" loading="lazy"></div>')
    if m.get('handy'):
        h.append(f'<div class="rk-handy"><img src="{pre}{m["handy"]}" alt="Website von {esc(p["kurzname"])} auf dem Handy" loading="lazy"></div>')
    if m.get('karte'):
        h.append(f'<div class="rk-objekt"><img src="{pre}{m["karte"]}" alt="Gestaltung für {esc(p["kurzname"])}" loading="lazy"></div>')
    if m.get('folien'):
        h.append('<div class="rk-folien">' + ''.join(f'<img src="{pre}{f}" alt="" loading="lazy">' for f in m['folien']) + '<span>Unternehmenspräsentation</span></div>')
    f = p.get('film')
    if f:
        h.append(f'<button type="button" class="rk-schwebe rk-film film-knopf" data-film="{pre}{f["datei"]}" data-titel="{html.escape(f["titel"])}" aria-label="{html.escape(f["titel"])} ansehen">'
                 f'<span class="rk-film-bild"><img src="{pre}{f["vorschau"]}" alt="" loading="lazy"></span><b>Launch-Film ansehen</b><span>die neue Website im Film</span></button>')
    elif p.get('stimme'):
        s = next((x for x in STIMMEN if x['name'] == p['stimme']), None)
        if s:
            satz = re.sub(r'<[^>]+>', '', s['absaetze_html'][0])
            satz = satz[:satz.find('!') + 1] if '!' in satz[:200] else satz[:160].rsplit(' ', 1)[0] + ' …'
            bild = f'<img src="{pre}bilder/{s["bild"]}" alt="" loading="lazy">' if s.get('bild') else ''
            h.append(f'<div class="rk-schwebe">{bild}<b>{esc(s["name"])}</b><span>{s["rolle_html"]}</span><p>„{html.escape(satz, quote=False)}“</p></div>')
    return ''.join(h)


def referenz_karten(liste, pre, kennung='ref'):
    karten = []
    for p in liste:
        link = p['links'][0] if p.get('links') else None
        karten.append(f'''      <article class="rk" style="--rk-farbe: {p.get("farbe", "#eeece7")}">
        <div class="rk-text">
          <p class="meta">{esc(p["branche"])} · {esc(p["zeitraum"])}</p>
          <h3 class="rk-name">{esc(p["kurzname"])}</h3>
          <ul class="rk-chips">{_chips(p)}</ul>
          {f'<p class="rk-link"><a class="textlink" href="{link["url"]}" target="_blank" rel="noopener">{esc(link["text"])} ↗</a></p>' if link else ''}
        </div>
        <div class="rk-buehne">{_mockup(p, pre)}</div>
      </article>''')
    if len(karten) == 1:
        return '    <div class="rk-einzeln">\n' + karten[0] + '\n    </div>'
    return (f'    <div class="ks" data-karussell id="{kennung}-karussell">\n      <div class="ks-spur" aria-live="polite">\n' + '\n'.join(karten) + '\n      </div>\n'
            '      <div class="ks-steuerung">\n        <div class="ks-pfeile"><button type="button" class="ks-knopf" data-zurueck aria-label="Vorheriges Projekt">←</button>'
            '<button type="button" class="ks-knopf" data-weiter aria-label="Nächstes Projekt">→</button></div>\n'
            '        <div class="ks-rechts"><button type="button" class="ks-knopf" data-pause aria-label="Automatisches Weiterblättern anhalten">❚❚</button><div class="ks-punkte" aria-hidden="true"></div></div>\n'
            '      </div>\n    </div>')


# --- Für wen: dunkler Abschnitt mit Umschalter; zeigt je Zielgruppe, was STUDIO AAH! vor allem verkauft ---
def fuer_wen(pre=''):
    pd = json.loads((basis / 'werkzeuge' / 'preise-daten.json').read_text(encoding='utf-8'))
    paket = {e['id']: e for g in pd['gruppen'] for e in g['pakete']}
    euro = lambda n: f'{n:,.0f}'.replace(',', '.') + ' €'
    preis = lambda i: f'ab {euro(paket[i]["preis"])} <small>netto</small>'
    felder = [
        ('mittelstand', 'Mittelstand', 'Ihre ganze Website, neu gedacht.', paket['unternehmen']['wer'], [
            ('Website', paket['unternehmen']['name'], 'Design-System, neue Startseite, Leistungs-, Branchen- und Referenzseiten.', preis('unternehmen'), f'{pre}service/website/#pakete'),
            ('Karriere', 'Karrierebereich', 'Stellenangebote und Bewerbungsformular, damit Fachkräfte Sie finden.', 'im Paket', f'{pre}service/website/#pakete'),
            ('Referenz', 'Wolfgang Bauer Ingenieurbau', 'Strategie, Rebranding, UX/UI Design, Website und Unternehmenspräsentation.', 'Ansehen →', f'{pre}#referenzen')]),
        ('selbststaendige', 'Selbstständige', 'Klar auftreten, ohne Umwege.', 'Für Selbstständige und kleine Angebote: eine Website, die alles auf den Punkt bringt, und eine Marke, die zu Ihnen passt.', [
            ('Website', paket['onepager']['name'], 'Alles auf einer Seite, responsiv, mit SEO & LLM-Zitierfähigkeit.', preis('onepager'), f'{pre}service/website/#pakete'),
            ('Brand', 'Basic', 'Fragebogen, Brand Experience und Mitbewerberrecherche.', preis('brand-0'), f'{pre}service/brand/#pakete'),
            ('Referenz', 'Deinetwegen', 'Branding, UI/UX Design und Website für eine HR-Beratung.', 'Ansehen →', f'{pre}#referenzen')]),
        ('vereine', 'Vereine &amp; Kultur', 'Demokratie braucht Sichtbarkeit.', 'Kostenfreie Websites für Vereine, NGOs, Kunst und Kultur. Du zahlst, was es dir wert ist.', [
            ('Aktion', 'Kostenfreie Website', 'Für Organisationen, die sich für Demokratie, Frauen- und Kinderrechte, Natur- und Tierschutz oder Kunst und Kultur einsetzen.', 'kostenfrei', f'{pre}demokratie-braucht-sichtbarkeit/'),
            ('Aktion', 'Eine Website im Monat', 'Ich gestalte bis zu eine Website im Monat kostenfrei.', 'Mehr erfahren →', f'{pre}demokratie-braucht-sichtbarkeit/'),
            ('Referenz', 'Jana Voigtmann', 'Webdesign für eine Künstlerin aus Leipzig.', 'Ansehen →', f'{pre}#referenzen')]),
    ]
    TAB_AUS = ' tabindex="-1"'
    knoepfe = ''.join(f'<button type="button" role="tab" id="fw-r-{k}" aria-controls="fw-{k}" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else TAB_AUS}>{n}</button>' for i, (k, n, *_ ) in enumerate(felder))
    teile = []
    for i, (k, n, titel, unter, karten) in enumerate(felder):
        kh = ''.join(f'<a class="dk-karte" href="{l}"><span class="meta">{m}</span><span class="dk-karte-titel">{esc(h)}</span><span class="dk-karte-text">{esc(x)}</span><span class="dk-preis">{pr}</span></a>' for m, h, x, pr, l in karten)
        teile.append(f'      <div class="dk-feld" id="fw-{k}" role="tabpanel" aria-labelledby="fw-r-{k}"{"" if i == 0 else " hidden"}>\n        <h3 class="dk-titel">{esc(titel)}</h3>\n'
                     f'        <p class="dk-unter">{esc(unter)}</p>\n        <div class="dk-karten">{kh}</div>\n      </div>')
    return (f'  <section class="dk" aria-labelledby="fuer-wen-titel">\n    <p class="meta">Für wen</p>\n    <h2 class="unsichtbar" id="fuer-wen-titel">Für wen ich arbeite</h2>\n'
            f'    <div class="dk-umschalter" role="tablist" aria-label="Zielgruppe wählen">{knoepfe}</div>\n' + '\n'.join(teile) + '\n  </section>')


# --- Erfolgsgeschichte (Website-Seite): Film groß, Zitat nur mit Freigabe der Person ---
def erfolg(p, pre):
    e, f = p['erfolg'], p.get('film')
    if e.get('freigegeben'):
        kopf = f'<blockquote class="eg-zitat"><p>„{esc(e["zitat"])}“</p></blockquote><p class="eg-person"><b>{esc(e["person"])}</b> · {esc(e["rolle"])}, {esc(p["name"])}</p>'
    else:
        kopf = f'<h2 class="eg-zitat" id="erfolg-titel">{esc(p["kurzname"])}</h2><p class="eg-person">{esc(p["branche"])}</p>'
    fakten = ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in e['fakten'])
    link = p['links'][0] if p.get('links') else None
    film = (f'<button type="button" class="eg-film film-knopf" data-film="{pre}{f["datei"]}" data-titel="{html.escape(f["titel"])}" aria-label="{html.escape(f["titel"])} ansehen">'
            f'<img src="{pre}{f["vorschau"]}" alt="" loading="lazy"><span>▶ Launch-Film ansehen</span></button>') if f else ''
    return (f'''  <section class="eg" aria-labelledby="erfolg-titel">
    {film}
    <div>
      <p class="meta">Erfolgsgeschichte</p>
      {kopf}
      <dl class="eg-fakten">{fakten}</dl>
      {f'<p><a class="button" href="{link["url"]}" target="_blank" rel="noopener">Website ansehen ↗</a></p>' if link else ''}
    </div>
  </section>''')

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
        'index.html': [('PROJEKTE', lambda: referenz_karten(PROJEKTE, '', 'start')), ('FUERWEN', lambda: fuer_wen('')), ('STIMMEN', lambda: stimmen(STIMMEN, '')),
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
