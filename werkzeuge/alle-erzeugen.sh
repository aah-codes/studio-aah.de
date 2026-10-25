#!/bin/bash
# Lässt alle Generatoren in der richtigen Reihenfolge laufen (nach jeder Änderung an Daten oder Vorlagen).
# Reihenfolge zählt: Kopf und Fuß zuerst (die anderen übernehmen sie aus bestehenden Seiten), der Blogbeitrag muss vor inhalte-erzeugen.py fertig sein (Lesezeit), die Startseite
# vor leistungsseiten.py (Prozess) und die Webdesign-Seite vor referenzen.py (Kopf und Fuß).
# Aufruf im Repository-Ordner:  bash werkzeuge/alle-erzeugen.sh
set -e
cd "$(dirname "$0")/.."
python3 werkzeuge/kopf-fuss.py
python3 werkzeuge/preise-erzeugen.py
python3 werkzeuge/blog/was-kostet-eine-website.py
python3 werkzeuge/blog/was-sollte-eine-website-2027-koennen.py
python3 werkzeuge/inhalte-erzeugen.py
python3 werkzeuge/leistungsseiten.py
python3 werkzeuge/website-check.py
python3 werkzeuge/referenzen.py
