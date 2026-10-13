# Hosting-Preise IONOS, STRATO, ALL-INKL.COM (Stand 13.10.2026)

Alle Angaben selbst abgerufen am **13.10.2026** (curl; IONOS zusätzlich mit Playwright gerendert). Rohdaten: `preise/roh/`, `preise/render/`.
Alle Preise **brutto (inkl. 19 % MwSt.)**, soweit nicht anders vermerkt. „Eigene Rechnung“ = von mir aus den belegten Zahlen errechnet, steht so nicht auf der Seite.

---

## 1. IONOS (ionos.de)

| Angabe | Wert | Beleg |
|---|---|---|
| **Domain .de** – 1. Jahr | 0,08 €/Monat für 12 Monate | I1 |
| Domain .de – danach | **Unsicher:** kein „danach“-Preis genannt; durchgestrichener Normalpreis 1,30 €/Monat (JSON `strikePrice` 1,30 brutto / 1,09 netto) | I1 |
| Domain .de – Einrichtung | keine angegeben (JSON `"setup":null`) | I1 |
| **WordPress: „Start“** (günstigstes) | 3 €/Monat für 6 Monate, danach 5 €/Monat | I2 |
| Start – Einrichtung | keine angezeigt (JSON `"setup":null`) | I2 |
| Start – Leistungen | 25 GB, 1 Postfach, 1 Domain, 1 SSL (DV, Wildcard) | I2 |
| **WordPress: „Grow“** (Stufe darüber, „Bestseller“) | 1 €/Monat für 12 Monate, danach 10 €/Monat; keine Einrichtung | I2 |
| Grow – Leistungen | 50 GB, 5 Postfächer, 1 Domain, 1 SSL (DV) | I2 |
| Alternative **Webhosting „Standard“** | 3 €/Monat für 6 Monate, danach 6 €/Monat, Einrichtung 10 € | I3 |
| Alternative **Webhosting „Plus“** | 1 €/Monat für 12 Monate, danach 11 €/Monat, Einrichtung 10 € durchgestrichen (entfällt) | I3, I4 |
| Abrechnung | monatlich (JSON `"billingCycle":"MONTHLY"`) | I2, I3 |
| Mindestvertragslaufzeit | **12 Monate** laut JSON `"mct":{"duration":1,"durationType":"YEARLY"}` bei allen Paketen; im sichtbaren Text nur „teils abhängig von Mindestvertragslaufzeiten“. FAQ nennt „auf Wunsch Webhosting ohne Vertragslaufzeit“ (Preise dafür auf der Seite nicht gefunden) | I2, I3, I5 |
| Domain im Paket | **Unsicher/Widerspruch:** Tooltip „Kostenlose Domain für 1 Jahr bei Abschluss einer Vertragslaufzeit von 12 Monaten“; FAQ derselben Seite: „1 Domain dauerhaft inklusive“ | I2, I6 |
| E-Mail-Postfach | ja (Start 1, Grow 5; Webhosting Standard 1, Plus 2), je 2 GB | I2, I3 |
| SSL | inklusive, „1 SSL (DV)“ Wildcard; Aussteller (z. B. Let's Encrypt) nicht genannt | I2, I3 |
| Brutto/Netto | brutto: „Preise inkl. MwSt.“ | I1–I3 |
| Serverstandort | WordPress-Hosting: Deutschland. Webhosting: „europäische Infrastruktur“ | I6, I3 |
| AVV | ja, Bestandteil der AGB seit 19.07.2022, Text online, kostenlos | I7, I8, I9 |

Erstes Jahr (eigene Rechnung, ohne Zusatzoptionen): Start 6×3 + 6×5 = **48 €**; Grow 12×1 = **12 €**, ab Monat 13 dann 120 €/Jahr; Webhosting Standard 6×3 + 6×6 + 10 = **64 €**.

---

## 2. STRATO (strato.de)

| Angabe | Wert | Beleg |
|---|---|---|
| **Domain .de** – 1. Jahr | 0,05 €/Monat für 12 Monate | S1 |
| Domain .de – danach | 1 €/Monat („Standardpreis 1 €“) | S1 |
| Domain .de – Einrichtung | 0 € | S1 |
| Domain .de – Laufzeit | Bestellcode `STRATO_DOMAIN_DE_AKTION_VLZ12` (deutet auf 12 Monate; als Text nicht gefunden) | S1 |
| **Hosting für WordPress „Basic“** (günstigstes, Laufzeit 12 Monate) | 0 € für 1 Monat, danach 5 €/Monat, Einrichtung 0 € | S2 |
| WP Basic, Laufzeit 1 Monat | 6 €/Monat, Einrichtung („Installation“) 10 € | S2 |
| WP Basic – Leistungen | 25 GB, 1 Postfach (5 GB), 1 Domain dauerhaft inkl., 1 SSL, 1 Datenbank | S2 |
| **Hosting für WordPress „Plus“** (Stufe darüber) | 1 €/Monat für 12 Monate, danach 9 €/Monat, Einrichtung 0 €; bei 1 Monat Laufzeit 10 €/Monat + 10 € | S2 |
| WP Plus – Leistungen | 50 GB, 3 Postfächer, 1 Domain dauerhaft inkl., 1 SSL | S2 |
| Alternative **Hosting „Starter“** (12 Monate) | 0 € für 1 Monat, danach 5 €/Monat, Einrichtung 0 €, Mindestvertragslaufzeit 12 Monate; 1 Domain, 1 SSL, 1 Postfach, 2 Datenbanken | S3 |
| Alternative **Hosting „Basic“** (12 Monate) | 1 €/Monat für 12 Monate, danach 9 €/Monat, Einrichtung 0 €, Mindestvertragslaufzeit 12 Monate; 3 Domains, 3 SSL, 2 Postfächer | S3 |
| Hosting bei 1 Monat Laufzeit | Starter 6 €, Basic 10 €/Monat, Einrichtung je 10 €, Mindestvertragslaufzeit 1 Monat | S3 |
| Abrechnung | Hosting-Tabelle: „Abrechnung nach Aktionslaufzeit“ Starter 1 Monat, Basic 6 Monate. Für WordPress-Pakete nicht angegeben | S3 |
| Mindestvertragslaufzeit WordPress | als Text **nicht gefunden**; Umschalter „1 Monat / 12 Monate“, Bestellcodes `…_VLZ1` / `…_AKTION_VLZ12` | S2 |
| Brutto/Netto | brutto: „Preise inkl. MwSt.“ | S1–S3 |
| SSL | inklusive („1 SSL-Zertifikat“). Typ/Aussteller des Inklusiv-Zertifikats nicht gefunden (die STRATO-SSL-Seite nennt Sectigo nur für die Zusatz-Zertifikate) | S2, S3, S6 |
| Serverstandort | Deutschland (zwei Rechenzentren) | S2, S3 |
| AVV | ja, nach Art. 28 DSGVO, Text unter www.strato.de/agb/avv/ | S4, S5 |

Erstes Jahr (eigene Rechnung): WP Basic 1×0 + 11×5 = **55 €**; WP Plus 12×1 = **12 €**, danach 108 €/Jahr.

---

## 3. ALL-INKL.COM (all-inkl.com)

| Angabe | Wert | Beleg |
|---|---|---|
| **Domain .de** (einzeln) | 9,90 €/Jahr, Einrichtung 0,00 €; kein Aktionspreis, also 1. Jahr = danach | A1, A2 |
| **Webhosting „Privat“** (günstigstes) | 1 Monat kostenlos, danach 4,95 €/Monat | A3, A4 |
| Privat – Einrichtung | 14,95 € durchgestrichen, „entfällt!“ | A4 |
| Privat – Mindestvertragslaufzeit | keine | A3, A4 |
| Privat – Leistungen | 50 GB, 3 Domains inklusive (u. a. .de), 500 Postfächer, 5 Datenbanken, WordPress per Software-Installer | A3, A4 |
| Privat – SSL | **nicht inklusive:** Let's Encrypt „kostet zusätzlich 0,95 EUR*/Monat“ | A4 |
| **Webhosting „Privat+“** (Stufe darüber) | 1 Monat kostenlos, danach 7,95 €/Monat; Einrichtung 14,95 € entfällt; keine Mindestvertragslaufzeit | A3, A5 |
| Privat+ – Leistungen | 100 GB, 5 Domains inklusive, 1000 Postfächer, 25 Datenbanken, Let's Encrypt inklusive | A3, A5 |
| Abrechnung | monatlich zahlbar; auf Wunsch Vorauszahlung 3, 6 oder 12 Monate | A6 |
| Brutto/Netto | brutto: „enthält die gesetzliche Mehrwertsteuer in Höhe von 19%“ | A3 |
| Serverstandort | Deutschland, eigene Rechenzentren in Dresden | A7 |
| AVV | ja, nach Art. 28 DS-GVO; Bestandteil jedes Webhosting-Vertrags („Vertragsbedingungen über die Auftragsverarbeitung im Webhosting-Vertrag“), einsehbar/abschließbar in der MembersArea. **Eigene öffentliche Seite mit dem AVV-Text: nicht gefunden** | A8, A9 |

Erstes Jahr (eigene Rechnung): Privat mit Let's Encrypt 11×4,95 + 12×0,95 = **65,85 €**, danach 70,80 €/Jahr (Unsicher: ob die 0,95 € auch im Gratismonat anfallen); Privat+ 11×7,95 = **87,45 €**, danach 95,40 €/Jahr. Domain im Paket inklusive.

---

## Belegliste (alle abgerufen am 13.10.2026)

### IONOS
- **I1** https://www.ionos.de/domains/de-domain – „.de … Sparen Sie 94% 1,30 € 0,08 € /Monat für 12 Monate“; Fußzeile „Preise inkl. MwSt., Angebote sind nur für begrenzte Zeit gültig und sind teils abhängig von Mindestvertragslaufzeiten.“; JSON: `"price":{"net":0.07,"gross":0.08},…"setup":null,"strikePrice":{"net":1.09,"gross":1.3}`
- **I2** https://www.ionos.de/hosting/wordpress-hosting – „Start … Sparen Sie 33% 6 € 3 € /Monat für 6 Monate Danach 5 € /Monat“; „Grow … Sparen Sie 91% 11 € 1 € /Monat für 12 Monate Danach 10 € /Monat“; Tabelle „E-Mail-Postfächer 1 | 5 | 10 | 10“, „SSL Wildcard-Zertifikate inklusive 1 SSL (DV)“; Tooltip „Kostenlose Domain für 1 Jahr bei Abschluss einer Vertragslaufzeit von 12 Monaten.“; JSON Start: `"mct":{"duration":1,"durationType":"YEARLY"},"offer":{"duration":6,…},"price":{"net":2.52,"gross":3},…"setup":null`
- **I3** https://www.ionos.de/hosting/webhosting – „Webhosting Standard Sparen Sie 32% 7 € 3 € /Monat für 6 Monate Danach 6 € /Monat Einrichtung 10 €“; „Webhosting Plus Sparen Sie 92% 12 € 1 € /Monat für 12 Monate Danach 11 € /Monat Einrichtung 10 €“; „E-Mail-Postfächer 1 | 2 | 4 | 5“; „SSL-Zertifikat 1 DV Wildcard“; „Wählen Sie bei der Bestellung Ihre Wunschadresse – für 1 Jahr kostenlos.“; „Georedundante, zertifizierte europäische Infrastruktur“
- **I4** dieselbe Seite, mit Playwright gerendert: beim Plus-Tarif `<span class="setup-strike">Einrichtung 10 €</span>` (durchgestrichen), beim Standard-Tarif `class="setup-price"`; JSON Plus `"setup":null,"strikeSetup":{"net":8.4,"gross":10}`
- **I5** https://www.ionos.de/hosting/webhosting (FAQ) – „Bei uns bekommen Sie auf Wunsch Webhosting ohne Vertragslaufzeit, das heißt, die Kündigungsfrist in den entsprechenden Tarifen beträgt nur einen Monat.“
- **I6** https://www.ionos.de/hosting/wordpress-hosting (FAQ) – „In unseren Managed Hosting-Pakete für WordPress erhalten Sie 1 Domain dauerhaft inklusive. Ein SSL-Zertifikat ist ebenfalls inklusive.“; „Auch befindet sich der Serverstandort für unser Hosting für WordPress in Deutschland.“
- **I7** https://www.ionos.de/terms-gtc/AVV/ – „Vereinbarung zur Auftragsverarbeitung Nach Art. 28 Abs. 3 Datenschutz-Grundverordnung (DSGVO)“; „Die vertraglich vereinbarte Datenverarbeitung findet in einem Mitgliedstaat der Europäischen Union oder in einem anderen Vertragsstaat des Abkommens über den Europäischen Wirtschaftsraum statt, sofern nicht zur Erbringung der Leistung der Datentransfer in Drittstaaten erforderlich ist.“
- **I8** https://www.ionos.de/hilfe/datenschutz/allgemeine-informationen-zur-datenschutz-grundverordnung-dsgvo/vereinbarung-zur-auftragsverarbeitung-avv-mit-ionos-abschliessen/ – „Seit dem 19.07.2022 ist die Vereinbarung zur Auftragsverarbeitung Bestandteil der IONOS AGB.“; „Der Abschluss dieser Vereinbarung ist für Sie ohne zusätzliche Kosten.“
- **I9** https://www.ionos.de/terms-gtc/terms/ (AGB 11.3) – „Insoweit die IONOS für den Kunden als Auftragsverarbeiter im Sinne von Art. 28 Abs. 3 DSGVO tätig wird, gelten ergänzend … spezielle Regelungen zur Auftragsverarbeitungsvereinbarung“

### STRATO
- **S1** https://www.strato.de/domains/de-domain/ – „.de 0,05 € /Mon. für 12 Monate danach 1 € /Mon. Einrichtung: 0 € … Preise inkl. MwSt.“; Tabelle „Aktionspreis 12 Monate 0,05 €/Mon. Standardpreis 1 € Einrichtungsgebühr 0 €“
- **S2** https://www.strato.de/hosting/wordpress-hosting/ – 12 Monate: „Basic 8 % Sparen 0 € für 1 Monat danach 5 €/Mon. Einrichtung: 0 € … 1 Domain dauerhaft inkl. 1 SSL-Zertifikat 1 Postfach … 25 GB Webspace“; „Plus 89 % Sparen 1 € /Mon. für 12 Monate danach 9 €/Mon. Einrichtung: 0 €“; 1 Monat: „Basic 6 € /Mon. für 1 Monat Einrichtung: 10 €“; „Vertragsbedingungen Standardpreis (für 12 Monate) 5 € | 9 € | 15 € | 20 € … Installation 0 €“; „Das Hosting für WordPress von STRATO erfolgt auf Servern in deutschen Rechenzentren.“
- **S3** https://www.strato.de/hosting/ – „Starter … 0 € /Mon. für 1 Monat danach 5 €/Mon. Einrichtung: 0 €“; „Basic … 1 € /Mon. für 12 Monate danach 9 €/Mon. Einrichtung: 0 €“; Tabelle 12 Monate: „Standardpreis (monatlich) 5 € | 9 € | 12 € | 22 € Einrichtungsgebühr (einmalig) 0 € … Mindestvertragslaufzeit 12 Monate … Abrechnung nach Aktionslaufzeit 1 Monat | 6 Monate | 1 Monat | 1 Monat“; Tabelle 1 Monat: „6 € | 10 € | 14 € | 24 € Einrichtungsgebühr (einmalig) 10 € … Mindestvertragslaufzeit 1 Monat“; „E-Mail-Postfächer 1 | 2 | 2 | 5“; „Hosting in deutschen Rechenzentren – Ihre Daten bleiben in der EU“
- **S4** https://www.strato.de/agb/ (Ziffer 1.4) – „Wenn wir für Sie personenbezogene Daten als Auftragsverarbeiter nach Art. 28 DSGVO … verarbeiten, dann gilt neben diesen AGB auch eine Vereinbarung zur Auftragsdatenverarbeitung. … www.strato.de/agb/avv/“
- **S5** https://www.strato.de/agb/avv/ – „Nach Art. 28 Abs. 3 Datenschutz-Grundverordnung (DSGVO)“; „Die vertraglich vereinbarte Datenverarbeitung findet in einem Mitgliedstaat der Europäischen Union oder in einem anderen Vertragsstaat des Abkommens über den Europäischen Wirtschaftsraum statt …“
- **S6** https://www.strato.de/ssl-zertifikat/ – „SSL Starter Domain Validation (DV)“; „Unser Kooperationspartner: Sectigo“ (betrifft Zusatz-Zertifikate; welches Zertifikat im Paket steckt: nicht gefunden)

### ALL-INKL.COM
- **A1** https://all-inkl.com/domains/preise – „.de Deutschland 0,00 €* 9,90 €*“ (Spalten „Einrichtung“, „Jahresgebühr“); „* Die Preise enthalten die gesetzliche Mehrwertsteuer in Höhe von 19%.“
- **A2** https://all-inkl.com/domains – „Top-Domain-Preise de 9,90 EUR* pro Jahr“
- **A3** https://all-inkl.com/webhosting – „4,95 € 0 € mtl.* … * für 1 Monat, danach regulärer Preis 4,95 € … Keine Mindestvertragslaufzeit 3 Domains inklusive“; „7,95 € … Keine Mindestvertragslaufzeit 5 Domains inklusive“; „* Preis je Monat in Euro. Ab dem 2. Monat der Vertragslaufzeit gelten die regulären Gebühren. Der angezeigte Gesamtpreis enthält die gesetzliche Mehrwertsteuer in Höhe von 19%.“
- **A4** https://all-inkl.com/webhosting/privat – „Einrichtungsgebühr ~~14,95 €~~ entfällt!“ (HTML `<del>14,95&nbsp;€</del> … entfällt!`); „Mindestvertragslaufzeit keine“; „Der SSL-Schutz wird über die MembersArea beantragt und kostet zusätzlich 0,95 EUR*/Monat für sämtliche Domains Ihres Vertrages. In dem PrivatPlus-, Premium- und Business-Tarif ist diese Option kostenlos enthalten.“; „E-Mail-Postfächer 500“; „MySQL/MariaDB 5“
- **A5** https://all-inkl.com/webhosting/privatplus – „1 Monat kostenlos! danach 7,95 €“; „Einrichtungsgebühr 14,95 € entfällt!“; „Let’s Encrypt-SSL-Zertifikat … ja“; https://all-inkl.com/webhosting/paketvergleich – „Let’s Encrypt-SSL-Zertifikate … gegen Aufpreis | ja | ja | ja“
- **A6** https://all-inkl.com/webhosting/zahlungsweise – „Jeder unserer Tarife ist dabei monatlich zahlbar; es sind jedoch auch längere Vorauszahlungszeiträume (3 Monate, 6 Monate, 12 Monate) möglich.“
- **A7** https://all-inkl.com/info/rechenzentrum – „Als einer der wenigen Anbieter verfügt ALL‑INKL.COM über mehrere eigene Rechenzentren. Diese befinden sich am Standort Dresden. Alle Daten unserer Kunden werden somit ausschließlich auf Servern in Deutschland gespeichert“
- **A8** https://all-inkl.com/agb (Ziffer 15.2/15.3) – „Ohne Einbeziehungen der ergänzenden ‚Vertragsbedingungen über die Auftragsverarbeitung im Webhosting-Vertrag‘ kann der Kunde standardmäßig keinen Webhosting-Vertrag mit NMM abschließen. … Den Abschluss eines Auftragsverarbeitungsvertrags kann der Kunde auch in der MembersArea (MA) unter der Rubrik Stammdaten/Auftragsverarbeitung in einem elektronischen Format veranlassen.“; „… entsprechen somit den gesetzlichen Vorgaben aus Artikel 28 Abs. 3 und 4 der DS-GVO.“
- **A9** https://all-inkl.com/datenschutzinformationen (22.6.2) – „Diese Konstellation verpflichtet uns und den Kunden, nach Art. 28 DS-GVO eine Vereinbarung über die Auftrags(daten)verarbeitung abzuschließen.“

---

## Unsicherheiten / offen
1. **IONOS .de-Folgepreis:** Die Seite nennt keinen „danach“-Preis, nur den durchgestrichenen Normalpreis 1,30 €/Monat. Dass das der Preis ab Monat 13 ist, ist naheliegend, steht aber so nicht da.
2. **IONOS-Laufzeit:** 12 Monate nur aus dem eingebetteten JSON (`mct` = 1 Jahr) abgeleitet. Ein Tarif ohne Laufzeit wird in der FAQ erwähnt, Preise dafür nicht gefunden.
3. **IONOS-Domain im Paket:** Tooltip sagt „für 1 Jahr kostenlos“, FAQ sagt „dauerhaft inklusive“. Das widerspricht sich.
4. **SSL-Typ:** IONOS „DV Wildcard“, ALL-INKL Let's Encrypt; bei STRATO ist nicht angegeben, welches Zertifikat im Paket steckt.
5. **STRATO WordPress:** Mindestvertragslaufzeit und Abrechnungszeitraum stehen nicht als Text auf der Seite (nur der Umschalter „1 Monat / 12 Monate“).
6. **ALL-INKL Privat:** SSL kostet 0,95 €/Monat extra. Ob das schon im Gratismonat anfällt: nicht gefunden.
7. Aktionspreise gelten laut IONOS „nur für begrenzte Zeit“. Vor dem Veröffentlichen erneut prüfen.
