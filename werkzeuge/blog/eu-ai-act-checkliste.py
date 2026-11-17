# Checkliste „EU AI Act“ zum Ausdrucken und Abhaken, eine Seite A4 (Anna 17.11.2026: „Button Checkliste downloaden … PDF mit Checkboxen …
# schöne Überschrift mit einem Bild zum EU AI Act, dann die Regeln relativ groß und präsent … ganz unten nicht zu dominant ein Call to Action
# mit einem Bild von mir … zum KI-Arbeits-Setup“). Inhalt = Checkliste im Artikel /blog/eu-ai-act-kleine-unternehmen/.
# Ausnahme von „keine PDFs im Repository“: öffentliche Download-Datei in website/downloads/ (.gitignore-Ausnahme, Anna 17.11.2026).
# Aufruf vom Repository-Ordner: python3 werkzeuge/blog/eu-ai-act-checkliste.py
import base64, pathlib, subprocess, tempfile

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent.parent
B = REPO / 'website' / 'bilder'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


def daten(datei, typ):
    return f'data:{typ};base64,' + base64.b64encode(datei.read_bytes()).decode()


def schriften():
    css = []
    for name, datei in (('Anton', 'anton-latin.woff2'), ('Manrope', 'manrope-latin.woff2'), ('JetBrains Mono', 'jetbrains-mono-latin.woff2')):
        css.append(f'@font-face {{ font-family: "{name}"; src: url({daten(REPO / "website" / "schriften" / datei, "font/woff2")}) format("woff2"); font-weight: 200 800; }}')
    return '\n'.join(css)


PUNKTE = [
    ('KI-Werkzeuge aufschreiben', 'Welche KI nutzt Ihr Team, und wofür?'),
    ('KI-Regelwerk fürs Team schreiben', 'Welche KI-Werkzeuge und Konnektoren (E-Mail, Aufgaben, Figma …) erlaubt sind, welche Daten hineindürfen und welche nicht.'),
    ('Team einführen', 'Einführung ansetzen und vermerken, wer teilgenommen hat.'),
    ('KI-Bilder kennzeichnen', 'Echt wirkende KI-Bilder, die seit dem 2. August 2026 erscheinen, sichtbar kennzeichnen.'),
    ('Chatbot-Hinweis einbauen', '„Sie chatten mit einer KI“ beim eigenen Chatbot auf der Website.'),
    ('KI-Compliance Kompass nutzen', 'Selbsttest der Bundesnetzagentur: bundesnetzagentur.de/ki-ck'),
    ('Personal-KI prüfen, bis Dezember 2027', 'Bewertet ein Werkzeug Bewerbungen, Leistung oder Gefühle? Dann genau hinsehen.'),
]

punkte = ''.join(f'<li><span class="box"></span><div><b>{t}</b><span>{z}</span></div></li>' for t, z in PUNKTE)

html = f'''<!doctype html><html lang="de"><meta charset="utf-8"><style>{schriften()}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; font-family: Manrope; color: #0e1011; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.seite {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; display: flex; flex-direction: column; }}
.kopf {{ height: 64mm; background: #0a2a78 url({daten(B / 'blog-eu-ai-act-og.jpg', 'image/jpeg')}) center 48% / cover; }}
.titel {{ margin: 7mm 14mm 0; }}
.dach {{ font-family: "JetBrains Mono"; font-size: 9pt; letter-spacing: .12em; text-transform: uppercase; margin: 0 0 2mm; }}
h1 {{ font-family: Anton; font-weight: 400; font-size: 30pt; line-height: 1.15; letter-spacing: .01em; margin: 0; text-transform: uppercase; }}
.unter {{ margin: 3mm 14mm 0; font-size: 11.5pt; line-height: 1.45; }}
ol {{ list-style: none; margin: 5mm 14mm 0; padding: 0; display: grid; gap: 2.6mm; }}
li {{ display: grid; grid-template-columns: 10mm 1fr; gap: 5mm; align-items: center; padding: 2.8mm 5mm; border: 1.2pt solid #0e1011; border-radius: 4mm; }}
.box {{ width: 9mm; height: 9mm; border: 1.6pt solid #0e1011; border-radius: 1.6mm; }}
li b {{ display: block; font-size: 13pt; line-height: 1.25; }}
li span {{ display: block; font-size: 10pt; line-height: 1.4; color: #3a3d3f; margin-top: .6mm; }}
.fuss {{ margin: auto 14mm 13mm; display: grid; grid-template-columns: 22mm 1fr auto; gap: 5mm; align-items: center; padding-top: 5mm; border-top: 1pt solid #9a9d9e; }}
.fuss img.foto {{ width: 22mm; height: 22mm; border-radius: 50%; object-fit: cover; }}
.fuss p {{ margin: 0; font-size: 9.5pt; line-height: 1.45; }}
.fuss p b {{ font-size: 11pt; }}
.fuss .logo {{ width: 34mm; }}
.recht {{ position: absolute; left: 14mm; right: 14mm; bottom: 5mm; font-size: 7pt; color: #6b6e6f; }}
</style>
<div class="seite">
  <div class="kopf"></div>
  <div class="titel"><p class="dach">Checkliste · Stand November 2026</p><h1>EU AI Act für kleine Unternehmen</h1></div>
  <p class="unter">Sieben Schritte, die Sie diese Woche erledigen können. Ausdrucken, aufhängen, abhaken.</p>
  <ol>{punkte}</ol>
  <div class="fuss">
    <img class="foto" src="{daten(B / 'anna-haertelt-studio-blau-rund.jpg', 'image/jpeg')}" alt="">
    <p><b>KI im Team, aber richtig?</b><br>Mit dem KI-Arbeits-Setup richte ich KI für Ihr Team ein, mit klaren Regeln und einer Einführung.<br>studio-aah.de/ki-arbeits-setup · info@studio-aah.de · 0176 83089879</p>
    <img class="logo" src="{daten(B / 'logo-studio-aah.svg', 'image/svg+xml')}" alt="STUDIO AAH!">
  </div>
  <p class="recht">Keine Rechtsberatung. Erklärungen und Quellen: studio-aah.de/blog/eu-ai-act-kleine-unternehmen</p>
</div></html>'''

if __name__ == '__main__':
    ziel = REPO / 'website' / 'downloads' / 'eu-ai-act-checkliste.pdf'
    ziel.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        seite = pathlib.Path(tmp) / 'checkliste.html'; seite.write_text(html, encoding='utf-8')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=3000',
                        f'--print-to-pdf={ziel}', seite.as_uri()], check=True, capture_output=True)
    print(ziel.relative_to(REPO), ziel.stat().st_size // 1024, 'KB')
