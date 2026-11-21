# Checkliste „EU AI Act“ zum Ausdrucken und Abhaken, eine Seite A4. Inhalt = Kurzfassung der Checkliste im Artikel /blog/eu-ai-act-kleine-unternehmen/.
# Anna 17.11.2026 (1): „Button Checkliste downloaden … PDF mit Checkboxen … schöne Überschrift mit einem Bild zum EU AI Act … ganz unten nicht zu dominant
#   ein Call to Action mit einem Bild von mir … zum KI-Arbeits-Setup“.
# Anna 17.11.2026 (2): keine Dachzeile, Titel „EU AI Act für Unternehmen“, fünf Punkte (Personal-KI raus), Logo weiß oben im Bild, QR-Code statt Link,
#   Abschluss „KI-Setup für Profis“ / „Ich richte Ihnen ein KI-Setup mit klaren Regeln ein.“, Kontaktzeile, kein Hinweis „Keine Rechtsberatung“.
# QR-Code aus werkzeuge/grafiken/qr-code.swift (Core Image von macOS, nichts aus dem Netz).
# Ausnahme von „keine PDFs im Repository“: öffentliche Download-Datei in website/downloads/ (.gitignore-Ausnahme, Anna 17.11.2026).
# Aufruf vom Repository-Ordner: python3 werkzeuge/blog/eu-ai-act-checkliste.py
import base64, pathlib, subprocess, tempfile

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent.parent
B = REPO / 'website' / 'bilder'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
QR_ZIEL = 'https://studio-aah.de/ki-arbeits-setup/'


def daten(datei, typ):
    return f'data:{typ};base64,' + base64.b64encode(pathlib.Path(datei).read_bytes()).decode()


def schriften():
    css = []
    for name, datei in (('Anton', 'anton-latin.woff2'), ('Manrope', 'manrope-latin.woff2')):
        css.append(f'@font-face {{ font-family: "{name}"; src: url({daten(REPO / "website" / "schriften" / datei, "font/woff2")}) format("woff2"); font-weight: 200 800; }}')
    return '\n'.join(css)


PUNKTE = [
    ('KI-Werkzeuge aufschreiben', 'Welche KI nutzt dein Team, und wofür?'),
    ('KI-Regelwerk fürs Team schreiben', 'Welche KI-Werkzeuge und Konnektoren (E-Mail, Aufgaben, Figma …) erlaubt sind, welche Daten hineindürfen und welche nicht.'),
    ('Team einführen', 'Einführung ansetzen und vermerken, wer teilgenommen hat.'),
    ('KI-Inhalte kennzeichnen', 'Echt wirkende KI-Bilder, die seit dem 2. August 2026 erscheinen, sichtbar kennzeichnen. Beim eigenen Chatbot: „Sie chatten mit einer KI“.'),
    ('KI-Compliance Kompass nutzen', 'Selbsttest der Bundesnetzagentur: bundesnetzagentur.de/ki-ck'),
]


def seite(qr_png):
    punkte = ''.join(f'<li><span class="box"></span><div><b>{t}</b><span>{z}</span></div></li>' for t, z in PUNKTE)
    return f'''<!doctype html><html lang="de"><meta charset="utf-8"><style>{schriften()}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; font-family: Manrope; color: #0e1011; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.seite {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; display: flex; flex-direction: column; }}
.kopf {{ position: relative; height: 60mm; background: #0a2a78 url({daten(B / 'blog-eu-ai-act-og.jpg', 'image/jpeg')}) center 48% / cover; }}
.kopf img {{ position: absolute; left: 14mm; top: 10mm; width: 40mm; }}
.titel {{ margin: 8mm 14mm 0; }}
h1 {{ font-family: Anton; font-weight: 400; font-size: 34pt; line-height: 1.15; letter-spacing: .01em; margin: 0; text-transform: uppercase; }}
.unter {{ margin: 3mm 14mm 0; font-size: 12pt; line-height: 1.45; }}
ol {{ list-style: none; margin: 6mm 14mm 0; padding: 0; display: grid; gap: 3.5mm; }}
li {{ display: grid; grid-template-columns: 11mm 1fr; gap: 6mm; align-items: center; padding: 4.2mm 6mm; border: 1.3pt solid #0e1011; border-radius: 4mm; }}
.box {{ width: 10mm; height: 10mm; border: 1.8pt solid #0e1011; border-radius: 1.8mm; }}
li b {{ display: block; font-size: 15pt; line-height: 1.25; }}
li span {{ display: block; font-size: 10.5pt; line-height: 1.4; color: #3a3d3f; margin-top: 1mm; }}
.fuss {{ margin: auto 14mm 13mm; display: grid; grid-template-columns: 24mm 1fr 26mm; gap: 6mm; align-items: center; padding-top: 6mm; border-top: 1pt solid #9a9d9e; }}
.fuss img {{ display: block; }}
.fuss .foto {{ width: 24mm; height: 24mm; border-radius: 50%; object-fit: cover; }}
.fuss .qr {{ width: 26mm; height: 26mm; image-rendering: pixelated; }}
.fuss p {{ margin: 0; font-size: 10.5pt; line-height: 1.45; }}
.fuss p b {{ display: block; font-size: 13pt; margin-bottom: 1mm; }}
.fuss .kontakt {{ display: block; margin-top: 4mm; font-size: 9.5pt; }}
</style>
<div class="seite">
  <div class="kopf"><img src="{daten(B / 'logo-studio-aah-weiss.svg', 'image/svg+xml')}" alt="STUDIO AAH!"></div>
  <div class="titel"><h1>EU AI Act für Unternehmen</h1></div>
  <p class="unter">Dein 5-Punkte-Plan: ausdrucken, aufhängen, abhaken.</p>
  <ol>{punkte}</ol>
  <div class="fuss">
    <img class="foto" src="{daten(B / 'anna-haertelt-studio-blau-rund.jpg', 'image/jpeg')}" alt="">
    <p><b>KI-Setup für Profis</b>Ich richte dir ein KI-Setup mit klaren Regeln ein.<span class="kontakt">info@studio-aah.de · 0176 83089879</span></p>
    <img class="qr" src="{daten(qr_png, 'image/png')}" alt="QR-Code zum KI-Arbeits-Setup">
  </div>
</div></html>'''


if __name__ == '__main__':
    ziel = REPO / 'website' / 'downloads' / 'eu-ai-act-checkliste.pdf'
    ziel.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        qr = pathlib.Path(tmp) / 'qr.png'
        subprocess.run(['swift', str(REPO / 'werkzeuge' / 'grafiken' / 'qr-code.swift'), QR_ZIEL, str(qr), '12'], check=True, capture_output=True)
        html = pathlib.Path(tmp) / 'checkliste.html'; html.write_text(seite(qr), encoding='utf-8')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=3000',
                        f'--print-to-pdf={ziel}', html.as_uri()], check=True, capture_output=True)
    print(ziel.relative_to(REPO), ziel.stat().st_size // 1024, 'KB')
