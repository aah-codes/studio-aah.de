# Übernimmt Kopf und Fuß aus website/index.html in alle anderen Seiten (Pfade passend zur Ordnertiefe;
# die 404-Seite bekommt Pfade ab der Wurzel, weil der Server sie unter jeder Adresse ausliefert).
# Kopf: von <a class="sprunglink" bis <!-- /KOPF -->, Fuß: von <!-- FUSS: bis <!-- /FUSS -->.
# Kopf oder Fuß also nur in website/index.html ändern, dann dieses Skript (oder alle-erzeugen.sh) laufen lassen.
# Weiterleitungsseiten (http-equiv="refresh") bleiben unberührt; Seiten mit dem Kommentar <!-- LANDINGPAGE (eigener Kopf/Fuß)
# bekommen nur die preload-Zeilen. Derzeit gibt es keine solche Seite (website-check/ hat seit 25.10.2026 den normalen Kopf).
# Aufruf im Repository-Ordner:  python3 werkzeuge/kopf-fuss.py
import pathlib, re

website = pathlib.Path(__file__).resolve().parent.parent / 'website'
BEREICHE = {'Kopf': r'<a class="sprunglink".*?<!-- /KOPF -->', 'Fuß': r'<!-- FUSS:.*?<!-- /FUSS -->'}
EXTERN = ('http:', 'https:', 'mailto:', 'tel:', 'data:', '/')
UEBERALL = ('#inhalt',)  # Sprungziele, die es auf jeder Seite gibt


def umschreiben(block, vorne):
    """Setzt `vorne` ('../../', '/' …) vor die relativen Pfade der Startseite.
    Sprungmarken wie #leistungen zeigen auf Abschnitte der Startseite und bekommen den Pfad auch."""
    def pfad(m):
        ziel = m.group(2)
        if ziel.startswith(EXTERN) or ziel in UEBERALL or (ziel.startswith('#') and f'id="{ziel[1:]}"' in block):
            return m.group(0)
        return f'{m.group(1)}="{vorne + ziel if ziel != "./" else vorne or "./"}"'
    return re.sub(r'\b(href|src)="([^"]*)"', pfad, block)


# Hauptschriften vorab laden (Anna 25.10.2026, Website-Check: Verrutschen beim Laden am Handy, weil Überschriften
# mit der Ersatzschrift breiter sind und anders umbrechen). Steht direkt nach dem Link auf stil.css, Pfad passend zur Ordnertiefe.
SCHRIFTEN = ('anton-latin.woff2', 'manrope-latin.woff2')
STIL = re.compile(r'(\n?)([ \t]*)<link rel="stylesheet" href="([^"]*?)css/stil\.css\?v=[^"]*">')


def vorladen(text):
    """Setzt die preload-Zeilen für die Hauptschriften hinter den Link auf stil.css (nur einmal)."""
    if 'rel="preload"' in text and 'anton-latin.woff2' in text:
        return text
    def ersetzen(m):
        zeilen = ''.join(f'\n{m.group(2)}<link rel="preload" href="{m.group(3)}schriften/{s}" as="font" type="font/woff2" crossorigin>'
                         for s in SCHRIFTEN)
        return m.group(0) + zeilen
    return STIL.sub(ersetzen, text, count=1)


def main():
    start = (website / 'index.html').read_text(encoding='utf-8')
    neu_start = vorladen(start)
    if neu_start != start:
        (website / 'index.html').write_text(neu_start, encoding='utf-8')
        start = neu_start
    vorlagen = {}
    for name, muster in BEREICHE.items():
        m = re.search(muster, start, flags=re.S)
        if not m:
            raise SystemExit(f'{name} fehlt in website/index.html')
        vorlagen[name] = (muster, m.group(0))

    geaendert = 0
    for seite in sorted(website.rglob('*.html')):
        if seite == website / 'index.html':
            continue
        # Entwurfsseiten (website/entwurf-…) haben bewusst keinen Kopf und Fuß (CLAUDE.md)
        if seite.relative_to(website).parts[0].startswith('entwurf-'):
            continue
        text = seite.read_text(encoding='utf-8')
        # Landingpages (z. B. website-check/) haben einen eigenen Kopf ohne Hauptnavigation und einen eigenen Fuß
        if 'http-equiv="refresh"' in text:
            continue
        text_vorher, text = text, vorladen(text)
        if text != text_vorher:
            seite.write_text(text, encoding='utf-8')
            geaendert += 1
        if '<!-- LANDINGPAGE' in text:
            continue
        vorne = '/' if seite == website / '404.html' else '../' * (len(seite.relative_to(website).parts) - 1)
        neu = text
        for name, (muster, block) in vorlagen.items():
            neu, n = re.subn(muster, lambda _: umschreiben(block, vorne), neu, count=1, flags=re.S)
            if not n:
                raise SystemExit(f'{name} fehlt in {seite.relative_to(website)}')
        if neu != text:
            seite.write_text(neu, encoding='utf-8')
            geaendert += 1
    print(f'Kopf und Fuß übernommen ({geaendert} Seiten geändert)')


if __name__ == '__main__':
    main()
