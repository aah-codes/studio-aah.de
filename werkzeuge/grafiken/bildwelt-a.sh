#!/bin/bash
# Bildwelt A: ein Asset-Set aus einem KI-Rohbild bauen (vier Formate als WebP, höchstens 250 KB).
# Aufruf vom Repository-Ordner aus:
#   bash werkzeuge/grafiken/bildwelt-a.sh ROH.png ZIELORDNER NAME FORM [FORMFARBE]
# Braucht cwebp (libwebp von Google, auf dem MacBook in ~/bin). Rohbild bleibt unverändert.
set -euo pipefail
ROH="$1"; ZIEL="$2"; NAME="$3"; FORM="$4"; FARBE="${5:-blau}"
CWEBP="$(command -v cwebp || echo "$HOME/bin/cwebp")"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$ZIEL"
swift "$(dirname "$0")/bildwelt-a.swift" "$ROH" "$TMP" "$NAME" "$FORM" "$FARBE"
for png in "$TMP"/*.png; do
  ziel="$ZIEL/$(basename "${png%.png}").webp"
  for q in 86 82 78 74 70 66; do
    "$CWEBP" -quiet -q "$q" -m 6 -sharp_yuv "$png" -o "$ziel"
    [ "$(stat -f%z "$ziel")" -le 256000 ] && break
  done
  printf '%s  %s KB (q %s)\n' "$(basename "$ziel")" "$(( $(stat -f%z "$ziel") / 1024 ))" "$q"
done
