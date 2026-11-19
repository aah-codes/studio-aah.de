# Erzeugt website/llms.txt (Übersicht für KI-Dienste nach llmstxt.org; noch kein fester Standard).
# Anna 19.11.2026, Website-Check von außen: „Keine llms.txt“. Nur vorhandene Texte: Seitentitel und
# Meta-Description jeder Seite aus website/sitemap.xml, gruppiert nach dem ersten Pfadteil. Nichts von Hand.
# Läuft als letzter Schritt in alle-erzeugen.sh. Aufruf im Repository-Ordner:  python3 werkzeuge/llms-txt.py
import html, pathlib, re

website = pathlib.Path(__file__).resolve().parent.parent / 'website'
BASIS = 'https://studio-aah.de'
GRUPPEN = [  # (erster Pfadteil, Überschrift); alles andere unter „Weitere Seiten“
    ('service', 'Leistungen'), ('website-check', 'Feste Angebote'), ('marken-regelwerk', 'Feste Angebote'),
    ('ki-arbeits-setup', 'Feste Angebote'), ('preise', 'Feste Angebote'), ('branchen', 'Branchen'),
    ('fuer-wen', 'Für wen'), ('referenzen', 'Projekte'), ('blog', 'Blog'), ('profil', 'Über mich'),
    ('kontakt', 'Kontakt'),
]
OHNE = ('impressum', 'datenschutz')  # Pflichtseiten am Ende unter „Optional“


def meta(text, muster):
    m = re.search(muster, text, re.S)
    return html.unescape(m.group(1).strip()) if m else ''


def main():
    adressen = re.findall(r'<loc>([^<]+)</loc>', (website / 'sitemap.xml').read_text(encoding='utf-8'))
    start = (website / 'index.html').read_text(encoding='utf-8')
    abschnitte, optional = {}, []
    for url in adressen:
        pfad = url.replace(BASIS, '').strip('/')
        if not pfad:
            continue
        datei = website / pfad / 'index.html'
        if not datei.exists():
            raise SystemExit(f'llms.txt: Seite aus der Sitemap fehlt: {pfad}')
        text = datei.read_text(encoding='utf-8')
        titel = meta(text, r'<title>(.*?)</title>').replace(' | STUDIO AAH!', '')
        beschr = meta(text, r'<meta name="description" content="([^"]*)"')
        zeile = f'- [{titel}]({url})' + (f': {beschr}' if beschr else '')
        teil = pfad.split('/')[0]
        if teil in OHNE:
            optional.append(zeile)
            continue
        gruppe = next((g for t, g in GRUPPEN if t == teil), 'Weitere Seiten')
        abschnitte.setdefault(gruppe, []).append(zeile)
    reihenfolge = list(dict.fromkeys(g for _, g in GRUPPEN)) + ['Weitere Seiten']
    kurz = meta(start, r'<meta name="description" content="([^"]*)"')
    teile = ['# STUDIO AAH!', '', f'> {kurz}', '',
             'Kontakt: info@studio-aah.de, Gießerstraße 75, 04229 Leipzig.', '']
    for g in reihenfolge:
        if g in abschnitte:
            teile += [f'## {g}', ''] + abschnitte[g] + ['']
    if optional:
        teile += ['## Optional', ''] + optional + ['']
    (website / 'llms.txt').write_text('\n'.join(teile), encoding='utf-8')
    print(f'llms.txt erzeugt ({sum(map(len, abschnitte.values())) + len(optional)} Seiten)')


if __name__ == '__main__':
    main()
