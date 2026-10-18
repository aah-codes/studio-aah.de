#!/bin/bash
# Kleinere WebP-Fassungen der langen Seitenaufnahmen für srcset (Projektkarten) und die Hero-Leiste, damit Handys nicht die
# 1440-px-Originale laden (Website-Check 18.10.2026, Nachtrag Anna 19.10.2026: WebP in Anzeigegröße; die großen JPGs bleiben).
# Name: <bild>-<breite>.webp neben dem Original. Erst mit sips verkleinert (PNG, verlustfrei), dann mit cwebp kodiert.
# Braucht macOS (sips) und cwebp (libwebp von Google, liegt in ~/bin).
# Aufruf im Repository-Ordner:  bash werkzeuge/grafiken/bild/varianten.sh   – danach bash werkzeuge/alle-erzeugen.sh und bash werkzeuge/pruefen.sh
set -e
CWEBP=$(command -v cwebp || echo "$HOME/bin/cwebp")
cd "$(dirname "$0")/../../../website/bilder/referenzen"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
QUALITAET=88
erzeuge() {  # erzeuge DATEI BREITE…
  local datei=$1; shift
  for b in "$@"; do
    ziel="${datei%.*}-$b.webp"
    sips -s format png --resampleWidth "$b" "$datei" --out "$TMP/v.png" >/dev/null
    "$CWEBP" -quiet -q $QUALITAET -sharp_yuv -metadata none "$TMP/v.png" -o "$ziel"
    echo "$ziel $(( $(stat -f%z "$ziel") / 1024 )) KB"
  done
}
erzeuge_jpg() {  # wie erzeuge, aber JPG – für lange Seitenaufnahmen, deren WebP über 250 KB läge (CLAUDE.md, Bilder: Ausnahme JPG)
  local datei=$1; shift
  for b in "$@"; do
    ziel="${datei%.*}-$b.jpg"
    sips -s format jpeg -s formatOptions 80 --resampleWidth "$b" "$datei" --out "$ziel" >/dev/null
    echo "$ziel $(( $(stat -f%z "$ziel") / 1024 )) KB"
  done
}
# Desktop-Aufnahmen (1440 px): Handy 480, Tablet und Handys mit hoher Pixeldichte 720, kleiner Desktop 960 – WebP nur bis 250 KB (CLAUDE.md, Bilder);
# bei Bauer und Deinetwegen liegt WebP ab 720 darüber, dort 720 als JPG und darüber das Original. Bauer zusätzlich 320 für den Laptop in der Hero-Leiste
erzeuge bauer-website.jpg 320 480
erzeuge_jpg bauer-website.jpg 720
erzeuge deinetwegen-website.jpg 480
erzeuge_jpg deinetwegen-website.jpg 720
erzeuge jana-website.jpg 480 720 960
# Handy-Aufnahmen (780–860 px): Hero-Leiste 180 (dort höchstens 58 px breit), Karte am Handy 240, am Desktop 480
erzeuge bauer-handy.jpg 240 480
erzeuge deinetwegen-handy.jpg 180 240 480
erzeuge studio-aah-handy.jpg 180
# UI/UX-Karte der Hero-Leiste (höchstens 134 px breit)
erzeuge leben-website.webp 320
