# Gemeinsame Hilfsfunktionen der Generatoren (preise-erzeugen, inhalte-erzeugen, leistungsseiten, referenzen, Blog).
# Nur Werkzeuge, keine Inhalte: Texte und Preise stehen in den JSON-Dateien unter werkzeuge/.
import functools, html, importlib.util, json, pathlib, re

BASIS = pathlib.Path(__file__).resolve().parent.parent
WEBSITE = BASIS / 'website'
WERKZEUGE = BASIS / 'werkzeuge'

STUDIO_ID = 'https://studio-aah.de/#studio'
LINKEDIN = 'https://www.linkedin.com/in/anna-h%C3%A4rtelt-8513b8213/details/recommendations/'
NETTO = '<small class="lsx-netto">netto</small>'
NETTO_SATZ = 'Alle Preise sind Nettopreise zzgl. 19&nbsp;% Umsatzsteuer (USt.).'
PFEIL = ' <span aria-hidden="true">→</span>'
# Weiche Trennstriche in Paketnamen und Prozess-Schritten, damit lange Wörter auf schmalen Handys sauber umbrechen (Anna 13.10.2026)
TRENNEN_LEISTUNGEN = {'Unternehmenspräsentation': 'Unternehmens&shy;präsentation', 'Mitbewerberrecherche': 'Mitbewerber&shy;recherche', 'Unternehmensidentität': 'Unternehmens&shy;identität'}


def esc(text):
    """Text für HTML maskieren (& < >); Anführungszeichen bleiben, für Attribute html.escape nehmen."""
    return html.escape(text, quote=False)


def lade_json(pfad):
    """JSON-Datei relativ zu werkzeuge/ laden, z. B. lade_json('preise-daten.json')."""
    return json.loads((WERKZEUGE / pfad).read_text(encoding='utf-8'))


def lade_skript(datei):
    """Ein Generator-Skript als Modul laden (Dateinamen mit Bindestrich lassen sich nicht importieren)."""
    spec = importlib.util.spec_from_file_location(pathlib.Path(datei).stem.replace('-', '_'), WERKZEUGE / datei)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def euro(betrag, leer='&nbsp;'):
    """2450 -> '2.450&nbsp;€'"""
    return f'{betrag:,}'.replace(',', '.') + leer + '€'


def trennen(text, woerter):
    """Weiche Trennstriche für lange Wörter (Anna 13./14.10.2026); nach esc() anwenden. woerter: {'Wort': 'Wo&shy;rt'}"""
    for wort, getrennt in woerter.items():
        text = text.replace(wort, getrennt)
    return text


def lesezeit(woerter):
    """Lesezeit in Minuten bei 200 Wörtern pro Minute, mindestens 1."""
    return max(1, round(woerter / 200))


def ersetze_einmal(muster, ersatz, text, was, flags=0):
    """Wie re.sub mit count=1, bricht aber mit Meldung ab, wenn das Muster fehlt (statt still nichts zu tun)."""
    neu, n = re.subn(muster, ersatz, text, count=1, flags=flags)
    if not n:
        raise SystemExit(f'Nicht gefunden: {was}')
    return neu


def einsetzen(text, name, inhalt):
    """Inhalt zwischen <!-- NAME:START --> und <!-- NAME:ENDE --> setzen."""
    return ersetze_einmal(rf'<!-- {name}:START -->.*?<!-- {name}:ENDE -->',
                          lambda m: f'<!-- {name}:START -->\n{inhalt}\n<!-- {name}:ENDE -->', text, f'Marker {name}', re.S)


# Daumen-Rückmeldung unter Selbsttest und Rechnern (Anna 20.11.2026, Vorbild Gelbe Seiten): Daumen hoch oder runter,
# nach Daumen runter freiwillig ein Satz. Ablauf in js/menue.js, Versand über Formspark ohne Namen und E-Mail-Adresse.
DAUMEN_HOCH = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 10v11H3V10h4Zm0 0 4.5-7.5c1.4 0 2.5 1.1 2.5 2.5v3.5h5.3c1.3 0 2.2 1.2 1.9 2.4l-2 7.6c-.3 1-1.1 1.5-2 1.5H7"/></svg>'
DAUMEN_RUNTER = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17 14V3h4v11h-4Zm0 0-4.5 7.5c-1.4 0-2.5-1.1-2.5-2.5v-3.5H4.7c-1.3 0-2.2-1.2-1.9-2.4l2-7.6c.3-1 1.1-1.5 2-1.5H17"/></svg>'


def daumen(werkzeug, frage, pre='', selbst=False):
    """Block „Wie fanden Sie …?“ mit zwei Daumen. selbst=True: das Werkzeug-Skript blendet ihn ein (Kostenrechner, erst im letzten Schritt)."""
    return (f'<div class="daumen" data-daumen="{esc(werkzeug)}"{" data-daumen-selbst" if selbst else ""} hidden>'
            f'<p class="daumen-frage" id="daumen-{esc(werkzeug.lower().replace(" ", "-"))}">{esc(frage)}</p>'
            f'<div class="daumen-knoepfe" role="group" aria-labelledby="daumen-{esc(werkzeug.lower().replace(" ", "-"))}">'
            f'<button type="button" data-wert="gut" aria-pressed="false" aria-label="Gut">{DAUMEN_HOCH}</button>'
            f'<button type="button" data-wert="schlecht" aria-pressed="false" aria-label="Nicht gut">{DAUMEN_RUNTER}</button></div>'
            '<div class="daumen-danach" role="status" aria-live="polite"></div></div>')  # ohne Datenschutz-Hinweis, steht in der Datenschutzerklärung #rueckmeldung (Anna 20.11.2026)


def spiel_sektion(pre, version):
    """Sektion „Play the game.“ mit dem Spiel (Anna 16.11.2026: über dem Fuß von Aktuelles und Webdesign)."""
    t = (WERKZEUGE / 'inhalte' / 'spiel.html').read_text(encoding='utf-8')
    return t.replace('{pre}', pre).replace('{version}', version)


KURZWORT = re.compile(r'(?<![\w&;/-])([A-ZÄÖÜ]{1,3}-[A-Za-zÄÖÜäöüß]+)')


def kurzwoerter_schuetzen(main):
    """Kein Zeilenumbruch nach kurzem Vorderglied (Anna 16.11.2026: „IT-Projekt ist ein zusammenhängendes Wort“):
    IT-Projekt, KI-Check, E-Mail bleiben zusammen. Nur im sichtbaren Text, nicht in Tags, Attributen, Skripten."""
    # Fragen (summary) sind Flexboxen: Text in einen Span legen, sonst wird jedes Teilstück ein eigenes, nicht umbrechendes Element
    main = re.sub(r'<summary>([^<]+)</summary>', r'<summary><span>\1</span></summary>', main)
    teile = re.split(r'(<script.*?</script>|<style.*?</style>|<[^>]+>)', main, flags=re.S)
    return ''.join(t if i % 2 else KURZWORT.sub(r'<span class="ohne-umbruch">\1</span>', t) for i, t in enumerate(teile))


def seitenrahmen(vorlage, main, titel, beschreibung, url, ld):
    """Seite aus einer bestehenden Seite (Kopf, Fuß) bauen: <main>, Titel, Beschreibung, Adresse und strukturierte Daten ersetzen."""
    main = kurzwoerter_schuetzen(main)
    t = ersetze_einmal(r'<main id="inhalt">.*?</main>', lambda m: main, vorlage, '<main>', re.S)
    t = ersetze_einmal(r'<title>.*?</title>', f'<title>{esc(titel)}</title>', t, '<title>')
    for name in ('name="description"', 'property="og:description"'):
        t = ersetze_einmal(rf'<meta {name} content="[^"]*">', f'<meta {name} content="{html.escape(beschreibung)}">', t, name)
    t = ersetze_einmal(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', t, 'canonical')
    t = ersetze_einmal(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', t, 'og:url')
    t = ersetze_einmal(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(titel)}">', t, 'og:title')
    t = re.sub(r'<meta name="robots" content="[^"]*">\n?', '', t)
    skript = f'<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False, indent=2)}\n  </script>'
    if '<script type="application/ld+json">' not in t:  # Vorlage ohne strukturierte Daten: vor </head> ergänzen
        return ersetze_einmal(r'\n</head>', lambda m: f'\n  {skript}\n</head>', t, '</head>')
    return ersetze_einmal(r'<script type="application/ld\+json">.*?</script>', lambda m: skript, t, 'JSON-LD', re.S)


@functools.lru_cache(maxsize=None)
def bildmass(datei):
    """(Breite, Höhe) eines Bildes unter website/ aus dem Dateikopf (JPEG, PNG, WebP, SVG-viewBox); None bei SVG ohne viewBox."""
    pfad = WEBSITE / datei
    if datei.endswith('.svg'):
        m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', pfad.read_text(encoding='utf-8'))
        return (round(float(m.group(1))), round(float(m.group(2)))) if m else None
    d = pfad.read_bytes()
    if d[:8] == b'\x89PNG\r\n\x1a\n':
        return int.from_bytes(d[16:20], 'big'), int.from_bytes(d[20:24], 'big')
    if d[:4] == b'RIFF' and d[8:12] == b'WEBP':
        if d[12:16] == b'VP8X':
            return int.from_bytes(d[24:27], 'little') + 1, int.from_bytes(d[27:30], 'little') + 1
        if d[12:16] == b'VP8 ':
            return int.from_bytes(d[26:28], 'little') & 0x3fff, int.from_bytes(d[28:30], 'little') & 0x3fff
    if d[:2] == b'\xff\xd8':
        i = 2
        while i < len(d):
            marke, laenge = d[i + 1], int.from_bytes(d[i + 2:i + 4], 'big')
            if marke in (0xC0, 0xC1, 0xC2):
                return int.from_bytes(d[i + 7:i + 9], 'big'), int.from_bytes(d[i + 5:i + 7], 'big')
            i += 2 + laenge
    raise SystemExit(f'Bildmaße nicht lesbar: {datei}')


def mass_attr(datei, teiler=1):
    """' width="…" height="…"' für ein Bild unter website/ (gegen Springen beim Laden); teiler 2 = Bild in doppelter Auflösung."""
    mass = bildmass(datei.split('?')[0])
    return f' width="{mass[0] // teiler}" height="{mass[1] // teiler}"' if mass else ''


def bild_attr(datei, pre='', sizes=None):
    """' src="…" width="…" height="…"' und, wenn es kleinere Fassungen <bild>-<breite>.webp/.jpg gibt (werkzeuge/grafiken/bild/varianten.sh),
    ' srcset="…" sizes="…"' – so laden Handys nicht die 1440-px-Seitenaufnahmen (Website-Check 18.10.2026)."""
    a = f' src="{pre}{datei}"{mass_attr(datei)}'
    pfad = WEBSITE / datei.split('?')[0]
    breite = bildmass(datei.split('?')[0])[0]
    # nur Fassungen, deren Zahl wirklich eine kleinere Breite ist (nicht z. B. bauer-magazin-1.webp)
    ordner = datei.split('?')[0].rsplit('/', 1)[0]
    varianten = sorted((int(m.group(1)), v.name) for v in pfad.parent.glob(f'{pfad.stem}-*')
                       if v.suffix in ('.webp', '.jpg') and (m := re.fullmatch(re.escape(pfad.stem) + r'-(\d+)', v.stem))
                       and bildmass(f'{ordner}/{v.name}')[0] == int(m.group(1)) < breite)
    if sizes and varianten:
        liste = [f'{pre}{ordner}/{n} {b}w' for b, n in varianten] + [f'{pre}{datei} {breite}w']
        a += f' srcset="{", ".join(liste)}" sizes="{sizes}"'
    return a


# --- Preise und Paketkarten (Preisseite und Leistungsseiten zeigen dieselben Karten, Anna 16.10.2026) ---
def preis(e):
    """Preisangabe eines Pakets oder einer Zusatzleistung aus preise-daten.json."""
    if e.get('anfrage'): return 'auf Anfrage'
    if e.get('anteil'): return f"+{int(e['anteil'] * 100)}&nbsp;% {NETTO}"
    if e.get('monat'): return f"ab {euro(e['monat'])} {NETTO} / Monat"
    if e.get('stunde') and e.get('stundeBis'):
        # ohneZusatz: Karte, deren Text die Unternehmensgröße schon nennt (Retainer-Seite)
        return f"{e['stunde']}–{euro(e['stundeBis'])} {NETTO} / Stunde" + ('' if e.get('ohneZusatz') else ', je nach Unternehmensgröße')
    if e.get('stunde'): return f"ab {euro(e['stunde'])} {NETTO} / Stunde"
    return ('ab ' if e.get('ab', True) else '') + euro(e['preis']) + ' ' + NETTO


def zwei_pakete(g):
    """Höchstens zwei Paketkarten je Leistung (Anna 17.11.2026: „überall zwei Pakete, die, die am meisten gesucht werden“).
    Feld „karten“ in preise-daten.json nennt die zwei Pakete; alle übrigen kommen als Zeile „Außerdem buchbar“ darunter.
    Baut ein gezeigtes Paket auf ein ausgeblendetes auf („Alles aus Basic, plus:“), stehen dessen Inhalte mit in der Liste."""
    ids = g.get('karten')
    if not ids: return list(g['pakete']), []
    nach_id = {e['id']: e for e in g['pakete']}

    def voll(e):
        plus = e.get('plus') or ''
        if not plus.startswith('Alles aus '): return e
        name = plus[len('Alles aus '):].split(',')[0].strip()
        basis = next((x for x in g['pakete'] if name in x['name'] and x is not e), None)
        if basis is None or basis['id'] in ids: return e
        b = voll(basis)
        return {**e, 'plus': 'Enthalten:', 'items': list(b.get('items', [])) + list(e.get('items', []))}
    return [voll(nach_id[i]) for i in ids], [e for e in g['pakete'] if e['id'] not in ids]


def weitere_pakete(rest):
    """Zeile unter den zwei Karten: übrige Pakete mit Preis (Anna 17.11.2026)."""
    if not rest: return ''
    return ('    <p class="lsx-weitere">Außerdem buchbar: '
            + ' · '.join(f'<strong>{esc(e["name"])}</strong> {preis(e).replace(NETTO, "netto")}' for e in rest) + '</p>\n')


def paket_karte(e, woerter, pre=''):
    """Karte eines Pakets (Name, Preis, für wen, Dauer, Inhalt); woerter: Trennliste für den Namen.
    Optional "link" (ab der Website-Wurzel, z. B. "ki-arbeits-setup/"): Textlink zur eigenen Paketseite, pre = Pfad zur Wurzel."""
    gefragt = e.get('gefragt')
    zur_seite = (f' <a class="textlink" href="{pre}{e["link"]}">Zur Paketseite <span aria-hidden="true">→</span></a>'
                 if e.get('link') else '')
    badge = f'<p class="lsx-badge">{esc(e.get("badge", "Beliebt"))}</p>' if gefragt else ''
    liste = ''.join(f'<li>{esc(x)}</li>' for x in e.get('items', []))
    dauer = f'<span class="meta">Dauer</span> {esc(e["dauer"])}' if e.get('dauer') else ''
    return (f'      <article class="lsx-karte{" lsx-gefragt" if gefragt else ""}">\n'
            f'        {badge}<h3 class="lsx-karte-name">{trennen(esc(e["name"]), woerter)}</h3>\n'
            f'        <p class="lsx-karte-preis">{preis(e)}</p>\n'
            f'        <p class="lsx-karte-wer">{esc(e.get("wer") or "")}{zur_seite}</p>\n'
            f'        <p class="lsx-karte-dauer">{dauer}</p>\n'
            f'        <p class="lsx-karte-plus">{esc(e.get("plus") or "")}</p><ul class="lsx-karte-liste">{liste}</ul>\n'
            '      </article>')


def ankerleiste(ziele, titel='Leistung im Überblick'):
    """Inhaltsverzeichnis mit Ankerlinks nach dem Vorbild IT Sonix (Anna 12.11.2026): graue Spur, eine aktive weiße Pille.
    ziele: Liste aus (anker, text_html). menue.js markiert beim Scrollen den Abschnitt, in dem man gerade ist."""
    lis = []
    for i, (anker, text) in enumerate(ziele):
        aktiv = ' class="aktiv"' if i == 0 else ''
        lis.append(f'<li><a href="#{anker}"{aktiv}>{text}</a></li>')
    return (f'  <nav class="anker" aria-labelledby="anker-titel">\n    <h2 class="anker-titel" id="anker-titel">{titel}</h2>\n'
            f'    <ul class="anker-spur">{"".join(lis)}</ul>\n  </nav>')


# Papierriss und Kringel (Anna 18.11.2026, Vorbild Focus Lab: gerissenes Papier und gestische Linien als Zeichen von Handarbeit).
# Beide selbst gezeichnet, Farbe über currentColor aus dem CSS (keine festen Farben). Zuerst nur im Selbsttest.
def _welle(n, seed, oktaven):
    """glatte Zufallskurve aus mehreren Frequenzen, Anfang = Ende"""
    import math, random
    r = random.Random(seed)
    teile = [(max(1, round(f * n)), a, r.uniform(0, 6.283), r.uniform(0, 6.283)) for f, a in oktaven]
    return [sum(a * (math.sin(6.283185 * k * i / n + p1) + .5 * math.sin(6.283185 * (2 * k + 1) * i / n + p2)) for k, a, p1, p2 in teile)
            for i in range(n + 1)]


def papierriss(seed=3, faser=False):
    """SVG-Kante für den oberen Rand eines Abschnitts (Fläche unter der Kante); optional heller Faserrand dahinter"""
    import random
    breite, hoehe, n = 1440, 56, 480

    def kante(mit_faser):
        grob = _welle(n, seed, ((0.012, 1.0), (0.05, .45), (0.17, .18), (0.6, .07)))
        fein = _welle(n, seed + 11, ((0.9, .5), (2.1, .3)))
        r, mx = random.Random(seed + 99), max(abs(v) for v in grob)
        pkt = []
        for i in range(n + 1):
            y = hoehe * .5 + grob[i] / mx * hoehe * .36 + fein[i] * (3.2 if mit_faser else 1.2)
            if mit_faser:
                y += r.uniform(-1.4, 1.4) - 5 - abs(fein[i]) * 4
            pkt.append('L%.1f %.1f' % (i / n * breite, max(0, min(hoehe, y))))
        return f'M0 {hoehe} ' + ' '.join(pkt) + f' L{breite} {hoehe} Z'
    faserpfad = f'<path class="riss-faser" d="{kante(True)}"/>' if faser else ''
    return (f'<svg class="riss" viewBox="0 0 {breite} {hoehe}" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">'
            f'{faserpfad}<path d="{kante(False)}" fill="currentColor"/></svg>')


def kringel(seed=7):
    """handgezogener Kringel um ein Wort (Strich zeichnet sich per CSS), Start und Ende überlappen leicht"""
    import math
    b, h, n = 400, 130, 160
    wob, dreh, pkt = _welle(n, seed, ((0.02, 1), (0.05, .4))), math.radians(-4), []
    for i in range(n + 1):
        u = i / n
        t = math.radians(200 + 372 * u)
        s = 1 + .06 * (u - .5)
        x, y = math.cos(t) * 190 * s * (1 + wob[i] * .015), math.sin(t) * 53 * s * (1 + wob[i] * .03)
        pkt.append('%.1f %.1f' % (b / 2 + x * math.cos(dreh) - y * math.sin(dreh), h / 2 + x * math.sin(dreh) + y * math.cos(dreh)))
    return (f'<svg class="kringel" viewBox="0 0 {b} {h}" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<path pathLength="1" d="M{" L".join(pkt)}" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
