#!/bin/bash
# Bildwelt A: ein Asset-Set aus einem KI-Rohbild bauen (vier Formate als WebP, höchstens 250 KB).
# Aufruf vom Repository-Ordner aus:
# bash werkzeuge/grafiken/bildwelt-a.sh ROH.png ZIELORDNER NAME FORM [FORMFARBE]
# Braucht cwebp (libwebp von Google) und c2patool (Content Authenticity Initiative), beide auf dem MacBook in ~/bin.
# Rohbild bleibt unverändert; jedes WebP bekommt die Herkunftskette des Rohbilds (Canva-Bedingungen: Herkunftsdaten nicht entfernen).
# Unterschrift bisher mit Testzertifikat.
set -euo pipefail
ROH="$1"; ZIEL="$2"; NAME="$3"; FORM="$4"; FARBE="${5:-blau}"
CWEBP="$(command -v cwebp || echo "$HOME/bin/cwebp")"
C2PA="$(command -v c2patool || echo "$HOME/bin/c2patool")"
HIER="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$ZIEL"
swift "$(dirname "$0")/bildwelt-a.swift" "$ROH" "$TMP" "$NAME" "$FORM" "$FARBE"
for png in "$TMP"/*.png; do
  ziel="$ZIEL/$(basename "${png%.png}").webp"
  for q in 86 82 78 74 70 66; do
    "$CWEBP" -quiet -q "$q" -m 6 -sharp_yuv "$png" -o "$TMP/ohne.webp"
    if [ -x "$C2PA" ]; then
      "$C2PA" "$TMP/ohne.webp" --settings "$HIER/bildwelt-herkunft.toml" -m "$HIER/bildwelt-herkunft.json" -p "$ROH" -o "$ziel" -f >/dev/null 2>&1
    else
      echo "WARNUNG: c2patool fehlt – ohne Herkunftsdaten nicht veröffentlichen"; cp "$TMP/ohne.webp" "$ziel"
    fi
    [ "$(stat -f%z "$ziel")" -le 256000 ] && break
  done
  printf '%s  %s KB (q %s)\n' "$(basename "$ziel")" "$(( $(stat -f%z "$ziel") / 1024 ))" "$q"
done
