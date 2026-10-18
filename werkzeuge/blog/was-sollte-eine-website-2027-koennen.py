# Baut website/blog/was-sollte-eine-website-2027-koennen/index.html aus Vorlage (Kopf/Fuß vom KI-Artikel) + Inhalt + Grafiken + JSON-LD.
# Reihe „Website-Fragen“, Teil 2 (Anna 19.10.2026). Texte nur in was-sollte-eine-website-2027-koennen-inhalt.html ändern (Reinzeichnung, von Anna freigegeben 19.10.2026).
# Eingebunden: Golden Circle (werkzeuge/grafiken/golden-circle.html), CI-Grafik der Markenbildung und Ökosystem der Webdesign-Seite (dieselben Dateien wie dort).
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/was-sollte-eine-website-2027-koennen.py
import html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from gemeinsam import STUDIO_ID, WEBSITE, WERKZEUGE, lesezeit as minuten

vorlage = (WEBSITE / 'blog' / 'was-ki-an-meiner-arbeit-veraendert-hat' / 'index.html').read_text(encoding='utf-8')
main = (WERKZEUGE / 'blog' / 'was-sollte-eine-website-2027-koennen-inhalt.html').read_text(encoding='utf-8')
slug = 'was-sollte-eine-website-2027-koennen'
url = f'https://studio-aah.de/blog/{slug}/'
titel = 'Was sollte eine Website 2027 können?'
h1 = titel
beschr = 'Markenidentität, Nutzen, Zukunft: was eine Website 2027 leisten muss – mit Beispielen aus Software, Arztpraxis und Handwerk und dem Blick auf KI.'
datum = '2026-10-20'
alt_titel = 'Figur aus Bauhaus-Grundformen zeigt auf den Golden Circle: drei Kreise ineinander, innen schwarz das Warum, darum das Wie, außen das Was.'
alt_og = 'Titel „Was sollte eine Website 2027 können?“ neben einer Figur aus Bauhaus-Grundformen und dem Golden Circle aus drei Kreisen.'


def grafik(name):
    return (WERKZEUGE / 'grafiken' / f'{name}.html').read_text(encoding='utf-8').rstrip('\n')


def nur_figur(t):
    """Aus einer Grafik mit eigenem Abschnitt (Überschrift der Leistungsseite) nur die Abbildung samt Kommentar davor."""
    a = t.index('    <!-- Ökosystem'); e = t.rindex('</figure>') + len('</figure>')
    return t[a:e]


for marke, inhalt in (('GOLDEN_CIRCLE', grafik('golden-circle')), ('CI_GRAFIK', grafik('corporate-identity')), ('OEKOSYSTEM', nur_figur(grafik('website-oekosystem')))):
    if main.count(marke) != 1: raise SystemExit(f'Marke {marke} fehlt oder doppelt in der Inhaltsdatei')
    main = main.replace(marke, inhalt)
main = main.replace('ALT_TITELBILD', html.escape(alt_titel))
# Lesezeit nur aus dem Fließtext: Grafiken (figure) zählen nicht mit, 200 Wörter pro Minute
text = re.sub(r'<figure.*?</figure>', ' ', main, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', text); woerter = len(re.findall(r'\w+', text))
lesezeit = minuten(woerter)
main = main.replace('LESEZEIT', str(lesezeit))
ld = {"@context": "https://schema.org", "@graph": [
 {"@type": "BlogPosting", "@id": url + "#beitrag", "headline": h1, "name": titel, "description": beschr,
  "image": ["https://studio-aah.de/bilder/blog-website-2027-og.jpg", "https://studio-aah.de/bilder/blog-website-2027.webp"],
  "datePublished": datum, "dateModified": datum, "inLanguage": "de-DE", "url": url, "mainEntityOfPage": url,
  "wordCount": woerter, "articleSection": "Webdesign",
  "keywords": ["Website 2027", "Was muss eine Website können", "Corporate Identity", "Golden Circle", "Website und KI", "GEO", "Webdesign Leipzig"],
  "author": {"@type": "Person", "name": "Anna Härtelt", "url": "https://studio-aah.de/profil/", "jobTitle": "UX/UI-Designerin, Strategin und Webentwicklerin", "worksFor": {"@id": STUDIO_ID}},
  "publisher": {"@id": STUDIO_ID},
  "isPartOf": {"@type": "Blog", "@id": "https://studio-aah.de/blog/#blog", "name": "Blog von STUDIO AAH!", "url": "https://studio-aah.de/blog/"}},
 {"@type": "ProfessionalService", "@id": STUDIO_ID, "name": "STUDIO AAH!", "url": "https://studio-aah.de/", "logo": "https://studio-aah.de/bilder/icon-512.png",
  "address": {"@type": "PostalAddress", "streetAddress": "Gießerstraße 75", "postalCode": "04229", "addressLocality": "Leipzig", "addressCountry": "DE"},
  "founder": {"@type": "Person", "name": "Anna Härtelt"}},
 {"@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Startseite", "item": "https://studio-aah.de/"},
  {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://studio-aah.de/blog/"},
  {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}
]}
kopf_ende = vorlage.index('<main id="inhalt">')
fuss_start = vorlage.index('</main>')
head = vorlage[:kopf_ende]
alt_head = head[head.index('<title>'):head.index('<link rel="stylesheet"')]
neu_head = f'''<title>{titel} | STUDIO AAH!</title>
  <meta name="description" content="{html.escape(beschr)}">
  <meta name="author" content="Anna Härtelt">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="../../bilder/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="../../bilder/apple-touch-icon.png">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="STUDIO AAH!">
  <meta property="og:locale" content="de_DE">
  <meta property="og:title" content="{titel}">
  <meta property="og:description" content="{html.escape(beschr)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://studio-aah.de/bilder/blog-website-2027-og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(alt_og)}">
  <meta property="article:published_time" content="{datum}">
  <meta property="article:author" content="Anna Härtelt">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
  </script>
  '''
head = head.replace(alt_head, neu_head)
seite = head + '<main id="inhalt">\n\n' + main + '\n</main>' + vorlage[fuss_start + len('</main>'):]
ziel = WEBSITE / 'blog' / slug / 'index.html'
ziel.parent.mkdir(parents=True, exist_ok=True)
ziel.write_text(seite, encoding='utf-8')
print('Wörter', woerter, 'Lesezeit', lesezeit)
