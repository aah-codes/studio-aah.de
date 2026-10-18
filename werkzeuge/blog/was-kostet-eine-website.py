# Baut website/blog/was-kostet-eine-website/index.html aus Vorlage (Kopf/Fuß vom KI-Artikel) + Inhalt + FAQ + JSON-LD.
# Texte nur in was-kostet-eine-website-inhalt.html und in der FAQ unten ändern.
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/was-kostet-eine-website.py
import html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from gemeinsam import STUDIO_ID, WEBSITE, WERKZEUGE, esc, lesezeit as minuten

vorlage = (WEBSITE / 'blog' / 'was-ki-an-meiner-arbeit-veraendert-hat' / 'index.html').read_text(encoding='utf-8')
main = (WERKZEUGE / 'blog' / 'was-kostet-eine-website-inhalt.html').read_text(encoding='utf-8')
slug='was-kostet-eine-website'
url=f'https://studio-aah.de/blog/{slug}/'
titel='Was kostet eine Website? Preise, laufende Kosten und Dauer 2026'
h1='Was kostet eine Website – und wie lange dauert sie?'
beschr='Was kostet eine Website 2026? Preise ab 2.450 €, laufende Kosten und realistische Dauer – mit Beispielrechnungen und Erfahrungen aus Projekten eines Leipziger Studios.'
faq=[
("Was kostet eine einfache Website für Selbstständige?",
 "Bei STUDIO AAH! beginnt eine neue Website bei 2.450 € netto, auch als Onepager; der Launch ist enthalten. Jede Unterseite kostet 190 € mit Texten und Bildern, ein Redesign 400 € mehr."),
("Was kostet eine Website im Monat?",
 "Nach dem Launch zahlen Sie Hosting, Domain und eventuelle Lizenzen direkt an die Anbieter; die Höhe hängt von Anbieter und Tarif ab. Wer Unterstützung möchte: Wartung kostet bei STUDIO AAH! ab 45 € im Monat, Änderungen und Weiterentwicklung 50–85 € netto pro Stunde, je nach Unternehmensgröße."),
("Wie lange dauert es, eine Website erstellen zu lassen?",
 "Ein Onepager dauert bei STUDIO AAH! etwa 4 bis 6 Wochen. Eine Website mit mehreren Unterseiten dauert etwa 3 bis 4 Monate, je nach Umfang bis zu 6 Monate. Wie schnell es geht, hängt auch davon ab, wie zügig Texte, Bilder und Feedback vorliegen."),
("Was kostet eine zusätzliche Unterseite?",
 "Bei STUDIO AAH! kostet jede Unterseite 190 € mit Texten und Bildern, dazu kommt der Basispreis ab 2.450 €. Eine Website mit 10 Unterseiten kostet damit ab 4.350 € netto, Launch eingerechnet."),
("Was kostet eine mehrsprachige Website?",
 "Jede weitere Sprache kostet 30 % des Website-Preises. Die Übersetzung liefern Sie. Eine zweisprachige Website mit 6 Unterseiten kostet damit ab 4.667 € netto, Launch eingerechnet."),
("Woher kommen die Bilder für meine Website?",
 "Sie können eigene Fotos liefern. Außerdem kann STUDIO AAH! Bilder liefern: lizenzfreie Bilder von Plattformen wie Unsplash oder mit KI erstellte Bilder. Ein Fotoshooting führt STUDIO AAH! nicht selbst durch, kann es aber vermitteln."),
("Muss ich alles auf einmal bezahlen?",
 "Nein. Größere Projekte zahlen Sie bei STUDIO AAH! in drei Raten: bei Start, nach Freigabe des Konzepts und beim Go-live."),
("Was passiert, wenn ich mehr Änderungen möchte?",
 "Zwei Korrekturrunden sind im Festpreis enthalten. Jede weitere Runde rechnet STUDIO AAH! nach Aufwand ab, 50–85 € netto pro Stunde, je nach Unternehmensgröße."),
("Lohnt sich ein Relaunch oder reicht eine Überarbeitung?",
 "Eine Überarbeitung reicht, wenn Marke, Angebot, Technik und Seitenstruktur noch passen und es um einzelne Seiten, Texte oder die Sichtbarkeit geht. Ein Relaunch lohnt sich, wenn sich Angebot oder Marke verändert haben, die Seite auf dem Handy schlecht funktioniert oder die Technik veraltet ist. Beim Relaunch müssen alte Adressen auf die neuen Seiten weiterleiten."),
("Sind die Preise netto?",
 "Ja. Alle genannten Preise sind Einstiegspreise ohne Umsatzsteuer. Den Festpreis erhalten Sie nach einem kostenlosen Erstgespräch."),
]
fh=[]
for f,a in faq:
    fh.append(f'''        <details class="faq-eintrag">
          <summary>{esc(f)}</summary>
          <div class="faq-antwort"><p>{esc(a)}</p></div>
        </details>''')
main=main.replace('FAQ_HTML','\n'.join(fh))
# Lesezeit aus dem Text der Seite (ohne Tags), 200 Wörter pro Minute
text=re.sub(r'<[^>]+>',' ',main); woerter=len(re.findall(r'\w+',text))
lesezeit=minuten(woerter)
main=main.replace('LESEZEIT',str(lesezeit))
ld={"@context":"https://schema.org","@graph":[
 {"@type":"BlogPosting","@id":url+"#beitrag","headline":h1,"name":titel,"description":beschr,
  "image":["https://studio-aah.de/bilder/blog-geld-und-zeit-og.jpg","https://studio-aah.de/bilder/blog-geld-und-zeit.webp"],
  "datePublished":"2026-10-13","dateModified":"2026-10-19","inLanguage":"de-DE","url":url,"mainEntityOfPage":url,
  "wordCount":woerter,"articleSection":"Website",
  "keywords":["Website Kosten","Was kostet eine Website","Website erstellen lassen Dauer","laufende Kosten Website","Relaunch","Webdesign Leipzig"],
  "author":{"@type":"Person","name":"Anna Härtelt","url":"https://studio-aah.de/profil/","jobTitle":"UX/UI-Designerin, Strategin und Webentwicklerin","worksFor":{"@id":STUDIO_ID}},
  "publisher":{"@id":STUDIO_ID},
  "isPartOf":{"@type":"Blog","@id":"https://studio-aah.de/blog/#blog","name":"Blog von STUDIO AAH!","url":"https://studio-aah.de/blog/"}},
 {"@type":"ProfessionalService","@id":STUDIO_ID,"name":"STUDIO AAH!","url":"https://studio-aah.de/","logo":"https://studio-aah.de/bilder/icon-512.png",
  "address":{"@type":"PostalAddress","streetAddress":"Gießerstraße 75","postalCode":"04229","addressLocality":"Leipzig","addressCountry":"DE"},
  "founder":{"@type":"Person","name":"Anna Härtelt"}},
 {"@type":"FAQPage","@id":url+"#faq","url":url,"inLanguage":"de","mainEntity":[{"@type":"Question","name":f,"acceptedAnswer":{"@type":"Answer","text":a}} for f,a in faq]},
 {"@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Startseite","item":"https://studio-aah.de/"},
  {"@type":"ListItem","position":2,"name":"Blog","item":"https://studio-aah.de/blog/"},
  {"@type":"ListItem","position":3,"name":h1,"item":url}]}
]}
kopf_ende=vorlage.index('<main id="inhalt">')
fuss_start=vorlage.index('</main>')
head=vorlage[:kopf_ende]
alt_head=head[head.index('<title>'):head.index('<link rel="stylesheet"')]
neu_head=f'''<title>{titel} | STUDIO AAH!</title>
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
  <meta property="og:image" content="https://studio-aah.de/bilder/blog-geld-und-zeit-og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Titel „Was kostet eine Website – und wie lange dauert sie?“ neben einer Figur aus Bauhaus-Grundformen mit blauem Modul und einer Uhr.">
  <meta property="article:published_time" content="2026-10-13">
  <meta property="article:author" content="Anna Härtelt">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
  </script>
  '''
head=head.replace(alt_head,neu_head)
seite=head+'<main id="inhalt">\n\n'+main+'\n</main>'+vorlage[fuss_start+len('</main>'):]
ziel = WEBSITE / 'blog' / slug / 'index.html'
ziel.parent.mkdir(parents=True, exist_ok=True)
ziel.write_text(seite, encoding='utf-8')
print('Wörter',woerter,'Lesezeit',lesezeit)
