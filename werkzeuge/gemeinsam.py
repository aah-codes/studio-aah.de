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


def seitenrahmen(vorlage, main, titel, beschreibung, url, ld):
    """Seite aus einer bestehenden Seite (Kopf, Fuß) bauen: <main>, Titel, Beschreibung, Adresse und strukturierte Daten ersetzen."""
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
    if e.get('stunde') and e.get('stundeBis'): return f"{e['stunde']}–{euro(e['stundeBis'])} {NETTO} / Stunde, je nach Unternehmensgröße"
    if e.get('stunde'): return f"ab {euro(e['stunde'])} {NETTO} / Stunde"
    return ('ab ' if e.get('ab', True) else '') + euro(e['preis']) + ' ' + NETTO


def paket_karte(e, woerter):
    """Karte eines Pakets (Name, Preis, für wen, Dauer, Inhalt); woerter: Trennliste für den Namen."""
    gefragt = e.get('gefragt')
    badge = f'<p class="lsx-badge">{esc(e.get("badge", "Gefragt"))}</p>' if gefragt else ''
    liste = ''.join(f'<li>{esc(x)}</li>' for x in e.get('items', []))
    dauer = f'<span class="meta">Dauer</span> {esc(e["dauer"])}' if e.get('dauer') else ''
    return (f'      <article class="lsx-karte{" lsx-gefragt" if gefragt else ""}">\n'
            f'        {badge}<h3 class="lsx-karte-name">{trennen(esc(e["name"]), woerter)}</h3>\n'
            f'        <p class="lsx-karte-preis">{preis(e)}</p>\n'
            f'        <p class="lsx-karte-wer">{esc(e.get("wer") or "")}</p>\n'
            f'        <p class="lsx-karte-dauer">{dauer}</p>\n'
            f'        <p class="lsx-karte-plus">{esc(e.get("plus") or "")}</p><ul class="lsx-karte-liste">{liste}</ul>\n'
            '      </article>')
