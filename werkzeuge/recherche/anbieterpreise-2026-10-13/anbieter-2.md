# Hosting-Preise Deutschland – Hetzner, netcup, Raidboxes, mittwald

- Abruf aller Quellen: **13.10.2026** (curl bzw. Playwright/Chromium, wo Preise erst per JavaScript geladen werden).
- Rohdaten: `a2roh/` im selben Ordner.
- „berechnet“ = eigene Umrechnung (19 % USt.), steht so nicht auf der Seite.
- „nicht gefunden“ = auf den abgerufenen Seiten nicht belegt.
- Auswahlregel: „günstigstes Paket“ = günstigster Tarif, der laut Anbieter WordPress kann. Wenn der Anbieter einen höheren Tarif ausdrücklich für Firmen empfiehlt, steht das bei den Unsicherheiten.

---

## 1. Hetzner (Webhosting, konsoleH)

| Angabe | Webhosting S (günstigstes) | Webhosting M (Stufe darüber) |
|---|---|---|
| Preis regulär | 1,90 € max./Monat **brutto** (netto 1,60 €) [H1, H2] | 4,90 € max./Monat **brutto** (netto 4,12 €) [H1, H2] |
| Aktion | Einrichtung 0,00 € statt 9,90 € (durchgestrichen) [H1] | Einrichtung 0,00 € statt 4,90 € (durchgestrichen) [H1] |
| Abrechnung | Monatsdeckel „max/mo.“, dazu Stundenpreis 0,0031 €/Std. [H1] | „max/mo.“, 0,0079 €/Std. [H1] |
| Mindestlaufzeit | „Keine Mindestlaufzeit“ [H1] | wie S [H1] |
| Einrichtungsgebühr | derzeit 0,00 € (regulär 9,90 € brutto / 8,32 € netto) [H1] | derzeit 0,00 € (regulär 4,90 €) [H1] |
| Domain inklusive? | **Nein** [H1] | Nein [H1] |
| E-Mail inklusive? | Ja, „unbegrenzt Mailboxen“ [H1] | Ja [H1] |
| SSL inklusive? | Ja, kostenlose Let's-Encrypt- und Basic-Zertifikate [H4] | Ja [H4] |
| WordPress | „One-Click-WordPress Installer“; 1 Datenbank, 10 GB, 2 PHP-Prozesse [H1] | 5 Datenbanken, 50 GB, 5 PHP-Prozesse [H1] |
| Brutto/Netto | brutto, „inkl. 19 % USt.“ [H1] | brutto [H1] |

- **Domain .de:** 5,83 € pro Jahr, brutto (netto 4,90 €, laut Preis-API) [H3, H2]. Einrichtungsgebühr für Domains: **nicht gefunden**. Domains, die woanders registriert sind, kosten 0,76 € pro Monat [H1].
- **Serverstandort:** nur Nürnberg [H1].
- **AVV:** ja, als Muster. Man schließt ihn im Kundenkonto ab: https://accounts.hetzner.com/account/dpa, PDF: https://www.hetzner.com/AV/DPA_de.pdf [H5]
- Zusatzinfo: Webhosting L kostet 9,90 € brutto pro Monat (netto 8,32 €). Hetzner nennt ihn „Für kleinere Unternehmen“ [H1, H2].
- **Unsicher:**
  - Wie lange die Einrichtungs-Aktion läuft, steht nicht auf der Seite.
  - „max/mo.“ plus Stundenpreis deutet auf Abrechnung nach Stunden mit einer Monatsobergrenze hin. Ein ausdrücklicher Satz dazu wurde nicht gefunden.

## 2. netcup (Webhosting, Standort wählbar)

| Angabe | Webhosting 1000 (günstigstes) | Webhosting 2000 (Stufe darüber) |
|---|---|---|
| Preis | 2,69 € pro Monat **brutto** (netto ca. 2,26 € – berechnet) [N1, N2] | 4,03 € pro Monat **brutto** (netto ca. 3,39 € – berechnet) [N1, N3] |
| Aktion | keine; Preise gelten „über die gesamte Laufzeit“ [N1] | keine [N1] |
| Abrechnungsperiode | 12 Monate (also 32,28 € pro Jahr brutto – berechnet) [N2] | 12 Monate (48,36 € pro Jahr brutto – berechnet) [N3] |
| Mindestvertragslaufzeit | 12 Monate [N2] | 12 Monate [N3] |
| Einrichtungsgebühr | 0,00 € [N2] | 0,00 € [N3] |
| Domain inklusive? | Ja, 1 .de-Domain [N2] | Ja, 3 .de-Domains [N3] |
| E-Mail inklusive? | Ja, 100 Adressen [N2] | Ja, 500 Adressen [N3] |
| SSL inklusive? | Ja, „Kostenlose SSL-Zertifikate: unbegrenzt“ (Let's Encrypt) [N1, N2] | Ja [N3] |
| WordPress | App-Installer, WordPress-Toolkit; 1 Datenbank [N2] | 10 Datenbanken, 4096 MB garantierter RAM [N3] |
| Brutto/Netto | brutto „(inkl. 19% MwSt.)“ [N1] | brutto [N1] |

- **Domain .de, zusätzlich gebucht:**
  - 0,42 € pro Monat brutto (5,04 € pro Jahr – berechnet).
  - Einrichtung 0,00 €.
  - Mindestlaufzeit und Abrechnung je 12 Monate [N4].
- **Kündigung:**
  - Verträge laufen auf unbestimmte Zeit.
  - Kündbar mit einem Monat Frist zum Monatsende, frühestens zum Ende der Mindestlaufzeit [N5].
- **Serverstandort:** wählbar zwischen Nürnberg (Deutschland), Wien (Österreich) und Manassas (USA). Voreingestellt ist Nürnberg [N2].
- **AVV:**
  - Ja, kostenlos über den Vertragsgenerator.
  - Abschluss im CCP unter „Stammdaten“ → „Auftragsverarbeitung“.
  - Erklärung dazu: https://www.netcup.com/de/helpcenter/dokumentation/general/avv [N6]
- **Unsicher:** Der Speicherplatz widerspricht sich.
  - Übersicht: WH 1000 hat „50 GB“, WH 2000 „150 GB“ [N1].
  - Detailseite (Standort Nürnberg): 25 GB bzw. 75 GB [N2, N3].
  - WH 1000 beschreibt netcup als „kleine, private Webseite“. WH 2000 heißt „Ideal für Ihren Blog oder den Webauftritt Ihrer Firma“ [N1, N3].

## 3. Raidboxes (Managed WordPress)

| Angabe | Mini (günstigstes) | Starter (Stufe darüber) |
|---|---|---|
| Preis monatlich | 18,00 € pro Monat **netto** (21,42 € brutto – berechnet) [R1] | 24,00 € pro Monat netto (28,56 € brutto – berechnet) [R1] |
| Bei jährlicher Zahlung | 16,20 € pro Monat netto, „10% Rabatt“ (194,40 € pro Jahr netto – berechnet) [R1] | 21,60 € pro Monat netto (259,20 € pro Jahr netto – berechnet) [R1] |
| Aktion | keine; nur 10 % Rabatt bei jährlicher Zahlung [R1] | wie Mini |
| Abrechnungszeitraum | monatlich oder jährlich, wählbar [R1] | wie Mini |
| Mindestvertragslaufzeit | laut AGB in der „Leistungsbeschreibung“ geregelt; verlängert sich um den gewählten Abrechnungszeitraum; Unternehmer sind für diesen Zeitraum gebunden [R4] | wie Mini |
| Einrichtungsgebühr | **nicht gefunden** | nicht gefunden |
| Domain inklusive? | Nein, „Domain & E-Mail zusätzl. buchbar“ [R1] | Nein [R1] |
| E-Mail inklusive? | Nein; Mail Mini kostet 3,00 € pro Monat netto für 3 Postfächer [R1, R3] | Nein |
| SSL inklusive? | Ja, kostenloses Let's-Encrypt-Zertifikat für alle Boxen [R1] | Ja |
| Leistung | 1 vCore, 2 GB RAM, 5 GB SSD, 128 MB PHP Memory Limit [R1] | 2 vCores, 4 GB RAM, 10 GB SSD, bis 1024 MB PHP [R1] |
| Brutto/Netto | **netto**, „Alle Preise zzgl. 19% MwSt.“ [R1] | netto |

- **Domain .de:** 1,50 € pro Monat netto bei jährlicher Zahlung (18,00 € pro Jahr netto, 21,42 € brutto – berechnet) [R2]. Einrichtungsgebühr für die Domain: **nicht gefunden**.
- **Serverstandort:** „Serverstandort Deutschland“ [R1].
- **AVV:**
  - Ja, online abschließbar.
  - Er gilt für alle Websites eines Kontos [R1, R5].
  - Anleitung im Helpcenter: https://helpcenter.raidboxes.de/de/articles/1947634-auftragsverarbeitungsvertrag-av. Die Adresse steht auf der Preisseite verlinkt; die Seite selbst war von hier aus gesperrt (Proxy) und wurde nicht gelesen.
- **Unsicher:**
  - Mini ist laut Raidboxes „Geeignet für kleine statische Websites oder einfache Blogs“. Starter ist „Geeignet für kleinere bis mittlere WordPress Websites“. Für eine Firmenwebsite ist Starter wohl der realistische Einstieg.
  - Die genaue Mindestlaufzeit steht in der „Leistungsbeschreibung“, die nicht eingesehen wurde.

## 4. mittwald (Webhosting im mStudio)

| Angabe | Webhosting S (günstigstes) | Webhosting M (Stufe darüber) |
|---|---|---|
| Preis | 13 € pro Monat **netto** (15,47 € brutto – berechnet) [M1] | 19 € pro Monat netto (22,61 € brutto – berechnet) [M1] |
| Aktion | keine gefunden; kostenloser Start möglich („Jetzt kostenlos loslegen“) [M1] | wie S |
| Abrechnungszeitraum | frei wählbar: 1, 3, 6 oder 12 Monate [M1] | wie S |
| Vertragslaufzeit | 1 Monat; verlängert sich automatisch; Kündigungsfrist 30 Tage zum Laufzeitende [M1] | wie S |
| Einrichtungsgebühr | 0,00 EUR [M1] | 0,00 EUR [M1] |
| Domain inklusive? | Nein; Domains „über uns registrieren“, kein Inklusiv-Hinweis gefunden [M1, M2] | Nein |
| E-Mail inklusive? | Ja, Postfächer unbegrenzt bis zum gebuchten Speicherplatz [M1] | Ja |
| SSL inklusive? | Ja, „Let's Encrypt Flatrate“; eigene externe Zertifikate optional für 4,90 € pro Monat [M1] | Ja |
| Leistung | 1 vCPU, 1 GiB RAM, 20 GiB; WordPress als „managed App“ [M1] | 1 vCPU, 2 GiB RAM, 40 GiB [M1] |
| Brutto/Netto | **netto**, „Alle Preise zzgl. gesetzlicher Umsatzsteuer“; nur für Gewerbetreibende [M1] | netto |

- **Domain .de:** 0,89 € pro Monat netto (10,68 € pro Jahr netto, 12,71 € brutto – berechnet) [M2].
  - Einmalige Einrichtungsgebühr 2,99 € netto (3,56 € brutto – berechnet).
  - Mindestlaufzeit 1 Jahr, Abrechnung jährlich im Voraus [M2].
- **Serverstandort:** eigenes Rechenzentrum in Espelkamp, dazu Flächen in Frankfurt und Hannover [M1].
- **AVV:**
  - Ja, Abschluss im Kundencenter unter „Vertragsdaten“.
  - Erklärung: https://www.mittwald.de/faq/service-informationen/faq/datenschutz-alles-wichtige-zur-dsgvo [M3]. Dazu gibt es einen „AV Manager“ (FAQ-Seite in der Sitemap, nicht gelesen).
- **Unsicher:**
  - S heißt bei mittwald „für Web-Visitenkarten oder persönliche Blogs“. M heißt „für Vereinsseiten oder kleinere Unternehmensseiten“ [M1].
  - Vertragslaufzeit (1 Monat) und Einrichtungsgebühr (0,00 EUR) stehen in der Tariftabelle, in der Werte und Bezeichnungen getrennt aufgeführt sind. Die Zuordnung habe ich aus der Reihenfolge abgeleitet. Sie passt zur Werbeaussage „1 Monat Kündigungsfrist“ [M1].
  - Die Preise sind „Beispielkonfigurationen“; der Tarif lässt sich frei zusammenstellen.

---

## Belegliste (alle abgerufen am 13.10.2026)

### Hetzner
- **[H1]** https://www.hetzner.com/de/webhosting/ (mit Playwright gerendert)
  - „Webhosting S | startet ab | € 1,90 max/mo. | 0,0031 € /std | inkl. 19 % USt. | Setup einmalig 9,90 € € 0.00“ (9,90 € im HTML mit Klasse `product-setup-label-strike`, also durchgestrichen)
  - „Webhosting M | startet ab | € 4,90 max/mo. | 0,0079 € /std | inkl. 19 % USt. | Setup einmalig 4,90 € € 0.00“
  - „Keine Mindestlaufzeit“
  - „Webhosting-Pakete enthalten keine Domain. Diese muss zusätzlich gebucht werden …“
  - „Domainregistrierung ab 5,83 € /Jahr“
  - „unbegrenzt Mailboxen“ · „One-Click-WordPress Installer“
  - „Unsere Webhosting-Pakete laufen ausschließlich auf Servern in unseren eigenen Rechenzentren in unserem Datacenter-Park in Nürnberg.“
  - „Die Nutzung von Domains, die außerhalb von Hetzner gebucht wurden, kostet 0,76€ monatlich (inkl. 19% USt.) je Domain.“
  - „Webhosting L … Für kleinere Unternehmen … € 9,90 max/mo.“
- **[H2]** https://website-price-api.hetzner.com/api/v1/products/KONSOLEH_13933 (…13934, …13935) und …/views/nav_prices – diese Schnittstelle (API) lädt die Seite
  - `"monthly":{"EUR":"1.60"}`, `"setup":{"EUR":"0.00"}` (S)
  - `"monthly":{"EUR":"4.12"}` (M)
  - `"monthly":{"EUR":"8.32"}` (L)
  - Domain: `"dataKey": "10006", "prices": {"domain": {"EUR": "4.90"}`
- **[H3]** https://www.hetzner.com/de/domainregistration/ (leitet weiter auf /de/whois/, gerendert): „.de € 5.83 pro Jahr“. Zum Vergleich: https://docs.hetzner.com/de/managed/domain-and-dns/domain-price-adjustments-konsoleh/ nennt Domainpreise mit „(inkl. 19% USt.)“.
- **[H4]** https://docs.hetzner.com/de/managed/ssl/certificates/ (zuletzt geändert 2026-10-12):
  - „Basic-Zertifikat | DigiCert | kostenlos“ · „Let's-Encrypt-Zertifikat | … | kostenlos“
  - Dazu https://docs.hetzner.com/de/managed/ssl/general-information/: „Hetzner bietet kostenlose Basic-Zertifikate von DigiCert, kostenlose Let's-Encrypt-Zertifikate und kostenpflichtige Business-Zertifikate von Thawte an.“
- **[H5]** https://docs.hetzner.com/de/general/general-terms-and-conditions/data-privacy-faq/ (leitet weiter auf …/company-and-policy/data-protection-at-hetzner/):
  - „Der AV-Vertrag (AVV) regelt die Rechte und Pflichten zwischen dir als Verantwortlichem und Hetzner als Auftragsverarbeiter (Art. 28 DSGVO).“
  - „Den AV-Vertrag kannst du direkt in deinem Kundenaccount abschließen: https://accounts.hetzner.com/account/dpa“

### netcup
- **[N1]** https://www.netcup.com/de/hosting
  - „Webhosting 1000 … 1 .de-Domain oder 1 Alternativdomain* inklusive | 50 GB SSD Speicherplatz | SSL-Zertifikate inklusive | pro Monat 2,69 € (inkl. 19% MwSt.)“
  - „Webhosting 2000 … 3 .de-Domains … | 150 GB SSD Speicherplatz | … Wordpress-Toolkit inklusive | pro Monat 4,03 € (inkl. 19% MwSt.)“
  - „Kostenlose SSL-Zertifikate für alle Domains und Subdomains via Let's Encrypt“
  - „Die Preise unsere Webhosting Pakete sind über die gesamte Laufzeit gültig und nicht nur für die ersten Monate“
- **[N2]** https://www.netcup.com/de/hosting/webhosting/webhosting-1000-nue
  - „Einrichtungsgebühr 0,00 € (inkl. 19% MwSt.) | Mindestvertragslaufzeit 12 Monate | Abrechnungsperiode 12 Monate“
  - „Web-Speicherplatz 25 GB SSD | Server Standort Nürnberg, Deutschland | Inklusivdomain 1 .de Domain | Datenbanken 1“
  - „Kostenlose SSL-Zertifikate unbegrenzt“ · „E-Mail Adressen 100“ · „Wordpress-Toolkit Ja“
  - „Standort: Manassas, USA … Wien, Österreich … Nürnberg, Deutschland“
- **[N3]** https://www.netcup.com/de/hosting/webhosting/webhosting-2000-nue
  - „Ideal für Ihren Blog oder den Webauftritt Ihrer Firma“
  - „Einrichtungsgebühr 0,00 € (inkl. 19% MwSt.) | Mindestvertragslaufzeit 12 Monate | Abrechnungsperiode 12 Monate“
  - „Web-Speicherplatz 75 GB SSD“ · „Datenbanken 10“ · „Garantiert nutzbarer RAM 4096 MB“ · „E-Mail Adressen 500“
  - „4,03 € pro Monat (inkl. 19% MwSt.)“
- **[N4]** https://www.netcup.com/de/domain/zusaetzliche-domain-de
  - „Domain .de … Einrichtungsgebühr 0,00 € (inkl. 19% MwSt.) | Mindestvertragslaufzeit 12 Monate | Abrechnungsperiode 12 Monate“
  - „0,42 € pro Monat (inkl. 19% MwSt.)“
- **[N5]** https://www.netcup.com/de/agb, Nr. 6: „Soweit nicht anders vereinbart, werden Verträge auf unbestimmte Zeit geschlossen. Solche Verträge sind von beiden Parteien mit einer Frist von einem Monat zum Monatsende kündbar, frühestens jedoch zum Ablauf einer vertraglich vereinbarten Mindestlaufzeit.“
- **[N6]** https://www.netcup.com/de/helpcenter/dokumentation/general/avv
  - „Wenn unser bereitgestellter Vertragsgenerator genutzt wird, fallen hierfür keine zusätzlichen Gebühren an.“
  - „… im Customer Control Panel (CCP) in den Menüpunkt Stammdaten. Wechsle in die Registerkarte Auftragsverarbeitung und klicke auf AV-Vertrag erstellen.“

### Raidboxes
- **[R1]** https://raidboxes.io/wordpress-hosting-pricing/ (gerendert; Umschalter „Monatlich“ per Playwright geklickt)
  - „Mini | Geeignet für kleine statische Websites oder einfache Blogs. | statt 18,00 € | 10 % Rabatt | 16,20 € pro Monat“
  - Bei Umschalter „Monatlich“: „Mini … 18,00 € pro Monat“ · „Starter 24,00 €/Monat“
  - „Starter … Geeignet für kleinere bis mittlere WordPress Websites oder Blogs. | statt 24,00 € | … 21,60 € pro Monat“
  - „Alle Preise zzgl. 19% MwSt.“ · „Domain & E-Mail zusätzl. buchbar“
  - „Bei Raidboxes ist SSL standardmäßig für alle Boxen aktiviert. Deine Website wird automatisch mit einem kostenlosen Let’s Encrypt Zertifikat geschützt.“
  - „Serverstandort Deutschland“
  - „… solltest du einen Auftragsverarbeitungsvertrag (AVV, früher ADV) mit uns schließen. Dieser gilt für alle deine Webseiten …“
  - „Du kannst bei all unseren WordPress Hosting Tarifen wählen, ob du monatlich oder jährlich (mit 10 % Rabatt) bezahlen möchtest.“
  - „Zusätzlich buchbar (Preis pro Monat) … Domain ab 1,50 € … E-Mail Postfach ab 3,00 €“
- **[R2]** https://raidboxes.io/domains/ (gerendert): „de 1,50 * … *Monatlicher Nettopreis bei jährlicher Zahlung“ · „zzgl. 19 % MwSt bei jährlicher Zahlung“
- **[R3]** https://raidboxes.io/email-hosting/ (gerendert): „Mail Mini 3,00 € pro Monat … 3 Postfächer 3 GB Mailspeicher“ · „Alle Preise zzgl. 19 % MwSt.“
- **[R4]** https://raidboxes.io/legal/terms/, § 12:
  - „Die Vertragslaufzeit ergibt sich jeweils aus der im Zeitpunkt des Vertragsschlusses geltenden Leistungsbeschreibung.“
  - „Ohne Kündigung verlängert sich die anfängliche Laufzeit an ihrem Ende automatisch um den ausgewählten Abrechnungszeitraum. … Unternehmer sind für die Dauer des gewählten Abrechnungszeitraums an den Vertrag gebunden.“
- **[R5]** https://raidboxes.io/legal/privacy/, Nr. 22: „… ermöglichen dir, einen Vertrag zur Auftragsverarbeitung (AVV) online mit uns zu schließen“

### mittwald
- **[M1]** https://www.mittwald.de/webhosting
  - „Webhosting S für Web-Visitenkarten oder persönliche Blogs 13 € pro Monat zzgl. USt.*“
  - „Webhosting M für Vereinsseiten oder kleinere Unternehmensseiten 19 € pro Monat zzgl. USt.*“
  - „* Angebote richten sich ausschließlich an Gewerbetreibende. Alle Preise zzgl. gesetzlicher Umsatzsteuer.“
  - Tariftabelle: „frei wählbar (1-, 3-, 6- oder 12-monatlich) | 1 Monat | 0,00 EUR“
  - „Die Kündigungsfrist beträgt 30 Tage zum jeweiligen Laufzeitende.“
  - „Let's Encrypt Flatrate | optional: Einbinden von externen Zertifikaten (4,90 € mtl.)“
  - „Die Anzahl von E-Mail-Adressen und -Postfächern sowie die Postfachgröße sind unbegrenzt (bis der gebuchte Speicherplatz deines Webhostings voll ist).“
  - „Mit unserem eigenen Rechenzentrum am Standort Espelkamp und weiteren Flächen in Frankfurt und Hannover …“
  - „Als managed Apps kannst du WordPress, … betreiben.“
- **[M2]** https://www.mittwald.de/produkte/domains (gerendert)
  - „TLD | Monatlicher Preis | .de | 0,89 €“
  - „Für jede Domain fällt einmalig eine Einrichtungsgebühr von 2,99 € an.“
  - „* Alle genannten Preise verstehen sich pro Monat, zzgl. 19% MwSt. und einer einmaligen Einrichtungsgebühr. Die Mindestlaufzeit aller Domains beträgt ein Jahr und die Abrechnung erfolgt jährlich im Voraus.“
- **[M3]** https://www.mittwald.de/faq/service-informationen/faq/datenschutz-alles-wichtige-zur-dsgvo: „Einen AV-Vertrag kannst du direkt in deinem Kundencenter unter „Vertragsdaten“ abschließen.“
