# studio-aah.de

Statische Website von Studio AAH: reines HTML und CSS, ohne WordPress, ohne Bau-Schritt.

## Aufbau
- `website/` – alles, was online geht (nur dieser Ordner wird veröffentlicht)
- `werkzeuge/pruefen.sh` – prüft Kopf, Fuß, interne Links und Bilder (ändert nichts)
- `.github/workflows/github-pages.yml` – veröffentlicht `website/` bei jedem Push auf `main`
- `CLAUDE.md` – Hinweise für Claude Code

## Veröffentlichen
- Hosting: GitHub Pages mit eigener Domain studio-aah.de (DNS bei IONOS; E-Mail bleibt bei IONOS).
- Jeder Push auf `main` geht nach etwa einer Minute live.

## Schriften
- Anton, Inter, Newsreader – SIL Open Font License 1.1 (Hinweise in `website/css/stil.css`).

## Inhalte
- Texte und Bilder: © Anna Härtelt / Studio AAH, alle Rechte vorbehalten. Der Code darf angesehen, die Inhalte dürfen nicht übernommen werden.
- Blogbild „Was KI an meiner Arbeit verändert hat“: Unsplash (@szolkin), Unsplash-Lizenz.
