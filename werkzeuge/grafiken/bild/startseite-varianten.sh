#!/bin/bash
# Kleinere Bildfassungen für die Startseite.
# Name: <bild>-<breite>.webp (bzw. .jpg) neben dem Original; eingebunden per srcset/sizes in website/index.html.
# Erst mit sips verkleinert (PNG, verlustfrei), dann mit cwebp kodiert. Braucht macOS (sips) und cwebp (~/bin).
# Aufruf im Repository-Ordner: bash werkzeuge/grafiken/bild/startseite-varianten.sh – danach bash werkzeuge/alle-erzeugen.sh
set -e
CWEBP=$(command -v cwebp || echo "$HOME/bin/cwebp")
cd "$(dirname "$0")/../../../website/bilder"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
erzeuge() {  # erzeuge DATEI QUALITÄT BREITE…
  local datei=$1 q=$2; shift 2
  for b in "$@"; do
    ziel="${datei%.*}-$b.webp"
    sips -s format png --resampleWidth "$b" "$datei" --out "$TMP/v.png" >/dev/null
    "$CWEBP" -quiet -q "$q" -sharp_yuv -metadata none "$TMP/v.png" -o "$ziel"
    echo "$ziel $(( $(stat -f%z "$ziel") / 1024 )) KB"
  done
}
# Hero-Diashow: am Handy höchstens ca. 400 px breit, am Tablet bis 990 px, am Desktop ca. 700 px (dort bei hoher Pixeldichte das Original)
erzeuge anna-haertelt-studio-blau.webp 82 640 960
for f in start/arbeitsplatz-winkekatze.webp start/leipzig-voelkerschlachtdenkmal.webp start/leipzig-zentrum-von-oben.webp; do
  erzeuge "$f" 82 640 960
done
erzeuge start/leipzig-plagwitz-kanal.webp 82 640   # Original nur 1000 px breit; 960 läge über 250 KB
# „Im Fokus“-Karten: 330–460 px breit
erzeuge website-check/pruefbericht-mockup-1200.webp 85 640
erzeuge ki-arbeits-setup-cockpit.webp 88 640
erzeuge marken-regelwerk/miniatur-tastatur-figur.webp 85 640
erzeuge leistung-retainer.webp 85 640
# Icons der Ökosystem-Grafik und des Sticky-Buttons: höchstens 36 px groß
for f in icons/thumb-up.webp icons/compass.webp icons/mail.webp icons/folder.webp icons/chart.webp icons/heart.webp icons/star.webp icons/megaphone.webp icons/target.webp; do
  erzeuge "$f" 90 96
done
# Rundes Porträt: höchstens 96 px groß (Intro, Kontakt, Chat)
sips -s format jpeg -s formatOptions 82 --resampleWidth 192 anna-haertelt-studio-blau-rund.jpg --out anna-haertelt-studio-blau-rund-192.jpg >/dev/null
echo "anna-haertelt-studio-blau-rund-192.jpg $(( $(stat -f%z anna-haertelt-studio-blau-rund-192.jpg) / 1024 )) KB"
