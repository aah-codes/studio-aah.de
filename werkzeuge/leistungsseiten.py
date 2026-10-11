# Erzeugt die Leistungsunterseiten (service/…/index.html) aus werkzeuge/leistungen-inhalte.json (Texte, FAQ)
# und werkzeuge/preise-daten.json (Pakete, Preise, Zusatzleistungen). Kopf und Fuß bleiben aus der bestehenden Seite erhalten.
# Aufruf im Repository-Ordner:  python3 werkzeuge/leistungsseiten.py [id …]   (ohne id: alle)
import html, importlib.util, json, pathlib, re, sys

basis = pathlib.Path(__file__).resolve().parent.parent
preise = json.loads((basis / 'werkzeuge' / 'preise-daten.json').read_text(encoding='utf-8'))
inhalte = json.loads((basis / 'werkzeuge' / 'leistungen-inhalte.json').read_text(encoding='utf-8'))
esc = lambda s: html.escape(s, quote=False)
_spec = importlib.util.spec_from_file_location('inhalte', basis / 'werkzeuge' / 'inhalte-erzeugen.py')
I = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(I)
GEMEINSAM = json.loads((basis / 'werkzeuge' / 'inhalte' / 'faq-gemeinsam.json').read_text(encoding='utf-8'))['faq']
euro = lambda n: f"{n:,}".replace(',', '.') + '&nbsp;€'


TERMINE = 'Einmal pro Woche einen Termin, 45 Minuten, online über Google Meet oder Teams, je nachdem, was Sie brauchen.'
NETTO = '<small class="lsx-netto">netto</small>'
# Hinweis im Kleingedruckten unter Karten, Tabelle und Zusatzleistungen (B2B: Nettopreise, Umsatzsteuer kommt dazu)
NETTO_HINWEIS = '<p class="lsx-klein">Alle Preise sind Nettopreise zzgl. 19&nbsp;% Umsatzsteuer (USt.).</p>'


def preis(e):
    if e.get('anfrage'): return 'auf Anfrage'
    if e.get('anteil'): return f"+{int(e['anteil'] * 100)}&nbsp;% {NETTO}"
    if e.get('monat'): return f"ab {euro(e['monat'])} {NETTO} / Monat"
    if e.get('stunde'): return f"ab {euro(e['stunde'])} {NETTO} / Stunde"
    return ('ab ' if e.get('ab', True) else '') + euro(e['preis']) + ' ' + NETTO


def karten(g):
    out = []
    for e in g['pakete']:
        liste = ''.join(f'<li>{esc(x)}</li>' for x in e.get('items', []))
        out.append(f'''      <article class="lsx-karte{' lsx-gefragt' if e.get('gefragt') else ''}">
        {'<p class="lsx-badge">Gefragt</p>' if e.get('gefragt') else ''}<h3 class="lsx-karte-name">{esc(e['name'])}</h3>
        <p class="lsx-karte-preis">{preis(e)}</p>
        {f'<p class="lsx-karte-wer">{esc(e["wer"])}</p>' if e.get('wer') else ''}
        {f'<p class="lsx-karte-dauer"><span class="meta">Dauer</span> {esc(e["dauer"])}</p>' if e.get('dauer') else ''}
        {f'<p class="lsx-karte-plus">{esc(e["plus"])}</p>' if e.get('plus') else ''}<ul class="lsx-karte-liste">{liste}</ul>
      </article>''')
    return '\n'.join(out)


def vergleich(g):
    pakete = [e for e in g['pakete'] if e.get('items')]  # Einzelleistungen ohne Inhaltsliste (z. B. Logo einzeln) nicht in die Tabelle
    # Tabelle nur, wenn Pakete aufeinander aufbauen („Alles aus …“); einzeln buchbare Leistungen vergleicht man nicht
    if len(pakete) < 2 or not any((e.get('plus') or '').startswith('Alles aus') for e in pakete): return ''
    # Zeilen: alle Leistungen in Reihenfolge; ein Paket „enthält“ alle Zeilen der vorherigen Pakete, wenn es mit „Alles aus …“ beginnt
    zeilen, hat = [], []
    for i, e in enumerate(pakete):
        erbt = (e.get('plus') or '').startswith('Alles aus')
        eigene = set(e.get('items', []))
        for x in e.get('items', []):
            if x not in zeilen: zeilen.append(x)
        hat.append((erbt, eigene))
    def zelle(i, x):
        erbt, eigene = hat[i]
        if x in eigene: return True
        if erbt: return any(zelle(j, x) for j in range(i))
        return False
    kopf = ''.join(f'<th scope="col">{esc(e["name"])}<span>{preis(e)}</span></th>' for e in pakete)
    JA = '<span class="lsx-ja" aria-label="enthalten">✓</span>'
    NEIN = '<span class="lsx-nein" aria-label="nicht enthalten">–</span>'
    rumpf = ''.join('<tr><th scope="row">' + esc(x) + '</th>' + ''.join('<td>' + (JA if zelle(i, x) else NEIN) + '</td>' for i in range(len(pakete))) + '</tr>' for x in zeilen)
    if any(e.get('dauer') for e in pakete):
        rumpf = '<tr><th scope="row">Dauer</th>' + ''.join('<td>' + esc(e.get('dauer', '–')) + '</td>' for e in pakete) + '</tr>' + rumpf
    return f'''  <section class="lsx-vergleich" id="vergleich" aria-labelledby="vergleich-titel">
    <h2 class="gr-h3" id="vergleich-titel">Vergleich</h2>
    <div class="lsx-tabelle-rahmen"><table class="lsx-tabelle"><thead><tr><th scope="col">Leistung</th>{kopf}</tr></thead><tbody>{rumpf}</tbody></table></div>
    {NETTO_HINWEIS}
  </section>'''


def extras(g):
    ex = [e for e in g.get('extras', []) if not e.get('auto')]  # Launch ist bei jeder Website dabei, keine Zusatzleistung
    if not ex: return ''
    li = ''.join(f'<li><span class="lsx-extra-name">{esc(e["name"])}</span><span class="lsx-extra-text">{esc(e.get("kurz") or e.get("wer") or "")}</span><span class="lsx-extra-preis">{preis(e)}</span></li>' for e in ex)
    return f'''  <section class="lsx-extras" id="extras" aria-labelledby="extras-titel">
    <h2 class="gr-h3" id="extras-titel">Zusatzleistungen</h2>
    <ul class="lsx-extra-liste">{li}</ul>
    {NETTO_HINWEIS}
  </section>'''


START = (basis / 'website' / 'index.html').read_text(encoding='utf-8')


def ablauf_eigen(pre, schritte):
    li = ''.join(f'<li><span class="pz-nr">{i:02d}</span><span class="meta">{esc(m)}</span><h3>{esc(h)}</h3><p class="gedaempft">{esc(x)}</p></li>' for i, (m, h, x) in enumerate(schritte, 1))
    return (f'  <section class="prozess-kompakt" id="ablauf" aria-labelledby="prozess">\n    <p class="meta">Wie ich arbeite</p>\n    <h2 class="preis-h2" id="prozess">Prozess</h2>\n'
            f'    <ol class="pz-schritte">{li}</ol>\n    <p><a class="button" href="{pre}kontakt/">Projekt anfragen <span aria-hidden="true">→</span></a></p>\n  </section>')


def ablauf(pre):
    m = re.search(r'<section class="prozess-kompakt".*?</section>', START, re.S)
    s = m.group(0).replace('href="kontakt/"', f'href="{pre}kontakt/"')
    return '  ' + s.replace('<section class="prozess-kompakt"', '<section class="prozess-kompakt" id="ablauf"', 1)


def stimmen(pre, tag):
    liste = I.mit_tag(I.STIMMEN, [tag])[:3]
    if not liste: return ''
    return '  <section class="lsx-stimmen" aria-labelledby="stimmen-titel">\n    <p class="meta">Stimmen</p>\n    <h2 class="gr-h3" id="stimmen-titel">Das sagen Kundinnen und Kolleginnen</h2>\n    <div class="stimmen">\n' + I.stimmen(liste, pre) + '\n    </div>\n  </section>'


def fakten(pre):
    return I.kennzahlen('fakten lsx-fakten', '    ')


def nicht_enthalten(c):
    if not c.get('nicht_enthalten'): return ''
    li = ''.join(f'<li>{esc(x)}</li>' for x in c['nicht_enthalten'])
    return f'<div class="lsx-nicht"><p class="meta">Nicht enthalten</p><ul>{li}</ul></div>'


def referenzen(tag, pre):
    liste = I.mit_tag(I.PROJEKTE, [tag])
    if not liste: return ''
    return '  <section class="lsx-referenzen" id="referenzen" aria-labelledby="referenzen-titel">\n    <p class="meta">Referenzen</p>\n    <h2 class="gr-h3" id="referenzen-titel">Projekte aus diesem Bereich</h2>\n    <div class="referenzen">\n' + I.projekte(liste, pre) + '\n    </div>\n  </section>'


def artikel(pre, tag):
    liste = I.mit_tag(I.BLOG, [tag])[:3]
    if not liste: return ''
    return '  <section class="lsx-artikel blog-neu" id="artikel" aria-labelledby="artikel-titel">\n    <div class="lsx-artikel-kopf"><p class="meta">Blog</p><h2 class="gr-h3" id="artikel-titel">Passende Artikel</h2></div>\n    <ul class="blog-liste">\n' + I.blog(liste, pre, pre + 'blog/') + '\n    </ul>\n  </section>'


def direkt(pre):
    return f'''  <section class="lsx-direkt" aria-labelledby="direkt-titel">
    <img src="{pre}bilder/studio-aah-gruenderin-anna-haertelt.webp" alt="Anna Härtelt, Gründerin von STUDIO AAH!" width="768" height="1024" loading="lazy">
    <div>
      <p class="meta">Ihre Ansprechpartnerin</p>
      <h2 class="gr-h3" id="direkt-titel">Sie arbeiten direkt mit mir.</h2>
      <p>Bei STUDIO AAH! arbeiten Sie direkt mit mir, von der ersten Idee bis zum Launch. Ich bin Anna Härtelt, UX/UI-Designerin, Strategin und Webentwicklerin.</p>
      <p><a class="textlink" href="{pre}profil/">Mehr über mich</a></p>
    </div>
  </section>'''


def seite(key, c):
    g = next(x for x in preise['gruppen'] if x['id'] == c['gruppe'])
    # Mehrere Seiten teilen sich eine Gruppe (zusatz): nur die genannten Pakete, eigener Einleitungssatz;
    # „paket_extra“ ergänzt die Paketdaten nur für diese Seite (z. B. Stundensatz statt „auf Anfrage“)
    if c.get('pakete'):
        g = {**g, 'pakete': [{**e, **c.get('paket_extra', {})} for e in g['pakete'] if e['id'] in c['pakete']], 'extras': []}
    intro = c.get('intro') or g['intro']
    # Der Prozess der Startseite beschreibt Website-Projekte; andere Leistungen brauchen eigene Schritte (noch offen)
    mit_ablauf = bool(c.get('ablauf_schritte')) or c.get('ablauf', c['gruppe'] == 'website')
    # Abstimmungstermine (Anna, 11.10.2026): im Projekt wöchentlich, bei laufender Betreuung seltener
    termine = c.get('termine', TERMINE)
    satz = termine if termine.startswith('Termine') else termine[0].lower() + termine[1:]  # Substantiv bleibt groß
    faq_termine = [['Wie oft gibt es bei STUDIO AAH! Abstimmungstermine?', 'Bei STUDIO AAH! gibt es ' + satz + ('' if 'nach Absprache' in termine else ' Weitere Termine vereinbaren wir nach Absprache.')]]
    pfad = basis / 'website' / c['pfad'] / 'index.html'
    if not pfad.exists():  # neue Seite: Kopf und Fuß von der Website-Seite übernehmen (gleiche Ordnertiefe)
        pfad.parent.mkdir(parents=True, exist_ok=True)
        pfad.write_text((basis / 'website' / 'service' / 'website' / 'index.html').read_text(encoding='utf-8'), encoding='utf-8')
    t = pfad.read_text(encoding='utf-8')
    tiefe = c['pfad'].strip('/').count('/') + 1
    pre = '../' * tiefe
    url = 'https://studio-aah.de/' + c['pfad']
    absatz = ''.join(f'<p>{esc(a)}</p>' for a in c['zusammenfassung'])
    faq = ''.join(f'''      <details class="faq-eintrag">
        <summary>{esc(q)}</summary>
        <div class="faq-antwort"><p>{esc(a)}</p></div>
      </details>
''' for q, a in c['faq'] + faq_termine + GEMEINSAM)
    main = f'''<main id="inhalt">

  <section class="seitenkopf lsx-kopf">
    <p class="meta"><a href="{pre}#leistungen">Leistungen</a> / {esc(c['titel'])}</p>
    <h1 class="gr-xxl"><span class="wort-mit-icon">{esc(c['titel'])}<img class="icon-3d" src="{pre}{c['icon']}" alt="" width="400" height="400"></span></h1>
    <p class="alt-klein">{esc(intro)}</p>
    <p class="lsx-termine"><span class="meta">So arbeite ich</span> {esc(termine)}</p>
    {fakten(pre)}
  </section>

  <nav class="preis-leiste lsx-chips" aria-label="Auf dieser Seite"><a href="#loesung">Problem &amp; Lösung</a><a href="#pakete">Pakete</a>{'<a href="#vergleich">Vergleich</a>' if vergleich(g) else ''}{'<a href="#extras">Zusatzleistungen</a>' if g.get('extras') else ''}{'<a href="#ablauf">Ablauf</a>' if mit_ablauf else ''}{'<a href="#referenzen">Referenzen</a>' if I.mit_tag(I.PROJEKTE, [c['tag']]) else ''}{'<a href="#artikel">Artikel</a>' if I.mit_tag(I.BLOG, [c['tag']]) else ''}<a href="#faq">Fragen</a><a href="{pre}preise/#r-{g['id']}">Kostenrechner →</a></nav>

  <section class="lsx-loesung" id="loesung" aria-labelledby="loesung-titel">
    <div class="lsx-loesung-text">
      <p class="meta">Problem &amp; Lösung</p>
      <h2 class="gr-h3" id="loesung-titel">{esc(c['problem_titel'])}</h2>
      {absatz}
      {'' if c.get('grafik') == 'corporate-identity' else f'<p class="lsx-grundsatz"><a class="textlink" href="{pre}service/brand/#corporate-identity">Grundlage für alles, was ich gestalte: das Rad der Corporate Identity <span aria-hidden="true">→</span></a></p>'}
      <p class="lsx-knoepfe"><a class="button" href="{pre}kontakt/">Projekt anfragen</a> <a class="textlink" href="{pre}preise/#r-{g['id']}">Kosten berechnen <span aria-hidden="true">→</span></a></p>
    </div>
    <div class="lsx-gegenueber">
      <div class="lsx-spalte lsx-schlecht"><p class="meta">Woran es oft hakt</p><ul>{''.join(f'<li>{esc(x)}</li>' for x in c['probleme'])}</ul></div>
      <div class="lsx-spalte lsx-gut"><p class="meta">So mache ich es</p><ul>{''.join(f'<li>{esc(x)}</li>' for x in c['loesungen'])}</ul></div>
    </div>
  </section>

{(basis / 'werkzeuge' / 'grafiken' / (c['grafik'] + '.html')).read_text(encoding='utf-8') if c.get('grafik') else ''}
{(basis / 'werkzeuge' / 'grafiken' / (c['nutzen'] + '.html')).read_text(encoding='utf-8') if c.get('nutzen') else ''}

  <section class="lsx-pakete" id="pakete" aria-labelledby="pakete-titel">
    <p class="meta">Pakete</p>
    <h2 class="gr-h3" id="pakete-titel">Pakete im Überblick</h2>
    {f'<p class="lsx-hinweis">{esc(g["hinweis"])}</p>' if g.get('hinweis') else ''}
    <div class="lsx-karten">
{karten(g)}
    </div>
    {NETTO_HINWEIS}
    {nicht_enthalten(c)}
  </section>

{vergleich(g)}

{extras(g)}

{(ablauf_eigen(pre, c['ablauf_schritte']) if c.get('ablauf_schritte') else ablauf(pre)) if mit_ablauf else ''}

{stimmen(pre, c['tag'])}

{referenzen(c['tag'], pre)}

{direkt(pre)}

  <section class="lsx-rechner" aria-labelledby="rechner-hinweis">
    <div>
      <p class="meta">Kostenrechner</p>
      <h2 class="gr-h3" id="rechner-hinweis">Was kostet Ihr Projekt?</h2>
      <p>Stellen Sie sich Ihre Pakete und Zusatzleistungen selbst zusammen und erhalten Sie sofort einen unverbindlichen Kostenvoranschlag, als PDF oder per E-Mail.</p>
    </div>
    <a class="button" href="{pre}preise/#r-{g['id']}">Zum Kostenrechner <span aria-hidden="true">→</span></a>
  </section>

{artikel(pre, c['tag'])}

  <section class="faq" id="faq" aria-labelledby="faq-titel">
    <h2 class="gr-h2" id="faq-titel">Häufige Fragen</h2>
    <div class="faq-liste">
{faq}    </div>
    <p class="faq-mehr">Noch Fragen? Ich freue mich auf Ihre Nachricht. <a class="textlink" href="{pre}kontakt/">Kontakt</a></p>
  </section>

</main>'''
    t = re.sub(r'<main id="inhalt">.*?</main>', lambda m: main, t, count=1, flags=re.S)
    t = re.sub(r'<title>.*?</title>', f'<title>{esc(c["seitentitel"])}</title>', t, count=1)
    for name in ('name="description"', 'property="og:description"'):
        t = re.sub(rf'<meta {name} content="[^"]*">', f'<meta {name} content="{html.escape(c["beschreibung"])}">', t, count=1)
    t = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', t, count=1)
    t = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', t, count=1)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(c["seitentitel"])}">', t, count=1)
    # Strukturierte Daten: Leistung mit Angeboten und FAQ (für Suchmaschinen und KI-Antworten)
    studio = re.search(r'\{\s*"@type": "ProfessionalService".*?"areaServed": \[[^\]]*\]\s*\}', t, re.S)
    angebote = [{"@type": "Offer", "name": e['name'], "priceCurrency": "EUR", "price": str(e['preis']),
                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": e['preis'], "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}
                for e in g['pakete'] if e.get('preis')]
    angebote += [{"@type": "Offer", "name": e['name'], "priceCurrency": "EUR",
                  "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": e['stunde'], "priceCurrency": "EUR", "unitText": "Stunde", "valueAddedTaxIncluded": False}}
                 for e in g['pakete'] if e.get('stunde') and not e.get('preis')]
    graph = [json.loads(studio.group(0)) if studio else {"@id": "https://studio-aah.de/#studio"},
             {"@type": "Service", "@id": url + '#leistung', "name": c['titel'], "description": intro, "url": url,
              "provider": {"@id": "https://studio-aah.de/#studio"}, "areaServed": "Leipzig", "offers": angebote},
             {"@type": "FAQPage", "@id": url + '#faq', "url": url, "inLanguage": "de",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faq'] + faq_termine + GEMEINSAM]}]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: f'<script type="application/ld+json">\n{ld}\n  </script>', t, count=1, flags=re.S)
    if 'zaehlen.js' not in t:
        t = t.replace('</body>', f'  <script src="{pre}js/zaehlen.js?v=20261012w" defer></script>\n</body>', 1)
    pfad.write_text(t, encoding='utf-8')
    print('geschrieben:', c['pfad'])


wahl = sys.argv[1:] or [k for k in inhalte if not k.startswith('_')]
for k in wahl: seite(k, inhalte[k])
