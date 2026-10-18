# Drei Branchenbilder für den Blog „Was sollte eine Website 2027 können?“ (Teil 2 der Reihe Website-Fragen): Software, Arztpraxis, Bäckerei/Handwerk.
# Gleiche Machart wie das Titelbild (website-2027-titel.py): Punkteraster, feine schwarze Linien, Bauhaus-Figur, Blau nur als Akzent und nie an Schwarz (weiße Fugen).
# Ergebnis: website/bilder/blog-website-2027-software.webp, -arztpraxis.webp, -handwerk.webp (2400 × 1500, angezeigt bis etwa 780 px breit)
# Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/blog/website-2027-branchen.py
import importlib.util, pathlib, tempfile

HIER = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('titel', HIER / 'website-2027-titel.py')
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
SCH, BL, WS, GR, MG, FUGE, CREME = T.SCH, T.BL, T.WS, T.GR, T.MG, T.FUGE, T.CREME
ns = T.ns
B, H = 1200, 750
linie = f'fill="none" stroke="{SCH}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'


def rahmen(inhalt):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {B} {H}" width="{B}" height="{H}">{T.PUNKTE}'
            f'<rect width="{B}" height="{H}" fill="{WS}"/><rect width="{B}" height="{H}" fill="url(#punkte)"/>{inhalt}</svg>')


def figur(fx, fy, arm_l, arm_r, blick=-1, boden=(860, 1160)):
    return (f'<line x1="{boden[0]}" y1="{fy}" x2="{boden[1]}" y2="{fy}" stroke="{SCH}" stroke-width="2"/>'
            f'<g transform="translate({fx} {fy})">' + ns['figur'](arm_l, arm_r, 14, -10, blick=blick) + '</g>')


def text(x, y, t, gr=14, schrift='JetBrains Mono', farbe=SCH, anker='start', extra=''):
    return f'<text x="{x}" y="{y}" font-family="{schrift}" font-size="{gr}" fill="{farbe}" text-anchor="{anker}" {extra}>{t}</text>'


def browser(x, y, w, h, adresse):
    return (f'<g {linie}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{WS}"/><line x1="{x}" y1="{y + 46}" x2="{x + w}" y2="{y + 46}"/>'
            f'<circle cx="{x + 30}" cy="{y + 23}" r="6"/><circle cx="{x + 52}" cy="{y + 23}" r="6"/><circle cx="{x + 74}" cy="{y + 23}" r="6"/>'
            f'<rect x="{x + 110}" y="{y + 11}" width="300" height="24" rx="12"/></g>' + text(x + 128, y + 28, adresse, 13, farbe=MG))


def software():
    s = [browser(70, 80, 740, 580, 'ihre-software.de/produkttour')]
    s.append(text(110, 200, 'PRODUKTTOUR', 46, 'Anton', extra='letter-spacing="1"'))
    s.append(text(112, 232, 'Erst ausprobieren, dann sprechen.', 17, 'Manrope'))
    for i, x in enumerate((110, 330, 550)):
        gestrichelt = '' if i == 0 else ' stroke-dasharray="8 8"'
        s.append(f'<rect x="{x}" y="270" width="200" height="160" rx="12" fill="{WS}" stroke="{SCH}" stroke-width="2"{gestrichelt}/>')
        s.append(f'<circle cx="{x + 34}" cy="304" r="18" fill="{SCH}"/>' + text(x + 34, 310, str(i + 1), 18, 'Anton', WS, 'middle'))
        s.append(f'<g stroke="{MG}" stroke-width="2"><line x1="{x + 24}" y1="350" x2="{x + 176}" y2="350"/><line x1="{x + 24}" y1="372" x2="{x + 150}" y2="372"/><line x1="{x + 24}" y1="394" x2="{x + 120}" y2="394"/></g>')
    s.append(f'<rect x="110" y="460" width="400" height="160" rx="12" fill="{CREME}" stroke="{SCH}" stroke-width="2"/>'
             f'<circle cx="310" cy="540" r="40" fill="{SCH}"/><path d="M298 518 L332 540 L298 562 Z" fill="{WS}"/>'
             + text(130, 600, 'VIDEO · 2 MIN', 13, farbe=SCH))
    s.append(f'<rect x="540" y="510" width="210" height="56" rx="28" fill="{BL}"/>' + text(645, 544, 'DEMO BUCHEN →', 15, farbe=WS, anker='middle'))
    s.append(figur(1010, 690, 100, ns['ARM_UNTEN']))
    return rahmen(''.join(s))


def arztpraxis():
    s = ['<g transform="translate(-130 0)">']
    # Telefon mit Kalender, ein Termin blau gebucht
    s.append(f'<rect x="250" y="50" width="300" height="640" rx="40" fill="{WS}" stroke="{SCH}" stroke-width="3"/><rect x="350" y="70" width="100" height="16" rx="8" fill="{SCH}"/>')
    s.append(text(280, 140, 'TERMIN BUCHEN', 30, 'Anton', extra='letter-spacing="1"') + text(282, 168, 'Ihre Hausarztpraxis', 13, farbe=MG))
    tage = ['MO', 'DI', 'MI', 'DO']
    for i, t in enumerate(tage):
        s.append(text(318 + i * 58, 205, t, 12, farbe=MG, anker='middle'))
        for j in range(5):
            x, y = 292 + i * 58, 220 + j * 50
            if (i, j) == (2, 1):
                s.append(f'<rect x="{x}" y="{y}" width="52" height="42" rx="8" fill="{BL}"/><path d="M{x + 16} {y + 22} l7 7 l14 -15" fill="none" stroke="{WS}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
            elif (i + j) % 3 == 0:
                s.append(f'<rect x="{x}" y="{y}" width="52" height="42" rx="8" fill="{GR}"/>')
            else:
                s.append(f'<rect x="{x}" y="{y}" width="52" height="42" rx="8" fill="{WS}" stroke="{SCH}" stroke-width="1.5"/>')
    s.append(text(400, 520, 'Mi, 9:00 Uhr – gebucht', 16, 'Manrope', anker='middle', extra='font-weight="600"'))
    s.append(f'<rect x="300" y="560" width="200" height="50" rx="25" fill="{SCH}"/>' + text(400, 591, 'Videosprechstunde', 14, 'Manrope', WS, 'middle', 'font-weight="600"'))
    # SMS-Erinnerung
    s.append(f'<path d="M600 170 h270 a16 16 0 0 1 16 16 v96 a16 16 0 0 1 -16 16 h-230 l-30 26 v-26 h-10 a16 16 0 0 1 -16 -16 v-96 a16 16 0 0 1 16 -16 Z" fill="{CREME}" stroke="{SCH}" stroke-width="2"/>')
    s.append(text(618, 206, 'SMS · ERINNERUNG', 13, farbe=SCH) + text(618, 240, 'Ihr Termin ist morgen', 18, 'Manrope') + text(618, 266, 'um 9:00 Uhr.', 18, 'Manrope'))
    s.append('</g>')
    s.append(figur(1030, 690, 34, ns['ARM_UNTEN'], blick=-1, boden=(880, 1170)))
    return rahmen(''.join(s))


def handwerk():
    s = []
    s.append(text(390, 150, 'BÄCKEREI', 64, 'Anton', anker='middle', extra='letter-spacing="3"'))
    s.append(f'<rect x="90" y="250" width="600" height="440" fill="{WS}" stroke="{SCH}" stroke-width="2"/>')
    # Markise aus Streifen mit Halbkreis-Kante (über dem Laden)
    n, x0, w = 8, 70, 80
    for i in range(n):
        f = SCH if i % 2 == 0 else WS
        s.append(f'<rect x="{x0 + i * w}" y="180" width="{w}" height="70" fill="{f}" stroke="{SCH}" stroke-width="2"/>'
                 f'<path d="M{x0 + i * w} 250 a{w / 2} {w / 2} 0 0 0 {w} 0 Z" fill="{f}" stroke="{SCH}" stroke-width="2"/>')
    # Schaufenster mit Brötchen (Halbkreise) und Aushang
    s.append(f'<rect x="120" y="320" width="320" height="260" rx="6" fill="{CREME}" stroke="{SCH}" stroke-width="2"/><line x1="130" y1="540" x2="430" y2="540" stroke="{SCH}" stroke-width="2"/>')
    for i, x in enumerate((170, 240, 310, 380)):
        f = BL if i == 2 else SCH
        s.append(f'<path d="M{x - 28} 538 a28 28 0 0 1 56 0 Z" fill="{f}"/>')
    s.append(f'<g transform="rotate(-3 280 410)"><rect x="160" y="345" width="240" height="140" fill="{WS}" stroke="{SCH}" stroke-width="2"/>'
             + text(280, 400, 'WIR BILDEN AUS!', 30, 'Anton', anker='middle', extra='letter-spacing="1"')
             + text(280, 430, 'Bäcker:in · Verkauf', 14, 'Manrope', anker='middle')
             + f'<rect x="200" y="446" width="160" height="26" rx="13" fill="{BL}"/>' + text(280, 464, 'Jetzt bewerben →', 13, 'Manrope', WS, 'middle', 'font-weight="600"') + '</g>')
    # Tür mit Öffnungszeiten
    s.append(f'<rect x="480" y="330" width="170" height="360" fill="{WS}" stroke="{SCH}" stroke-width="2"/><circle cx="630" cy="520" r="8" fill="{SCH}"/>'
             f'<rect x="505" y="360" width="120" height="90" fill="{WS}" stroke="{SCH}" stroke-width="1.5"/>' + text(565, 386, 'GEÖFFNET', 12, anker='middle')
             + text(565, 410, 'Mo–Fr 6–18', 12, 'Manrope', anker='middle') + text(565, 432, 'Sa 6–12', 12, 'Manrope', anker='middle'))
    s.append(f'<line x1="40" y1="690" x2="720" y2="690" stroke="{SCH}" stroke-width="2"/>')
    s.append(figur(1000, 690, 100, ns['ARM_UNTEN'], boden=(840, 1160)))
    return rahmen(''.join(s))


if __name__ == '__main__':
    bilder = T.REPO / 'website' / 'bilder'
    with tempfile.TemporaryDirectory() as tmp:
        for name, svg in (('software', software()), ('arztpraxis', arztpraxis()), ('handwerk', handwerk())):
            png = pathlib.Path(tmp) / f'{name}.png'
            T.aufnahme(T.seite(svg).replace('svg{display:block}', 'svg{display:block;width:1200px;height:750px}'), B, H, png, skala=2)
            ziel = bilder / f'blog-website-2027-{name}.webp'
            T.als_webp(png, ziel, 0.88)
            print(ziel.name, ziel.stat().st_size // 1024, 'KB')
