# Erzeugt die Leistungsunterseiten (service/…/index.html) aus werkzeuge/leistungen-inhalte.json (Texte, FAQ)
# und werkzeuge/preise-daten.json (Pakete, Preise, Zusatzleistungen). Kopf und Fuß bleiben aus der bestehenden Seite erhalten,
# der Prozess kommt von der Startseite.
# Aufruf im Repository-Ordner:  python3 werkzeuge/leistungsseiten.py [id …]   (ohne id: alle)
import json, re, sys

from gemeinsam import (LINKEDIN, NETTO_SATZ, STUDIO_ID, TRENNEN_LEISTUNGEN, WEBSITE, WERKZEUGE, esc, lade_json, lade_skript,
                       paket_karte, preis, seitenrahmen, trennen as trennen_mit)

preise = lade_json('preise-daten.json')
inhalte = lade_json('leistungen-inhalte.json')
I = lade_skript('inhalte-erzeugen.py')
GEMEINSAM = lade_json('inhalte/faq-gemeinsam.json')['faq']


def inhaltslisten(preise):
    """Webdesign-Pakete (Neue Website, Redesign) übernehmen ihre Inhaltsliste aus dem Kostenrechner (eine Quelle, Anna 16.10.2026)."""
    w = preise['webrechner']
    neu = [w['texte']['liste'] if i == 'TEXTE' else i for g in w['basis_inhalt'] for i in g['items']]
    redesign = [i for v in w['redesign_inhalt'].values() for i in v]
    for g in preise['gruppen']:
        for e in g['pakete']:
            if e.get('items_aus') == 'basis':
                e['items'] = neu + [f"Jede Unterseite {e['seite']} € mit Texten und Bildern"]
            elif e.get('items_aus'):
                e['items'] = redesign


inhaltslisten(preise)


def preise_link(g, pre):
    # Rechner gibt es nur für Webdesign; die übrigen Leistungen haben eine Preisliste auf der Preisseite
    return (f'{pre}preise/#rechner', 'Kostenrechner') if g['id'] == 'website' else (f'{pre}preise/#r-{g["id"]}', 'Alle Preise')


TERMINE = 'Einmal pro Woche einen Termin, 45 Minuten, online über Google Meet oder Teams, je nachdem, was Sie brauchen.'
# Hinweis im Kleingedruckten unter Karten, Tabelle und Zusatzleistungen (B2B: Nettopreise, Umsatzsteuer kommt dazu)
NETTO_HINWEIS = f'<p class="lsx-klein">{NETTO_SATZ}</p>'
TRENNEN = TRENNEN_LEISTUNGEN


def trennen(text):
    return trennen_mit(text, TRENNEN)


def karten(g):
    return '\n'.join(paket_karte(e, TRENNEN) for e in g['pakete'])


def paket_reihen(g, c, pre=''):
    if len(g['pakete']) == 1:
        h = c.get('hintergrund')
        rechts = (f'<div class="lsx-hintergrund"><p class="meta">Mein Hintergrund</p><h3 class="lsx-hintergrund-titel">{esc(h["titel"])}</h3>'
                  + ''.join(f'<p>{esc(x)}</p>' for x in h['text'])
                  + (f'<p><a class="textlink" href="{pre}profil/#ansatz-titel">Mehr über meinen Hintergrund <span aria-hidden="true">→</span></a></p>' if h.get('link') else '') + '</div>') if h else nicht_enthalten(c)
        return '    <div class="lsx-einzeln">\n' + karten(g) + '\n      ' + rechts + '\n    </div>'
    if not c.get('paket_reihen'):
        return '    <div class="lsx-karten">\n' + karten(g) + '\n    </div>'
    nach_id = {e['id']: e for e in g['pakete']}
    return '\n'.join(f'    <div class="lsx-karten lsx-karten-{len(r)}">\n' + karten({**g, 'pakete': [nach_id[i] for i in r]}) + '\n    </div>' for r in c['paket_reihen'])


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
    ex = [e for e in g.get('extras', []) if not e.get('nurRechner')]  # seltene Funktionen nur im Kostenrechner
    if not ex: return ''
    li = ''.join(f'<li><span class="lsx-extra-name">{esc(e["name"])}</span><span class="lsx-extra-text">{esc(e.get("kurz") or e.get("wer") or "")}</span><span class="lsx-extra-preis">{preis(e)}</span></li>' for e in ex)
    return f'''  <section class="lsx-extras" id="extras" aria-labelledby="extras-titel">
    <h2 class="gr-h3" id="extras-titel">Zusatzleistungen</h2>
    <ul class="lsx-extra-liste">{li}</ul>
    {NETTO_HINWEIS}
  </section>'''


START = (WEBSITE / 'index.html').read_text(encoding='utf-8')


def dachzeile(m, h):
    # Dachzeile weglassen, wenn sie die Überschrift nur wiederholt (z. B. „Launch“ über „Launch.“, Anna 12.10.2026)
    return '' if m.rstrip('.').lower() == h.rstrip('.').lower() else f'<p class="meta">{esc(m)}</p>'


# Hinweiskarte neben „Direkt anfragen“: Webdesign führt zum Kostenrechner, alle anderen zur Preisliste
DUO_WEB = ('<p class="meta">Kostenrechner</p>\n      <h2 class="gr-h3" id="rechner-hinweis">Was kostet Ihre Website?</h2>\n'
           '      <p>In fünf Schritten zum unverbindlichen Kostenvoranschlag: Marke, neu oder Redesign, Seitenstruktur und Extras. Der Kassenbon rechnet mit, als PDF oder per E-Mail.</p>')
DUO_PREISE = ('<p class="meta">Preise</p>\n      <h2 class="gr-h3" id="rechner-hinweis">Was kostet Ihr Projekt?</h2>\n'
              '      <p>Alle Pakete und Einstiegspreise im Überblick – und für Websites der Kostenrechner mit unverbindlichem Kostenvoranschlag.</p>')


def ablauf_eigen(pre, schritte):
    li = ''.join(f'<li><span class="zl-marke"><small>Schritt</small><b>{i:02d}</b></span><div class="zl-text">{dachzeile(m, h)}<h3>{trennen(esc(h))}</h3><p class="gedaempft">{trennen(esc(x))}</p></div></li>' for i, (m, h, x) in enumerate(schritte, 1))
    return (f'  <section class="prozess-kompakt" id="ablauf" aria-labelledby="prozess">\n    <p class="meta">Wie ich arbeite</p>\n    <h2 class="preis-h2" id="prozess">Prozess</h2>\n'
            f'    <ol class="zeitleiste">{li}</ol>\n    <p><a class="button" href="{pre}kontakt/">Projekt anfragen <span aria-hidden="true">→</span></a></p>\n  </section>')


def ablauf(pre):
    m = re.search(r'<section class="prozess-kompakt".*?</section>', START, re.S)
    if not m: raise SystemExit('Prozess (section.prozess-kompakt) fehlt in website/index.html')
    s = m.group(0).replace('href="kontakt/"', f'href="{pre}kontakt/"')
    return '  ' + s.replace('<section class="prozess-kompakt"', '<section class="prozess-kompakt" id="ablauf"', 1)


def stimmen(pre, tag):
    liste = I.mit_tag(I.STIMMEN, [tag])[:3]
    if not liste: return ''
    return '  <section class="lsx-stimmen" aria-labelledby="stimmen-titel">\n    <p class="meta">Stimmen</p>\n    <h2 class="gr-h3" id="stimmen-titel">Das sagen Kundinnen und Kolleginnen</h2>\n    <div class="stimmen">\n' + I.stimmen(liste, pre) + '\n    </div>\n    <p class="stimmen-quelle"><a class="textlink" href="' + LINKEDIN + '" target="_blank" rel="noopener">Alle Empfehlungen auf LinkedIn <span aria-hidden="true">↗</span></a></p>\n  </section>'


def nicht_enthalten(c):
    if not c.get('nicht_enthalten'): return ''
    li = ''.join(f'<li>{esc(x)}</li>' for x in c['nicht_enthalten'])
    return f'<div class="lsx-nicht"><p class="meta">Nicht enthalten</p><ul>{li}</ul></div>'


def referenzen(tag, pre):
    liste = I.mit_tag(I.PROJEKTE, [tag])
    if not liste: return ''
    return '  <section class="lsx-referenzen" id="referenzen" aria-labelledby="referenzen-titel">\n    <p class="meta">Referenzen</p>\n    <h2 class="gr-h3" id="referenzen-titel">Projekte aus diesem Bereich</h2>\n    <div class="referenz-rahmen">\n' + I.referenz_karten(liste, pre, 'lsx', tag) + '\n    </div>\n  </section>'


def artikel(pre, tag):
    liste = I.mit_tag(I.BLOG, [tag])[:3]
    if not liste: return ''
    return '  <section class="lsx-artikel blog-neu" id="artikel" aria-labelledby="artikel-titel">\n    <div class="lsx-artikel-kopf"><p class="meta">Blog</p><h2 class="gr-h3" id="artikel-titel">Passende Artikel</h2></div>\n    <ul class="blog-liste">\n' + I.blog(liste, pre, pre + 'blog/') + '\n    </ul>\n  </section>'


def direkt(pre):
    return f'''    <div class="lsx-duo-karte lsx-direkt">
    <img src="{pre}bilder/anna-haertelt-studio-blau.webp" alt="Anna Härtelt, Gründerin von STUDIO AAH!" width="1200" height="1600" loading="lazy">
    <div>
      <p class="meta">Ihre Ansprechpartnerin</p>
      <h2 class="gr-h3" id="direkt-titel">Sie arbeiten direkt mit mir.</h2>
      <p>Bei STUDIO AAH! arbeiten Sie direkt mit mir, von der ersten Idee bis zum Launch. Ich bin Anna Härtelt, UX/UI-Designerin, Strategin und Webentwicklerin.</p>
      <p><a class="textlink" href="{pre}profil/">Mehr über mich <span aria-hidden="true">→</span></a></p>
    </div>
    </div>'''


# Beispiel aus der Praxis (Anna 13.10.2026): dasselbe Mockup wie in der Leiste der Startseite, weiter unten auf der Seite
MOCKUPS = {
    'brand': ('seite-markenbildung.webp', 'Rebranding für Wolfgang Bauer Ingenieurbau: Unternehmenspräsentation in den neuen Markenfarben.'),
    'website': ('seite-webdesign.webp', 'Website für Wolfgang Bauer Ingenieurbau.'),
    'print': ('seite-druck.webp', 'Visitenkarten für Dr. Simone Goldhammer.'),
    'motion': ('seite-animation.webp', 'Launch-Film zur neuen Website von Wolfgang Bauer Ingenieurbau.'),
    'illustration': ('seite-illustration.webp', 'Eigene Illustration: Figur aus Bauhaus-Grundformen.'),
    'ui-ux': ('seite-ui-ux.webp', 'Mobile Ansicht: die Websites von Deinetwegen und STUDIO AAH!'),
}


def grafik(name):
    """Grafik aus werkzeuge/grafiken/<name>.html (für Leistungsseiten mit ../../ geschrieben)."""
    return (WERKZEUGE / 'grafiken' / f'{name}.html').read_text(encoding='utf-8')


def mockup(key, pre):
    if key not in MOCKUPS: return ''
    datei, text = MOCKUPS[key]
    return ('  <section class="lsx-beispiel" aria-label="Beispiel aus der Praxis">\n    <figure class="lsx-beispiel-figur">'
            '<img src="' + pre + 'bilder/mockups/' + datei + '" alt="' + esc(text) + '" width="896" height="672" loading="lazy">'
            '<figcaption><p class="meta">Aus der Praxis</p><p>' + esc(text) + '</p></figcaption></figure>\n  </section>')


def seite(key, c):
    g = next(x for x in preise['gruppen'] if x['id'] == c['gruppe'])
    # Mehrere Seiten teilen sich eine Gruppe (zusatz): nur die genannten Pakete, eigener Einleitungssatz;
    # „paket_extra“ ergänzt die Paketdaten nur für diese Seite (z. B. Stundensatz statt „auf Anfrage“)
    if c.get('pakete'):
        g = {**g, 'pakete': [{**e, **c.get('paket_extra', {})} for e in g['pakete'] if e['id'] in c['pakete']], 'extras': []}
    intro = c.get('intro') or g['intro']
    titel_vorne = esc(' '.join(c['titel'].split()[:-1])) + ' ' if len(c['titel'].split()) > 1 else ''
    # Der Prozess der Startseite beschreibt Website-Projekte; andere Leistungen brauchen eigene Schritte (noch offen)
    mit_ablauf = bool(c.get('ablauf_schritte')) or c.get('ablauf', c['gruppe'] == 'website')
    # Abstimmungstermine (Anna, 11.10.2026): im Projekt wöchentlich, bei laufender Betreuung seltener
    termine = c.get('termine', TERMINE)
    satz = termine if termine.startswith('Termine') else termine[0].lower() + termine[1:]  # Substantiv bleibt groß
    faq_termine = [['Wie oft gibt es bei STUDIO AAH! Abstimmungstermine?', 'Bei STUDIO AAH! gibt es ' + satz + ('' if 'nach Absprache' in termine else ' Weitere Termine vereinbaren wir nach Absprache.')]]
    pre = '../' * (c['pfad'].strip('/').count('/') + 1)
    link, link_text = preise_link(g, pre)
    pfad = WEBSITE / c['pfad'] / 'index.html'
    # neue Seite: Kopf und Fuß von der Webdesign-Seite übernehmen (gleiche Ordnertiefe)
    vorlage = (pfad if pfad.exists() else WEBSITE / 'service' / 'webdesign' / 'index.html').read_text(encoding='utf-8')
    url = 'https://studio-aah.de/' + c['pfad']
    vergleich_html = vergleich(g)
    faq = ''.join(f'''      <details class="faq-eintrag">
        <summary>{esc(q)}</summary>
        <div class="faq-antwort"><p>{esc(a)}</p></div>
      </details>
''' for q, a in c['faq'] + faq_termine + GEMEINSAM)
    main = f'''<main id="inhalt">

  <section class="seitenkopf lsx-kopf">
    <p class="meta brotkrumen"><a href="{pre}#leistungen">Leistungen</a> / <span aria-current="page">{esc(c['titel'])}</span></p>
    <h1 class="gr-xxl lsx-titel" style="--n:{max(len(w) for w in c['titel'].split())}">{titel_vorne}<span class="wort-mit-icon">{esc(c['titel'].split()[-1])}<img class="icon-3d" src="{pre}{c['icon']}" alt="" width="400" height="400"></span></h1>
    <p class="alt-klein">{trennen(esc(intro))}</p>
    <p class="lsx-termine"><span class="meta">So arbeite ich</span> {esc(termine)}</p>
    {I.kennzahlen('fakten lsx-fakten', '    ')}
  </section>

  <nav class="preis-leiste lsx-chips" aria-label="Auf dieser Seite"><a href="#loesung">Problem &amp; Lösung</a><a href="#pakete">Pakete</a>{'<a href="#vergleich">Vergleich</a>' if vergleich_html else ''}{'<a href="#extras">Zusatzleistungen</a>' if g.get('extras') else ''}{'<a href="#ablauf">Ablauf</a>' if mit_ablauf else ''}{'<a href="#referenzen">Referenzen</a>' if I.mit_tag(I.PROJEKTE, [c['tag']]) else ''}{'<a href="#artikel">Artikel</a>' if c.get('artikel', True) and I.mit_tag(I.BLOG, [c['tag']]) else ''}<a href="#faq">Fragen</a><a href="{link}">{link_text} →</a></nav>

  <section class="lsx-loesung lsx-pl" id="loesung" aria-labelledby="loesung-titel">
    <p class="meta">Problem &amp; Lösung</p>
    <h2 class="gr-h3" id="loesung-titel">{esc(c['problem_titel'])}</h2>
    <div class="lsx-pl-raster">
      <div class="lsx-pl-problem"><p class="meta">Woran es oft hakt</p><ul>{''.join(f'<li>{esc(x)}</li>' for x in c['probleme'])}</ul></div>
      <div class="lsx-pl-loesung"><p class="meta">So mache ich es</p><p class="lsx-pl-text">{esc(c['loesung_text'])}</p><ul>{''.join(f'<li>{esc(x)}</li>' for x in c['loesung_punkte'][:3])}</ul>
        {'' if c.get('grafik') == 'corporate-identity' else f'<p class="lsx-grundsatz"><a class="textlink" href="{pre}service/markenbildung/#corporate-identity">Form follows function, die Form folgt der Funktion. Grundlage für alles, was ich gestalte, ist die Corporate Identity <span aria-hidden="true">→</span></a></p>'}</div>
      <p class="lsx-knoepfe"><a class="button" href="{pre}kontakt/">Projekt anfragen <span aria-hidden="true">→</span></a> <a class="textlink" href="{link}">{'Kosten berechnen' if g['id'] == 'website' else 'Alle Preise'} <span aria-hidden="true">→</span></a></p>
    </div>
  </section>

{grafik('website-oekosystem') if c.get('herz') else ''}
{grafik(c['grafik']) if c.get('grafik') else ''}
{grafik(c['nutzen']) if c.get('nutzen') else ''}

  <section class="lsx-pakete" id="pakete" aria-labelledby="pakete-titel">
    <p class="meta">Pakete</p>
    <h2 class="gr-h3" id="pakete-titel">Pakete im Überblick</h2>
    {f'<p class="lsx-hinweis">{esc(g["hinweis"])}</p>' if g.get('hinweis') else ''}
{paket_reihen(g, c, pre)}
    {NETTO_HINWEIS}
    {'' if len(g['pakete']) == 1 and not c.get('hintergrund') else nicht_enthalten(c)}
  </section>

{vergleich_html}

{extras(g)}

{(ablauf_eigen(pre, c['ablauf_schritte']) if c.get('ablauf_schritte') else ablauf(pre)) if mit_ablauf else ''}

{stimmen(pre, c['tag'])}

{mockup(key, pre)}

{referenzen(c['tag'], pre)}


  <section class="lsx-duo" aria-label="Kontakt und Kostenrechner">
{direkt(pre)}
    <div class="lsx-duo-karte lsx-duo-rechner">
      <img class="lsx-duo-icon" src="{pre}bilder/icons/money-bag.webp" alt="" width="400" height="400" loading="lazy">
      {DUO_WEB if g['id'] == 'website' else DUO_PREISE}
      <p><a class="button button-zweit button-hell" href="{link}">{'Zum Kostenrechner' if g['id'] == 'website' else 'Zu den Preisen'} <span aria-hidden="true">→</span></a></p>
    </div>
  </section>

{artikel(pre, c['tag']) if c.get('artikel', True) else ''}

  <section class="faq" id="faq" aria-labelledby="faq-titel">
    <h2 class="gr-h2" id="faq-titel">Häufige Fragen</h2>
    <div class="faq-liste">
{faq}    </div>
    <p class="faq-mehr">Noch Fragen? Ich freue mich auf Ihre Nachricht. <a class="textlink" href="{pre}kontakt/">Kontakt</a></p>
  </section>

</main>'''
    # Strukturierte Daten: Leistung mit Angeboten und FAQ (für Suchmaschinen und KI-Antworten)
    studio = re.search(r'\{\s*"@type": "ProfessionalService".*?"areaServed": \[[^\]]*\]\s*\}', vorlage, re.S)
    angebote = [{"@type": "Offer", "name": e['name'], "priceCurrency": "EUR", "price": str(e['preis']),
                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": e['preis'], "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}
                for e in g['pakete'] if e.get('preis')]
    angebote += [{"@type": "Offer", "name": e['name'], "priceCurrency": "EUR",
                  "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": e['stunde'], **({"maxPrice": e['stundeBis']} if e.get('stundeBis') else {}), "priceCurrency": "EUR", "unitText": "Stunde", "valueAddedTaxIncluded": False}}
                 for e in g['pakete'] if e.get('stunde') and not e.get('preis')]
    graph = [json.loads(studio.group(0)) if studio else {"@id": STUDIO_ID},
             {"@type": "Service", "@id": url + '#leistung', "name": c['titel'], "description": intro, "url": url,
              "provider": {"@id": STUDIO_ID}, "areaServed": "Leipzig", "offers": angebote},
             {"@type": "FAQPage", "@id": url + '#faq', "url": url, "inLanguage": "de",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faq'] + faq_termine + GEMEINSAM]}]
    t = seitenrahmen(vorlage, main, c['seitentitel'], c['beschreibung'], url, {"@context": "https://schema.org", "@graph": graph})
    if 'zaehlen.js' not in t:  # Kennzahlen zählen hoch; Version wie auf der Startseite
        version = re.search(r'zaehlen\.js\?v=(\w+)', START).group(1)
        t = t.replace('</body>', f'  <script src="{pre}js/zaehlen.js?v={version}" defer></script>\n</body>', 1)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(t, encoding='utf-8')
    print('geschrieben:', c['pfad'])


if __name__ == '__main__':
    for k in sys.argv[1:] or [k for k in inhalte if not k.startswith('_')]:
        seite(k, inhalte[k])
