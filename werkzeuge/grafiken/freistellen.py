#!/usr/bin/env python3
"""Stellt Fotos frei und färbt die Person blau ein – Entwurf 13.10.2026.

Anna: „Der Hintergrund muss monochrom sein“ – die Person steht freigestellt vor einer
einfarbigen Fläche; die Farbe der Fläche setzt das CSS (Bild mit Transparenz).
Freistell-Modelle aus den rembg-Releases (nicht im Repository, ONNX):
  empfohlen für Porträts (Haare): BiRefNet-portrait-epoch_150.onnx (ca. 970 MB, braucht viel Arbeitsspeicher)
  https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-portrait-epoch_150.onnx
  schneller, gröber: isnet-general-use.onnx (gleiche Adresse, anderer Dateiname)
Vergleich am 13.10.2026: BiRefNet-portrait schneidet die Haare sauberer; Photocraft („Motiv auswählen“)
erkannte nur den Pullover, seine Kantenverfeinerung brachte danach kaum noch Gewinn.
Benötigt: numpy, onnxruntime, Pillow.
Aufruf vom Repository-Ordner aus: python3 werkzeuge/grafiken/freistellen.py PFAD/MODELL.onnx
"""
import sys
from pathlib import Path
import numpy as np
import onnxruntime as ort
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
from duoton import einfaerben, FARBVERLAEUFE  # noqa: E402

QUELLE = Path("website/bilder")
ZIEL = Path("werkzeuge/grafiken/bilder-blau")  # nicht veröffentlicht; für den Einsatz nach website/bilder/ kopieren
BILDER = ["anna-haertelt-portraet.webp", "studio-aah-gruenderin-anna-haertelt.webp"]


def maske(sitzung, bild, birefnet):
    x = np.asarray(bild.resize((1024, 1024), Image.LANCZOS), dtype=np.float32)
    if birefnet:  # Vorverarbeitung wie in rembg (BiRefNet)
        x = x / max(float(x.max()), 1.0)
        x = (x - np.array([0.485, 0.456, 0.406], dtype=np.float32)) / np.array([0.229, 0.224, 0.225], dtype=np.float32)
    else:  # IS-Net
        x = x / 255.0 - 0.5
    vorhersage = sitzung.run(None, {sitzung.get_inputs()[0].name: x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    if birefnet:
        vorhersage = 1 / (1 + np.exp(-vorhersage))
    vorhersage = (vorhersage - vorhersage.min()) / (vorhersage.max() - vorhersage.min())
    return Image.fromarray((vorhersage * 255).astype(np.uint8)).resize(bild.size, Image.LANCZOS)


def main():
    if len(sys.argv) < 2:
        sys.exit("Aufruf: python3 werkzeuge/grafiken/freistellen.py PFAD/isnet-general-use.onnx")
    optionen = ort.SessionOptions()
    optionen.enable_cpu_mem_arena = False  # spart Arbeitsspeicher (BiRefNet ist groß)
    optionen.enable_mem_pattern = False
    optionen.intra_op_num_threads = 2
    sitzung = ort.InferenceSession(sys.argv[1], sess_options=optionen, providers=["CPUExecutionProvider"])
    birefnet = "birefnet" in Path(sys.argv[1]).name.lower()
    ZIEL.mkdir(parents=True, exist_ok=True)
    for datei in BILDER:
        bild = ImageOps.exif_transpose(Image.open(QUELLE / datei)).convert("RGB")
        alpha = maske(sitzung, bild, birefnet)
        grau = ImageOps.autocontrast(bild.convert("L"), cutoff=1)
        stamm = Path(datei).stem
        for name, person in [("frei-blau", einfaerben(grau, FARBVERLAEUFE["triton"])), ("frei-sw", grau.convert("RGB"))]:
            ausgabe = person.convert("RGBA")
            ausgabe.putalpha(alpha)
            ziel = ZIEL / f"{stamm}-{name}.webp"
            ausgabe.save(ziel, "WEBP", quality=82, method=6)
            print(ziel, ziel.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
