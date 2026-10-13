# Preise und Datenschutz-Angaben: Kadence, Webflow, Wix, Jimdo

Abruf aller Quellen: 13.10.2026 (aus einer Cloud-Umgebung; der Standort der Abfrage wurde von Wix und Jimdo als **USA** erkannt – siehe Hinweise je Anbieter).
Rohdaten (HTML, gerenderter Text, JSON) liegen in `preise/roh/`.

---

## 1. Kadence (kadencewp.com)

| Paket | Preis | Währung | Websites | Verlängerung |
|---|---|---|---|---|
| alle | **nicht gefunden** | – | nicht gefunden | nicht gefunden |

- `https://www.kadencewp.com/pricing/` leitet (HTTP 301) weiter auf `https://www.liquidweb.com/software/kadence/#pricing`. Auch `/kadence-theme/`, `/kadence-blocks/`, `/frequently-asked-questions/`, `/terms-and-conditions/` leiten auf liquidweb.com weiter; `/help-center/` auf `docs.nexcess.com`.
- liquidweb.com ist aus dieser Umgebung gesperrt (Proxy: „connect_rejected“). Paketnamen, Preise, Website-Anzahl und Verlängerung konnten deshalb **nicht** erhoben werden.
- Einziger Beleg zur Währung, Fußzeile von `https://www.kadencewp.com/kadence-theme/design-collective/pro-template-subscription/`: „© 2026 Kadence WP | All prices are in USD“.
- Menü derselben Seite nennt als Produktkategorien u. a. „Premium Plans – Get all the tools you need in one plan“, „Kadence Theme“, „Kadence Blocks“, „Kadence Shop Kit“, „Kadence Conversions“, „Kadence Insights“ (keine Preise).
- **Nachholen:** Preisseite `https://www.liquidweb.com/software/kadence/#pricing` von einem normalen Rechner aus öffnen.

---

## 2. Webflow (webflow.com/pricing)

Hinweis auf der Seite: „All prices in USD, per site, plus applicable taxes added at checkout.“ Umschalter: „Monthly“ / „Yearly (Save up to 40%)“. Auch mit deutscher Browser-Sprache (de-DE) wurde **US-Dollar** angezeigt.

| Site-Plan | jährliche Zahlung (pro Monat) | monatliche Zahlung | Währung | Enthalten (laut Seite) |
|---|---|---|---|---|
| Starter | Free | Free | – | „Webflow.io domain“, „Limited Webflow CMS“, „2 static pages“, „1 GB bandwidth“, „50 form submissions“; CMS items: 50 |
| Basic | $15 /mo, „billed yearly“ | $25 /mo, „billed monthly“ | USD, zzgl. Steuern | „Custom domain“, „300 static pages“, „10 GB bandwidth“, „Unlimited form submissions“, „Password protection“; „For simple sites that don't need a CMS.“; CMS items: „—“ |
| Premium (als „New“ markiert) | $25 /mo, „billed yearly“ | $39 /mo, „billed monthly“ | USD, zzgl. Steuern | „Everything in Basic, plus: Webflow CMS“, Bandbreite ab „50 GB“ (wählbar bis 2,5 TB gegen Aufpreis), „Code components“, „Site search“, „Form file upload“; CMS items: „20,000“ |
| Team (Platform plan) | $2,500 /mo | – | USD | „Annual contract required“, „Talk to us“ |
| Enterprise | „Talk to us“ | – | – | – |

- Bandbreiten-Aufpreis Premium (Auswahlfeld „bandwidth“, Werte aus der Seite): 100 GB +20, 150 GB +40, 200 GB +60, 300 GB +100 … 2,5 TB +974 USD/Monat (jährlich); Bandbreiten-Zusatz-Tabelle: „+50 GB … +$20 /month, billed annually … +$30 /month, billed monthly“.
- **Unsicher:** In der Vergleichstabelle heißt die dritte Spalte „Premier“ statt „Premium“; die Zahl „20,000“ CMS items steht in dieser Spalte. Die alten Namen „CMS“/„Business“ tauchen nur noch in internen Attributen auf („Business Site Plan - Bandwidth“), nicht als Plannamen.
- Ob für Deutschland Euro-Preise angezeigt werden: **nicht gefunden** (Seite sagt ausdrücklich USD).

**Hosting/Serverstandort und DPA (Webflow)**
- DPA vorhanden: `https://webflow.com/legal/dpa` – „Effective date: November 15, 2023“; „This Webflow Data Processing Addendum (this "DPA") forms part of, and is subject to the provisions of, the Agreement.“; „If you would like to execute a DocuSigned version of this Data Processing Addendum, please review and sign our pre-signed DPA here.“
- Übermittlung: Rangfolge „(a) the EU-U.S. and Swiss-U.S. Data Privacy Framework … (b) the EU Standard Contractual Clauses …“ (gleiche Seite).
- Rechenzentren: „Webflow infrastructure is managed via Amazon Web Services’ ISO 27001 certified data centers, and hosted in multiple regions and availability zones.“ (gleiche Seite). Eine wählbare EU-Region: **nicht gefunden**.
- Unterauftragsverarbeiter `https://webflow.com/legal/subprocessors` („Last updated: July 9, 2026“): „Amazon Web Services, Inc. Cloud services, hosting, and translation services USA“; „Cloudflare, Inc. Content delivery network USA“.

---

## 3. Wix (de.wix.com)

`https://de.wix.com/upgrade/website` → leitet weiter auf `https://de.wix.com/pricing`. Die Preise werden dort nur per JavaScript von `static.parastorage.com` geladen; dieser Server ist hier gesperrt. Die Seite meldet im eingebetteten Datenblock `"geo":"US"`. **Paketpreise für Deutschland: nicht gefunden.**

| Paket (Name von www.wix.com/plans, englisch) | Preis Deutschland | Enthalten (laut englischer Seite) |
|---|---|---|
| Light | nicht gefunden | „Free domain for 1 year“, „2 GB storage space“, „2 site collaborators“ |
| Core | nicht gefunden | „Free domain for 1 year“, „50 GB storage space“, „Accept payments“, „5 site collaborators“ |
| Business („RECOMMENDED“) | nicht gefunden | „Free domain for 1 year“, „100 GB storage space“, „10 site collaborators“ |
| Business Elite | nicht gefunden | „Free domain for 1 year“, „Unlimited storage space“, „100 site collaborators“ |
| Free | $0 | „Reliable web hosting“ |

- Alle Pakete laut `https://www.wix.com/plans`: „All plans include: Custom domain Reliable web hosting AI creation tools 24/7 customer care 14-day money-back guarantee“.
- Preishinweis derselben Seite: „Prices and currency vary by location. USD prices displayed for reference only. Displayed prices are for yearly subscriptions, paid in full at the time of purchase. Additional subscription periods are available. Prices do not include applicable taxes, which are determined according to your billing address.“
- **Unsicher / nicht verwenden:** Im Server-HTML von www.wix.com/plans stehen Platzhalter wie „$ 17 .77 mo … Price includes GST“ – offensichtlich keine deutschen Preise.
- Einziger deutscher Preisbeleg, `https://de.wix.com/domain/kaufen` (weitergeleitet von `/domain/names`): „Bei Wix erhältst du eine kostenlose Domain mit Gutschein für ein Jahr, wenn du zum ersten Mal ein jährliches Premiumpaket ab 16,66 € im Monat erwirbst.“ und „Eine .de-Domain bekommst du ab 14,95 €, eine .com-Domain ab 19,35 € für das erste Jahr“. Ob mit/ohne MwSt.: auf dieser Stelle nicht angegeben.
- `https://de.wix.com/hosting`: „Außerdem erhältst du eine kostenlose Domain für ein Jahr mit ausgewählten Website-Paketen.“

**Serverstandort und DPA (Wix)**
- Hosting, `https://de.wix.com/hosting`: „Multi-Cloud-Hosting Sei immer verfügbar mit weltweiten Datenzentren unterstützt durch Google Cloud, AWS, Fastly und Wix.“ Ein fester Serverstandort in der EU: **nicht gefunden**.
- DPA („NDV“), `https://de.wix.com/about/privacy-dpa-users`: „Nachtrag betreffend die Datenverarbeitung - Nutzer Datum des Inkrafttretens: 27. September 2021“; „Dieser NDV stellt einen wesentlichen Bestandteil der Nutzungsbedingungen von Wix … dar“ (also Teil der Nutzungsbedingungen, kein gesonderter Abschluss nötig – Auslegung, **unsicher**).
- Datenschutzrichtlinie `https://de.wix.com/about/privacy` („Gültig ab dem 18. Juni 2026“): „Die Verarbeitung der personenbezogenen Daten der Nutzer von Nutzern erfolgt im Hoheitsgebiet der Europäischen Union, Israels oder in einem Drittland, … für das die Europäische Kommission entschieden hat, dass es ein angemessenes Schutzniveau gewährleistet“; „Wix und seine verbundenen Unternehmen … sind konform mit dem Datenschutzrahmen („Data Privacy Framework“, „DPF“)“; „Die personenbezogenen Daten der Nutzer werden von Wix.com Ltd. in Israel kontrolliert“.

---

## 4. Jimdo (jimdo.com/de/preise)

`https://www.jimdo.com/de/preise/` → `https://www.jimdo.com/de/preise/website/`. Die Preise lädt die Seite aus der Schnittstelle `https://api.e.jimdo.com/o2c-backend/api/v1/product-catalog?country=…`. Aus dieser Umgebung fragte die Seite selbst `country=US` ab und zeigte Dollar (z. B. Grow „17 $“). Für Deutschland wurde dieselbe Schnittstelle mit `country=DE&language=de&group=DOLPHIN&includeFreePackage=true` abgerufen; die damit gerenderte Seite zeigt:

„Preise für Vertragslaufzeit von 12 Monaten. Preise für andere Vertragslaufzeiten können abweichen. Alle Preise inklusive MwSt.“

| Paket | 1 Monat (monatlich zahlbar) | 12 Monate: pro Monat / gesamt | 24 Monate: pro Monat / gesamt | Speicher | Domain | E-Mail | Unterseiten |
|---|---|---|---|---|---|---|---|
| Free | 0 € | 0 € | – | 5 GB | „.jimdosite.com Subdomain“ | – | 5 |
| Start | 18 € | 12 € / 144 € | 10 € / 240 € | 30 GB | „Kostenlose Website-Adresse für die erste Vertragslaufzeit“ | „E-Mail-Adresse verbinden“, 1 Weiterleitung | 10 |
| Grow („BELIEBTESTE OPTION“) | 29 € | 20 € / 240 € | 17 € / 408 € | 50 GB | ja (erste Laufzeit) | verbinden, 5 Weiterleitungen | 50 |
| Grow Legal | 41 € | 29 € / 348 € | 26 € / 624 € | 50 GB | ja (erste Laufzeit) | verbinden, 5 Weiterleitungen | 50; + „Abmahnsichere Rechtstexte“ |
| Unlimited | 74 € | 50 € / 600 € | 43 € / 1.032 € | 500 GB | ja (erste Laufzeit) | verbinden, 20 Weiterleitungen | „Unbegrenzt“ |

- Alle Werte in EUR, brutto mit 19 % MwSt. (JSON-Felder `"currency": "EUR"`, `"taxRate": 19.0`; z. B. Grow 12 Monate: `"total": 240.0, "subtotal": 201.68, "tax": 38.32`).
- Zusätzlich im Katalog (nicht auf der Website-Preisseite sichtbar): „Start Legal“ 30 € / 21 € / 19 € (1/12/24 Monate pro Monat); Shop-Pakete „Basic“, „Business“, „VIP“.
- Domain: „Beim Kauf eines Jimdo Pakets gewähren wir einen Rabatt für die erste Vertragslaufzeit, der den Kosten einer Domain entspricht. Dieses Angebot gilt für die folgenden Domains: de, com, net, org, info, at, ch, es, it, fr, nl. … Bei der Verlängerung wird der gewählte Plan zum vollen Preis bzw. ohne den Rabatt, verlängert.“ (Katalog-Text zu „Kostenlose Website-Adresse für die erste Vertragslaufzeit“). Domain-Rabatt im JSON: 26 € (12 Monate), 52 € (24 Monate), 3 € (1 Monat).
- E-Postfach: Ein eigenes **Postfach wird nicht genannt**; genannt sind nur „E-Mail-Adresse verbinden“ und „E-Mail-Weiterleitungen“.
- Laufzeit (FAQ der Preisseite): „Du kannst entweder monatlich zahlen oder direkt für eine Laufzeit von 12 oder 24 Monaten bezahlen und damit Geld sparen.“
- **Unsicher:** Die Euro-Werte stammen aus Jimdos eigener Preis-Schnittstelle mit Länderangabe DE (in die Seite eingespielt), nicht aus einem Abruf mit deutscher IP-Adresse. Die Spalten „Website“-Vergleichstabelle (z. B. „Datei-Uploads in Smart Forms“ bei Start) bitte vor Veröffentlichung an einem Rechner in Deutschland gegenprüfen.

**Serverstandort und AVV (Jimdo)**
- Unterauftragnehmer, `https://legal.jimdo.com/hc/de/articles/4414660225172-Jimdo-Informationen-zu-Unterauftragnehmern`: „Amazon Web Services EMEA SARL Dienst: Webhosting und Infrastruktur Unternehmenssitz: EU Ort der Datenverarbeitung: EU“; „Cloudflare Dienst: Webhosting und Infrastruktur Unternehmenssitz: USA Ort der Datenverarbeitung: Weltweit … Standardvertragsklauseln (SCCs) und/oder EU-U.S. Data Privacy Framework“.
- AVV: dieselbe Seite: „Wie in unserem Auftragsverarbeitungsvertrag beschrieben, haben Kund:innen das Recht, solchen Änderungen zu widersprechen.“ Den AVV-Text selbst bzw. wie man ihn abschließt: **nicht gefunden** (`/de/info/auftragsverarbeitung/` und `/de/info/avv/` = 404).
- Produkt-Datenschutzhinweise: `https://legal.jimdo.com/hc/de/articles/20331833326612-Jimdo-Produkt-Datenschutzhinweise` („Aktueller Stand: 1. Oktober 2026“).
- Anbieter: „Jimdo GmbH“; Fußzeile: „Made in Hamburg since 2007“.

---

## Belegliste (alle abgerufen am 13.10.2026)

| # | URL | Wörtliches Zitat |
|---|---|---|
| K1 | https://www.kadencewp.com/pricing/ | HTTP 301 → „location: https://www.liquidweb.com/software/kadence/#pricing“ |
| K2 | https://www.kadencewp.com/kadence-theme/design-collective/pro-template-subscription/ | „© 2026 Kadence WP \| All prices are in USD“ |
| W1 | https://webflow.com/pricing | „Basic … For simple sites that don't need a CMS. $ 15 /mo billed yearly … Custom domain 300 static pages 10 GB bandwidth“ |
| W2 | https://webflow.com/pricing (Umschalter „Monthly“, Playwright) | „Basic … $ 25 /mo billed monthly“; „Premium … $ 39 /mo billed monthly“ |
| W3 | https://webflow.com/pricing | „Premium For content-rich sites with robust CMS and traffic needs. New $ 25 /mo billed yearly … Everything in Basic, plus: Webflow CMS“ |
| W4 | https://webflow.com/pricing | „All prices in USD, per site, plus applicable taxes added at checkout.“ |
| W5 | https://webflow.com/pricing | „CMS items … 50 \| — \| 20,000“ (Spalten „Starter \| Basic \| Premier“) |
| W6 | https://webflow.com/pricing | „Team … $ 2500 /mo Annual contract required“ |
| W7 | https://webflow.com/legal/dpa | „Effective date: November 15, 2023“; „This Webflow Data Processing Addendum (this "DPA") forms part of … the Agreement.“ |
| W8 | https://webflow.com/legal/dpa | „managed via Amazon Web Services’ ISO 27001 certified data centers, and hosted in multiple regions and availability zones.“ |
| W9 | https://webflow.com/legal/subprocessors | „Last updated: July 9, 2026“; „Amazon Web Services, Inc. Cloud services, hosting, and translation services USA“ |
| X1 | https://de.wix.com/upgrade/website | Weiterleitung auf https://de.wix.com/pricing; Datenblock: `"geo":"US"`; Preise nur per JavaScript |
| X2 | https://www.wix.com/plans | „Prices and currency vary by location. USD prices displayed for reference only. Displayed prices are for yearly subscriptions, paid in full at the time of purchase.“ |
| X3 | https://www.wix.com/plans | „Light Get the basics … Free domain for 1 year 2 GB storage space“; „Core … 50 GB storage space“; „Business … 100 GB storage space“; „Business Elite … Unlimited storage space“ |
| X4 | https://de.wix.com/domain/kaufen | „jährliches Premiumpaket ab 16,66 € im Monat“; „Eine .de-Domain bekommst du ab 14,95 €“ |
| X5 | https://de.wix.com/hosting | „weltweiten Datenzentren unterstützt durch Google Cloud, AWS, Fastly und Wix“ |
| X6 | https://de.wix.com/about/privacy-dpa-users | „Datum des Inkrafttretens: 27. September 2021“; „Dieser NDV stellt einen wesentlichen Bestandteil der Nutzungsbedingungen von Wix … dar“ |
| X7 | https://de.wix.com/about/privacy | „Gültig ab dem 18. Juni 2026“; „erfolgt im Hoheitsgebiet der Europäischen Union, Israels oder in einem Drittland …“ |
| J1 | https://www.jimdo.com/de/preise/website/ (gerendert mit DE-Katalog) | „Unlimited 50 € pro Monat … Grow Legal 29 € … Grow 20 € … Start 12 € … Free 0 €“; „Preise für Vertragslaufzeit von 12 Monaten. … Alle Preise inklusive MwSt.“ |
| J2 | https://api.e.jimdo.com/o2c-backend/api/v1/product-catalog?country=DE&language=de&group=DOLPHIN&includeFreePackage=true | Grow: `"termLength": "ONE_MONTH", "currency": "EUR", "total": 29.0`; `"ONE_YEAR" … "total": 240.0`; `"TWO_YEARS" … "total": 408.0` |
| J3 | wie J2 | „Bei der Verlängerung wird der gewählte Plan zum vollen Preis bzw. ohne den Rabatt, verlängert.“ |
| J4 | https://www.jimdo.com/de/preise/website/ | „Du kannst entweder monatlich zahlen oder direkt für eine Laufzeit von 12 oder 24 Monaten bezahlen“ |
| J5 | https://legal.jimdo.com/hc/de/articles/4414660225172-Jimdo-Informationen-zu-Unterauftragnehmern | „Amazon Web Services EMEA SARL Dienst: Webhosting und Infrastruktur … Ort der Datenverarbeitung: EU“; „Wie in unserem Auftragsverarbeitungsvertrag beschrieben …“ |
