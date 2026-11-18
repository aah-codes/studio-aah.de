# Erzeugt die Leistungsunterseiten (service/…/index.html) aus werkzeuge/leistungen-inhalte.json (Texte, FAQ)
# und werkzeuge/preise-daten.json (Pakete, Preise, Zusatzleistungen). Kopf und Fuß bleiben aus der bestehenden Seite erhalten,
# der Prozess kommt aus werkzeuge/inhalte/prozess.html (bis 09.11.2026 von der Startseite).
# Aufruf im Repository-Ordner:  python3 werkzeuge/leistungsseiten.py [id …]   (ohne id: alle)
import json, re, sys

from gemeinsam import (ankerleiste, spiel_sektion, LINKEDIN, NETTO_SATZ, STUDIO_ID, TRENNEN_LEISTUNGEN, WEBSITE, WERKZEUGE, esc, lade_json, lade_skript,
                       paket_karte, preis, seitenrahmen, trennen as trennen_mit, weitere_pakete, zwei_pakete)

preise = lade_json('preise-daten.json')
inhalte = lade_json('leistungen-inhalte.json')
I = lade_skript('inhalte-erzeugen.py')
GEMEINSAM = lade_json('inhalte/faq-gemeinsam.json')['faq']


# Website-Check-Knopf und -Karte nur, wenn es die Seite /website-check/ gibt (im Zweig mit dem Website-Check-Formular)
MIT_CHECK = (WEBSITE / 'website-check' / 'index.html').exists()


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


def karten(g, pre=''):
    return '\n'.join(paket_karte(e, TRENNEN, pre) for e in g['pakete'])


def paket_reihen(g, c, pre=''):
    if len(g['pakete']) == 1:
        h = c.get('hintergrund')
        rechts = (f'<div class="lsx-hintergrund"><p class="meta">Mein Hintergrund</p><h3 class="lsx-hintergrund-titel">{esc(h["titel"])}</h3>'
                  + ''.join(f'<p>{esc(x)}</p>' for x in h['text'])
                  + (f'<p><a class="textlink" href="{pre}profil/#ansatz-titel">Mehr über meinen Hintergrund <span aria-hidden="true">→</span></a></p>' if h.get('link') else '') + '</div>') if h else nicht_enthalten(c)
        return '    <div class="lsx-einzeln">\n' + karten(g, pre) + '\n      ' + rechts + '\n    </div>'
    if not c.get('paket_reihen'):
        return '    <div class="lsx-karten">\n' + karten(g, pre) + '\n    </div>'
    nach_id = {e['id']: e for e in g['pakete']}
    return '\n'.join(f'    <div class="lsx-karten lsx-karten-{len(r)}">\n' + karten({**g, 'pakete': [nach_id[i] for i in r]}, pre) + '\n    </div>' for r in c['paket_reihen'])


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
# Prozess der Website-Projekte: eigene Quelle, seit er nicht mehr auf der Startseite steht (Anna, 09.11.2026)
MENUE_VERSION = re.search(r'menue\.js\?v=(\w+)', START).group(1)  # Version für js/spiel.js
PROZESS = (WEBSITE.parent / 'werkzeuge' / 'inhalte' / 'prozess.html').read_text(encoding='utf-8')


def dachzeile(m, h):
    # Dachzeile weglassen, wenn sie die Überschrift nur wiederholt (z. B. „Launch“ über „Launch.“, Anna 12.10.2026)
    return '' if m.rstrip('.').lower() == h.rstrip('.').lower() else f'<p class="meta">{esc(m)}</p>'


def ablauf_eigen(pre, schritte, hinweis=''):
    """Eigene Schritte einer Leistung als horizontale Zeitleiste mit Punkten (zl-quer, wie Startseite und Profil; Anna 16.11.2026)."""
    li = ''.join(f'<li><span class="zlq-nr">{i:02d}</span><div class="zl-text">{dachzeile(m, h)}<h3>{trennen(esc(h))}</h3><p class="gedaempft">{trennen(esc(x))}</p></div></li>' for i, (m, h, x) in enumerate(schritte, 1))
    return (f'  <section class="prozess-kompakt" id="ablauf" aria-labelledby="prozess">\n    <p class="meta">Wie ich arbeite</p>\n    <h2 class="preis-h2" id="prozess">Prozess</h2>\n'
            + (f'    <p class="lsx-ablauf-hinweis">{esc(hinweis)}</p>\n' if hinweis else '') +
            f'    <ol class="zl-quer zlq-{len(schritte)}">{li}</ol>\n    <p><a class="button" href="{pre}kontakt/">Beratung anfragen <span aria-hidden="true">→</span></a></p>\n  </section>')


def ablauf(pre):
    m = re.search(r'<section class="prozess-kompakt".*?</section>', PROZESS, re.S)
    if not m: raise SystemExit('Prozess (section.prozess-kompakt) fehlt in werkzeuge/inhalte/prozess.html')
    s = re.sub(r'href="(kontakt/|website-check/)"', lambda h: f'href="{pre}{h.group(1)}"', m.group(0))
    return '  ' + s.replace('<section class="prozess-kompakt"', '<section class="prozess-kompakt" id="ablauf"', 1)


def stimmen(pre, tag):
    liste = I.mit_tag(I.STIMMEN, [tag])[:3]
    if not liste: return ''
    return '  <section class="lsx-stimmen" aria-labelledby="stimmen-titel">\n    <p class="meta">Stimmen</p>\n    <h2 class="gr-h3" id="stimmen-titel">Das sagen Kundinnen und Kolleginnen</h2>\n    <div class="stimmen">\n' + I.stimmen(liste, pre) + '\n    </div>\n    <p class="stimmen-quelle"><a class="textlink" href="' + LINKEDIN + '" target="_blank" rel="noopener">Alle Empfehlungen auf LinkedIn <span aria-hidden="true">↗</span></a></p>\n  </section>'


def nicht_enthalten(c):
    if not c.get('nicht_enthalten'): return ''
    li = ''.join(f'<li>{esc(x)}</li>' for x in c['nicht_enthalten'])
    return f'<div class="lsx-nicht"><p class="meta">Nicht enthalten</p><ul>{li}</ul></div>'


def ohne_bauer(liste, tag):
    # Anna 12.11.2026: Bauer nur bei Webdesign, Branche Bau und auf der Startseite
    return liste if tag == 'website' else [p for p in liste if p.get('slug') != 'bauer']


def referenzen(tag, pre):
    liste = ohne_bauer(I.mit_tag(I.PROJEKTE, [tag]), tag)
    if not liste: return ''
    return '  <section class="lsx-referenzen" id="referenzen" aria-labelledby="referenzen-titel">\n    <p class="meta">Referenzen</p>\n    <h2 class="gr-h2" id="referenzen-titel">Projekte aus diesem Bereich</h2>\n    <div class="referenz-rahmen">\n' + I.referenz_karten(liste, pre, 'lsx', tag) + '\n    </div>\n  </section>'


# Ersatz-Schlagworte, solange es zu einer Leistung weniger als zwei eigene Artikel gibt (Anna 18.11.2026: „mindestens 2“)
ARTIKEL_ERSATZ = {'marketing': ['brand', 'website'], 'print': ['brand'], 'illustration': ['ui-ux', 'brand'], 'motion': ['brand', 'website'], 'retainer': ['website']}


def artikel(pre, tag):
    return I.passende_artikel([tag], pre, ARTIKEL_ERSATZ.get(tag, ()))


def kontakt(g, pre, link, link_text, termine, anfrage, satz='Bei STUDIO AAH! arbeiten Sie direkt mit mir, von der ersten Idee bis zum Launch.'):
    check = (f'<a class="textlink" href="{pre}website-check/">Kostenloser Website-Check <span aria-hidden="true">→</span></a>' if MIT_CHECK and g['id'] == 'website' else '')
    return f'''  <section class="lsx-ansprech" id="kontakt" aria-labelledby="kontakt-titel">
    <img src="{pre}bilder/anna-haertelt-studio-blau.webp" alt="Anna Härtelt, Gründerin von STUDIO AAH!" width="1200" height="1600" loading="lazy">
    <div>
      <p class="meta">Ihre Ansprechpartnerin</p>
      <h2 class="gr-h2" id="kontakt-titel">Starten Sie Ihr Projekt</h2>
      <p class="lsx-ansprech-name"><strong>Anna Härtelt</strong> · UX/UI-Designerin, Strategin und Webentwicklerin</p>
      <p>{esc(satz)}</p>
      <ul class="lsx-ansprech-wege">
        <li><span class="meta">Telefon</span><a href="tel:+4917683089879">0176 830 898 79</a></li>
        <li><span class="meta">E-Mail</span><a href="mailto:info@studio-aah.de">info@studio-aah.de</a></li>
      </ul>
{f'      <p class="lsx-termine"><span class="meta">Abstimmung</span> {esc(termine)}</p>' if termine else ''}
      <p class="lsx-knoepfe"><a class="button" href="{pre}kontakt/">{anfrage} <span aria-hidden="true">→</span></a> {check} <a class="textlink" href="{link}">{link_text} <span aria-hidden="true">→</span></a> <a class="textlink" href="{pre}profil/">Mehr über mich <span aria-hidden="true">→</span></a></p>
    </div>
{I.kennzahlen('fakten lsx-fakten', '    ')}
  </section>'''


def grafik(name):
    """Grafik aus werkzeuge/grafiken/<name>.html (für Leistungsseiten mit ../../ geschrieben)."""
    return (WERKZEUGE / 'grafiken' / f'{name}.html').read_text(encoding='utf-8')


def gruppe_fuer(c):
    """Preisgruppe der Seite. Mehrere Seiten teilen sich eine Gruppe (zusatz): nur die genannten Pakete, eigener Einleitungssatz;
    „paket_extra“ ergänzt die Paketdaten nur für diese Seite (z. B. Stundensatz statt „auf Anfrage“)."""
    g = next(x for x in preise['gruppen'] if x['id'] == c['gruppe'])
    if c.get('pakete'):
        g = {**g, 'pakete': [{**e, **c.get('paket_extra', {})} for e in g['pakete'] if e['id'] in c['pakete']], 'extras': []}
    else:
        gezeigt, rest = zwei_pakete(g)  # höchstens zwei Karten, der Rest als Zeile (Anna 17.11.2026)
        g = {**g, 'pakete': gezeigt, 'weitere': rest}
    return g


def fragen_fuer(c, termine):
    """FAQ der Seite: eigene Fragen, Frage zu den Abstimmungsterminen, gemeinsame Fragen aller Leistungsseiten."""
    satz = termine if termine.startswith('Termine') else termine[0].lower() + termine[1:]  # Substantiv bleibt groß
    zusatz = '' if 'nach Absprache' in termine else ' Weitere Termine vereinbaren wir nach Absprache.'
    # Antwort ohne „Bei STUDIO AAH!“ (Anna 16.11.2026: in der Antwort Ich-Form oder allgemein); entfällt, wo der Prozess die Termine zeigt
    termin_frage = [['Wie oft gibt es bei STUDIO AAH! Abstimmungstermine?', 'Es gibt ' + satz + zusatz]] if c.get('termine_zeigen', True) else []
    return c['faq'] + termin_frage + ([] if c.get('ohne_gemeinsame_fragen') else GEMEINSAM)


def seitenkopf(c, pre, intro, termine):
    woerter = c['titel'].split()
    titel_vorne = esc(' '.join(woerter[:-1])) + ' ' if len(woerter) > 1 else ''
    # Icon der Leistung über der Dachzeile (Anna 18.11.2026: „Dieses Icon dann auch oben im Hero über der Dachzeile einfügen“)
    return f'''  <section class="seitenkopf lsx-kopf">
    <img class="lsx-kopf-icon" src="{pre}{c['icon']}" alt="" width="400" height="400">
    <p class="meta brotkrumen"><a href="{pre}#leistungen">Leistungen</a> / <span aria-current="page">{esc(c['titel'])}</span></p>
    <h1 class="gr-xxl lsx-titel" style="--n:{max(len(w) for w in woerter)}">{titel_vorne}<span class="wort-mit-icon">{esc(woerter[-1])}<img class="icon-3d" src="{pre}{c['icon']}" alt="" width="400" height="400"></span></h1>
    <p class="alt-klein">{trennen(esc(intro))}</p>
    <p class="lsx-hero-knopf"><a class="button" href="#ueberblick">Kurz erklärt <span aria-hidden="true">→</span></a></p>
  </section>'''


def sprungleiste(c, g, mit_vergleich, mit_ablauf, link, link_text):
    # Content-First (Anna 16.11.2026): eine Frage je Abschnitt, Preise unter einem Anker, Artikel nicht in der Leiste
    ziele = [('loesung', 'Ausgangslage' if c.get('gegenueber') else 'Warum', True), ('anwendungen', 'Anwendungsfälle', bool(c.get('anwendungen'))),
             ('wege', 'Lösung', bool(c.get('wege'))), ('praxis', 'Beispiel', bool(c.get('praxis'))), ('recht', 'KI-Verordnung', bool(c.get('recht'))), ('leistungen', 'Leistungen', bool(c.get('loesungen')) and not c.get('ohne_detail')), ('ablauf', 'Ablauf', mit_ablauf),
             ('referenzen', 'Referenzen', bool(ohne_bauer(I.mit_tag(I.PROJEKTE, [c['tag']]), c['tag']))),
             ('selbst', 'Selbst bauen', bool(c.get('selbstbau'))), ('pakete', 'Preise', True), ('faq', 'Häufige Fragen', True)]
    return ankerleiste([(anker, text) for anker, text, an in ziele if an])


# „Was Sie davon haben“ und „Für Sie, wenn“ oben auf jeder Leistungsseite (Anna, 09./10.11.2026: Schmerzpunkte 1–4 überall, immer den Nutzen)
PROBLEME = {x['id']: x for x in lade_json('inhalte/fuer-wen-seiten.json')['probleme']}


def was_ist(c, pre):
    """Abschnitt 1 nach dem Hero (IT Sonix „Individuelle Software: Was ist das?“): Definition aus „zusammenfassung“,
    daneben der Nutzen („gewinn“) und die Anliegen („fuer_sie“). Überschrift überschreibbar mit „frage“."""
    frage = c.get('frage') or f"{c['titel']}: Was ist das?"
    text = ''.join(f'<p>{trennen(esc(x))}</p>' for x in c.get('zusammenfassung', []))
    punkte = ''.join(f'<li>{esc(x)}</li>' for x in c.get('gewinn', []))
    # Linktext = Schlagwort der Zielseite (Anna 16.11.2026: „nur jeweils ein Wort, ein Keyword“)
    fuer = ''.join(f'<li><a href="{pre}{PROBLEME[i]["pfad"]}"><span>{esc(PROBLEME[i]["meta"])}</span> <span aria-hidden="true">→</span></a></li>'
                   for i in c.get('fuer_sie', []))
    rechts = ((f'<div class="lsx-was-nutzen"><p class="meta">Was Sie davon haben</p><ol class="lsx-gewinn-liste">{punkte}</ol></div>' if punkte else '')
              + (f'<div class="lsx-fuer"><p class="meta">Für Sie, wenn</p><ul>{fuer}</ul></div>' if fuer else ''))
    return f'''  <section class="lsx-was" id="ueberblick" aria-labelledby="was-titel">
    <div class="lsx-was-text"><p class="meta">Kurz erklärt</p><h2 class="gr-h2" id="was-titel">{trennen(esc(frage))}</h2>{text}</div>
    <div class="lsx-was-seite">{rechts}</div>
  </section>'''


def gegenueber(c, g, pre, link):
    """Problemraum und Lösungsraum als Gegenüberstellung (Anna 16.11.2026, KI-Beratung): je Zeile ein Problem von heute
    und was sich ändert. Ersetzt „Warum“, wenn das Feld „gegenueber“ gesetzt ist."""
    x = c['gegenueber']
    zeilen = ''.join(f'''<li><p class="lsx-gg-heute">{esc(a)}</p><span class="lsx-gg-pfeil" aria-hidden="true">→</span><div class="lsx-gg-dann"><h3>{esc(t)}</h3><p>{esc(b)}</p></div></li>''' for a, t, b in x['zeilen'])
    return f'''  <section class="lsx-gg" id="loesung" aria-labelledby="loesung-titel">
    <p class="meta">Ausgangslage</p>
    <h2 class="gr-h2" id="loesung-titel">{esc(c['problem_titel'])}</h2>
    <div class="lsx-gg-kopf" aria-hidden="true"><span>{esc(x['links'])}</span><span>{esc(x['rechts'])}</span></div>
    <ol class="lsx-gg-liste">{zeilen}</ol>
{f'    <p class="lsx-gg-kosten">{esc(x["kosten"])}</p>' if x.get('kosten') else ''}
  </section>'''


def anwendungen(c, pre):
    """Konkrete Anwendungsfälle als Karten, dazu ein Beleg aus der eigenen Praxis (Feld „anwendungen“)."""
    if not c.get('anwendungen'): return ''
    x = c['anwendungen']
    karten = ''.join(f'<li><span class="lsx-nr" aria-hidden="true">{i:02d}</span><h3>{esc(t)}</h3><p>{esc(b)}</p></li>' for i, (t, b) in enumerate(x['karten'], 1))
    titel, text = x['beleg']
    extra = ''
    if x.get('extra'):
        et, eb, eh, el = x['extra']
        extra = (f'    <div class="lsx-anw-extra"><h3>{esc(et)}</h3><p>{esc(eb)}</p>'
                 f'<p><a class="textlink" href="{pre}{eh}">{esc(el)} <span aria-hidden="true">→</span></a></p></div>')
    return f'''  <section class="lsx-anw" id="anwendungen" aria-labelledby="anwendungen-titel">
    <p class="meta">Anwendungsfälle</p>
    <h2 class="gr-h2" id="anwendungen-titel">{esc(x['titel'])}</h2>
    <ul class="lsx-anw-liste">{karten}</ul>
{f'    <p class="lsx-anw-hinweis">{esc(x["hinweis"])}</p>' if x.get('hinweis') else ''}
    <div class="lsx-anw-beleg"><p class="meta">{esc(titel)}</p><p>{esc(text)}</p></div>
{extra}
  </section>'''


def wege(c, pre):
    """Lösung (Feld „wege“): ein Angebot mit seinen Bausteinen als Karten und Link zur Angebotsseite (Anna 16.11.2026: nur KI-Arbeits-Setup)."""
    if not c.get('wege'): return ''
    x = c['wege']
    karten = ''.join(f'<li><span class="lsx-nr" aria-hidden="true">{i:02d}</span><h3>{esc(t)}</h3><p>{esc(b)}</p></li>' for i, (t, b) in enumerate(x['karten'], 1))
    ziel, text = x['link']
    return f'''  <section class="lsx-wege" id="wege" aria-labelledby="wege-titel">
    <p class="meta">{esc(x.get('meta', 'Lösung'))}</p>
    <h2 class="gr-h2" id="wege-titel">{esc(x['titel'])}</h2>
    <p class="lsx-wege-einleitung">{esc(x['einleitung'])}</p>
    <ol class="lsx-wege-liste">{karten}</ol>
    <p class="lsx-wege-mehr"><a class="button button-zweit" href="{pre}{ziel}">{esc(text)} <span aria-hidden="true">→</span></a></p>
  </section>'''


def praxis(c, pre):
    """Beispiel aus einem echten Projekt, anonym (Feld „praxis“, KI-Beratung: KI-Arbeits-Setup, Anna 16.11.2026)."""
    if not c.get('praxis'): return ''
    x = c['praxis']
    spalten = ''.join(f'<div><h3>{esc(t)}</h3><ul>' + ''.join(f'<li>{esc(i)}</li>' for i in liste) + '</ul></div>' for t, liste in x['gruppen'])
    return f'''  <section class="lsx-praxis" id="praxis" aria-labelledby="praxis-titel">
    <p class="meta">Aus der Praxis</p>
    <h2 class="gr-h2" id="praxis-titel">{esc(x['titel'])}</h2>
    <p class="lsx-praxis-einleitung">{esc(x['einleitung'])}</p>
    <div class="lsx-praxis-raster">{spalten}</div>
    <p class="lsx-praxis-grenze">{esc(x['grenze'])} <a class="textlink" href="{pre}ki-arbeits-setup/">Zum KI-Arbeits-Setup <span aria-hidden="true">→</span></a></p>
  </section>'''


def recht(c):
    """Rechtlicher Rahmen kurz erklärt (Feld „recht“, KI-Verordnung); Stand im Text, keine Rechtsberatung."""
    if not c.get('recht'): return ''
    x = c['recht']
    punkte = ''.join(f'<li><p class="lsx-recht-datum">{esc(d)}</p><h3>{esc(t)}</h3><p>{esc(b)}</p></li>' for d, t, b in x['punkte'])
    # optional: weiterführender Blogartikel (Feld „artikel“: [Linktext, Pfad ab Wurzel]), Anna 17.11.2026
    artikel = f'\n    <p><a class="textlink" href="../../{x["artikel"][1]}">{esc(x["artikel"][0])} <span aria-hidden="true">→</span></a></p>' if x.get('artikel') else ''
    return f'''  <section class="lsx-recht" id="recht" aria-labelledby="recht-titel">
    <p class="meta">Recht</p>
    <h2 class="gr-h2" id="recht-titel">{esc(x['titel'])}</h2>
    <p class="lsx-recht-einleitung">{esc(x['einleitung'])}</p>
    <ol class="lsx-recht-liste">{punkte}</ol>
    <p class="lsx-recht-bei-mir">{esc(x['bei_mir'])} <span class="lsx-recht-stand">{esc(x['stand'])}</span></p>{artikel}
  </section>'''


def selbstbau(c, pre):
    """Für alle, die ihre Website selbst bauen (Vibe-Coding, Baukasten; Anna 17.11.2026): vier Einstiege von vorher bis nachher."""
    if not c.get('selbstbau'): return ''
    x = c['selbstbau']
    karten = ''.join(f'<li><span class="lsx-nr" aria-hidden="true">{i:02d}</span><h3>{esc(t)}</h3><p>{esc(b)}</p>'
                     f'<p class="lsx-sb-link"><a class="textlink" href="{pre}{h}">{esc(l)} <span aria-hidden="true">→</span></a></p></li>'
                     for i, (t, b, h, l) in enumerate(x['schritte'], 1))
    return f'''  <section class="lsx-selbst" id="selbst" aria-labelledby="selbst-titel">
    <p class="meta">Selbst bauen</p>
    <h2 class="gr-h2" id="selbst-titel">{esc(x['titel'])}</h2>
    <p class="lsx-wege-einleitung">{esc(x['einleitung'])}</p>
    <ol class="lsx-selbst-liste">{karten}</ol>
  </section>'''


def kompetenzen(c):
    """Was genau dazugehört, nummeriert wie die Kernkompetenzen bei IT Sonix (Daten: „loesungen“)."""
    if not c.get('loesungen') or c.get('ohne_detail'): return ''
    li = ''.join(f'<li><span class="lsx-nr" aria-hidden="true">{i:02d}</span><p>{trennen(esc(x))}</p></li>' for i, x in enumerate(c['loesungen'], 1))
    return f'''  <section class="lsx-kompetenz" id="leistungen" aria-labelledby="leistungen-titel">
    <p class="meta">Leistung im Detail</p>
    <h2 class="gr-h2" id="leistungen-titel">Was dazugehört</h2>
    <ol class="lsx-kompetenz-liste">{li}</ol>
  </section>'''


def problem_loesung(c, g, pre, link):
    anfrage = c.get('anfrage', 'Beratung anfragen')  # Retainer: „Beratung anfragen“ (Anna 16.11.2026)
    probleme = ''.join(f'<li>{esc(x)}</li>' for x in c['probleme'])
    punkte = '' if c.get('loesungen') else ''.join(f'<li>{esc(x)}</li>' for x in c['loesung_punkte'][:3])
    grundsatz = '' if c.get('grafik') == 'corporate-identity' or any('Form follows' in x for x in c.get('loesungen', [])) else (
        f'<p class="lsx-grundsatz"><a class="textlink" href="{pre}service/markenbildung/#corporate-identity">Form follows function, die Form folgt der Funktion. '
        'Grundlage für alles, was ich gestalte, ist die Corporate Identity <span aria-hidden="true">→</span></a></p>')
    # Webdesign: Website-Check als zweiter Knopf (Anna 25.10.2026: niedrigschwelligster Einstieg)
    check = (f'<a class="button button-zweit" href="{pre}website-check/">Kostenloser <span class="ohne-umbruch">Website-Check&nbsp;<span aria-hidden="true">→</span></span></a> '
             if g['id'] == 'website' and MIT_CHECK else '')
    # Content-First: keine Dopplung. Wiederholt „loesung_text“ den Einstieg (Was ist das?), entfällt die Lösungskarte
    doppelt = any(c['loesung_text'][:30] == z[:30] for z in c.get('zusammenfassung', []))
    loesung = '' if doppelt else f'''<div class="lsx-pl-loesung"><p class="meta">So mache ich es</p><p class="lsx-pl-text">{esc(c['loesung_text'])}</p>{f'<ul>{punkte}</ul>' if punkte else ''}
        {grundsatz}</div>'''
    if doppelt and grundsatz:
        probleme_extra = grundsatz.replace('lsx-grundsatz', 'lsx-grundsatz lsx-grundsatz-hell')
    else:
        probleme_extra = ''
    return f'''  <section class="lsx-loesung lsx-pl{' lsx-pl-allein' if doppelt else ''}" id="loesung" aria-labelledby="loesung-titel">
    <p class="meta">Warum</p>
    <h2 class="gr-h2" id="loesung-titel">{esc(c['problem_titel'])}</h2>
    <div class="lsx-pl-raster">
      <div class="lsx-pl-problem"><p class="meta">Woran es oft hakt</p><ul>{probleme}</ul>{probleme_extra}</div>
      {loesung}
      <p class="lsx-knoepfe"><a class="button" href="{pre}kontakt/">{anfrage} <span aria-hidden="true">→</span></a> {check}<a class="textlink" href="{link}">{'Kosten berechnen' if g['id'] == 'website' else 'Alle Preise'} <span aria-hidden="true">→</span></a></p>
    </div>
  </section>'''


def pakete(c, g, pre):
    hinweis = f'<p class="lsx-hinweis">{esc(g["hinweis"])}</p>' if g.get('hinweis') else ''
    return f'''  <section class="lsx-pakete" id="pakete" aria-labelledby="pakete-titel">
    <p class="meta">Preise</p>
    <h2 class="gr-h2" id="pakete-titel">Was es kostet</h2>
    {hinweis}
{paket_reihen(g, c, pre)}
{weitere_pakete(g.get('weitere', []))}    {NETTO_HINWEIS}
    {'' if len(g['pakete']) == 1 and not c.get('hintergrund') else nicht_enthalten(c)}
  </section>'''


def retainer_hinweis(g, pre):
    """Nach dem Ablauf: Retainer als nächster Schritt nach dem Launch (Anna 25.10.2026, nur Webdesign). Texte aus den Paketdaten."""
    r = next((e for e in g['pakete'] + g.get('extras', []) if e['id'] == 'retainer-web'), None)
    if not r: return ''
    preis = f"{r['stunde']}–{r['stundeBis']} € netto pro Stunde, {r['mindestens']}"
    return f'''  <section class="lsx-retainer" aria-labelledby="retainer-titel">
    <p class="meta">Nach dem Launch</p>
    <h2 class="gr-h3" id="retainer-titel">{esc(r['name'])}</h2>
    <p>{esc(r['kurz'])}. {esc(preis)}.</p>
    <p><a class="textlink" href="{pre}service/retainer/">Mehr zum Retainer <span aria-hidden="true">→</span></a></p>
  </section>'''


def faq(fragen, pre):
    eintraege = ''.join(f'''      <details class="faq-eintrag">
        <summary>{esc(q)}</summary>
        <div class="faq-antwort"><p>{esc(a)}</p></div>
      </details>
''' for q, a in fragen)
    return f'''  <section class="faq" id="faq" aria-labelledby="faq-titel">
    <h2 class="gr-h2" id="faq-titel">Häufige Fragen</h2>
    <div class="faq-liste faq-einspaltig">
{eintraege}    </div>
  </section>'''


def strukturierte_daten(c, g, intro, url, fragen, vorlage):
    """Leistung mit Angeboten und FAQ (für Suchmaschinen und KI-Antworten); Studio-Angaben aus der Vorlage."""
    studio = re.search(r'\{\s*"@type": "ProfessionalService".*?"areaServed": \[[^\]]*\]\s*\}', vorlage, re.S)
    angebote = [{"@type": "Offer", "name": e['name'], "priceCurrency": "EUR", "price": str(e['preis']),
                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": e['preis'], "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}
                for e in g['pakete'] + g.get('weitere', []) if e.get('preis')]
    angebote += [{"@type": "Offer", "name": e['name'], "priceCurrency": "EUR",
                  "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": e['stunde'], **({"maxPrice": e['stundeBis']} if e.get('stundeBis') else {}),
                                         "priceCurrency": "EUR", "unitText": "Stunde", "valueAddedTaxIncluded": False}}
                 for e in g['pakete'] + g.get('weitere', []) if e.get('stunde') and not e.get('preis')]
    graph = [json.loads(studio.group(0)) if studio else {"@id": STUDIO_ID},
             {"@type": "Service", "@id": url + '#leistung', "name": c['titel'], "description": intro, "url": url,
              "provider": {"@id": STUDIO_ID}, "areaServed": "Leipzig", "offers": angebote},
             {"@type": "FAQPage", "@id": url + '#faq', "url": url, "inLanguage": "de",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fragen]}]
    return {"@context": "https://schema.org", "@graph": graph}


def seite(key, c):
    g = gruppe_fuer(c)
    intro = c.get('intro') or g['intro']
    # Der Prozess der Startseite beschreibt Website-Projekte; andere Leistungen brauchen eigene Schritte
    mit_ablauf = bool(c.get('ablauf_schritte')) or c.get('ablauf', c['gruppe'] == 'website')
    # Abstimmungstermine (Anna, 11.10.2026): im Projekt wöchentlich, bei laufender Betreuung seltener
    termine = c.get('termine', TERMINE)
    fragen = fragen_fuer(c, termine)
    pre = '../' * (c['pfad'].strip('/').count('/') + 1)
    link, link_text = preise_link(g, pre)
    pfad = WEBSITE / c['pfad'] / 'index.html'
    # neue Seite: Kopf und Fuß von der Webdesign-Seite übernehmen (gleiche Ordnertiefe)
    vorlage = (pfad if pfad.exists() else WEBSITE / 'service' / 'webdesign' / 'index.html').read_text(encoding='utf-8')
    url = 'https://studio-aah.de/' + c['pfad']
    vergleich_html = vergleich(g)
    prozess = (ablauf_eigen(pre, c['ablauf_schritte'], c.get('ablauf_hinweis', '')) if c.get('ablauf_schritte') else ablauf(pre)) if mit_ablauf else ''
    main = f'''<main id="inhalt">

{seitenkopf(c, pre, intro, termine)}

{was_ist(c, pre)}

{sprungleiste(c, g, bool(vergleich_html), mit_ablauf, link, link_text)}

{gegenueber(c, g, pre, link) if c.get('gegenueber') else problem_loesung(c, g, pre, link)}

{anwendungen(c, pre)}

{grafik('website-oekosystem') if c.get('herz') else ''}
{grafik(c['grafik']) if c.get('grafik') else ''}
{grafik(c['nutzen']) if c.get('nutzen') else ''}

{kompetenzen(c)}

{wege(c, pre)}

{praxis(c, pre)}

{recht(c)}

{prozess}

{retainer_hinweis(g, pre) if mit_ablauf else ''}

{selbstbau(c, pre)}

{stimmen(pre, c['tag'])}

{referenzen(c['tag'], pre)}

{pakete(c, g, pre)}

{vergleich_html}

{extras(g)}

{faq(fragen, pre)}

{kontakt(g, pre, link, link_text, termine if c.get('termine_zeigen', True) else '', c.get('anfrage', 'Beratung anfragen'), **({'satz': c['ansprech_satz']} if c.get('ansprech_satz') else {}))}

{artikel(pre, c['tag'])}

{spiel_sektion(pre, MENUE_VERSION) if c.get('spiel') else ''}

</main>'''
    t = seitenrahmen(vorlage, main, c['seitentitel'], c['beschreibung'], url, strukturierte_daten(c, g, intro, url, fragen, vorlage))
    if 'zaehlen.js' not in t:  # Kennzahlen zählen hoch; Version wie auf der Startseite
        version = re.search(r'zaehlen\.js\?v=(\w+)', START).group(1)
        t = t.replace('</body>', f'  <script src="{pre}js/zaehlen.js?v={version}" defer></script>\n</body>', 1)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(t, encoding='utf-8')
    print('geschrieben:', c['pfad'])


if __name__ == '__main__':
    for k in sys.argv[1:] or [k for k in inhalte if not k.startswith('_')]:
        seite(k, inhalte[k])
