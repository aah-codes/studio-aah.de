#!/bin/bash
# Prüfskript für website/ – ändert nichts, meldet nur.
# 1. Kopf und Fuß sind auf allen Seiten gleich (wie in website/index.html).
# 2. Alle internen Links und Bilder zeigen auf vorhandene Dateien.
# Aufruf im Repository-Ordner:  bash werkzeuge/pruefen.sh

cd "$(dirname "$0")/../website" || exit 1
fehler=0

# Pfade vereinheitlichen, damit Unterseiten (../) mit der Startseite vergleichbar sind
einheitlich() { sed -E 's#="(\.\./)+#="#g; s#(href|src)="/#\1="#g; s#href="\.\./"#href="./"#g; s#href=""#href="./"#g'; }
kopf() { awk '/<a class="sprunglink"/,/<!-- \/KOPF -->/' "$1" | einheitlich; }
fuss() { awk '/<!-- FUSS:/,/<!-- \/FUSS -->/' "$1" | einheitlich; }

seiten=$(find . -name "*.html" | sort | while read -r s; do grep -q 'http-equiv="refresh"' "$s" || echo "$s"; done)
# Weiterleitungsseiten (work/, angebot/ …) haben keinen Kopf und Fuß und werden übersprungen

echo "== Kopf und Fuß"
for s in $seiten; do
  [ "$s" = "./index.html" ] && continue
  if ! diff -q <(kopf index.html) <(kopf "$s") >/dev/null; then
    echo "  ABWEICHUNG Kopf: $s"; fehler=1
  fi
  if ! diff -q <(fuss index.html) <(fuss "$s") >/dev/null; then
    echo "  ABWEICHUNG Fuß:  $s"; fehler=1
  fi
done

echo "== Interne Links und Bilder"
meldungen=$(for s in $seiten; do
  ordner=$(dirname "$s")
  grep -oE '(href|src)="[^"#]+"' "$s" | sed -E 's/^(href|src)="//; s/"$//' |
  grep -vE '^(https?:|mailto:|tel:)' | sort -u |
  while read -r ziel; do
    pfad="$ordner/$ziel"
    case "$ziel" in (*/|.|..) pfad="${pfad%/}/index.html" ;; esac
    [ -e "$pfad" ] || echo "  FEHLT: $s -> $ziel"
  done
done)
if [ -n "$meldungen" ]; then echo "$meldungen"; fehler=1; fi

[ $fehler -eq 0 ] && echo "Alles in Ordnung." || echo "Es gibt Meldungen (siehe oben)."
exit $fehler
