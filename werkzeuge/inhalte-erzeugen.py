# Erzeugt wiederkehrende Inhalte aus werkzeuge/inhalte/*.json (Projekte, Kundenstimmen, Blogartikel, Kennzahlen)
# und setzt sie zwischen die Marker <!-- NAME:START --> … <!-- NAME:ENDE --> der Seiten.
# Jeder Eintrag hat Schlagworte (tags), z. B. "website", "brand", "ui-ux"; die Leistungsseiten wählen danach aus.
# Neuer Eintrag: in die passende Datei schreiben, dann  python3 werkzeuge/inhalte-erzeugen.py  (und danach leistungsseiten.py)
import datetime, html, json, pathlib, re

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



# --- Projekt-Titelbild (Cover) wie bei Behance (Anna 14.10.2026): Fläche in der Hausfarbe des Kunden, oben eine Kopfzeile
#     „Kunde · Leistung · Jahr“ (redaktioneller Rahmen), Geräte gerade gestellt, bei allen Projekten gleiche Machart.
#     Beim Überfahren scrollt der Bildschirm langsam nach unten (nur ohne „Bewegung reduzieren“).
def cover(p, pre, c=None, kopfzeile=True):
    c, h = c or p['cover'], []
    if kopfzeile:
        h.append(f'<p class="pc-zeile" aria-hidden="true"><span>{esc(p["kurzname"])}</span><span>{esc(p["kopf"])}</span><span>{esc(p["jahr"])}</span></p>')
    if c.get('desktop'):
        h.append(f'<span class="pc-desktop"><img src="{pre}{c["desktop"]}" alt="" loading="lazy"></span>')
    if c.get('handy'):
        h.append(f'<span class="pc-handy"><img src="{pre}{c["handy"]}" alt="" loading="lazy"></span>')
    if c.get('bild'):
        h.append(f'<span class="pc-bild"><img src="{pre}{c["bild"]}" alt="" loading="lazy"></span>')
    art = ' pc-mit-handy' if c.get('handy') else ''
    return f'<span class="pc pc-{c.get("ton", "dunkel")}{art}" style="--pc-farbe: {c["farbe"]}">{"".join(h)}</span>'


def projekt_link(p, pre):
    # Projekte mit eigener Seite verlinken dorthin, alle anderen auf die Website der Kundin
    if p.get('case'):
        return f'{pre}referenzen/{p["slug"]}/', 'Projekt ansehen <span aria-hidden="true">→</span>', ''
    l = p['links'][0]
    return l['url'], f'{esc(l["text"])} <span aria-hidden="true">↗</span>', ' target="_blank" rel="noopener"'


def projekt_karte(p, pre, ansicht=None, h='h3'):
    url, text, ziel = projekt_link(p, pre)
    c = p.get(f'cover_{ansicht}') if ansicht else None
    return (f'<article class="pk">\n'
            f'          <a class="pk-bild" href="{url}"{ziel} tabindex="-1" aria-hidden="true">{cover(p, pre, c)}</a>\n'
            f'          <{h} class="pk-name"><a href="{url}"{ziel}>{esc(p["kurzname"])}</a></{h}>\n'
            f'          <p class="pk-satz">{esc(p["satz"])}</p>\n'
            f'          <p class="pk-link"><a class="textlink" href="{url}"{ziel}>{text}</a></p>\n'
            f'        </article>')


def referenz_karten(liste, pre, kennung='ref', ansicht=None):
    # Karussell (Startseite, Leistungsseiten): ein Projekt pro Blatt, großes Titelbild, darunter Name, ein Satz, Link
    karten = [projekt_karte(p, pre, ansicht) for p in liste]
    if len(karten) == 1:
        return '    <div class="pk-einzeln">\n        ' + karten[0] + '\n    </div>'
    return (f'    <div class="ks" data-karussell id="{kennung}-karussell">\n      <div class="ks-spur" aria-live="polite">\n        ' + '\n        '.join(karten) + '\n      </div>\n'
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
         # Kostenrechner v4 (Anna 16.10.2026): Paket „Redesign für Unternehmen“ gestrichen, die Karte zeigt das Redesign; Text der Karte bleibt
         ('Webdesign', paket['redesign']['name'], 'Für mittelständische Unternehmen, die ihre ganze Website umbauen: mit Leistungs-, Branchen-, Referenz- und Karriereseiten.',
          ['Design-System und neue Startseite', 'Leistungs-, Branchen- und Referenzseiten', 'Karrierebereich mit Stellenangeboten und Bewerbungsformular'],
          preis('redesign'), f'{pre}service/webdesign/#pakete'),
         ('Wolfgang Bauer Ingenieurbau', f'{pre}referenzen/bauer/'), 'bilder/fuer-wen-mittelstand.webp', 'review'),
        ('selbststaendige', 'Selbstständige', 'Klar auftreten, ohne Umwege.',
         ('Webdesign', 'Onepager', 'Für Selbstständige und kleine Angebote: eine Website, die alles auf den Punkt bringt, und eine Marke, die zu Ihnen passt.',
          ['Alles auf einer Seite, responsiv', 'Mit SEO & LLM-Zitierfähigkeit', f'Dazu buchbar: Brand Basic mit Fragebogen, Brand Experience und Mitbewerberrecherche, {preis("brand-0")}'],
          preis('neu'), f'{pre}service/webdesign/#pakete'),
         ('Deinetwegen', f'{pre}referenzen/deinetwegen/'), 'bilder/fuer-wen-selbststaendige.webp', 'rechner'),
        ('vereine', 'Vereine &amp; Kultur', 'Demokratie braucht Sichtbarkeit.',
         ('Initiative', 'Website ohne Honorar', 'Für Vereine, NGOs, Kunst und Kultur. Ihr zahlt, was ihr könnt – weniger oder nichts ist auch in Ordnung.',
          ['Für Organisationen, die sich für Demokratie, Frauen- und Kinderrechte, Natur- und Tierschutz oder Kunst und Kultur einsetzen',
           'Bis zu eine Website im Monat'],
          'Richtwert ab 250 € <small>Onepager · etwa 500 € Vereinswebsite</small>', f'{pre}demokratie-braucht-sichtbarkeit/'),
         ('Jana Voigtmann', f'{pre}referenzen/jana-voigtmann/'), 'bilder/programm-haende.jpg', 'initiative'),
    ]
    TAB_AUS = ' tabindex="-1"'
    knoepfe = ''.join(f'<button type="button" role="tab" id="fw-r-{k}" aria-controls="fw-{k}" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else TAB_AUS}>{n}</button>' for i, (k, n, *_ ) in enumerate(felder))
    teile = []
    # Angebot im Mittelpunkt (Anna 16.10.2026): eine Karte mit eigenem Bild je Zielgruppe; Referenz nur als kleiner Link (Referenzen stehen weiter unten)
    for i, (k, n, titel, (m, h, x, punkte, pr, l), (rn, rl), bild, knopf) in enumerate(felder):
        li = ''.join(f'<li>{p}</li>' for p in punkte)
        # Handlungsaufforderung je Zielgruppe (Anna 16.10.2026): Mittelstand zuerst Website-Review, Selbstständige zuerst Kostenrechner
        pfeil = ' <span aria-hidden="true">→</span>'
        ziele = {'review': (f'{pre}website-review/', 'Kostenloses Website-Review'), 'rechner': (f'{pre}preise/#rechner', 'Kosten berechnen'), 'initiative': (l, 'Zur Initiative')}
        reihen = {'review': ['review', 'rechner'], 'rechner': ['rechner', 'review'], 'initiative': ['initiative']}[knopf]
        haupt, *neben = [ziele[r] for r in reihen]
        aktionen = f'<a class="button" href="{haupt[0]}">{haupt[1]}{pfeil}</a>' + ''.join(f'<a class="textlink" href="{u}">{t}{pfeil}</a>' for u, t in neben)
        angebot = (f'<div class="dk-angebot"><div class="dk-angebot-text"><p class="meta">{m}</p><h4 class="dk-karte-titel"><a href="{l}">{esc(h)}</a></h4>'
                   f'<p class="dk-karte-text">{esc(x)}</p><ul class="dk-punkte">{li}</ul>'
                   f'<p class="dk-preis">{pr}</p><p class="dk-aktionen">{aktionen}</p></div>'
                   f'<div class="dk-angebot-bild{"" if bild.endswith(".jpg") else " dk-grafik"}"><img src="{pre}{bild}" alt="" loading="lazy" width="1200" height="900"></div></div>'
                   f'<p class="dk-beleg">{"Aus Kunst und Kultur:" if k == "vereine" else "Zum Beispiel umgesetzt für"} <a href="{rl}">{esc(rn)} <span aria-hidden="true">→</span></a></p>')
        teile.append(f'      <div class="dk-feld" id="fw-{k}" role="tabpanel" aria-labelledby="fw-r-{k}"{"" if i == 0 else " hidden"}>\n        <h3 class="dk-titel">{esc(titel)}</h3>\n'
                     f'        {angebot}\n      </div>')
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


# Blog-Kategorien = Leistungen (Anna 13.10.2026), in dieser Reihenfolge; Kategorien ohne Beitrag werden ausgeblendet, bis einer da ist
BLOG_KATEGORIEN = ['Markenbildung', 'UI/UX', 'Webdesign', 'Marketing & Vertrieb']


def blog_themen():
    # Blog-Übersicht (Anna 13.10.2026): oben „Aktuelles“ mit den 3 neuesten Beiträgen (der neueste groß),
    # darunter die Kategorien mit Überschrift und Linie; Chip-Leiste mit Anzahl je Kategorie
    fremd = sorted({b['kategorie'] for b in BLOG} - set(BLOG_KATEGORIEN))
    if fremd: raise SystemExit(f'Unbekannte Blog-Kategorie in blog.json: {fremd}')
    gruppen = {k: [b for b in BLOG if b['kategorie'] == k] for k in BLOG_KATEGORIEN}
    themen = [k for k in BLOG_KATEGORIEN if gruppen[k]]
    chips = '<a href="#aktuelles">Aktuelles</a>' + ''.join(f'<a href="#{anker(k)}">{esc(k)} <span class="chip-zahl">{len(gruppen[k])}</span></a>' for k in themen)
    gross = blog(BLOG[:1], '../', '', 'h3', '      ', klasse='blog-karte blog-karte-gross', lazy=False).replace('<li>', '<li class="blog-li-gross">', 1)
    out = [f'  <nav class="preis-leiste lsx-chips blog-leiste" aria-label="Kategorien im Blog">\n    {chips}\n  </nav>',
           f'''  <section class="blog-thema blog-aktuell" id="aktuelles" aria-labelledby="aktuelles-titel">
    <div class="blog-thema-kopf"><h2 id="aktuelles-titel">Aktuelles</h2><p class="meta">Die neuesten Beiträge</p></div>
    <ul class="blog-liste">
{gross}
{blog(BLOG[1:3], '../', '', 'h3', '      ')}
    </ul>
  </section>''']
    for k in themen:
        zahl = f'{len(gruppen[k])} Beitrag' if len(gruppen[k]) == 1 else f'{len(gruppen[k])} Beiträge'
        out.append(f'''  <section class="blog-thema" id="{anker(k)}" aria-labelledby="{anker(k)}-titel">
    <div class="blog-thema-kopf"><h2 id="{anker(k)}-titel">{esc(k)}</h2><p class="meta">{zahl}</p></div>
    <ul class="blog-liste">
{blog(gruppen[k], '../', '', 'h3', '      ', kategorie=False)}
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
            # "seit": Jahre aus dem Startjahr berechnen (Anna 16.10.2026: selbstständig seit 2020) – zählt bei jedem Erzeugen von selbst weiter
            zahl = datetime.date.today().year - k['seit'] if 'seit' in k else k['zahl']
            text = k['text'].replace('{seit}', str(k.get('seit', '')))
            z.append(f'{einrueck}  <div><dt><span data-zaehlen="{zahl}">{zahl}</span>{plus}</dt><dd>{esc(text)}</dd></div>')
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
        'index.html': [('PROJEKTE', lambda: referenz_karten([x for x in PROJEKTE if x.get('case')], '', 'start')), ('FUERWEN', lambda: fuer_wen('')), ('STIMMEN', lambda: stimmen(STIMMEN, '')),
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
