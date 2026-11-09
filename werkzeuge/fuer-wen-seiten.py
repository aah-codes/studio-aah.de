# Problem- und Branchenseiten (Anna, 09./10.11.2026): /fuer-wen/, /neue-kunden/, /fachkraefte/, /ki-im-team/, /entlastung/,
# /branchen/<slug>/ aus werkzeuge/inhalte/fuer-wen-seiten.json. Kopf und Fuß kommen aus einer Vorlage gleicher Ordnertiefe
# (profil/ bzw. service/webdesign/); danach setzt kopf-fuss.py sie ohnehin neu.
# Aufruf im Repository-Ordner:  python3 werkzeuge/fuer-wen-seiten.py
import runpy
from gemeinsam import PFEIL, STUDIO_ID, WEBSITE, WERKZEUGE, esc, lade_json, seitenrahmen

# Hero-Illustrationen (werkzeuge/grafiken/fuer-wen-hero.py, Anna 10.11.2026); Titel dienen als Alternativtext
BILD_ALT = {k: v[0] for k, v in runpy.run_path(str(WERKZEUGE / 'grafiken' / 'fuer-wen-hero.py'))['BILDER'].items()}

D = lade_json('inhalte/fuer-wen-seiten.json')
BASIS_URL = 'https://studio-aah.de/'
PROBLEME = {p['id']: p for p in D['probleme']}
VORLAGE = {1: 'profil/index.html', 2: 'service/webdesign/index.html'}
ICON = {
    1: '<svg class="ik-icon" viewBox="0 0 48 48" aria-hidden="true"><rect x="2" y="30" width="12" height="16" fill="#0e1011"/><rect x="18" y="20" width="12" height="26" fill="#0e1011"/><circle cx="40" cy="14" r="7" fill="#2a5fe6"/><rect x="34" y="26" width="12" height="20" fill="#9a9d9e"/></svg>',
    2: '<svg class="ik-icon" viewBox="0 0 48 48" aria-hidden="true"><circle cx="12" cy="10" r="8" fill="#0e1011"/><rect x="4" y="22" width="16" height="24" fill="#0e1011"/><circle cx="36" cy="10" r="8" fill="#2a5fe6"/><rect x="28" y="22" width="16" height="24" fill="#9a9d9e"/></svg>',
    3: '<svg class="ik-icon" viewBox="0 0 48 48" aria-hidden="true"><rect x="2" y="2" width="20" height="20" fill="#0e1011"/><circle cx="36" cy="12" r="10" fill="#2a5fe6"/><path d="M2 46 L12 26 L22 46 Z" fill="#9a9d9e"/><path d="M26 46 A10 10 0 0 1 46 46 Z" fill="#0e1011"/></svg>',
    4: '<svg class="ik-icon" viewBox="0 0 48 48" aria-hidden="true"><path d="M4 22 L18 2 L32 22 Z" fill="#0e1011"/><rect x="12" y="26" width="12" height="20" fill="#0e1011"/><circle cx="39" cy="39" r="7" fill="#2a5fe6"/></svg>',
}


def link(pre, ziel):
    return ziel if ziel.startswith('http') else pre + ziel


def kopfbereich(meta, h1, unter, pre, knopf=('website-check/', 'Kostenloser Website-Check'), bild=None):
    figur = (f'\n    <figure class="fw-bild"><img src="{pre}bilder/fuer-wen/{bild}.svg" alt="{esc(BILD_ALT[bild])}" width="800" height="640"></figure>'
             if bild else '')
    return (f'  <section class="fw-kopf{" fw-kopf-bild" if bild else ""}">\n    <div class="fw-kopf-text">\n    <p class="meta">{esc(meta)}</p>\n    <h1 class="gr-h2 fw-h1">{esc(h1)}</h1>\n'
            f'    <p class="haken-unter">{esc(unter)}</p>\n'
            f'    <p class="fw-knoepfe"><a class="button" href="{pre}{knopf[0]}">{esc(knopf[1])}{PFEIL}</a> '
            f'<a class="button button-zweit" href="{pre}kontakt/">Projekt anfragen{PFEIL}</a></p>\n    </div>{figur}\n  </section>')


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
    extern = b['link'][0].startswith('http')
    pfeil = ' <span aria-hidden="true">↗</span><span class="unsichtbar"> (öffnet in neuem Tab)</span>' if extern else PFEIL
    ziel = ' target="_blank" rel="noopener"' if extern else ''
    return (f'  <section class="fw-beleg" aria-labelledby="beleg-titel">\n    <div class="fw-beleg-box">\n      <p class="meta">Beleg</p>\n'
            f'      <h2 class="gr-h3" id="beleg-titel">{esc(b["titel"])}</h2>\n      <p>{esc(b["text"])}</p>\n'
            f'      <p><a class="textlink" href="{link(pre, b["link"][0])}"{ziel}>{esc(b["link"][1])}{pfeil}</a></p>\n    </div>\n  </section>')


def faq(liste, titel='Ehrliche Antworten'):
    # Zwei unabhängige Spalten (Anna 10.11.2026: Aufklappen links soll rechts keine Lücke reißen), spaltenweise gelesen
    h = ['  <section class="faq ehrlich" aria-labelledby="faq-titel">', '    <p class="meta">Häufige Fragen</p>',
         f'    <h2 class="gr-h2" id="faq-titel">{esc(titel)}</h2>', '    <div class="faq-liste faq-spalten">']
    mitte = (len(liste) + 1) // 2
    for spalte in (liste[:mitte], liste[mitte:]):
        h.append('      <div class="faq-spalte">')
        for q, a in spalte:
            h.append(f'        <details class="faq-eintrag">\n          <summary>{esc(q)}</summary>\n          <div class="faq-antwort"><p>{esc(a)}</p></div>\n        </details>')
        h.append('      </div>')
    h += ['    </div>', '  </section>']
    return '\n'.join(h)


def abschluss(pre):
    return ('  <section class="weg-ziel" aria-labelledby="weg-ziel-titel">\n  <p class="meta">Nächster Schritt</p>\n'
            '  <h2 class="gr-h2" id="weg-ziel-titel">Fangen wir klein an.</h2>\n'
            '  <p class="alt-klein">Mit dem kostenlosen <span class="ohne-umbruch">Website-Check</span> – oder einem Gespräch, in dem Sie mir erzählen, wo es hakt.</p>\n'
            f'  <p><a class="button weg-ziel-knopf" href="{pre}website-check/">Kostenloser <span class="ohne-umbruch">Website-Check&nbsp;<span aria-hidden="true">→</span></span></a></p>\n</section>')


def ld(titel, beschreibung, url, fragen):
    graph = [{'@type': 'WebPage', '@id': url + '#seite', 'url': url, 'name': titel, 'description': beschreibung,
              'inLanguage': 'de-DE', 'publisher': {'@id': STUDIO_ID}}]
    if fragen:
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in fragen]})
    return {'@context': 'https://schema.org', '@graph': graph}


def schreibe(pfad, main, titel, beschreibung, fragen):
    tiefe = pfad.count('/')
    vorlage = (WEBSITE / VORLAGE[tiefe]).read_text(encoding='utf-8')
    url = BASIS_URL + pfad
    ziel = WEBSITE / pfad / 'index.html'
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(seitenrahmen(vorlage, f'<main id="inhalt">\n{main}\n</main>', titel, beschreibung, url, ld(titel, beschreibung, url, fragen)), encoding='utf-8')
    print('geschrieben:', pfad)


def problemseite(p):
    pre = '../'
    teile = [kopfbereich(p['meta'], p['h1'], p['unter'], pre, bild=p['id']),
             '  <section class="fw-zwei" aria-labelledby="kennen-titel">\n    <div>\n      <p class="meta">Kennen Sie das?</p>\n'
             '      <h2 class="gr-h3" id="kennen-titel">Woran Sie es merken</h2>\n      <ul class="fw-liste">\n'
             + '\n'.join(f'        <li>{esc(s)}</li>' for s in p['symptome']) + '\n      </ul>\n    </div>\n'
             f'    <div>\n      <p class="meta">Was es Sie kostet</p>\n      <p class="fw-kosten">{esc(p["kosten"])}</p>\n    </div>\n  </section>',
             '  <section class="ablauf-start" aria-labelledby="loesung-titel">\n    <div class="sektionskopf"><p class="meta">So gehe ich vor</p>'
             '<h2 class="gr-h2" id="loesung-titel">Drei Schritte.</h2></div>\n' + schritte(p['schritte']) + '\n  </section>',
             '  <section class="haken fw-nutzen" aria-labelledby="nutzen-titel">\n    <div class="sektionskopf"><p class="meta">Was Sie davon haben</p>'
             '<h2 class="gr-h2" id="nutzen-titel">Mit mir an Ihrer Seite.</h2></div>\n'
             + karten([{'titel': t, 'text': x} for t, x in p['nutzen']], pre, 'haken-karten fw-drei') + '\n  </section>',
             beleg(p['beleg'], pre),
             faq(p['faq']),
             '  <section class="fw-leistungen" aria-labelledby="leistungen-titel">\n    <p class="meta">Passende Leistungen</p>\n'
             '    <h2 class="gr-h3" id="leistungen-titel">Damit arbeite ich</h2>\n    <ul class="fw-chips">\n'
             + '\n'.join(f'      <li><a href="{pre}{z}">{esc(t)}{PFEIL}</a></li>' for z, t in p['leistungen']) + '\n    </ul>\n  </section>',
             abschluss(pre)]
    schreibe(p['pfad'], '\n\n'.join(teile), p['seitentitel'], p['beschreibung'], p['faq'])


def branchenseite(b):
    pre = '../../'
    eintraege = [{'icon': ICON[PROBLEME[i]['nr']], 'titel': PROBLEME[i]['karte'], 'text': t, 'href': PROBLEME[i]['pfad'],
                  'linktext': PROBLEME[i]['meta']} for i, t in b['schmerz']]
    quelle = ''
    if b.get('quelle'):
        quelle = (f'\n    <p class="fw-quelle">Quelle: <a href="{b["quelle"][0]}" target="_blank" rel="noopener">{esc(b["quelle"][1])} '
                  '<span aria-hidden="true">↗</span></a></p>')
    teile = [kopfbereich('Branche: ' + b['name'], b['h1'], b['unter'], pre, bild=b['id']),
             '  <section class="haken" aria-labelledby="haken-titel">\n    <div class="sektionskopf"><p class="meta">Wo es in Ihrer Branche hakt</p>'
             '<h2 class="gr-h2" id="haken-titel">Das höre ich am häufigsten.</h2></div>\n'
             + karten(eintraege, pre, 'haken-karten fw-drei') + quelle + '\n  </section>',
             beleg(b['beleg'], pre),
             faq(b['faq']),
             abschluss(pre)]
    schreibe(b['pfad'], '\n\n'.join(teile), b['seitentitel'], b['beschreibung'], b['faq'])


def uebersicht():
    u = D['uebersicht']
    pre = '../'
    probleme = [{'icon': ICON[p['nr']], 'titel': p['karte'], 'text': p['kurz'], 'href': p['pfad'], 'linktext': p['meta']} for p in D['probleme']]
    branchen = [{'titel': b['name'], 'text': b['kurz'], 'href': b['pfad'], 'linktext': 'Zur Branche'} for b in D['branchen']]
    weitere = [{'titel': t, 'text': x, 'href': z, 'linktext': 'Mehr erfahren'} for t, x, z in u['weitere']]
    teile = [kopfbereich(u['meta'], u['h1'], u['unter'], pre, bild='fuer-wen'),
             '  <section class="haken" aria-labelledby="haken-titel">\n    <div class="sektionskopf"><p class="meta">Wo es gerade hakt</p>'
             '<h2 class="gr-h2" id="haken-titel">Vier Fragen aus dem Mittelstand.</h2></div>\n' + karten(probleme, pre) + '\n  </section>',
             '  <section class="haken" aria-labelledby="branchen-titel">\n    <div class="sektionskopf"><p class="meta">Branchen</p>'
             '<h2 class="gr-h2" id="branchen-titel">Ihre Branche.</h2></div>\n' + karten(branchen, pre, 'haken-karten fw-drei') + '\n  </section>',
             '  <section class="haken fw-weitere" aria-labelledby="weitere-titel">\n    <div class="sektionskopf"><p class="meta">Außerdem</p>'
             '<h2 class="gr-h3" id="weitere-titel">Auch für Selbstständige und Vereine.</h2></div>\n' + karten(weitere, pre, 'haken-karten fw-zwei-k') + '\n  </section>',
             abschluss(pre)]
    schreibe(u['pfad'], '\n\n'.join(teile), u['seitentitel'], u['beschreibung'], [])


def produktseite(q):
    """Produktseite Employer Branding (Anna, 10.11.2026: ab 2.850 € netto, festes Angebot nach dem Karriere-Check)."""
    pre = '../'
    teile = [kopfbereich(q['meta'], q['h1'], q['unter'], pre, ('kontakt/', 'Projekt anfragen'), bild='employer-branding').replace(
                 f'<a class="button button-zweit" href="{pre}kontakt/">Projekt anfragen{PFEIL}</a>',
                 f'<a class="button button-zweit" href="{pre}website-check/">Kostenloser Website-Check{PFEIL}</a>'),
             '  <section class="fw-zwei" aria-labelledby="was-titel">\n    <div>\n      <p class="meta">Kurz erklärt</p>\n'
             '      <h2 class="gr-h3" id="was-titel">Was ist Employer Branding?</h2>\n'
             f'      <p class="fw-kosten">{esc(q["erklaerung"])}</p>\n    </div>\n'
             '    <div>\n      <p class="meta">Für Sie, wenn</p>\n      <h2 class="gr-h3">Woran Sie es merken</h2>\n      <ul class="fw-liste">\n'
             + '\n'.join(f'        <li>{esc(x)}</li>' for x in q['fuer']) + '\n      </ul>\n    </div>\n  </section>',
             '  <section class="ablauf-start" aria-labelledby="stufen-titel">\n    <div class="sektionskopf"><p class="meta">So gehe ich vor</p>'
             '<h2 class="gr-h2" id="stufen-titel">Drei Stufen.</h2></div>\n' + schritte(q['stufen']) + '\n  </section>',
             '  <section class="fw-paket" aria-labelledby="paket-titel">\n    <div class="fw-paket-box">\n      <p class="meta">Das Paket</p>\n'
             '      <h2 class="gr-h3" id="paket-titel">Das ist enthalten</h2>\n      <ul class="fw-liste">\n'
             + '\n'.join(f'        <li>{esc(x)}</li>' for x in q['enthalten']) + '\n      </ul>\n'
             f'      <p class="fw-preis"><span class="fw-preis-zahl">{esc(q["preis"])}</span> <small class="lsx-netto">netto</small></p>\n'
             f'      <p class="gedaempft">{esc(q["preis_hinweis"])}</p>\n'
             f'      <p><a class="button" href="{pre}kontakt/">Projekt anfragen{PFEIL}</a></p>\n    </div>\n  </section>',
             beleg(q['beleg'], pre),
             faq(q['faq']),
             abschluss(pre)]
    schreibe(q['pfad'], '\n\n'.join(teile), q['seitentitel'], q['beschreibung'], q['faq'])


if __name__ == '__main__':
    uebersicht()
    for p in D['probleme']:
        problemseite(p)
    for b in D['branchen']:
        branchenseite(b)
    produktseite(D['produkt'])
