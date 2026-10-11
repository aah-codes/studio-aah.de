// Erzeugt von werkzeuge/preise-erzeugen.py aus werkzeuge/preise-daten.json – nicht von Hand ändern
window.PREISE = {
 "launch": 150,
 "gruppen": [
  {
   "id": "brand",
   "name": "Brand",
   "wahl": "eins",
   "pakete": [
    {
     "id": "brand-0",
     "name": "Basic",
     "preis": 850,
     "wer": "Für Gründer:innen und Selbstständige, die erst Klarheit über Positionierung und Stil brauchen.",
     "plus": "Enthalten:",
     "items": [
      "Fragebogen und gemeinsamer Termin",
      "Markencheck",
      "Moodboard",
      "Grundpositionierung"
     ],
     "gefragt": false,
     "ab": true
    },
    {
     "id": "brand-1",
     "name": "Medium",
     "preis": 2500,
     "wer": "Für Unternehmen, die eine neue Marke mit Logo und Erscheinungsbild brauchen.",
     "plus": "Alles aus Basic, plus:",
     "items": [
      "Positionierung & Zielgruppe",
      "Logo-Entwicklung",
      "Farben, Schriften, Bildwelt, Gestaltungselemente",
      "Basishandbuch (kompakt)"
     ],
     "gefragt": true,
     "ab": true
    },
    {
     "id": "brand-2",
     "name": "Premium",
     "preis": 4500,
     "wer": "Für Unternehmen, die ihre Marke umfassend aufstellen und im Alltag einheitlich einsetzen wollen.",
     "plus": "Alles aus Medium, plus:",
     "items": [
      "Markenkern",
      "Messaging & Tonalität",
      "Brand Manual (ausführlich)",
      "Erste Vorlagen: Visitenkarte, Briefpapier, Präsentation, Social Media"
     ],
     "gefragt": false,
     "ab": true
    },
    {
     "id": "logo",
     "name": "Logo einzeln",
     "preis": 990,
     "wer": "",
     "plus": "",
     "items": [],
     "ab": true
    }
   ]
  },
  {
   "id": "ui-ux",
   "name": "UI/UX",
   "wahl": "eins",
   "pakete": [
    {
     "id": "ui-ux-0",
     "name": "Expert Review",
     "preis": 1200,
     "wer": "Expertenblick auf Ihre gesamte Website oder Anwendung.",
     "plus": "Enthalten:",
     "items": [
      "Ich versetze mich in Ihre Zielgruppe und nutze Ihre Website oder Anwendung",
      "Analyse: was sich verbessern lässt",
      "Handlungsempfehlungen"
     ],
     "gefragt": false,
     "ab": true
    },
    {
     "id": "ui-ux-1",
     "name": "UI/UX Audit Pro",
     "preis": 2900,
     "wer": "Die ganze Anwendung unter der Lupe.",
     "plus": "Enthalten:",
     "items": [
      "Expert Review",
      "Brand Experience",
      "Personas",
      "Mitbewerberrecherche",
      "Trendanalyse",
      "Ausführlicher PDF-Report mit Prioritäten"
     ],
     "gefragt": false,
     "ab": true,
     "vorschlag": true
    },
    {
     "id": "ui-ux-2",
     "name": "Redesign kleine Webanwendung",
     "preis": 4500,
     "wer": "Für Teams mit bestehender Webanwendung, die einfacher zu bedienen sein soll.",
     "plus": "Alles aus UI/UX Audit Pro, plus:",
     "items": [
      "Neue Nutzerführung",
      "Wireframes & klickbarer Prototyp (Figma)",
      "UI-Kit",
      "Übergabe mit Spezifikationen"
     ],
     "gefragt": false,
     "ab": true,
     "vorschlag": true
    },
    {
     "id": "ui-ux-3",
     "name": "Plattform / SaaS",
     "preis": 5850,
     "wer": "Für Software-Produkte, die von Grund auf durchdacht gestaltet werden sollen.",
     "plus": "Alles aus Redesign, plus:",
     "items": [
      "Umfassendes UX-Research & Zielgruppenanalyse",
      "Vollständiges Designsystem"
     ],
     "gefragt": false,
     "ab": true
    }
   ]
  },
  {
   "id": "website",
   "name": "Website",
   "wahl": "eins",
   "hinweis": "Typisch: Selbstständige 1–6 Unterseiten · kleine und mittlere Unternehmen mit Leistungs- und Branchenseiten 10–25 Unterseiten. Mehr als 25 Unterseiten, Shop oder Mitgliederbereich? Dann ist es ein komplexes Projekt ab 6.000 € – melden Sie sich am besten direkt.",
   "pakete": [
    {
     "id": "onepager",
     "name": "Onepager",
     "preis": 1150,
     "wer": "Für Selbstständige und kleine Angebote, die alles auf einer Seite zeigen.",
     "plus": "Enthalten:",
     "items": [
      "Expert Review (wenn es schon eine Website gibt)",
      "Marktanalyse",
      "Seitenstruktur (Sitemap)",
      "Design für Desktop & Handy (responsiv)",
      "Umsetzung in WordPress (Kadence)",
      "Texte und Bilder kann ich liefern",
      "SEO-Basics & Kontaktformular",
      "Launch (150 €, wird automatisch berechnet) & Übergabe",
      "Schulung zur Selbstpflege: als Zusatz buchbar"
     ],
     "launch": true,
     "ab": true
    },
    {
     "id": "website",
     "name": "Website – neu oder Redesign",
     "preis": 2450,
     "inkl": 6,
     "seite": 150,
     "wer": "Für Unternehmen, die ihr Angebot ausführlich vorstellen.",
     "plus": "Alles aus Onepager, plus:",
     "items": [
      "Mehrere Unterseiten nach Ihrer Sitemap",
      "SEO-Einrichtung für alle Unterseiten",
      "Bei Redesign: Analyse der bestehenden Website, Übernahme vorhandener Inhalte, Weiterleitungen alter Adressen"
     ],
     "gefragt": true,
     "launch": true,
     "ab": true
    }
   ],
   "extras": [
    {
     "id": "sprache",
     "name": "Weitere Sprache",
     "anteil": 0.3,
     "art": "anzahl",
     "wer": "ohne Website-Paket: auf Anfrage"
    },
    {
     "id": "blog",
     "name": "Blog",
     "preis": 490,
     "ab": false,
     "wer": "auch für bestehende Websites"
    },
    {
     "id": "newsletter",
     "name": "Newsletter-Anbindung",
     "preis": 260,
     "ab": false,
     "wer": "auch für bestehende Websites"
    },
    {
     "id": "seo",
     "name": "SEO-Grundeinrichtung",
     "preis": 260,
     "ab": false,
     "ohnePaket": true,
     "wer": "für bestehende Websites"
    },
    {
     "id": "schulung",
     "name": "Schulung",
     "preis": 70,
     "ab": false,
     "wahl": [
      "PDF-Anleitung",
      "Online-Termin"
     ],
     "wer": "für alle, die selbst pflegen"
    },
    {
     "id": "wartung",
     "name": "Wartung",
     "monat": 45,
     "wer": "Regelmäßige technische Pflege Ihrer WordPress-Website.",
     "items": [
      "Updates von WordPress, Plugins & Themes",
      "Technische Überwachung & Sicherheitschecks",
      "Kleine Bildänderungen",
      "Austausch von PDFs"
     ]
    }
   ]
  },
  {
   "id": "marketing",
   "name": "Marketing & Vertrieb",
   "wahl": "mehrere",
   "pakete": [
    {
     "id": "marketing-0",
     "name": "LinkedIn aufsetzen",
     "preis": 500,
     "wer": "Damit die richtigen Menschen Sie finden und sofort verstehen, was Sie anbieten.",
     "plus": "Enthalten:",
     "items": [
      "Profil",
      "Unternehmensseite",
      "Positionierung"
     ],
     "gefragt": false,
     "ab": true
    },
    {
     "id": "vorlagen",
     "name": "Social-Media- & Post-Vorlagen",
     "preis": 400,
     "wer": "Damit Sie regelmäßig posten können, ohne jedes Mal bei null anzufangen.",
     "plus": "Enthalten:",
     "items": [
      "5 Vorlagen in Canva",
      "im eigenen Design"
     ],
     "ab": true
    },
    {
     "id": "marketing-2",
     "name": "Fachartikel",
     "preis": 300,
     "wer": "Für Blog, LinkedIn oder Fachmedien – mit Ihrer Expertise im Mittelpunkt.",
     "plus": "Pro Artikel:",
     "items": [
      "1.000–1.500 Wörter",
      "recherchiert und verständlich"
     ],
     "gefragt": false,
     "ab": true
    },
    {
     "id": "marketing-3",
     "name": "Webinar aufsetzen",
     "preis": 850,
     "wer": "Damit Sie sich ganz auf Ihren Auftritt konzentrieren können.",
     "plus": "Enthalten:",
     "items": [
      "Konzept",
      "Anmeldeseite",
      "Folien als PowerPoint oder PDF"
     ],
     "gefragt": false,
     "ab": true
    }
   ]
  },
  {
   "id": "print",
   "name": "Print",
   "wahl": "mehrere",
   "pakete": [
    {
     "id": "visitenkarte",
     "name": "Visitenkarte",
     "preis": 195,
     "wer": "Gestaltung, druckfertig.",
     "plus": "Enthalten:",
     "items": [
      "Vorder- und Rückseite",
      "Druckdaten"
     ],
     "ab": true
    },
    {
     "id": "flyer",
     "name": "Flyer oder Postkarte",
     "preis": 290,
     "wer": "Für Aktionen, Veranstaltungen, Angebote.",
     "plus": "Enthalten:",
     "items": [
      "A6 oder A5",
      "Vorder- und Rückseite",
      "Druckdaten"
     ],
     "ab": true
    },
    {
     "id": "broschuere",
     "name": "Broschüre (zweiseitig)",
     "preis": 450,
     "wer": "Für kompakte Informationen auf Papier.",
     "plus": "Enthalten:",
     "items": [
      "zwei Seiten",
      "Druckdaten"
     ],
     "ab": true
    },
    {
     "id": "praesentation",
     "name": "Unternehmenspräsentation",
     "preis": 1200,
     "wer": "Als PDF und für den Druck – für Gespräche, Angebote, Messen.",
     "plus": "Enthalten:",
     "items": [
      "bis zu 20 Folien",
      "PDF und Druckdaten"
     ],
     "ab": true
    },
    {
     "id": "publikation",
     "name": "Mehrseitige Publikation",
     "preis": 2600,
     "wer": "Magazin, Katalog, Jahresbericht.",
     "plus": "Enthalten:",
     "items": [
      "Mehrseitige Publikation",
      "Druckbegleitung"
     ],
     "ab": true
    }
   ]
  },
  {
   "id": "ki",
   "name": "KI & Digitalisierung",
   "wahl": "eins",
   "pakete": [
    {
     "id": "ki-0",
     "name": "KI-Check",
     "preis": 900,
     "wer": "Für alle, die wissen wollen, wo KI im Alltag wirklich Zeit spart.",
     "plus": "Enthalten:",
     "items": [
      "Fragebogen und gemeinsamer Termin",
      "Analyse Ihrer Abläufe",
      "Empfehlungsbericht"
     ],
     "gefragt": false,
     "ab": true
    },
    {
     "id": "ki-1",
     "name": "KI-Einführung",
     "preis": 2000,
     "wer": "Für Teams, die die Empfehlungen aus dem Check umsetzen wollen.",
     "plus": "Nach dem KI-Check:",
     "items": [
      "Auswahl & Einrichtung passender KI-Werkzeuge",
      "1–2 digitale Arbeitsabläufe",
      "Team-Schulung"
     ],
     "gefragt": false,
     "ab": true
    }
   ]
  },
  {
   "id": "zusatz",
   "name": "Zusatzleistungen",
   "wahl": "mehrere",
   "pakete": [
    {
     "id": "illu",
     "name": "Illustration & Infografik",
     "anfrage": true,
     "wer": "sehr individuell – wir klären es im Erstgespräch",
     "items": [],
     "ab": true
    },
    {
     "id": "motion",
     "name": "Motion Design",
     "anfrage": true,
     "wer": "sehr individuell – wir klären es im Erstgespräch",
     "items": [],
     "ab": true
    }
   ]
  }
 ]
};
