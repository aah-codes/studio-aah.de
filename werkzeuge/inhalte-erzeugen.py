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
ORT = '<svg class="fakt-ort" viewBox="0 0 24 24" aria-hidden="true"><path d="M5.4 12.5h13.2L12 23z" fill="currentColor"/><circle cx="12" cy="9" r="7" fill="currentColor"/><circle cx="12" cy="9" r="3" fill="#fff"/></svg>'


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


def _mockup(p, pre, m=None):
    m, h = m or p.get('mockup', {}), []
    if m.get('browser'):
        h.append(f'<div class="rk-browser"><img src="{pre}{m["browser"]}" alt="Website von {esc(p["kurzname"])}" loading="lazy"></div>')
    if m.get('handy'):
        h.append(f'<div class="rk-handy"><img src="{pre}{m["handy"]}" alt="Website von {esc(p["kurzname"])} auf dem Handy" loading="lazy"></div>')
    if m.get('karte'):
        h.append(f'<div class="rk-objekt"><img src="{pre}{m["karte"]}" alt="Gestaltung für {esc(p["kurzname"])}" loading="lazy"></div>')
    if m.get('icons'):
        # Icon-Set als schwebende Karte (Vorbild Behance: Icon-Raster neben dem Einsatz)
        h.append('<div class="rk-icons"><div class="rk-icons-raster">' + ''.join(f'<img src="{pre}{s}" alt="" loading="lazy">' for s in m['icons']) + '</div>'
                 + (f'<img class="rk-icons-bunt" src="{pre}{m["icons_bunt"]}" alt="" loading="lazy">' if m.get('icons_bunt') else '')
                 + f'<span>{esc(m.get("icons_titel", "Icons"))}</span></div>')
    if m.get('visitenkarte'):
        h.append(f'<div class="rk-visitenkarte"><img src="{pre}{m["visitenkarte"]}" alt="Visitenkarte für {esc(p["kurzname"])}" loading="lazy"><span>Print</span></div>')
    if m.get('magazin'):
        # Magazin im Querformat: Seiten blättern nacheinander um (js/menue.js)
        h.append('<div class="rk-magazin"><div class="rk-heft">' + ''.join(f'<img src="{pre}{s}" alt="" loading="lazy">' for s in m['magazin'])
                 + '</div><span>Unternehmenspräsentation · Magazin A4 quer</span></div>')
    if m.get('folien'):
        h.append('<div class="rk-folien">' + ''.join(f'<img src="{pre}{f}" alt="" loading="lazy">' for f in m['folien']) + '<span>Unternehmenspräsentation</span></div>')
    f = None if m.get('ohne_film') else p.get('film')
    if f:
        h.append(f'<button type="button" class="rk-schwebe rk-film film-knopf" data-film="{pre}{f["datei"]}" data-titel="{html.escape(f["titel"])}" aria-label="{html.escape(f["titel"])} ansehen">'
                 f'<span class="rk-film-bild"><img src="{pre}{f["vorschau"]}" alt="" loading="lazy"></span><b>Launch-Film ansehen</b><span>die neue Website im Film</span></button>')
    elif p.get('stimme') and not m.get('ohne_film'):
        s = next((x for x in STIMMEN if x['name'] == p['stimme']), None)
        if s:
            satz = re.sub(r'<[^>]+>', '', s['absaetze_html'][0])
            satz = satz[:satz.find('!') + 1] if '!' in satz[:200] else satz[:160].rsplit(' ', 1)[0] + ' …'
            bild = f'<img src="{pre}bilder/{s["bild"]}" alt="" loading="lazy">' if s.get('bild') else ''
            h.append(f'<div class="rk-schwebe">{bild}<b>{esc(s["name"])}</b><span>{s["rolle_html"]}</span><p>„{html.escape(satz, quote=False)}“</p></div>')
    return ''.join(h)


def referenz_karten(liste, pre, kennung='ref', ansicht=None):
    # ansicht (z. B. 'print'): eigenes Mockup je Leistungsseite, falls im Projekt hinterlegt (mockup_print)
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
        <div class="rk-buehne">{_mockup(p, pre, p.get(f'mockup_{ansicht}') if ansicht else None)}</div>
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
    # Je Zielgruppe zwei Karten (Anna 11.10.2026, Skizze): links das Angebot mit Unterzeile und Punkten, rechts breit die Referenz mit großem Screenshot
    felder = [
        ('mittelstand', 'Mittelstand', 'Ihre ganze Website, neu gedacht.',
         ('Website', paket['unternehmen']['name'], paket['unternehmen']['wer'],
          ['Design-System und neue Startseite', 'Leistungs-, Branchen- und Referenzseiten', 'Karrierebereich mit Stellenangeboten und Bewerbungsformular'],
          preis('unternehmen'), f'{pre}service/website/#pakete'),
         ('Wolfgang Bauer Ingenieurbau', 'Strategie, Rebranding, UX/UI Design, Website und Unternehmenspräsentation.', 'bauer-website.jpg', f'{pre}#referenzen')),
        ('selbststaendige', 'Selbstständige', 'Klar auftreten, ohne Umwege.',
         ('Website', paket['onepager']['name'], 'Für Selbstständige und kleine Angebote: eine Website, die alles auf den Punkt bringt, und eine Marke, die zu Ihnen passt.',
          ['Alles auf einer Seite, responsiv', 'Mit SEO & LLM-Zitierfähigkeit', f'Dazu buchbar: Brand Basic mit Fragebogen, Brand Experience und Mitbewerberrecherche, {preis("brand-0")}'],
          preis('onepager'), f'{pre}service/website/#pakete'),
         ('Deinetwegen', 'Branding, UI/UX Design und Website für eine HR-Beratung.', 'deinetwegen-website.jpg', f'{pre}#referenzen')),
        ('vereine', 'Vereine &amp; Kultur', 'Demokratie braucht Sichtbarkeit.',
         ('Aktion', 'Kostenfreie Website', 'Kostenfreie Websites für Vereine, NGOs, Kunst und Kultur. Du zahlst, was es dir wert ist.',
          ['Für Organisationen, die sich für Demokratie, Frauen- und Kinderrechte, Natur- und Tierschutz oder Kunst und Kultur einsetzen', 'Bis zu eine Website im Monat'],
          'kostenfrei', f'{pre}demokratie-braucht-sichtbarkeit/'),
         ('Jana Voigtmann', 'Webdesign für eine Künstlerin aus Leipzig.', 'jana-mixed-media.jpg?v=2', f'{pre}#referenzen')),
    ]
    TAB_AUS = ' tabindex="-1"'
    knoepfe = ''.join(f'<button type="button" role="tab" id="fw-r-{k}" aria-controls="fw-{k}" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else TAB_AUS}>{n}</button>' for i, (k, n, *_ ) in enumerate(felder))
    teile = []
    for i, (k, n, titel, (m, h, x, punkte, pr, l), (rn, rx, rb, rl)) in enumerate(felder):
        li = ''.join(f'<li>{p}</li>' for p in punkte)
        angebot = (f'<a class="dk-karte" href="{l}"><span class="meta">{m}</span><span class="dk-karte-titel">{esc(h)}</span>'
                   f'<span class="dk-karte-text">{esc(x)}</span><ul class="dk-punkte">{li}</ul><span class="dk-preis">{pr}</span></a>')
        referenz = (f'<a class="dk-karte dk-karte-ref" href="{rl}"><span class="dk-ref-text"><span class="meta">Referenz</span><span class="dk-karte-titel">{esc(rn)}</span>'
                    f'<span class="dk-karte-text">{esc(rx)}</span><span class="dk-preis">Projekt ansehen →</span></span>'
                    f'<span class="dk-bild"><img src="{pre}bilder/referenzen/{rb}" alt="" loading="lazy"></span></a>')
        teile.append(f'      <div class="dk-feld" id="fw-{k}" role="tabpanel" aria-labelledby="fw-r-{k}"{"" if i == 0 else " hidden"}>\n        <h3 class="dk-titel">{esc(titel)}</h3>\n'
                     f'        <div class="dk-karten">{angebot}{referenz}</div>\n      </div>')
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
      {f'<p><a class="button button-zweit" href="{link["url"]}" target="_blank" rel="noopener">Website ansehen ↗</a></p>' if link else ''}
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


def lesezeit(slug):
    # Lesezeit wie im Artikel angegeben („Lesezeit 18 Minuten“), sonst aus dem Text des Artikels, 200 Wörter pro Minute
    t = (basis / 'website' / 'blog' / slug / 'index.html').read_text(encoding='utf-8')
    m = re.search(r'Lesezeit (\d+) Minuten', t)
    if m: return int(m.group(1))
    a = re.search(r'<article.*?</article>', t, re.S)
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>|<[^>]+>', ' ', a.group(0) if a else t, flags=re.S)
    return max(1, round(len(re.findall(r'\w+', text)) / 200))


def blog(liste, pre, linkpre, h='h3', einrueck='    ', kategorie=True, klasse='blog-karte', lazy=True):
    # Ganze Karte anklickbar: der Link liegt auf dem Titel und spannt sich per CSS über die Karte (ein Link je Karte, gut für Tastatur und Screenreader)
    out = []
    for b in liste:
        u = f'{linkpre}{b["slug"]}/'
        kat = f'{einrueck}      <p class="kategorie">{esc(b["kategorie"])}</p>\n' if kategorie else ''
        laden = ' loading="lazy"' if lazy else ''
        out.append(f'''{einrueck}<li>
{einrueck}  <article class="{klasse}">
{einrueck}    <div class="blog-karte-bild"><img src="{pre}bilder/{b["bild"]}" alt="" width="{b["bild_b"]}" height="{b["bild_h"]}"{laden}></div>
{einrueck}    <div class="blog-karte-text">
{kat}{einrueck}      <{h}><a href="{u}">{b["titel_html"]}</a></{h}>
{einrueck}      <p class="artikel-meta"><time datetime="{b["datum"]}">{b["datum_text"]}</time> · {lesezeit(b["slug"])} Min. Lesezeit</p>
{einrueck}      <p class="blog-karte-teaser">{b["teaser_html"]}</p>
{einrueck}      <p class="weiterlesen" aria-hidden="true">Weiterlesen →</p>
{einrueck}    </div>
{einrueck}  </article>
{einrueck}</li>''')
    return '\n'.join(out)


def anker(name):
    return 'thema-' + re.sub(r'[^a-z0-9]+', '-', name.lower().replace('&', ' ')).strip('-')


def blog_themen():
    # Blog-Übersicht (Anna 13.10.2026): Chip-Leiste mit Themen und Anzahl, je Thema eine Überschrift mit Linie und eigene Kartenreihe.
    # Reihenfolge der Themen nach dem neuesten Beitrag; der neueste Beitrag steht groß als erste Karte seines Themas (kein Doppel)
    themen = []
    for b in BLOG:
        if b['kategorie'] not in themen: themen.append(b['kategorie'])
    gruppen = {k: [b for b in BLOG if b['kategorie'] == k] for k in themen}
    chips = ''.join(f'<a href="#{anker(k)}">{esc(k)} <span class="chip-zahl">{len(gruppen[k])}</span></a>' for k in themen)
    out = [f'  <nav class="preis-leiste lsx-chips blog-leiste" aria-label="Themen im Blog">\n    {chips}\n  </nav>']
    for i, k in enumerate(themen):
        zahl = f'{len(gruppen[k])} Beitrag' if len(gruppen[k]) == 1 else f'{len(gruppen[k])} Beiträge'
        karten = blog(gruppen[k][1:] if i == 0 else gruppen[k], '../', '', 'h3', '      ', kategorie=False)
        if i == 0:
            gross = blog(gruppen[k][:1], '../', '', 'h3', '      ', kategorie=False, klasse='blog-karte blog-karte-gross', lazy=False)
            gross = gross.replace('<li>', '<li class="blog-li-gross">', 1).replace('<div class="blog-karte-text">\n', '<div class="blog-karte-text">\n          <p class="kategorie">Neuester Beitrag</p>\n', 1)
            karten = gross + ('\n' + karten if karten else '')
        out.append(f'''  <section class="blog-thema" id="{anker(k)}" aria-labelledby="{anker(k)}-titel">
    <div class="blog-thema-kopf"><h2 id="{anker(k)}-titel">{esc(k)}</h2><p class="meta">{zahl}</p></div>
    <ul class="blog-liste">
{karten}
    </ul>
  </section>''')
    return '\n'.join(out)


def kennzahlen(klasse='fakten hero-fakten', einrueck='    '):
    z = []
    for k in ZAHLEN:
        if k.get('symbol') == 'ort':
            z.append(f'{einrueck}  <div><dt>{ORT}</dt><dd><span class="mit-liebe">{esc(k["text"])}</span></dd></div>')
        else:
            plus = f'<span class="fakt-plus">{k["zusatz"]}</span>' if k["zusatz"] else ''
            z.append(f'{einrueck}  <div><dt><span data-zaehlen="{k["zahl"]}">{k["zahl"]}</span>{plus}</dt><dd>{esc(k["text"])}</dd></div>')
    return f'{einrueck}<dl class="{klasse}">\n' + '\n'.join(z) + f'\n{einrueck}</dl>'


def oeko(pre):
    # Grafik Website-Ökosystem (Quelle: werkzeuge/grafiken/website-oekosystem.html, dort für Leistungsseiten mit ../../ geschrieben)
    return (basis / 'werkzeuge' / 'grafiken' / 'website-oekosystem.html').read_text(encoding='utf-8').replace('../../', pre).rstrip()


def einsetzen(text, name, inhalt):
    neu, n = re.subn(rf'<!-- {name}:START -->.*?<!-- {name}:ENDE -->', lambda m: f'<!-- {name}:START -->\n{inhalt}\n<!-- {name}:ENDE -->', text, count=1, flags=re.S)
    if not n: raise SystemExit(f'Marker {name} fehlt')
    return neu


if __name__ == '__main__':
    seiten = {
        'index.html': [('PROJEKTE', lambda: referenz_karten(PROJEKTE, '', 'start')), ('FUERWEN', lambda: fuer_wen('')), ('STIMMEN', lambda: stimmen(STIMMEN, '')),
                       ('BLOG', lambda: blog(BLOG[:4], '', 'blog/')), ('KENNZAHLEN', lambda: kennzahlen())],
        'profil/index.html': [('STIMMEN', lambda: stimmen(STIMMEN, '../')), ('BLOG', lambda: blog(BLOG[:4], '../', '../blog/')),
                              ('KENNZAHLEN', lambda: kennzahlen('fakten', '      '))],
        'blog/index.html': [('BLOG', lambda: blog_themen())],
    }
    for datei, teile in seiten.items():
        p = basis / 'website' / datei
        t = p.read_text(encoding='utf-8')
        for name, f in teile: t = einsetzen(t, name, f())
        p.write_text(t, encoding='utf-8')
    print('Projekte, Stimmen, Blog und Kennzahlen geschrieben')
