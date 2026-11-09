# Brotkrumen-Navigation (Breadcrumbs) auf Unterseiten, wo sie Orientierung geben (Anna, 10.11.2026: „überall wo sinnvoll“).
# Setzt am Anfang von <main> eine kleine Navigation plus strukturierte Daten (BreadcrumbList) zwischen
# <!-- BROTKRUMEN:START --> und <!-- BROTKRUMEN:ENDE -->. Läuft als letzter Schritt von alle-erzeugen.sh.
# Leistungs- und Projektseiten haben ihre Brotkrumen schon im Seitenkopf (leistungsseiten.py, referenzen.py) und bleiben unberührt.
# Hauptseiten der ersten Ebene (Für wen, Blog, Referenzen, Preise, Über mich) brauchen keine.
# Aufruf im Repository-Ordner:  python3 werkzeuge/brotkrumen.py
import html, json, re

from gemeinsam import WEBSITE, lade_json

BASIS = 'https://studio-aah.de/'
FW = lade_json('inhalte/fuer-wen-seiten.json')
FUER_WEN = ('Für wen', 'fuer-wen/')
LEISTUNGEN = ('Leistungen', '#leistungen')


def ziele():
    """(Pfad, [(Name, Ziel) …], letzter Name) für alle Seiten mit Brotkrumen."""
    for p in FW['probleme']:
        yield p['pfad'], [FUER_WEN], p['meta']
    for b in FW['branchen']:
        yield b['pfad'], [FUER_WEN], b['name']
    yield FW['selbsttest']['pfad'], [FUER_WEN], 'Selbsttest'
    yield FW['ki_rechner']['pfad'], [FUER_WEN], 'KI-Zeitrechner'
    yield FW['produkt']['pfad'], [LEISTUNGEN], 'Employer Branding'
    yield 'ki-arbeits-setup/', [LEISTUNGEN], 'KI-Arbeits-Setup'
    yield 'marken-regelwerk/', [LEISTUNGEN], 'Marken-Regelwerk'
    for seite in sorted((WEBSITE / 'blog').glob('*/index.html')):
        text = seite.read_text(encoding='utf-8')
        if 'http-equiv="refresh"' in text:
            continue
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
        if h1:
            titel = html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).replace('­', '').strip()
            yield f'blog/{seite.parent.name}/', [('Blog', 'blog/')], titel


def block(pfad, eltern, titel):
    pre = '../' * pfad.strip('/').count('/') + '../'
    links = ' / '.join(f'<a href="{pre}{ziel}">{html.escape(name)}</a>' for name, ziel in eltern)
    sichtbar = (f'<nav class="bk-nav" aria-label="Brotkrumen"><p class="meta brotkrumen">{links} / '
                f'<span aria-current="page">{html.escape(titel)}</span></p></nav>')
    liste = [{'@type': 'ListItem', 'position': 1, 'name': 'Startseite', 'item': BASIS}]
    for i, (name, ziel) in enumerate(eltern, 2):
        liste.append({'@type': 'ListItem', 'position': i, 'name': name, 'item': BASIS + ziel})
    liste.append({'@type': 'ListItem', 'position': len(liste) + 1, 'name': titel, 'item': BASIS + pfad})
    daten = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': liste}, ensure_ascii=False)
    return f'<!-- BROTKRUMEN:START -->\n{sichtbar}\n<script type="application/ld+json">{daten}</script>\n<!-- BROTKRUMEN:ENDE -->'


def main():
    n = 0
    for pfad, eltern, titel in ziele():
        datei = WEBSITE / pfad / 'index.html'
        if not datei.exists():
            print('fehlt:', pfad)
            continue
        text = datei.read_text(encoding='utf-8')
        neu = block(pfad, eltern, titel)
        if '<!-- BROTKRUMEN:START -->' in text:
            text = re.sub(r'<!-- BROTKRUMEN:START -->.*?<!-- BROTKRUMEN:ENDE -->', lambda m: neu, text, flags=re.S)
        else:
            text, k = re.subn(r'(<main id="inhalt"[^>]*>)', lambda m: m.group(1) + '\n' + neu, text, count=1)
            if not k:
                raise SystemExit(f'Kein <main id="inhalt"> in {pfad}')
        datei.write_text(text, encoding='utf-8')
        n += 1
    print(f'Brotkrumen gesetzt: {n} Seiten')


if __name__ == '__main__':
    main()
