# Gemeinsamer Baustein für alle Blogbeiträge im Schema „Ratgeber“.
# Schema und Prüfliste: werkzeuge/blog/schema-blogbeitrag.md. Kopf/Fuß kommen vom KI-Artikel, der Inhalt aus <slug>-inhalt.html.
# Ein Beitrag ruft nur bauen(...) mit seinen Daten auf; FAQ, Lesezeit, Metadaten und strukturierte Daten (JSON-LD) entstehen hier für alle gleich.
import hashlib, html, json, re

from gemeinsam import STUDIO_ID, WEBSITE, WERKZEUGE, esc, lesezeit as minuten

BASIS = 'https://studio-aah.de'
REIHEN = {'website-fragen': 'Website-Fragen'}  # Reihen im Blog: Schlüssel -> Name


MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']


def _datum_text(d):
    j, m, t = d.split('-'); return f'{int(t)}. {MONATE[int(m) - 1]} {j}'


def _anker(k):
    """Anker der Blog-Kategorie wie auf /blog/ (z. B. Webdesign -> webdesign)."""
    k = k.lower().replace('&', '').replace('/', '-')
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')): k = k.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', k).strip('-')


def _ohne_trenn(t):
    """Weiche Trennstriche (U+00AD, für schmale Bildschirme in langen Wörtern) gehören nicht in die strukturierten Daten."""
    return t.replace('\u00ad', '')


def _faq_html(faq):
    return '\n'.join(f'''        <details class="faq-eintrag">
          <summary>{esc(f)}</summary>
          <div class="faq-antwort"><p>{esc(a)}</p></div>
        </details>''' for f, a in faq)


def _text(t):
    """Sichtbarer Text aus HTML (für abstract): Tags weg, Leerraum zusammengefasst, Entities aufgelöst."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t))).strip()


def _fussnoten(main):
    """Belege als Fußnoten.
    Im Text steht [[schlüssel]], in der Quellenliste <li data-quelle="schlüssel">. Nummeriert wird in der Reihenfolge des ersten Vorkommens;
    die Liste wird zur nummerierten Liste (ol) mit Sprungzielen #quelle-n, im Text steht eine hochgestellte, verlinkte Ziffer."""
    reihe = []
    for k in re.findall(r'\[\[([a-z0-9-]+)\]\]', main):
        if k not in reihe: reihe.append(k)
    if not reihe: return main
    m = re.search(r'<ul class="quellen">(.*?)</ul>', main, re.S)
    if not m: raise SystemExit('Fußnoten im Text, aber keine Quellenliste (ul.quellen)')
    eintraege = dict(re.findall(r'<li data-quelle="([a-z0-9-]+)">(.*?)</li>', m.group(1), re.S))
    fehlt = [k for k in reihe if k not in eintraege]
    if fehlt: raise SystemExit(f'Fußnote ohne Quelle: {fehlt}')
    ohne = [k for k in eintraege if k not in reihe]
    if ohne: raise SystemExit(f'Quelle ohne Fußnote im Text: {ohne}')
    nr = {k: i + 1 for i, k in enumerate(reihe)}
    einrueck = '\n        '
    ol = '<ol class="quellen">' + ''.join(f'{einrueck}<li id="quelle-{nr[k]}">{eintraege[k]}</li>' for k in reihe) + '\n      </ol>'
    main = main[:m.start()] + ol + main[m.end():]
    return re.sub(r'\[\[([a-z0-9-]+)\]\]', lambda x: f'<sup class="fn"><a href="#quelle-{nr[x.group(1)]}" aria-label="Quelle {nr[x.group(1)]}">{nr[x.group(1)]}</a></sup>', main)


def _kurz(main):
    """Punkte aus „Kurz gesagt“ (Antwort zuerst) als Text – für abstract im JSON-LD."""
    m = re.search(r'<section class="kurz".*?<ul>(.*?)</ul>', main, re.S)
    if not m: raise SystemExit('Schema: Abschnitt „Kurz gesagt“ (section.kurz) fehlt')
    ohne_fn = re.sub(r'<sup class="fn">.*?</sup>', '', m.group(1))
    return ' '.join(_text(li) for li in re.findall(r'<li>(.*?)</li>', ohne_fn, re.S))


def _quellen(main):
    """Externe Links aus der Quellenliste (ul.quellen) als citation."""
    m = re.search(r'<(?:ul|ol) class="quellen">(.*?)</(?:ul|ol)>', main, re.S)
    if not m: return []
    aus = []
    for li in re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.S):
        for href in re.findall(r'<a href="(https?://[^"]+)">', li):
            # ganzer Eintrag als Name (Herausgeber, Titel, Datum), damit die Quelle ohne Seite verständlich ist
            name = re.sub(r'\s*↗', '', _text(li)).strip()
            aus.append({"@type": "CreativeWork", "name": name, "url": href})
    return aus


def _raster(main, abschnitt, vorlage, slug):
    """Leselayout: links mitlaufende Kapitel-Leiste wie Schritte an einer Kasse, Mitte Text,
    rechts Thema und ähnliche Artikel; oben „Artikel anhören“, wenn website/audio/<slug>.mp3 existiert (werkzeuge/blog/vorlesen.py)."""
    kapitel = [(i, re.sub(r'<[^>]+>', '', t).strip()) for i, t in re.findall(r'<h2 id="([\w-]+)">(.*?)</h2>', main)
               if i not in ('quellen', 'schluss-titel')]
    schritte = '\n'.join(f'          <li><a href="#{i}"><span class="kl-punkt" aria-hidden="true"></span><span class="kl-text">{t}</span></a></li>' for i, t in kapitel)
    leiste = f'''<div class="artikel-raster">
      <aside class="artikel-leiste" aria-label="Kapitel">
        <p class="meta">Kapitel</p>
        <div class="kl-fortschritt" aria-hidden="true"><span></span></div>
        <ol class="kl-schritte">
{schritte}
        </ol>
      </aside>
'''
    seite = f'''      <aside class="artikel-seite" aria-label="Mehr zum Thema">
        <p class="meta">Thema</p>
        <p class="as-thema"><a href="../#thema-{_anker(abschnitt)}">{abschnitt}</a></p>
        <p class="meta">Ähnliche Artikel</p>
<!-- AEHNLICH:START -->
<!-- AEHNLICH:ENDE -->
      </aside>
    </div>'''
    # doppelte Brotkrumen raus (brotkrumen.py setzt sie fein über dem Artikel), „Stand“-Angabe aus der Meta-Zeile raus
    main = re.sub(r'\n    <nav class="meta" aria-label="Brotkrumen">.*?</nav>', '', main, count=1)
    main = re.sub(r'<span>(?:Preise und )?Zahlen: Stand [^<]*</span>', '', main)
    a = main.index('    <div class="artikel-text">')
    e = main.rindex('\n    </div>\n    <nav class="artikel-nav"') + len('\n    </div>')
    meta_ende = main.index('</p>', main.index('<p class="artikel-meta">')) + len('</p>\n')
    version = re.search(r'menue\.js\?v=(\w+)', vorlage).group(1)
    skript = f'\n  <script src="../../js/artikel.js?v={version}" defer></script>\n'
    audio = WEBSITE / 'audio' / f'{slug}.mp3'
    anhoeren = (f'''    <div class="anhoeren">
      <p class="meta">Artikel anhören · KI-Stimme</p>
      <audio controls preload="none" src="../../audio/{slug}.mp3?v={hashlib.md5(audio.read_bytes()).hexdigest()[:8]}"></audio>
    </div>
''' if audio.exists() else '')
    # Kopf zweispaltig: links Dachzeile, H1, Lead, Meta, Anhören; rechts das Titelbild
    k0 = main.index('\n', main.index('<article class="artikel')) + 1
    bild_a = main.index('    <img class="artikel-bild"'); bild_e = main.index('>', bild_a) + 1
    kopf = ('    <header class="artikel-kopf">\n      <div class="ak-text">\n' + main[k0:meta_ende] + anhoeren
            + '      </div>\n      <div class="ak-bild">\n' + main[bild_a:bild_e] + '\n      </div>\n    </header>\n')
    main = main[:k0] + kopf + main[bild_e:a] + leiste + main[a:e] + '\n' + seite + main[e:]
    return main + skript


def bauen(slug, titel, h1, beschr, datum, geaendert, bild, og_bild, og_alt, keywords, faq, abschnitt='Webdesign',
          reihe=None, teil=None, ersetzen=None, ohne_figuren=False, about=(), mentions=()):
    """Schreibt website/blog/<slug>/index.html.
    bild/og_bild: Dateinamen in website/bilder/ · faq: Liste (Frage, Antwort), Antworten eigenständig verständlich, ohne Links
    reihe/teil: Reihe (Schlüssel aus REIHEN) und Position · ersetzen: {MARKE: HTML} für Grafiken im Inhalt
    ohne_figuren: Grafiken (figure) zählen nicht zur Lesezeit · about/mentions: Themen und genannte Personen für KI-Suche"""
    vorlage = (WEBSITE / 'blog' / 'was-ki-an-meiner-arbeit-veraendert-hat' / 'index.html').read_text(encoding='utf-8')
    main = (WERKZEUGE / 'blog' / f'{slug}-inhalt.html').read_text(encoding='utf-8')
    url = f'{BASIS}/blog/{slug}/'
    for marke, inhalt in (ersetzen or {}).items():
        if main.count(marke) != 1: raise SystemExit(f'Marke {marke} fehlt oder doppelt in {slug}-inhalt.html')
        main = main.replace(marke, inhalt)
    # Schema-Pflichtteile (werkzeuge/blog/schema-blogbeitrag.md)
    for teil_html, name in (('<section class="kurz"', 'Kurz gesagt'), ('<nav class="inhalt-verzeichnis"', 'Inhalt'), ('FAQ_HTML', 'Häufige Fragen'),
                            ('<section class="artikel-schluss"', 'Dein nächster Schritt'), ('<section class="autorin"', 'Über die Autorin'), ('<ul class="quellen">', 'Quellen')):
        if teil_html not in main: raise SystemExit(f'Schema: Teil „{name}“ fehlt in {slug}-inhalt.html')
    if not faq: raise SystemExit('Schema: FAQ fehlt')
    main = main.replace('FAQ_HTML', _faq_html(faq))
    main = _fussnoten(main)
    # sichtbares Änderungsdatum, sobald ein veröffentlichter Beitrag geändert wurde (passt zu dateModified)
    if geaendert != datum:
        alt = f'<time datetime="{datum}">'
        i = main.index(alt); j = main.index('</span>', i) + len('</span>')
        main = main[:j] + f'<span>Aktualisiert <time datetime="{geaendert}">{_datum_text(geaendert)}</time></span>' + main[j:]
    # Lesezeit aus dem Text der Seite (ohne Tags), 200 Wörter pro Minute
    text = re.sub(r'<figure.*?</figure>', ' ', main, flags=re.S) if ohne_figuren else main
    text = re.sub(r'<[^>]+>', ' ', text); woerter = len(re.findall(r'\w+', text))
    main = main.replace('LESEZEIT', str(minuten(woerter)))
    beitrag = {"@type": "BlogPosting", "@id": url + "#beitrag", "headline": h1, "name": titel, "description": beschr,
               "abstract": _kurz(main),
               "image": [f"{BASIS}/bilder/{og_bild}", f"{BASIS}/bilder/{bild}"],
               "datePublished": datum, "dateModified": geaendert, "inLanguage": "de-DE", "url": url, "mainEntityOfPage": url,
               "wordCount": woerter, "articleSection": abschnitt, "keywords": list(keywords),
               "author": {"@type": "Person", "name": "Anna Härtelt", "url": f"{BASIS}/profil/", "jobTitle": "UX/UI-Designerin, Strategin und Webentwicklerin", "worksFor": {"@id": STUDIO_ID}},
               "publisher": {"@id": STUDIO_ID},
               "isPartOf": [{"@type": "Blog", "@id": f"{BASIS}/blog/#blog", "name": "Blog von STUDIO AAH!", "url": f"{BASIS}/blog/"}]}
    if reihe:
        beitrag["isPartOf"].append({"@type": "CreativeWorkSeries", "@id": f"{BASIS}/blog/#reihe-{reihe}", "name": f"Reihe „{REIHEN[reihe]}“"})
        beitrag["position"] = teil
    if about: beitrag["about"] = [{"@type": "Thing", "name": n} for n in about]
    if mentions: beitrag["mentions"] = [{"@type": "Person", "name": n} for n in mentions]
    quellen = _quellen(main)
    if quellen: beitrag["citation"] = quellen
    ld = {"@context": "https://schema.org", "@graph": [
        beitrag,
        {"@type": "ProfessionalService", "@id": STUDIO_ID, "name": "STUDIO AAH!", "url": f"{BASIS}/", "logo": f"{BASIS}/bilder/icon-512.png",
         "address": {"@type": "PostalAddress", "streetAddress": "Gießerstraße 75", "postalCode": "04229", "addressLocality": "Leipzig", "addressCountry": "DE"},
         "founder": {"@type": "Person", "name": "Anna Härtelt"}},
        {"@type": "FAQPage", "@id": url + "#faq", "url": url, "inLanguage": "de-DE", "isPartOf": {"@id": url + "#beitrag"}, "mainEntity": [{"@type": "Question", "name": _ohne_trenn(f), "acceptedAnswer": {"@type": "Answer", "text": _ohne_trenn(a)}} for f, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": f"{BASIS}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASIS}/blog/"},
            {"@type": "ListItem", "position": 3, "name": abschnitt, "item": f"{BASIS}/blog/#thema-{_anker(abschnitt)}"},
            {"@type": "ListItem", "position": 4, "name": h1, "item": url}]}
    ]}
    main = _raster(main, abschnitt, vorlage, slug)
    kopf_ende = vorlage.index('<main id="inhalt">')
    fuss_start = vorlage.index('</main>')
    head = vorlage[:kopf_ende]
    alt_head = head[head.index('<title>'):head.index('<link rel="stylesheet"')]
    neu_head = f'''<title>{titel} | STUDIO AAH!</title>
  <meta name="description" content="{html.escape(beschr)}">
  <meta name="author" content="Anna Härtelt">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="../../bilder/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="../../bilder/favicon-144.png" sizes="144x144" type="image/png">
  <link rel="apple-touch-icon" href="../../bilder/apple-touch-icon.png">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="STUDIO AAH!">
  <meta property="og:locale" content="de_DE">
  <meta property="og:title" content="{titel}">
  <meta property="og:description" content="{html.escape(beschr)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASIS}/bilder/{og_bild}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(og_alt)}">
  <meta property="article:published_time" content="{datum}">
  <meta property="article:modified_time" content="{geaendert}">
  <meta property="article:author" content="Anna Härtelt">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
  </script>
  '''
    head = head.replace(alt_head, neu_head)
    seite = head + '<main id="inhalt">\n\n' + main + '\n</main>' + vorlage[fuss_start + len('</main>'):]
    ziel = WEBSITE / 'blog' / slug / 'index.html'
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(seite, encoding='utf-8')
    print(slug, 'Wörter', woerter, 'Lesezeit', minuten(woerter))
