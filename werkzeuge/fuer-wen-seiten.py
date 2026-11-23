# Problem- und Branchenseiten (Anna, 09./10.11.2026): /fuer-wen/, /neue-kunden/, /fachkraefte/, /ki-im-team/ (/entlastung/ leitet dorthin weiter),
# /branchen/<slug>/ aus werkzeuge/inhalte/fuer-wen-seiten.json. Kopf und Fuß kommen aus einer Vorlage gleicher Ordnertiefe
# (profil/ bzw. service/webdesign/); danach setzt kopf-fuss.py sie ohnehin neu.
# Aufruf im Repository-Ordner:  python3 werkzeuge/fuer-wen-seiten.py
import runpy
from gemeinsam import ankerleiste, daumen, lade_skript, PFEIL, STUDIO_ID, WEBSITE, WERKZEUGE, esc, lade_json, seitenrahmen

# Hero-Illustrationen (werkzeuge/grafiken/fuer-wen-hero.py, Anna 10.11.2026); Titel dienen als Alternativtext
BILD_ALT = {k: v[0] for k, v in runpy.run_path(str(WERKZEUGE / 'grafiken' / 'fuer-wen-hero.py'))['BILDER'].items()}

D = lade_json('inhalte/fuer-wen-seiten.json')
I = lade_skript('inhalte-erzeugen.py')   # Projekt-Cards und Stimmen wie auf der Startseite
BASIS_URL = 'https://studio-aah.de/'
PROBLEME = {p['id']: p for p in D['probleme']}
VORLAGE = {1: 'profil/index.html', 2: 'service/webdesign/index.html'}
# Keine Icons auf den Problem-Karten (Anna 12.11.2026: „Grafiken raus“)


def link(pre, ziel):
    return ziel if ziel.startswith('http') else pre + ziel


FW_FOTO = {'employer-branding': 'employer-branding-bewerben.webp'}   # Hero wie Webdesign mit Riso-Foto (Anna 23.11.2026)


def kopfbereich(meta, h1, unter, pre, knopf=('website-check/', 'Kostenloser Website-Check'), bild=None, zeichnung=False, textlink=None):
    if zeichnung:   # Problemseiten „Wo es hakt“: Hero wie Leistungsseiten, Bauhaus-Zeichnung rechts; Brotkrumen setzt brotkrumen.py statt der Dachzeile (Anna 23.11.2026)
        return (f'  <section class="seitenkopf lsx-kopf lsx-m-kopf fw-kopf-zeichnung">\n    <p class="meta">{esc(meta)}</p>\n'
                f'    <h1 class="gr-xxl lsx-titel" style="--n:26">{ko(h1).replace(chr(10), "<br>")}</h1>\n    <p class="alt-klein">{esc(unter)}</p>\n'
                f'    <p class="lsx-hero-knopf"><a class="button" href="{pre}{knopf[0]}">{esc(knopf[1])}{PFEIL}</a>'
                + (f'<a class="textlink" href="{pre}{textlink[0]}">{esc(textlink[1])}{PFEIL}</a>' if textlink else '') + '</p>\n'
                f'    <img class="lsx-kopf-zeichnung" src="{pre}bilder/fuer-wen/{bild}.svg" alt="{esc(BILD_ALT[bild])}" width="800" height="640" loading="eager">\n  </section>')
    if bild in FW_FOTO:
        return (f'  <section class="seitenkopf lsx-kopf lsx-m-kopf fw-kopf-foto">\n    <p class="meta">{esc(meta)}</p>\n'
                f'    <h1 class="gr-xxl lsx-titel" style="--n:26">{esc(h1)}</h1>\n    <p class="alt-klein">{esc(unter)}</p>\n'
                f'    <p class="lsx-hero-knopf"><a class="button" href="{pre}{knopf[0]}">{esc(knopf[1])}{PFEIL}</a></p>\n'
                f'    <span class="lsx-repro" aria-hidden="true"><span class="lsx-repro-druck"><img src="{pre}bilder/{FW_FOTO[bild]}" alt="" loading="eager"></span></span>\n  </section>')
    figur = (f'\n    <figure class="fw-bild"><img src="{pre}bilder/fuer-wen/{bild}.svg" alt="{esc(BILD_ALT[bild])}" width="800" height="640"></figure>'
             if bild else '')
    return (f'  <section class="fw-kopf{" fw-kopf-bild" if bild else ""}">\n    <div class="fw-kopf-text">\n    <p class="meta">{esc(meta)}</p>\n    <h1 class="gr-h2 fw-h1">{esc(h1).replace(chr(10), "<br>")}</h1>\n'
            f'    <p class="haken-unter">{esc(unter)}</p>\n'
            f'    <p class="fw-knoepfe"><a class="button" href="{pre}{knopf[0]}">{esc(knopf[1])}{PFEIL}</a></p>\n    </div>{figur}\n  </section>')  # immer nur ein Button im Hero (Anna 13.11.2026)


def karten(eintraege, pre, klasse='haken-karten'):
    h = [f'    <ol class="{klasse}">']
    for e in eintraege:
        h.append(f'      <li class="haken-karte">{e.get("icon", "")}<h3>{esc(e["titel"])}</h3><p>{esc(e["text"])}</p>'
                 + (f'<a class="textlink" href="{link(pre, e["href"])}">{esc(e["linktext"])}{PFEIL}</a>' if e.get('href') else '') + '</li>')
    h.append('    </ol>')
    return '\n'.join(h)


def schritte(liste):
    h = ['    <ol class="zl-quer zl-drei">']
    for i, (meta, titel, text) in enumerate(liste, 1):
        h.append(f'      <li><span class="zlq-nr">{i:02d}</span><p class="meta">{esc(meta)}</p><h3>{esc(titel)}</h3><p class="gedaempft">{esc(text)}</p></li>')
    h.append('    </ol>')
    return '\n'.join(h)


def beleg(b, pre):
    if not b:  # Anna 12.11.2026: lieber keine Referenz als überall Bauer
        return ''
    def verweis(l):
        extern = l[0].startswith('http')
        pfeil = ' <span aria-hidden="true">↗</span><span class="unsichtbar"> (öffnet in neuem Tab)</span>' if extern else PFEIL
        ziel = ' target="_blank" rel="noopener"' if extern else ''
        return f'      <p><a class="textlink" href="{link(pre, l[0])}"{ziel}>{esc(l[1])}{pfeil}</a></p>\n'
    weitere = ''.join(f'      <p>{esc(w["text"])}</p>\n' + verweis(w['link']) for w in b.get('weitere', []))
    z = b.get('zitat')
    zitat = (f'      <blockquote class="fw-zitat"><p>„{esc(z["text"])}“</p><footer>{esc(z["name"])}, {esc(z["rolle"])}</footer></blockquote>\n' if z else '')
    return (f'  <section class="fw-beleg" aria-labelledby="beleg-titel">\n    <div class="fw-beleg-box">\n      <p class="meta">Beleg</p>\n'
            f'      <h2 class="gr-h3" id="beleg-titel">{esc(b["titel"])}</h2>\n      <p>{esc(b["text"])}</p>\n'
            + verweis(b['link']) + weitere + zitat + '    </div>\n  </section>')


def faq(liste, titel='Ehrliche Antworten'):
    # Zwei unabhängige Spalten (Anna 10.11.2026: Aufklappen links soll rechts keine Lücke reißen), spaltenweise gelesen
    # Seit 12.11.2026 einspaltig und mittig untereinander (Anna: „nicht zweispaltig, sondern untereinander, mittig“)
    h = ['  <section class="faq ehrlich" aria-labelledby="faq-titel">', '    <p class="meta">Häufige Fragen</p>',
         ('    <h2 class="gr-h2" id="faq-titel"><span class="korrektur ko-unten"><span class="notiz notiz-durch" aria-hidden="true">Standard-Antworten</span><span class="hand">Ehrliche Antworten</span></span></h2>'
          if titel == 'Ehrliche Antworten' else f'    <h2 class="gr-h2" id="faq-titel">{esc(titel)}</h2>'), '    <div class="faq-liste faq-einspaltig">']  # wie Startseite (Anna 23.11.2026)
    for q, a in liste:
        h.append(f'      <details class="faq-eintrag">\n        <summary>{esc(q)}</summary>\n        <div class="faq-antwort"><p>{esc(a)}</p></div>\n      </details>')
    h += ['    </div>', '  </section>']
    return '\n'.join(h)


def ko(text):
    """Text mit Handschrift-Korrektur „~~alt~~[neu]“ (Anna 23.11.2026): alt rot durchgestrichen, neu in Handschrift; Vorleser hören nur neu."""
    import re as _re
    # Handschrift über dem durchgestrichenen Wort (Anna 23.11.2026, Pfeil im Screenshot); „~~alt~~|[neu]“: linksbündig, für Korrekturen am Zeilenanfang
    return _re.sub(r'~~(.+?)~~(\|?)\[(.+?)\]', lambda m: (f'<span class="korrektur ko-oben{" ko-links" if m.group(2) else ""}"><span class="notiz notiz-durch" aria-hidden="true">'
                   f'{m.group(1)}</span><span class="hand">{m.group(3)}</span></span>'), esc(text))


def abschluss(pre, text=None, knopf=None, titel='Fangen wir klein an.'):
    """Gemeinsamer Abschluss; text und knopf (Ziel, Beschriftung) nur, wo der Website-Check nicht passt (z. B. KI-Zeitrechner)."""
    text = text or 'Mit dem kostenlosen <span class="ohne-umbruch">Website-Check</span> – oder einem Gespräch, in dem du uns erzählst, wo es hakt.'
    ziel, aufschrift = knopf or ('website-check/', 'Kostenloser <span class="ohne-umbruch">Website-Check&nbsp;<span aria-hidden="true">→</span></span>')
    return ('  <section class="preis-schluss start-schluss lsx-m-schluss" aria-labelledby="weg-ziel-titel">\n  <div class="schluss-karte schluss-blau">\n  <p class="meta">Erster Schritt</p>\n'
            f'  <h2 class="gr-h2" id="weg-ziel-titel">{ko(titel)}</h2>\n'
            f'  <p class="lsx-m-schluss-text">{text}</p>\n'
            f'  <p><a class="button" href="{pre}{ziel}">{aufschrift}</a></p>\n  </div>\n</section>')  # blaue Box wie Startseite (Anna 23.11.2026)


def branche_abschluss(pre):
    """Abschluss der Branchenseiten (Anna 22.11.2026, Vorbild Kochstrasse): Name aus dem Frag-Feld der Startseite aufgreifen,
    schräg in Annas Schrift, gezeichnete Sprechblase, Button zum Kontaktformular. Ohne Namen: „Hey, du bist ja noch da.“"""
    return ('  <section class="weg-ziel br-hallo" aria-labelledby="weg-ziel-titel">\n'
            f'  <img class="br-hallo-sticker" src="{pre}bilder/zeichnungen-sw/sprechblase.svg" alt="" width="400" height="400" loading="lazy">\n'
            '  <h2 class="gr-h2 br-hallo-titel" id="weg-ziel-titel"><span data-name-hallo>Hey, du bist ja noch da.</span></h2>\n'
            '  <p class="alt-klein">Wir sollten ins Gespräch kommen.</p>\n'
            f'  <p><a class="button weg-ziel-knopf" href="{pre}kontakt/">Beratung anfragen <span aria-hidden="true">→</span></a></p>\n</section>')


def ld(titel, beschreibung, url, fragen, branche=None):
    graph = [{'@type': 'WebPage', '@id': url + '#seite', 'url': url, 'name': titel, 'description': beschreibung,
              'inLanguage': 'de-DE', 'publisher': {'@id': STUDIO_ID}}]
    if branche:   # SEO/GEO (Anna 12.11.2026): Leistung mit Zielgruppe und Einzugsgebiet, damit Suche und KI-Antworten die Seite zuordnen
        graph.append({'@type': 'Service', '@id': url + '#leistung', 'name': branche['h1'].rstrip('.'), 'serviceType': 'Webdesign',
                      'description': branche['beschreibung'], 'provider': {'@id': STUDIO_ID},
                      'audience': {'@type': 'BusinessAudience', 'name': branche['name']},
                      'areaServed': [{'@type': 'City', 'name': 'Leipzig'}, {'@type': 'State', 'name': 'Sachsen'}, {'@type': 'Country', 'name': 'Deutschland'}]})
    if fragen:
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in fragen]})
    return {'@context': 'https://schema.org', '@graph': graph}


def schreibe(pfad, main, titel, beschreibung, fragen, skript=None, branche=None):
    tiefe = pfad.count('/')
    vorlage = (WEBSITE / VORLAGE[tiefe]).read_text(encoding='utf-8')
    url = BASIS_URL + pfad
    ziel = WEBSITE / pfad / 'index.html'
    ziel.parent.mkdir(parents=True, exist_ok=True)
    text = seitenrahmen(vorlage, f'<main id="inhalt">\n{main}\n</main>', titel, beschreibung, url, ld(titel, beschreibung, url, fragen, branche))
    if skript:  # seitenbezogenes Skript nach menue.js, gleiche Cache-Version
        import re as _re
        m = _re.search(r'js/menue\.js\?v=([^"]+)"', text)
        text = text.replace('</body>', f'<script src="../js/{skript}.js?v={m.group(1) if m else "1"}" defer></script>\n</body>', 1)
    ziel.write_text(text, encoding='utf-8')
    print('geschrieben:', pfad)


def weiterleitung(alt_pfad, pfad, name):
    """Alte Adresse leitet auf die neue weiter (statische Seite, wie service/brand/)."""
    ziel = WEBSITE / alt_pfad / 'index.html'
    ziel.parent.mkdir(parents=True, exist_ok=True)
    rel = '../' * alt_pfad.strip('/').count('/') + '../' + pfad
    ziel.write_text(f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Weiterleitung zu {esc(name)} | STUDIO AAH!</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{BASIS_URL}{pfad}">
<meta http-equiv="refresh" content="0; url={rel}">
</head>
<body>
<p>Diese Seite ist umgezogen: <a href="{rel}">{esc(name)}</a>.</p>
</body>
</html>
''', encoding='utf-8')
    print('Weiterleitung:', alt_pfad)


def teamfoto(pre):
    """Problemseiten ohne Beleg: Teamfoto über die ganze Breite, so hoch wie die Sticky-Notes-Fläche (Anna 23.11.2026; Foto Matheus Bertelli, Pexels, im Impressum)."""
    return (f'  <figure class="fw-teamfoto"><img src="{pre}bilder/blog-ai-act/team.webp" alt="Ein Team sitzt an einem langen Tisch mit Laptops in einem hellen Raum." '
            'width="1400" height="934" loading="lazy" decoding="async"></figure>')


def problemseite(p):
    pre = '../'
    teile = [kopfbereich(p['meta'], p['h1'], p['unter'], pre, tuple(p.get('knopf', ('website-check/', 'Kostenloser Website-Check'))), bild=p['id'], zeichnung=True, textlink=p.get('textlink')),
             '  <section class="fw-zwei fw-flaeche-rot" aria-labelledby="kennen-titel">\n    <div>\n      <p class="meta">Kennst du das?</p>\n'
             f'      <h2 class="gr-h3" id="kennen-titel">{ko(p.get("h2_kennen", "Woran du es merkst"))}</h2>\n      <ul class="fw-liste">\n'
             + '\n'.join(f'        <li>{esc(s)}</li>' for s in p['symptome']) + '\n      </ul>\n    </div>\n'
             f'    <div>\n      <p class="meta">Was es dich kostet</p>\n'
             + (f'      <h2 class="gr-h3">{esc(p["h2_kosten"])}</h2>\n' if p.get('h2_kosten') else '')
             + f'      <p class="fw-kosten">{esc(p["kosten"])}</p>\n    </div>\n  </section>',
             '  <section class="ablauf-start fw-flaeche-schwarz" aria-labelledby="loesung-titel">\n    <div class="sektionskopf"><p class="meta">So gehen wir vor</p>'
             f'<h2 class="gr-h2" id="loesung-titel">{ko(p.get("h2_loesung", "Drei Schritte."))}</h2></div>\n' + schritte(p['schritte']) + '\n  </section>',
             '  <section class="haken fw-nutzen fw-flaeche-orchidee" aria-labelledby="nutzen-titel">\n    <div class="sektionskopf"><p class="meta">Was du davon hast</p>'
             f'<h2 class="gr-h2" id="nutzen-titel">{ko(p.get("h2_nutzen", "Mit uns an deiner Seite."))}</h2></div>\n'
             + karten([{'titel': t, 'text': x} for t, x in p['nutzen']], pre, 'haken-karten fw-drei') + '\n  </section>',
             beleg(p.get('beleg'), pre) or teamfoto(pre),
             faq(p['faq']),   # „Passende Leistungen – Damit arbeite ich“ entfernt (Anna 12.11.2026)
             abschluss(pre, p.get('schluss'), (p['schluss_knopf'][0], esc(p['schluss_knopf'][1]) + '&nbsp;<span aria-hidden="true">→</span>') if p.get('schluss_knopf') else None)]
    schreibe(p['pfad'], '\n\n'.join(teile), p['seitentitel'], p['beschreibung'], p['faq'])
    if p.get('alt_pfad'):   # Entlastung ist in KI im Team aufgegangen (Anna 23.11.2026)
        weiterleitung(p['alt_pfad'], p['pfad'], p['meta'])


def branchen_kacheln(liste, pre, fotos=False):
    """Kacheln der Branchen mit Bild, Titel und Pfeil (Startseite und „Weitere Branchen“).
    fotos=True: KI-Bild der Bildwelt „Miniaturwelt“ statt Illustration, mit sichtbarem KI-Label (AI Act Art. 50, Anna 18.11.2026);
    vorerst nur auf der Startseite (Anna: „erstmal alle zusammen sehen“)."""
    teile = []
    for b in liste:
        ki = b.get('ki_bild') if fotos else None
        if ki and (WEBSITE / ki['datei']).exists():
            bild = (f'<span class="br-foto-bild"><img src="{pre}{ki["datei"]}" alt="{esc(ki["alt"])}" width="1080" height="1080" loading="lazy">'
                    f'<span class="ki-label" aria-hidden="true">KI</span></span>')
            klasse = 'br-kachel br-ki'
        else:
            bild = f'<img src="{pre}bilder/fuer-wen/{b["id"]}.svg" alt="" width="800" height="640" loading="lazy">'
            klasse = 'br-kachel'
        teile.append(f'      <li><a class="{klasse}" href="{pre}{b["pfad"]}">{bild}'
                     f'<span class="br-name">{esc(b["name"])}</span><span class="br-pfeil" aria-hidden="true">→</span></a></li>\n')
    return ''.join(teile)


def startseite_branchen():
    """Branchen-Mosaik der Startseite (Anna 12.11.2026, Muster IT Sonix): Text oben links, dann alle Branchen als Kacheln."""
    kopf = ('      <li class="br-kopf"><p class="meta">Branchen</p><h2 class="gr-h2" id="branchen-titel">Für wen wir <span class="korrektur ko-unten"><span class="notiz notiz-durch" aria-hidden="true">arbeiten</span><span class="hand">mitdenken</span></span></h2>\n'
            '        <p>Mittelständische B2B-Unternehmen. Wähl deine Branche.</p></li>\n')
    # Reihenfolge nach Potenzial (Anna 17.11.2026: Gesundheit nicht prominent); die breite Kachel ist Platz 6 (Beratung)
    reihenfolge = ['bau', 'software', 'elektro', 'energie', 'industrie', 'beratung', 'gesundheit']
    liste = sorted(D['branchen'], key=lambda b: reihenfolge.index(b['id']) if b['id'] in reihenfolge else 99)
    return '    <ul class="br-raster br-mosaik">\n' + kopf + branchen_kacheln(liste, '', fotos=True) + '    </ul>'


FLIP_BILDER = {  # Bildchen der Flipcard-Rückseiten (bis 18.11.2026 von der Startseite gelesen; dort gibt es seitdem keine Flipcards mehr)
    'neue-kunden/': '<svg class="hk-bild hk-loesung" viewBox="0 0 120 72" aria-hidden="true"><rect x="4" y="6" width="74" height="58" rx="6" fill="none" stroke="#fff" stroke-width="3"/><line x1="4" y1="18" x2="78" y2="18" stroke="#fff" stroke-width="3"/><rect x="14" y="42" width="40" height="12" rx="6" fill="#fff"/><circle cx="108" cy="16" r="6" fill="#fff"/><circle cx="108" cy="52" r="6" fill="#fff"/><path d="M100 18 C 90 28, 80 40, 62 46" fill="none" stroke="#fff" stroke-width="2.5" stroke-dasharray="3 5"/><path d="M100 50 C 90 50, 80 50, 62 49" fill="none" stroke="#fff" stroke-width="2.5" stroke-dasharray="3 5"/></svg>',
    'employer-branding/': '<svg class="hk-bild hk-loesung" viewBox="0 0 120 72" aria-hidden="true"><rect x="20" y="30" width="52" height="38" fill="#fff"/><path d="M14 32 L46 6 L78 32 Z" fill="#fff"/><rect x="38" y="48" width="16" height="20" fill="#2a5fe6"/><g transform="translate(46 36) scale(.18)"><rect x="-34" y="-34" width="68" height="68" transform="rotate(45)" fill="#2a5fe6"/><circle cx="-24" cy="-24" r="34" fill="#2a5fe6"/><circle cx="24" cy="-24" r="34" fill="#2a5fe6"/></g><circle cx="96" cy="44" r="6" fill="#fff"/><rect x="90" y="52" width="12" height="16" fill="#fff"/><circle cx="114" cy="44" r="5" fill="#fff"/><rect x="109" y="51" width="10" height="17" fill="#fff"/></svg>',
    'service/ki-digitalisierung/': '<svg class="hk-bild hk-loesung hk-stern" viewBox="0 0 120 72" aria-hidden="true"><path d="M50 4 C53 26 60 33 82 36 C60 39 53 46 50 68 C47 46 40 39 18 36 C40 33 47 26 50 4 Z" fill="#fff"/><path d="M96 6 C97.5 15 101 18.5 110 20 C101 21.5 97.5 25 96 34 C94.5 25 91 21.5 82 20 C91 18.5 94.5 15 96 6 Z" fill="#fff"/><path d="M94 46 C95 52 97 54 103 55 C97 56 95 58 94 64 C93 58 91 56 85 55 C91 54 93 52 94 46 Z" fill="#fff"/></svg>',
}


def flip_bilder():
    """Bildchen der Flipcard-Rückseiten (Ziel-Adresse → SVG), damit sie überall gleich sind."""
    return FLIP_BILDER


def flipkarten(eintraege, pre):
    """Drei Problem-Karten als Flipcards wie auf der Startseite (Anna 12.11.2026)."""
    bilder = flip_bilder()
    ersatz = list(bilder.values())[-1] if bilder else ''
    h = ['    <ol class="haken-karten haken-start haken-gelegt">']
    for n, e in enumerate(eintraege, 1):
        h.append(f'      <li class="haken-karte hk-flip"><div class="hk-innen"><div class="hk-vorne"><span class="hk-nr">{n:02d}</span><h3>{esc(e["titel"].rstrip("."))}</h3>'
                 f'<span class="hk-zeichen" aria-hidden="true">↻</span></div><div class="haken-nutzen hk-hinten">{bilder.get(e["href"], ersatz)}'
                 f'<span class="meta">Mit uns an deiner Seite</span><p>{esc(e["text"])}</p>'
                 f'<a class="textlink" href="{link(pre, e["href"])}">{esc(e["linktext"])}{PFEIL}</a></div></div></li>')
    h.append('    </ol>')
    return '\n'.join(h)


def projekte_abschnitt(b, pre):
    """Referenzen wie auf der Startseite: Projekt-Cards, darunter Stimmen (Anna 12.11.2026: statt Beleg-Box).
    Bauer nur bei Bau (Anna 12.11.2026); Branchen ohne eigenes Projekt zeigen keine Referenz."""
    namen = b.get('projekte', [])
    liste = [p for n in namen for p in I.PROJEKTE if n in (p.get('slug'), p.get('kurzname'))]
    if not liste: return ''
    stimmen = [x for n in b.get('stimmen', []) for x in I.STIMMEN if x['name'] == n]
    eine = ' br-stimmen-eine' if len(stimmen) == 1 else ''   # eine Stimme: mittig, doppelt so breit (Anna 13.11.2026: kein leerer Weißraum)
    st = f'\n    <div class="stimmen br-stimmen{eine}">\n{I.stimmen(stimmen, pre)}\n    </div>' if stimmen else ''
    return ('  <section class="start-projekte br-projekte" id="referenz" aria-labelledby="referenzen-titel">\n'
            + ('    <div class="sektionskopf"><p class="meta">Referenz</p><h2 class="gr-h2 pa-titel" id="referenzen-titel">Ein Beispiel aus der Praxis</h2></div>\n'  # nur ein Projekt (Anna 23.11.2026)
               if len(liste) == 1 else
               '    <div class="sektionskopf"><p class="meta">Referenzen</p><h2 class="gr-h2 pa-titel" id="referenzen-titel"><span class="korrektur korrektur-partner korrektur-links"><span class="notiz notiz-durch" aria-hidden="true">Projekte</span><span class="hand">Partnerschaften auf Augenhöhe</span></span></h2></div>\n')
            + f'{referenz_mit_zahlen(b, liste, pre)}{st}\n  </section>')


def zahlen_kasten(titel, zahlen):
    """Kennzahlen neben einer einzelnen Referenz (Anna 13.11.2026): groß, zählen beim Einblenden hoch (menue.js, data-zaehlen)."""
    return (f'      <div class="br-zahlen" aria-label="{esc(titel)}">\n        <p class="br-zahlen-titel">{esc(titel)}</p>\n'
            + ''.join(f'        <p class="br-zahl"><strong><span data-zaehlen="{z}">{z}</span>{(" <small>" + esc(e) + "</small>") if e else ""}</strong>{esc(t)}</p>\n'
                      for z, e, t in zahlen) + '      </div>\n')


def referenz_mit_zahlen(b, liste, pre):
    """Ein Projekt: Card und Kennzahlen nebeneinander (kein leerer Weißraum); mehrere Projekte: Raster wie auf der Startseite."""
    if len(liste) == 1 and b.get('zahlen'):
        return ('    <div class="br-ref">\n      <div class="referenz-rahmen">\n' + I.projekt_raster(liste, pre) + '\n      </div>\n'
                + zahlen_kasten(b['zahlen_titel'], b['zahlen']) + '    </div>')
    return f'    <div class="referenz-rahmen">\n{I.projekt_wechsel(liste, pre) if len(liste) > 1 else I.projekt_raster(liste, pre)}\n    </div>'


def weitere_branchen(andere, pre):
    """„Weitere Branchen“ als Mosaik mit Kopf-Kachel an erster Stelle wie auf der Startseite (Anna 12.11.2026)."""
    return ('  <section class="br-weitere-branchen" aria-labelledby="weitere-titel">\n    <ul class="br-raster br-mosaik">\n'
            '      <li class="br-kopf"><p class="meta">Branchen</p><h2 class="gr-h2" id="weitere-titel">Weitere Branchen</h2>\n'
            '        <p>Mittelständische B2B-Unternehmen. Wähl deine Branche.</p></li>\n'
            + branchen_kacheln(andere, pre) + '    </ul>\n  </section>')


VORGEHEN = [('Verstehen', 'Erst zuhören, dann gestalten.', 'Website-Check, Gespräche mit dir und deinem Team, Blick auf Mitbewerber und Zielgruppe.'),
            ('Ideation', 'Struktur und erster Entwurf.', 'Sitemap, Inhalte und der Entwurf der Startseite. Danach entscheidest du: weiter oder Schluss. Du zahlst nur, was abgeschlossen ist.'),
            ('Umsetzung', 'Design und Entwicklung.', 'Alle Seiten, Texte und Bilder, Feedback an festen Punkten. So wenig Aufwand für dich wie möglich.'),
            ('Launch & Begleitung', 'Live, und es geht weiter.', 'Deine Website geht online. Auf Wunsch betreuen wir sie danach als Retainer.')]


def vorgehen_schritte():
    """Vier Schritte der Zeitleiste."""
    h = []
    for n, (m, t, x) in enumerate(VORGEHEN, 1):
        marke = ''   # Marke „Hier können Sie aussteigen“ wieder raus (Anna 13.11.2026); der Satz steht im Text von Schritt 02
        h.append(f'      <li><span class="zlq-nr">{n:02d}</span><p class="meta">{esc(m)}</p><h3>{esc(t.rstrip("."))}</h3><p class="gedaempft">{esc(x)}</p>{marke}</li>\n')
    return ''.join(h)


def branchenseite(b):
    """Branchenseite nach dem Muster der IT-Sonix-Seite „Energiesektor“ (Anna 12.11.2026): Sprungmarken, Herausforderungen,
    was die Website können muss, Einwand, Referenz, Vorgehen, Fragen, erster Schritt, weitere Branchen."""
    pre = '../../'
    eintraege = [{'titel': PROBLEME[i]['karte'], 'text': t, 'href': PROBLEME[i]['pfad'],
                  'linktext': PROBLEME[i]['meta']} for i, t in b['schmerz']]
    if b.get('karten'):   # eigene Schmerzpunkte der Branche (Anna 13.11.2026, Bau)
        eintraege = [{'titel': t, 'text': x, 'href': h, 'linktext': l} for t, x, h, l in b['karten']]
    vorgehen = vorgehen_schritte()
    andere = [x for x in D['branchen'] if x['id'] != b['id']]
    kurz = (f'STUDIO AAH! aus Leipzig gestaltet Websites für {b["name"].replace("&", "und")} im Mittelstand. '
            f'Wichtig in dieser Branche: {b["muss"][0]}; {b["muss"][2]}. '
            'Der Einstieg ist ein kostenloser Website-Check, danach gibt es ein Angebot mit festem Preis.')
    bedarf = (f'\n      <p class="br-bedarf"><span class="meta">Bei Bedarf</span> {esc(" · ".join(b["bei_bedarf"]))}</p>' if b.get('bei_bedarf') else '')
    foto = (f'    <figure class="br-foto br-foto-spalte"><img src="{pre}{b["foto"]["datei"]}" alt="{esc(b["foto"]["alt"])}" width="2400" height="1000" loading="lazy"></figure>\n'
            if b.get('foto') else '')   # Bildnachweis nur im Impressum (Anna 12.11.2026)
    projekte = projekte_abschnitt(b, pre)
    sprung = [('herausforderungen', 'Herausforderungen'), ('website', 'Was deine Website können muss')] + ([('referenz', 'Referenzen')] if projekte else []) + [
              ('vorgehen', 'Vorgehen'), ('fragen', 'Häufige Fragen')]
    teile = [kopfbereich('Branche: ' + b['name'], b['h1'], b['unter'], pre, bild=b['id']),
             f'  <section class="br-kurz" aria-label="Kurz gesagt">\n    <p class="meta">Kurz gesagt</p>\n    <p>{esc(kurz)}</p>\n  </section>',
             ankerleiste([(a, esc(n)) for a, n in sprung]),
             '  <section class="haken haken-schwarz br-herausforderung" id="herausforderungen" aria-labelledby="haken-titel">\n    <div class="sektionskopf sk-mitte"><p class="meta">Deine Branche</p>'
             '<h2 class="gr-h2" id="haken-titel">Wo es in deiner Branche hakt.</h2>\n'
             f'    <p class="br-einleitung">{esc(b["einleitung"])}</p></div>\n' + flipkarten(eintraege, pre) + '\n  </section>',
             '  <section class="fw-zwei br-website" id="website" aria-labelledby="website-titel">\n    <div>\n      <p class="meta">Deine Website</p>\n'
             '      <h2 class="gr-h3" id="website-titel">Was deine Website können muss</h2>\n      <ul class="fw-liste">\n'
             + '\n'.join(f'        <li>{esc(x)}</li>' for x in b['muss']) + '\n      </ul>' + bedarf + '\n    </div>\n' + foto + '  </section>',
             projekte,
             '  <section class="ablauf-start" id="vorgehen" aria-labelledby="vorgehen-titel">\n    <div class="sektionskopf"><p class="meta">Vorgehen</p>'
             '<h2 class="gr-h2" id="vorgehen-titel">Vier Schritte.<br>Planbar von Anfang&nbsp;an.</h2></div>\n    <ol class="zl-quer">\n' + vorgehen + '    </ol>\n  </section>',
             faq(b['faq']).replace('<section class="faq ehrlich"', '<section class="faq ehrlich" id="fragen"', 1),
             branche_abschluss(pre),
             weitere_branchen(andere, pre)]
    teile = [t for t in teile if t]
    schreibe(b['pfad'], '\n\n'.join(teile), b['seitentitel'], b['beschreibung'], b['faq'], branche=b)
    if b.get('alt_pfad'):   # alte Adresse leitet weiter (wie service/brand/)
        weiterleitung(b['alt_pfad'], b['pfad'], b['name'])


def uebersicht():
    u = D['uebersicht']
    pre = '../'
    probleme = [{'titel': p['karte'], 'text': p['kurz'], 'href': p['pfad'], 'linktext': p['meta']} for p in D['probleme']]
    branchen = [{'titel': b['name'], 'text': b['kurz'], 'href': b['pfad'], 'linktext': 'Zur Branche'} for b in D['branchen']]
    weitere = [{'titel': t, 'text': x, 'href': z, 'linktext': 'Zum Test' if z in ('selbsttest/', 'ki-zeitrechner/') else 'Mehr erfahren'} for t, x, z in u['weitere']]
    teile = [kopfbereich(u['meta'], u['h1'], u['unter'], pre, bild='fuer-wen'),
             '  <section class="haken" aria-labelledby="haken-titel">\n    <div class="sektionskopf"><p class="meta">Herausforderungen</p>'
             '<h2 class="gr-h2" id="haken-titel">Vier Fragen aus dem Mittelstand.</h2></div>\n' + karten(probleme, pre) + '\n  </section>',
             '  <section class="haken" aria-labelledby="branchen-titel">\n    <div class="sektionskopf"><p class="meta">Branchen</p>'
             '<h2 class="gr-h2" id="branchen-titel">Deine Branche.</h2></div>\n' + karten(branchen, pre, 'haken-karten fw-drei') + '\n  </section>',
             '  <section class="haken fw-weitere" aria-labelledby="weitere-titel">\n    <div class="sektionskopf"><p class="meta">Außerdem</p>'
             '<h2 class="gr-h3" id="weitere-titel">Selbsttests und weitere Zielgruppen.</h2></div>\n' + karten(weitere, pre, 'haken-karten fw-zwei-k') + '\n  </section>',
             abschluss(pre)]
    schreibe(u['pfad'], '\n\n'.join(teile), u['seitentitel'], u['beschreibung'], [])


def produktseite(q):
    """Produktseite Employer Branding (Anna, 10.11.2026: ab 2.850 € netto, festes Angebot nach dem Karriere-Check)."""
    pre = '../'
    teile = [kopfbereich(q['meta'], q['h1'], q['unter'], pre, ('kontakt/', 'Beratung anfragen'), bild='employer-branding').replace(
                 f'<a class="button button-zweit" href="{pre}kontakt/">Beratung anfragen{PFEIL}</a>',
                 f'<a class="button button-zweit" href="{pre}website-check/">Kostenloser Website-Check{PFEIL}</a>'),
             ankerleiste([('was-titel', 'Kurz erklärt'), ('stufen-titel', 'Vorgehen'), ('paket-titel', 'Preise'), ('faq-titel', 'Ehrliche Antworten')]),  # wie Leistungsseiten (Anna 23.11.2026)
             '  <section class="fw-zwei" aria-labelledby="was-titel">\n    <div>\n      <p class="meta">Kurz erklärt</p>\n'
             '      <h2 class="gr-h3" id="was-titel">Was ist Employer Branding?</h2>\n'
             f'      <p class="fw-kosten">{esc(q["erklaerung"])}</p>\n    </div>\n'
             '    <div>\n      <p class="meta">Für dich, wenn</p>\n      <h2 class="gr-h3">Woran du es merkst</h2>\n      <ul class="fw-liste">\n'
             + '\n'.join(f'        <li>{esc(x)}</li>' for x in q['fuer']) + '\n      </ul>\n    </div>\n  </section>',
             '  <section class="ablauf-start" aria-labelledby="stufen-titel">\n    <div class="sektionskopf"><p class="meta">So gehen wir vor</p>'
             '<h2 class="gr-h2" id="stufen-titel">Drei Stufen.</h2></div>\n' + schritte(q['stufen']) + '\n  </section>',
             '  <section class="fw-paket" aria-labelledby="paket-titel">\n    <div class="fw-paket-box">\n      <p class="meta">Das Paket</p>\n'
             '      <h2 class="gr-h3" id="paket-titel">Das ist enthalten</h2>\n      <ul class="fw-liste">\n'
             + '\n'.join(f'        <li>{esc(x)}</li>' for x in q['enthalten']) + '\n      </ul>\n'
             f'      <p class="fw-preis"><span class="fw-preis-zahl">{esc(q["preis"])}</span> <small class="lsx-netto">netto</small></p>\n'
             f'      <p class="gedaempft">{esc(q["preis_hinweis"])}</p>\n'
             f'      <p><a class="button" href="{pre}kontakt/">Beratung anfragen{PFEIL}</a></p>\n    </div>\n  </section>',
             beleg(q.get('beleg'), pre),
             faq(q['faq']),
             abschluss(pre)]
    schreibe(q['pfad'], '\n\n'.join(teile), q['seitentitel'], q['beschreibung'], q['faq'])


def selbsttest(q):
    """Selbsttest „Wo hakt es?“ (Phase 4, Anna 10.11.2026; seit 17.11.2026 drei Themen, KI im Team und Entlastung zusammengelegt):
    Auswertung im Browser (js/selbsttest.js), nichts wird gesendet."""
    pre = '../'
    # Aussagen nach Themen gruppiert, je Thema eine Teilüberschrift (Anna 17.11.2026); Reihenfolge wie die Problemseiten
    zeilen, n = [], 0
    for p in D['probleme']:
        gruppe = [text for ziel, text in q['aussagen'] if ziel == p['id']]
        if not gruppe:
            continue
        zeilen.append(f'      <h3 class="st-thema">{esc(p["meta"])}</h3>')
        for text in gruppe:
            n += 1
            wahl = ''.join(f'<label><input type="radio" name="a{n}" value="{w}"> {t}</label>' for w, t in ((0, 'Stimmt nicht'), (1, 'Teils'), (2, 'Stimmt')))
            zeilen.append(f'      <fieldset class="st-frage" data-ziel="{p["id"]}"><legend><span class="st-nr">{n:02d}</span> {esc(text)}</legend><div class="st-wahl">{wahl}</div></fieldset>')
    assert n == len(q['aussagen']), 'Aussage mit unbekanntem Thema im Selbsttest'
    # Ergebnis (Anna 17.11.2026): je Thema eine Zeile in der Reihenfolge der Fragen, Name des Themas und Skala „Handlungsbedarf“
    themen = [p for p in D['probleme'] if any(z == p['id'] for z, _ in q['aussagen'])]
    ergebnis = ''.join(f'<li data-ergebnis="{p["id"]}"><a href="{pre}{p["pfad"]}"><span class="st-titel">{esc(p["meta"])}</span>'
                       f'<span class="st-balken" aria-hidden="true"><i></i></span><span class="st-stufe" data-stufe></span>'
                       f'<span class="st-link">Was hilft <span aria-hidden="true">→</span></span></a></li>'
                       for p in themen)
    teile = [kopfbereich(q['meta'], q['h1'], q['unter'], pre, bild='fuer-wen'),
             '  <section class="st" aria-labelledby="st-titel">\n    <h2 class="unsichtbar" id="st-titel">Deine Antworten</h2>\n'
             '    <form class="st-form" method="dialog" data-selbsttest novalidate>\n' + '\n'.join(zeilen) +
             f'\n      <p class="st-hinweis" role="alert" data-hinweis></p>\n      <p><button class="button" type="submit">Ergebnis zeigen{PFEIL}</button></p>\n'
             '      <noscript><p>Für die Auswertung braucht der Selbsttest JavaScript.</p></noscript>\n    </form>\n'
             '    <div class="st-ergebnis" data-ergebnis-box hidden tabindex="-1">\n      <p class="meta">Dein Ergebnis</p>\n'
             '      <h2 class="gr-h3" data-ergebnis-titel>Dein Handlungsbedarf</h2>\n'
             f'      <ol class="st-liste">{ergebnis}</ol>\n'
             # unter dem Ergebnis: EU-AI-Act-Artikel, dann Beratung oder Checkliste als Download (Anna 18.11.2026)
             f'      <p class="st-artikel">Passend zu KI im Team: <a class="textlink" href="{pre}blog/eu-ai-act-kleine-unternehmen/">EU AI Act: Was müssen kleine Unternehmen jetzt tun?{PFEIL}</a></p>\n'
             f'      <p class="st-weiter"><a class="button" href="{pre}kontakt/">Beratung anfragen{PFEIL}</a> <a class="button button-zweit" href="{pre}downloads/eu-ai-act-checkliste.pdf" download>Checkliste EU AI Act (PDF) <span aria-hidden="true">↓</span></a></p>\n'
             f'      {daumen("Selbsttest", "Wie hat dir der Selbsttest gefallen?", pre)}\n'
             '    </div>\n  </section>',
             abschluss(pre)]
    schreibe(q['pfad'], '\n\n'.join(teile), q['seitentitel'], q['beschreibung'], [], skript='selbsttest')


def ki_rechner(q):
    """KI-Zeitrechner (Phase 4, Anna 10.11.2026; neu gedacht 17.11.2026 nach dem Prinzip „Aufgaben statt Stellen“):
    erst schätzen, wie viel Routine KI vorbereiten kann, dann die frei gewordene Zeit auf Menschenarbeit verteilen. Rechnung im Browser."""
    pre = '../'
    kopf = kopfbereich(q['meta'], q['h1'], q['unter'], pre, bild='entlastung').replace(
        f'<a class="button" href="{pre}website-check/">Kostenloser Website-Check{PFEIL}</a>',
        f'<a class="button" href="#rechner">{esc(q["knopf"])}{PFEIL}</a>')
    assert '#rechner' in kopf, 'Hero-Button des Rechners nicht ersetzt'  # kopfbereich() hat den Standard-Button geändert
    regler = '\n'.join(
        f'        <div class="kr-bereich"><label for="kr-{b}">{esc(t)}</label>'
        f'<output for="kr-{b}" data-kr-aus="{b}" aria-hidden="true">{w} %</output>'
        f'<input id="kr-{b}" type="range" name="b_{b}" min="0" max="100" step="5" value="{w}" aria-valuetext="{w} Prozent"></div>'
        for b, t, w in q['bereiche'])
    farben = ''.join(f'<i data-kr-balken="{b}" class="kr-f{n}"></i>' for n, (b, t, w) in enumerate(q['bereiche'], 1))
    liste = '\n'.join(f'        <li><i class="kr-f{n}" aria-hidden="true"></i><span>{esc(t)}</span> <strong data-kr-std="{b}">0 Std.</strong></li>'
                      for n, (b, t, w) in enumerate(q['bereiche'], 1))
    teile = [kopf,
             f'''  <section class="st kr" id="rechner" aria-labelledby="kr-titel">
    <h2 class="unsichtbar" id="kr-titel">Deine Zahlen</h2>
    <form class="kr-form" method="dialog" data-ki-rechner>
      <h3 class="kr-schritt"><span class="st-nr">01</span> Zeit schätzen</h3>
      <label>Wie viele Menschen erledigen bei dir Büroarbeit oder Kundenanfragen?<input type="number" name="personen" min="1" max="500" value="5" inputmode="numeric"></label>
      <div class="kr-bereich"><label for="kr-stunden">Wie viele Stunden Fleißarbeit hat jede Person pro Woche?</label><output name="stunden_aus" for="kr-stunden" aria-hidden="true">6 Std.</output><input id="kr-stunden" type="range" name="stunden" min="1" max="20" value="6" aria-valuetext="6 Stunden" aria-describedby="kr-fleiss"><p class="kr-notiz" id="kr-fleiss">Zum Beispiel Ablage, Formulare, Standardanfragen per Mail oder Telefon.</p></div>
      <fieldset aria-describedby="kr-annahmen"><legend>Wie viel davon könnte KI vorbereiten?</legend>
        <label><input type="radio" name="anteil" value="0.15"> Wenig (15 %)</label>
        <label><input type="radio" name="anteil" value="0.25" checked> Mittel (25 %)</label>
        <label><input type="radio" name="anteil" value="0.4"> Viel (40 %)</label>
        <p class="kr-notiz" id="kr-annahmen">Annahmen, keine Messwerte</p></fieldset>
      <h3 class="kr-schritt"><span class="st-nr">02</span> Zeit neu verteilen</h3>
      <p class="kr-erklaer">Wofür soll dein Team die frei gewordene Zeit nutzen? Gewichte die Bereiche, der Rechner verteilt die Stunden danach. Die Prozente zeigen den Anteil an der frei gewordenen Zeit.</p>
{regler}
    </form>
    <div class="kr-ergebnis">
      <p class="meta">Deine Schätzung</p>
      <p class="kr-zahl" aria-live="polite" aria-atomic="true"><span data-kr-stunden>0</span> <small>Stunden pro Monat, die dein Team neu einsetzt</small></p>
      <p class="kr-balken" aria-hidden="true">{farben}</p>
      <ul class="kr-liste">
{liste}
      </ul>
      <p class="kr-warnung" data-kr-warnung role="status" hidden>Du hast keine Zeit fürs Lernen eingeplant. Ohne Übung bleiben neue Werkzeuge oft liegen, und die Fleißarbeit bleibt.</p>
      <p class="gedaempft">Gerechnet mit 4,3 Wochen pro Monat. Wie viel KI wirklich vorbereiten kann, zeigt der KI-Check an deinen Abläufen.</p>
      <p class="st-weiter"><a class="button" href="{pre}ki-arbeits-setup/">Zum KI-Arbeits-Setup{PFEIL}</a> <a class="button button-zweit" href="{pre}service/ki-digitalisierung/">KI-Check und Einführung{PFEIL}</a></p>
      <p class="st-artikel">Für den Start mit KI im Team: <a class="textlink" href="{pre}downloads/eu-ai-act-checkliste.pdf" download>Checkliste EU AI Act (PDF) <span aria-hidden="true">↓</span></a></p>
      {daumen("KI-Zeitrechner", "Wie hat dir der KI-Zeitrechner gefallen?", pre)}
    </div>
  </section>''',
             '  <section class="ablauf-start" aria-labelledby="grund-titel">\n    <div class="sektionskopf"><p class="meta">So führen wir KI ein</p>'
             '<h2 class="gr-h2" id="grund-titel">Aufgaben statt Stellen</h2></div>\n' + schritte(q['grundsaetze']) + '\n  </section>',
             abschluss(pre, 'Mit einem Gespräch über die Aufgaben deines Teams und darüber, wofür du mehr Zeit haben möchtest.',
                       ('kontakt/', f'Beratung anfragen{PFEIL}'))]
    schreibe(q['pfad'], '\n\n'.join(teile), q['seitentitel'], q['beschreibung'], [], skript='selbsttest')


if __name__ == '__main__':
    from gemeinsam import einsetzen
    start = WEBSITE / 'index.html'
    start.write_text(einsetzen(start.read_text(encoding='utf-8'), 'BRANCHEN', startseite_branchen()), encoding='utf-8')
    uebersicht()
    for p in D['probleme']:
        problemseite(p)
    for b in D['branchen']:
        branchenseite(b)
    produktseite(D['produkt'])
    selbsttest(D['selbsttest'])
    ki_rechner(D['ki_rechner'])
