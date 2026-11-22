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


# Handschrift-Redigat je Seite (Anna 22.11.2026): ersetzt fertige Überschriften; durchgestrichen = aria-hidden, Hand = gelesen
def _ko(alt, neu):
    return f'<span class="korrektur ko-unten"><span class="notiz notiz-durch" aria-hidden="true">{alt}</span><span class="hand">{neu}</span></span>'
REDIGAT = {
    'service/markenbildung/': [
        ('style="--n:13">Markenbildung<br>in Leipzig</h1>', 'style="--n:26">Markenbildung in Leipzig: Keine ' + _ko('Kosmetik.', 'Dekoration für die Visitenkarte.') + '<br>Sondern Klarheit, die anzieht.</h1>'),
        ('<p class="alt-klein">Eine unverwechselbare Marken- und Unternehmens&shy;identität, die bei deiner Zielgruppe wirklich ankommt.</p>', '<p class="alt-klein">Eine unverwechselbare Marken- und Unternehmens&shy;identität für den <span class="ohne-umbruch">B2B-Mittelstand</span> – damit Kunden und Fachkräfte sofort verstehen, warum ihr die Richtigen seid.</p>'),
        ('id="anlaesse-titel">Wann es sich lohnt</h2>', 'id="anlaesse-titel">Wann ein ' + _ko('neues Logo', 'echter Neustart') + ' fällig ist</h2>'),
        ('id="loesung-titel">Eine Marke wirkt nur, wenn sie zusammenhält.</h2>', 'id="loesung-titel">Eine Marke wirkt nur, wenn sie ' + _ko('zusammenhält.', 'innen und außen zusammenhält.') + '</h2>'),
        ('id="prozess">Prozess</h2>', 'id="prozess">Vier Schritte statt ' + _ko('Blindflug', 'Agentur-Blackbox') + '</h2>'),
        ('<span class="hand">Partnerschaften</span>', '<span class="hand">Partnerschaften auf Augenhöhe</span>'),
        ('id="stimmen-titel">Stimmen,<br>die zählen.</h2>', 'id="stimmen-titel">Stimmen,<br>die zählen.<span class="ko-block">Was passiert, wenn man es einfach anpackt</span></h2>'),
        ('id="faq-titel">Ehrliche Antworten</h2>', 'id="faq-titel">' + _ko('Standard-Antworten', 'Ehrliche Antworten') + '</h2>'),
        ('id="schluss-titel">Fangen wir klein an.</h2>', 'id="schluss-titel">Fangen wir <span class="ko-zitat-hand">klein</span> an.</h2>'),
    ],
}

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


TERMINE = 'Einmal pro Woche einen Termin, 45 Minuten, online über Google Meet oder Teams, je nachdem, was du brauchst.'
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
        # Nur eine Preiskarte: immer so groß wie bei der KI-Beratung (Anna 22.11.2026)
        k = karten(g, pre)
        if 'lsx-gefragt' not in k: k = k.replace('class="lsx-karte"', 'class="lsx-karte lsx-gefragt"', 1)
        return '    <div class="lsx-einzeln">\n' + k + '\n      ' + rechts + '\n    </div>'
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
    <p class="meta">Pakete</p>
    <h2 class="gr-h2" id="vergleich-titel">Im Vergleich</h2>
    <div class="lsx-tabelle-rahmen"><table class="lsx-tabelle"><thead><tr><th scope="col">Leistung</th>{kopf}</tr></thead><tbody>{rumpf}</tbody></table></div>
    {NETTO_HINWEIS}
  </section>'''


def extras(g):
    ex = [e for e in g.get('extras', []) if not e.get('nurRechner')]  # seltene Funktionen nur im Kostenrechner
    if not ex: return ''
    # Zusatzleistungen als Akkordeon (Anna 22.11.2026: „zu breit, zu viele Infos, eher verstecken“): Name und Preis sichtbar, Beschreibung aufklappbar
    li = ''.join(f'<li><details class="lsx-extra"><summary><span class="lsx-extra-name">{esc(e["name"])}</span><span class="lsx-extra-preis">{preis(e)}</span></summary>'
                 f'<p class="lsx-extra-text">{esc(e.get("kurz") or e.get("wer") or "")}</p></details></li>' for e in ex)
    return f'''  <section class="lsx-extras" id="extras" aria-labelledby="extras-titel">
    <h2 class="gr-h3" id="extras-titel">Zusatz&shy;leistungen</h2>
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
    return (f'  <section class="prozess-kompakt" id="ablauf" aria-labelledby="prozess">\n    <p class="meta">Wie ich arbeite</p>\n    <h2 class="gr-h2" id="prozess">Prozess</h2>\n'
            + (f'    <p class="lsx-ablauf-hinweis">{esc(hinweis)}</p>\n' if hinweis else '') +
            f'    <ol class="zl-quer zlq-{len(schritte)}">{li}</ol>\n    <p><a class="button" href="{pre}kontakt/">Beratung anfragen <span aria-hidden="true">→</span></a></p>\n  </section>')


def ablauf(pre):
    m = re.search(r'<section class="prozess-kompakt".*?</section>', PROZESS, re.S)
    if not m: raise SystemExit('Prozess (section.prozess-kompakt) fehlt in werkzeuge/inhalte/prozess.html')
    s = re.sub(r'href="(kontakt/|website-check/)"', lambda h: f'href="{pre}{h.group(1)}"', m.group(0))
    return '  ' + s.replace('<section class="prozess-kompakt"', '<section class="prozess-kompakt" id="ablauf"', 1)


def stimmen(pre, tag):
    # Immer genau zwei Stimmen (Anna 21.11.2026); fehlt eine passende, kommt eine allgemeine dazu
    liste = I.mit_tag(I.STIMMEN, [tag])[:2]
    for s in I.STIMMEN:
        if len(liste) >= 2: break
        if s not in liste: liste.append(s)
    if not liste: return ''
    # Anna 22.11.2026: Gestaltung wie auf der Startseite (Kopf mittig und groß)
    return '  <section class="lsx-stimmen" aria-labelledby="stimmen-titel">\n    <div class="sektionskopf sk-mitte"><p class="meta">Meinungen</p>\n    <h2 class="gr-xxl" id="stimmen-titel">Stimmen,<br>die zählen.</h2></div>\n    <div class="stimmen">\n' + I.stimmen(liste, pre) + '\n    </div>\n    <p class="stimmen-quelle"><a class="textlink" href="' + LINKEDIN + '" target="_blank" rel="noopener">Alle Empfehlungen auf LinkedIn <span aria-hidden="true">↗</span></a></p>\n  </section>'


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
    # Anna 22.11.2026: wie die Projektseite – „Projekte“ durchgestrichen zu „Partnerschaften“, Projektkarten im Raster
    karten = '\n'.join(f'      <li>{I.projekt_karte(p, pre, h="h3", satz=False)}</li>' for p in liste)
    return ('  <section class="lsx-referenzen" id="referenzen" aria-labelledby="referenzen-titel">\n    <div class="sektionskopf"><p class="meta">Referenzen</p>'
            '<h2 class="gr-h2 pa-titel" id="referenzen-titel"><span class="korrektur korrektur-partner korrektur-links"><span class="notiz notiz-durch" aria-hidden="true">Projekte</span><span class="hand">Partnerschaften</span></span></h2></div>\n'
            + (I.projekt_wechsel(liste, pre) if len(liste) > 1 else f'    <ul class="ref-raster">\n{karten}\n    </ul>') + '\n  </section>')


# Ersatz-Schlagworte, solange es zu einer Leistung weniger als zwei eigene Artikel gibt (Anna 18.11.2026: „mindestens 2“)
ARTIKEL_ERSATZ = {'marketing': ['brand', 'website'], 'print': ['brand'], 'illustration': ['ui-ux', 'brand'], 'motion': ['brand', 'website'], 'retainer': ['website']}


def artikel(pre, tag):
    return I.passende_artikel([tag], pre, ARTIKEL_ERSATZ.get(tag, ()))


def kontakt(g, pre, link, link_text, termine, anfrage, satz='Bei STUDIO AAH! arbeitest du direkt mit mir, von der ersten Idee bis zum Launch.'):
    check = (f'<a class="textlink" href="{pre}website-check/">Kostenloser Website-Check <span aria-hidden="true">→</span></a>' if MIT_CHECK and g['id'] == 'website' else '')
    return f'''  <section class="lsx-ansprech" id="kontakt" aria-labelledby="kontakt-titel">
    <img src="{pre}bilder/anna-haertelt-studio-blau.webp" alt="Anna Härtelt, Gründerin von STUDIO AAH!" width="1200" height="1600" loading="lazy">
    <div>
      <p class="meta">Deine Ansprechpartnerin</p>
      <h2 class="gr-h2" id="kontakt-titel">Starte dein Projekt</h2>
      <p class="lsx-ansprech-name"><strong>Anna Härtelt</strong> · UX/UI-Designerin, Strategin und Webentwicklerin</p>
      <p>{esc(satz)}</p>
      <p class="lsx-knoepfe"><a class="button" href="{pre}kontakt/">{anfrage} <span aria-hidden="true">→</span></a></p>
    </div>
  </section>'''   # aufgeräumt (Anna 21.11.2026): nur noch „Beratung anfragen“, ohne Telefon, Mail, Abstimmung, Preise, Kennzahlen


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


# „Was du davon hast“ und „Für dich, wenn“ oben auf jeder Leistungsseite (Anna, 09./10.11.2026: Schmerzpunkte 1–4 überall, immer den Nutzen)
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
    rechts = ((f'<div class="lsx-was-nutzen"><p class="meta">Was du davon hast</p><ol class="lsx-gewinn-liste">{punkte}</ol></div>' if punkte else '')
              + (f'<div class="lsx-fuer"><p class="meta">Für dich, wenn</p><ul>{fuer}</ul></div>' if fuer else ''))
    return f'''  <section class="lsx-was" id="ueberblick" aria-labelledby="was-titel">
    <div class="lsx-was-text"><p class="meta">Kurz erklärt</p><h2 class="gr-h2" id="was-titel">{trennen(esc(frage)).replace(': ', ':<br>', 1)}</h2>{text}</div>
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
    # Anna 22.11.2026: „liest sich so keiner durch“ – ohne Nummern als Liste zum Überfliegen; Teil vor dem Doppelpunkt fett
    def punkt(x):
        if ': ' in x:
            a, b = x.split(': ', 1)
            return f'<b>{trennen(esc(a))}</b> {trennen(esc(b[0].upper() + b[1:]))}'
        return f'<b>{trennen(esc(x))}</b>'
    li = ''.join(f'<li><p>{punkt(x)}</p></li>' for x in c['loesungen'])
    return f'''  <section class="lsx-kompetenz lsx-kompetenz-kurz" id="leistungen" aria-labelledby="leistungen-titel">
    <p class="meta">Leistung</p>
    <h2 class="gr-h2" id="leistungen-titel">Das bekommst du</h2>
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
      <div class="lsx-pl-problem lsx-pl-zettel"><p class="meta">Woran es oft hakt</p><ul>{probleme}</ul>{probleme_extra}</div>
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
{zusatz_block(c, g) if c.get('muster') else weitere_pakete(g.get('weitere', [])) + '    ' + NETTO_HINWEIS + chr(10) + '    ' + ('' if len(g['pakete']) == 1 and not c.get('hintergrund') else nicht_enthalten(c))}
  </section>'''


def zusatz_block(c, g):
    # Muster (Anna 22.11.2026: „anders“): zwei Kästen nebeneinander – Außerdem buchbar (Name und Preis je Zeile) und Nicht enthalten
    weitere = ''.join(f'<li><b>{esc(e["name"])}</b><span>{preis(e)}</span></li>' for e in g.get('weitere', []))
    links = f'<div class="lsx-m-kasten"><p class="meta">Außerdem buchbar</p><ul class="lsx-m-weitere">{weitere}</ul></div>' if weitere else ''
    # bei nur einer Preiskarte ohne Hintergrund steht „Nicht enthalten“ schon neben der Karte
    nicht = '' if len(g['pakete']) == 1 and not c.get('hintergrund') else ''.join(f'<li>{esc(x)}</li>' for x in c.get('nicht_enthalten', []))
    rechts = f'<div class="lsx-m-kasten"><p class="meta">Nicht enthalten</p><ul class="lsx-m-nicht">{nicht}</ul></div>' if nicht else ''
    return f'    <div class="lsx-m-zusatz">{links}{rechts}</div>\n    {NETTO_HINWEIS}'


def retainer_hinweis(g, pre):
    """Nach dem Ablauf: Retainer als nächster Schritt nach dem Launch (Anna 25.10.2026, nur Webdesign). Texte aus den Paketdaten."""
    r = next((e for e in g['pakete'] + g.get('extras', []) if e['id'] == 'retainer-web'), None)
    if not r: return ''
    preis = f"{r['stunde']}–{r['stundeBis']} € netto pro Stunde, {r['mindestens']}"
    return f'''  <section class="lsx-retainer" aria-labelledby="retainer-titel">
    <div class="lsx-retainer-text">
    <p class="meta">Nach dem Launch</p>
    <h2 class="gr-h3" id="retainer-titel">{esc(r['name'])}</h2>
    <p>{esc(r['kurz'])}. {esc(preis)}.</p>
    <p><a class="textlink" href="{pre}service/retainer/">Mehr zum Retainer <span aria-hidden="true">→</span></a></p>
    </div>
    <img class="lsx-retainer-bild" src="{pre}bilder/zeichnungen-sw/giesskanne.svg" alt="" width="400" height="400" loading="lazy">
  </section>'''


def faq(fragen, pre):
    eintraege = ''.join(f'''      <details class="faq-eintrag">
        <summary>{esc(q)}</summary>
        <div class="faq-antwort"><p>{esc(a)}</p></div>
      </details>
''' for q, a in fragen)
    return f'''  <section class="faq" id="faq" aria-labelledby="faq-titel">
    <p class="meta">Häufige Fragen</p>
    <h2 class="gr-h2" id="faq-titel">Ehrliche Antworten</h2>
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


# --- Muster-Leistungsseite (Anna 22.11.2026, zuerst Markenbildung): eine Frage je Abschnitt, Antwort zuerst, scanbar.
#     Konzept: Betrieb „Studio AAH/Website/2026-11-22_leistungsseite-markenbildung_muster.md“. Daten im Feld „muster“.
def fett_rest(paare):
    return ''.join(f'<li><b>{esc(a)}</b>{(" " + esc(b)) if b else ""}</li>' for a, b in paare)


def geteilt(x):
    # „Titel: Rest“ → (Titel, Rest mit großem Anfang); ohne Doppelpunkt nur Titel
    if ': ' in x:
        a, b = x.split(': ', 1)
        return a, b[:1].upper() + b[1:]
    return x, ''


def auto_muster(c, g, intro):
    """Muster-Aufbau für Leistungsseiten ohne eigenes Feld „muster“ (Anna 22.11.2026: „auf alle Leistungen anwenden“).
    Nur aus Texten, die schon auf der Seite stehen – keine neuen Aussagen."""
    pk = g.get('pakete', [])
    fakten, preiszeile = [], ''
    if pk and pk[0].get('stunde'):
        e = pk[0]
        fakten.append(f"{e['stunde']}–{e['stundeBis']} € netto pro Stunde")
    elif pk:
        ab = min((e.get('preis') for e in pk if isinstance(e.get('preis'), (int, float))), default=None)
        if ab: fakten.append(f"ab {ab:,.0f} € netto".replace(',', '.'))
        preiszeile = ', '.join(f"{e['name']} ab {e['preis']:,.0f} €".replace(',', '.') for e in pk if isinstance(e.get('preis'), (int, float)))
    fakten.append('Kostenloses Erstgespräch')
    kurz = []
    if c.get('zusammenfassung'):
        kurz.append([f"{c['titel']} bei STUDIO AAH!:", c['zusammenfassung'][0]])
    if preiszeile:
        kurz.append(['Preise:', preiszeile + ' (netto, Festpreis nach Erstgespräch).'])
    kurz += [['Ergebnis:', x] for x in c.get('gewinn', [])[:2]]
    return {'h1': c['titel'], 'intro': intro, 'fakten': fakten, 'kurz_gesagt': kurz,
            'probleme_kurz': [list(geteilt(x)) for x in c.get('probleme', [])],
            'ergebnisse': [] if c.get('ohne_detail') else [list(geteilt(x)) for x in c.get('loesungen', [])],
            'abschluss': {'meta': c['titel'], 'titel': 'Fangen wir klein an.', 'knopf': c.get('anfrage', 'Beratung anfragen'),
                          'text': 'Im kostenlosen Erstgespräch klären wir, wo du stehst|und was du brauchst.'}}


# Zeichnung schwarz-weiß rechts im Hero je Leistung (Anna 22.11.2026: „bei Leistungen immer ein Bild“), Set bilder/zeichnungen-sw/
ZEICHNUNG = {'Markenbildung': 'stern', 'Webdesign': 'bildschirm', 'UI': 'auge', 'KI & Digitalisierung': 'gluehbirne', 'KI-Beratung': 'gluehbirne',
             'Marketing & Vertrieb': 'megafon', 'Druck': 'pfeil', 'Illustration & Infografik': 'herz', 'Animation': 'blitz', 'Retainer': 'giesskanne'}


# Foto im Repro-Look rechts im Hero (Anna 22.11.2026, Vorbild Startseiten-Entwurf: blau gedruckt, gedreht, gelber Klebestreifen),
# Zeichnung klein als Sticker am Foto. Nur eigene Projektbilder.
HERO_FOTO = {'Markenbildung': 'start/leipzig-zentrum-von-oben-640.webp', 'Webdesign': 'hero/bauer-startseite-hero.webp', 'UI': 'hero/deinetwegen-handy-ganz.jpg',
             'KI & Digitalisierung': 'ki-arbeits-setup-cockpit-640.webp', 'KI-Beratung': 'ki-arbeits-setup-cockpit-640.webp',
             'Marketing & Vertrieb': 'hero/bauer-praes-01.webp', 'Druck': 'hero/kh-templates.jpg', 'Illustration & Infografik': 'hero/kh-pfau-gold.svg',
             'Animation': 'hero/spiel-animation.webp', 'Retainer': 'leistung-retainer-640.webp'}


def repro_bild(c, pre):
    foto = next((f for t, f in HERO_FOTO.items() if c["titel"].startswith(t)), None)
    z = next((z for t, z in ZEICHNUNG.items() if c["titel"].startswith(t)), None)
    if not foto:
        return f'    <img class="lsx-kopf-zeichnung" src="{pre}bilder/zeichnungen-sw/{z}.svg" alt="" width="400" height="400">\n' if z else ''
    sticker = f'<img class="lsx-repro-sticker" src="{pre}bilder/zeichnungen-sw/{z}.svg" alt="" width="400" height="400">' if z else ''
    return f'    <span class="lsx-repro" aria-hidden="true"><span class="lsx-repro-druck"><img src="{pre}bilder/{foto}" alt="" loading="eager"></span></span>\n'   # Sticker global raus (Anna 22.11.2026)


def muster_kopf(c, m, pre):
    fakten = ''.join(f'<li>{x}</li>' for x in m.get('fakten', []))   # Fakten aus den Daten, ohne Auszeichnung
    return (f'  <section class="seitenkopf lsx-kopf lsx-m-kopf">\n'
            f'    <img class="lsx-kopf-icon" src="{pre}{c["icon"]}" alt="" width="400" height="400">\n'
            f'    <p class="meta brotkrumen"><a href="{pre}#leistungen">Leistungen</a> / <span aria-current="page">{esc(c["titel"])}</span></p>\n'
            f'    <h1 class="gr-xxl lsx-titel" style="--n:{max(len(w) for w in m["h1"].split())}">{esc(m["h1"]).replace(" in ", "<br>in ", 1)}</h1>\n'
            f'    <p class="alt-klein">{trennen(esc(m.get("intro") or c.get("intro", "")))}</p>\n'
            + (f'    <ul class="lsx-m-fakten">{fakten}</ul>\n' if fakten else '') +
            f'    <p class="lsx-hero-knopf"><a class="button" href="{pre}kontakt/">{esc(c.get("anfrage", "Beratung anfragen"))} <span aria-hidden="true">→</span></a></p>\n'
            + repro_bild(c, pre)
            + f'  </section>')


def muster_kurz(m):
    if not m.get('kurz_gesagt'): return ''
    return (f'  <section class="lsx-m-kurz" id="ueberblick" aria-labelledby="kurz-titel">\n'
            f'    <p class="meta">Kurz gesagt</p>\n'
            f'    <h2 class="gr-h2" id="kurz-titel">Das Wichtigste auf einen Blick</h2>\n'
            f'    <ul class="lsx-m-kurz-liste">{fett_rest(m["kurz_gesagt"])}</ul>\n'
            f'  </section>')


def muster_anlaesse(m):
    if not m.get('anlaesse'): return ''
    li = ''.join(f'<li>{esc(x)}</li>' for x in m['anlaesse'])
    return (f'  <section class="lsx-m-anlaesse" id="anlaesse" aria-labelledby="anlaesse-titel">\n'
            f'    <p class="meta">Anlässe</p>\n'
            f'    <h2 class="gr-h2" id="anlaesse-titel">{esc(m.get("anlaesse_titel", "Wann es sich lohnt"))}</h2>\n'
            f'    <ul class="lsx-m-anlaesse-liste">{li}</ul>\n'
            f'  </section>')


def muster_warum(c, m):
    if not m.get('probleme_kurz'): return ''
    return (f'  <section class="lsx-loesung lsx-pl lsx-pl-allein lsx-m-warum" id="loesung" aria-labelledby="loesung-titel">\n'
            f'    <p class="meta">Warum</p>\n'
            f'    <h2 class="gr-h2" id="loesung-titel">{esc(c["problem_titel"])}</h2>\n'
            f'    <div class="lsx-pl-problem lsx-pl-zettel"><p class="meta">Woran es oft hakt</p><ul>{fett_rest(m["probleme_kurz"])}</ul></div>\n'
            f'  </section>')


def muster_so(c, m):
    teile = ''
    if m.get('so_titel'):
        teile = (f'  <section class="lsx-m-so" aria-labelledby="so-titel">\n'
                 f'    <p class="meta">So arbeite ich</p>\n'
                 f'    <h2 class="gr-h2" id="so-titel">{esc(m["so_titel"]).replace(", ", ",<br>", 1)}</h2>\n'
                 f'  </section>\n')
    if c.get('herz'): teile += grafik('website-oekosystem')
    if c.get('grafik'): teile += grafik(c['grafik'])
    return teile


def muster_ergebnisse(m):
    if not m.get('ergebnisse'): return ''
    # Neu gedacht (Anna 22./23.11.2026): oben das Ergebnis danach in Annas Worten, darunter kompakt, was dazugehört
    # Je Leistung passende Ergebnisse, nur aus Annas fünf Begriffen (Anna 23.11.2026: „je Leistung anpassen“)
    alle = {'s': ('Sichtbarkeit', 'auge'), 'k': ('Neue Kunden', 'megafon'), 'f': ('Fachkräfte', 'herz'), 'c': ('Mehr Conversion', 'pfeil'), 'v': ('Mehr Verkäufe', 'stern')}
    wahl = next((w for t, w in (('Markenbildung', 'skfv'), ('Webdesign', 'skcv'), ('UI', 'skcv'), ('KI', 'kfcv'), ('Marketing', 'skcv'), ('Druck', 'skfv'),
                                ('Illustration', 'skcv'), ('Animation', 'skcv'), ('Retainer', 'skcv')) if (m.get('h1') or '').startswith(t)), 'skcv')   # immer vier Karten (Anna 22.11.2026: Tarotkarten)
    ziele = tuple(alle[b] for b in wahl)
    zl = ''.join(f'<li><small aria-hidden="true">{r}</small><img src="{{PRE}}bilder/zeichnungen-sw/{z}.svg" alt="" width="400" height="400" loading="lazy"><span>{esc(t)}</span></li>' for r, (t, z) in zip(('I', 'II', 'III', 'IV'), ziele))
    li = ''.join(f'<li><b>{esc(a)}</b>' + (f' <span>{esc(b)}</span>' if b else '') + '</li>' for a, b in m['ergebnisse'])
    return (f'  <section class="lsx-m-ergebnisse lsx-ziel" id="leistungen" aria-labelledby="leistungen-titel">\n'
            f'    <p class="meta">Ergebnis</p>\n'
            f'    <h2 class="gr-h2" id="leistungen-titel">Das bekommst du</h2>\n'
            f'    <ul class="lsx-ziel-liste">{zl}</ul>\n'
            f'    <p class="meta lsx-dazu-titel">Das gehört dazu</p>\n'
            f'    <ul class="lsx-dazu-liste">{li}</ul>\n'
            f'  </section>')


def muster_abschluss(m, pre):
    a = m['abschluss']
    return (f'  <section class="preis-schluss start-schluss lsx-m-schluss" aria-labelledby="schluss-titel">\n'
            f'    <div class="schluss-karte schluss-blau">\n'
            f'      <p class="meta">{esc(a["meta"])}</p>\n'
            f'      <h2 class="gr-h2" id="schluss-titel">{esc(a["titel"])}</h2>\n'
            f'      <p class="lsx-m-schluss-text">{esc(a["text"]).replace("|", "<br>")}</p>\n'   # „|“ = Zeilenumbruch (Anna 22.11.2026)
            f'      <p><a class="button" href="{pre}kontakt/">{esc(a["knopf"])} <span aria-hidden="true">→</span></a></p>\n'
            f'    </div>\n'
            f'  </section>')


def muster_leiste(c, m, mit_ablauf):
    ziele = [('anlaesse', 'Anlässe', bool(m.get('anlaesse'))), ('loesung', 'Ausgangslage' if c.get('gegenueber') else 'Warum', True),
             ('anwendungen', 'Anwendungsfälle', bool(c.get('anwendungen'))), ('wege', 'Lösung', bool(c.get('wege'))),
             ('recht', 'KI-Verordnung', bool(c.get('recht'))), ('leistungen', 'Leistungen', bool(m.get('ergebnisse'))),
             ('ablauf', 'Ablauf', mit_ablauf), ('referenzen', 'Referenzen', bool(ohne_bauer(I.mit_tag(I.PROJEKTE, [c['tag']]), c['tag']))),
             ('selbst', 'Selbst bauen', bool(c.get('selbstbau'))), ('pakete', 'Preise', True), ('faq', 'Ehrliche Antworten', True)]
    return ankerleiste([(a, t) for a, t, an in ziele if an])


# Eine Leistungsfarbe je Seite, strikt durchgezogen (Anna 23.11.2026, Farb-Richtlinie 1.1 „Leistung und Form“, Vorbild farbenmeer):
# Voll für Seitenkopf und Ergebnis, Zart für Problem und Fragen, dazwischen Weiß. Schrift auf allen Stufen Dunkel.
# Je Leistung zwei verwandte Farben (Anna 23.11.2026: „zwei, die sich ähnlich sind, z. B. Rot und Rosa, Blau und Violett“): erste für Kopf und Problem,
# zweite für Ergebnis und Fragen. Rosa = Pink, Violett = Orchidee, Grün = Mint (Farb-Richtlinie 1.1).
ROT, PINK, ORCHIDEE, HIMMEL, MINT, GELB, ORANGE = '#FF3B2F', '#FF4FA3', '#EF87F9', '#5FD2FF', '#07F0A5', '#FFF329', '#EE6C29'
LEISTUNGSFARBE = {'Markenbildung': (ROT, PINK), 'Webdesign': (HIMMEL, ORCHIDEE), 'UI': (PINK, ORCHIDEE), 'KI': (GELB, MINT),
                  'Marketing': (ORCHIDEE, PINK), 'Druck': (MINT, HIMMEL), 'Illustration': (PINK, ROT), 'Animation': (GELB, ORANGE), 'Retainer': (MINT, GELB)}


def leistungsfarbe(c):
    a, b = next((v for k, v in LEISTUNGSFARBE.items() if c['titel'].startswith(k)), (HIMMEL, ORCHIDEE))
    mix = lambda v, t: '#%02X%02X%02X' % tuple(round(int(v[i:i + 2], 16) * (1 - t) + 255 * t) for i in (1, 3, 5))
    # Markenbildung: Warum-Zettel in Orchidee mit schwarzer Schrift (Anna 22.11.2026: erst „pink mit weißer schrift“, dann „das pink gefällt mir nicht … eher lila“)
    # Markenbildung: Anlässe auf Rot tief mit weißer Schrift (Anna 22.11.2026: „schrift weiß?“; Weiß auf Signalrot nur 3,6 : 1, auf Rot tief 5,9 : 1)
    zettel = '; --lf-zettel: #EF87F9; --lf-zettel-text: #0E1011; --lf-anlass: #C80C00; --lf-anlass-text: #FFFFFF' if c['titel'].startswith('Markenbildung') else ''
    return f'--lf: {a}; --lf-zart: {mix(a, .55)}; --lf-hauch: {mix(a, .8)}; --lf2: {b}; --lf2-zart: {mix(b, .55)}' + zettel


def muster_main(c, g, pre, vergleich_html, prozess, fragen, link, mit_ablauf):
    m = c['muster']
    if m.get('ablauf_dauer'):
        prozess = prozess.replace('<ol class="zl-quer', f'<p class="lsx-m-dauer">{esc(m["ablauf_dauer"])}</p>\n    <ol class="zl-quer', 1)
    prozess = prozess.replace('<p class="meta">Wie ich arbeite</p>', '<p class="meta">Wie wir arbeiten</p>', 1)   # Anna 22.11.2026
    warum = gegenueber(c, g, pre, link) if c.get('gegenueber') else muster_warum(c, m)
    teile = [muster_kopf(c, m, pre), muster_kurz(m), muster_leiste(c, m, mit_ablauf), muster_anlaesse(m), warum, anwendungen(c, pre),
             muster_so(c, m), wege(c, pre), praxis(c, pre), recht(c), muster_ergebnisse(m).replace("{PRE}", pre), prozess,
             retainer_hinweis(g, pre) if mit_ablauf else '', selbstbau(c, pre), referenzen(c['tag'], pre), stimmen(pre, c['tag']),
             pakete(c, g, pre), vergleich_html, extras(g), faq(fragen, pre), muster_abschluss(m, pre), artikel(pre, c['tag']),
             spiel_sektion(pre, MENUE_VERSION) if c.get('spiel') else '']
    return f'<main id="inhalt" class="lsx-muster lsx-farbe" style="{leistungsfarbe(c)}">\n\n' + '\n\n'.join(t for t in teile if t.strip()) + '\n\n</main>'


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
    vergleich_html = ''   # Vergleichstabellen raus (Anna 23.11.2026); Funktion vergleich() bleibt für später
    prozess = (ablauf_eigen(pre, c['ablauf_schritte'], c.get('ablauf_hinweis', '')) if c.get('ablauf_schritte') else ablauf(pre)) if mit_ablauf else ''
    # Muster für alle Leistungsseiten (Anna 22.11.2026); eigene Daten im Feld „muster“ gehen vor
    c = dict(c, muster=c.get('muster') or auto_muster(c, g, intro))
    if c['muster'].get('faq_muster'):
        fragen = c['muster']['faq_muster']
    main = muster_main(c, g, pre, vergleich_html, prozess, fragen, link, mit_ablauf) if c.get('muster') else f'''<main id="inhalt">

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
    for alt, neu in REDIGAT.get(c['pfad'], []):
        assert alt in t, (c['pfad'], alt[:40])
        t = t.replace(alt, neu, 1)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(t, encoding='utf-8')
    print('geschrieben:', c['pfad'])


if __name__ == '__main__':
    for k in sys.argv[1:] or [k for k in inhalte if not k.startswith('_')]:
        seite(k, inhalte[k])
