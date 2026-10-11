# Erzeugt die Leistungsunterseiten (service/…/index.html) aus werkzeuge/leistungen-inhalte.json (Texte, FAQ)
# und werkzeuge/preise-daten.json (Pakete, Preise, Zusatzleistungen). Kopf und Fuß bleiben aus der bestehenden Seite erhalten.
# Aufruf im Repository-Ordner:  python3 werkzeuge/leistungsseiten.py [id …]   (ohne id: alle)
import html, json, pathlib, re, sys

basis = pathlib.Path(__file__).resolve().parent.parent
preise = json.loads((basis / 'werkzeuge' / 'preise-daten.json').read_text(encoding='utf-8'))
inhalte = json.loads((basis / 'werkzeuge' / 'leistungen-inhalte.json').read_text(encoding='utf-8'))
esc = lambda s: html.escape(s, quote=False)
euro = lambda n: f"{n:,}".replace(',', '.') + '&nbsp;€'


def preis(e):
    if e.get('anfrage'): return 'auf Anfrage'
    if e.get('anteil'): return f"+{int(e['anteil'] * 100)}&nbsp;%"
    if e.get('monat'): return f"ab {euro(e['monat'])} / Monat"
    return ('ab ' if e.get('ab', True) else '') + euro(e['preis'])


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
    pakete = g['pakete']
    if len(pakete) < 2: return ''
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
  </section>'''


def extras(g):
    ex = [e for e in g.get('extras', [])]
    if not ex: return ''
    li = ''.join(f'<li><span class="lsx-extra-name">{esc(e["name"])}</span><span class="lsx-extra-text">{esc(e.get("kurz") or e.get("wer") or "")}</span><span class="lsx-extra-preis">{preis(e)}</span></li>' for e in ex)
    return f'''  <section class="lsx-extras" id="extras" aria-labelledby="extras-titel">
    <h2 class="gr-h3" id="extras-titel">Zusatzleistungen</h2>
    <ul class="lsx-extra-liste">{li}</ul>
  </section>'''


START = (basis / 'website' / 'index.html').read_text(encoding='utf-8')


def ablauf(pre):
    m = re.search(r'<section class="prozess-kompakt".*?</section>', START, re.S)
    s = m.group(0).replace('href="kontakt/"', f'href="{pre}kontakt/"')
    return '  ' + s.replace('<section class="prozess-kompakt"', '<section class="prozess-kompakt" id="ablauf"', 1)


def stimmen(pre, namen):
    if not namen: return ''
    teile = re.findall(r'      <article class="stimme.*?</article>', START, re.S)
    gew = [x for x in teile if any(n in x for n in namen)]
    if not gew: return ''
    gew = [x.replace('src="bilder/', f'src="{pre}bilder/') for x in gew]
    return '  <section class="lsx-stimmen" aria-labelledby="stimmen-titel">\n    <p class="meta">Stimmen</p>\n    <h2 class="gr-h3" id="stimmen-titel">Das sagen Kundinnen und Kolleginnen</h2>\n    <div class="stimmen">\n' + '\n'.join(gew) + '\n    </div>\n  </section>'


def seite(key, c):
    g = next(x for x in preise['gruppen'] if x['id'] == c['gruppe'])
    pfad = basis / 'website' / c['pfad'] / 'index.html'
    t = pfad.read_text(encoding='utf-8')
    tiefe = c['pfad'].strip('/').count('/') + 1
    pre = '../' * tiefe
    url = 'https://studio-aah.de/' + c['pfad']
    absatz = ''.join(f'<p>{esc(a)}</p>' for a in c['zusammenfassung'])
    faq = ''.join(f'''      <details class="faq-eintrag">
        <summary>{esc(q)}</summary>
        <div class="faq-antwort"><p>{esc(a)}</p></div>
      </details>
''' for q, a in c['faq'])
    main = f'''<main id="inhalt">

  <section class="seitenkopf lsx-kopf">
    <p class="meta"><a href="{pre}#leistungen">Leistungen</a> / {esc(c['titel'])}</p>
    <h1 class="gr-xxl"><span class="wort-mit-icon">{esc(c['titel'])}<img class="icon-3d" src="{pre}{c['icon']}" alt="" width="400" height="400"></span></h1>
    <p class="alt-klein">{esc(g['intro'])}</p>
  </section>

  <nav class="leistungs-chips lsx-chips" aria-label="Auf dieser Seite"><a href="#loesung">Problem &amp; Lösung</a><a href="#pakete">Pakete</a>{'<a href="#vergleich">Vergleich</a>' if len(g['pakete']) > 1 else ''}{'<a href="#extras">Zusatzleistungen</a>' if g.get('extras') else ''}<a href="#ablauf">Ablauf</a><a href="#faq">Fragen</a><a href="{pre}preise/#r-{g['id']}">Kostenrechner →</a></nav>

  <section class="lsx-loesung" id="loesung" aria-labelledby="loesung-titel">
    <div class="lsx-loesung-text">
      <p class="meta">Problem &amp; Lösung</p>
      <h2 class="gr-h3" id="loesung-titel">{esc(c['problem_titel'])}</h2>
      {absatz}
      <p class="lsx-knoepfe"><a class="button" href="{pre}kontakt/">Projekt anfragen</a> <a class="textlink" href="{pre}preise/#r-{g['id']}">Kosten berechnen <span aria-hidden="true">→</span></a></p>
    </div>
    <div class="lsx-gegenueber">
      <div class="lsx-spalte lsx-schlecht"><p class="meta">Woran es oft hakt</p><ul>{''.join(f'<li>{esc(x)}</li>' for x in c['probleme'])}</ul></div>
      <div class="lsx-spalte lsx-gut"><p class="meta">So mache ich es</p><ul>{''.join(f'<li>{esc(x)}</li>' for x in c['loesungen'])}</ul></div>
    </div>
  </section>

  <section class="lsx-pakete" id="pakete" aria-labelledby="pakete-titel">
    <p class="meta">Pakete</p>
    <h2 class="gr-h3" id="pakete-titel">Pakete im Überblick</h2>
    {f'<p class="lsx-hinweis">{esc(g["hinweis"])}</p>' if g.get('hinweis') else ''}
    <div class="lsx-karten">
{karten(g)}
    </div>
  </section>

{vergleich(g)}

{extras(g)}

{ablauf(pre)}

{stimmen(pre, c.get('stimmen', []))}

  <section class="lsx-rechner" aria-labelledby="rechner-hinweis">
    <div>
      <p class="meta">Kostenrechner</p>
      <h2 class="gr-h3" id="rechner-hinweis">Was kostet Ihr Projekt?</h2>
      <p>Stellen Sie sich Ihre Pakete und Zusatzleistungen selbst zusammen und erhalten Sie sofort einen unverbindlichen Kostenvoranschlag, als PDF oder per E-Mail.</p>
    </div>
    <a class="button" href="{pre}preise/#r-{g['id']}">Zum Kostenrechner <span aria-hidden="true">→</span></a>
  </section>

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
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(c["seitentitel"])}">', t, count=1)
    # Strukturierte Daten: Leistung mit Angeboten und FAQ (für Suchmaschinen und KI-Antworten)
    studio = re.search(r'\{\s*"@type": "ProfessionalService".*?"areaServed": \[[^\]]*\]\s*\}', t, re.S)
    angebote = [{"@type": "Offer", "name": e['name'], "priceCurrency": "EUR", "price": str(e['preis']),
                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": e['preis'], "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}
                for e in g['pakete'] if e.get('preis')]
    graph = [json.loads(studio.group(0)) if studio else {"@id": "https://studio-aah.de/#studio"},
             {"@type": "Service", "@id": url + '#leistung', "name": c['titel'], "description": g['intro'], "url": url,
              "provider": {"@id": "https://studio-aah.de/#studio"}, "areaServed": "Leipzig", "offers": angebote},
             {"@type": "FAQPage", "@id": url + '#faq', "url": url, "inLanguage": "de",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faq']]}]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: f'<script type="application/ld+json">\n{ld}\n  </script>', t, count=1, flags=re.S)
    pfad.write_text(t, encoding='utf-8')
    print('geschrieben:', c['pfad'])


wahl = sys.argv[1:] or [k for k in inhalte if not k.startswith('_')]
for k in wahl: seite(k, inhalte[k])
