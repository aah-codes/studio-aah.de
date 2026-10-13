#!/usr/bin/env python3
"""Stellt Fotos frei und färbt die Person blau ein – Entwurf 13.10.2026.

Anna: „Der Hintergrund muss monochrom sein“ – die Person steht freigestellt vor einer
einfarbigen Fläche; die Farbe der Fläche setzt das CSS (Bild mit Transparenz).
Freistell-Modell: IS-Net „isnet-general-use“ aus den rembg-Releases (nicht im Repository):
  https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx
Benötigt: numpy, onnxruntime, Pillow.
Aufruf vom Repository-Ordner aus: python3 werkzeuge/grafiken/freistellen.py PFAD/isnet-general-use.onnx
"""
import sys
from pathlib import Path
import numpy as np
import onnxruntime as ort
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
from duoton import einfaerben, FARBVERLAEUFE  # noqa: E402

QUELLE = Path("website/bilder")
ZIEL = Path("website/bilder/blau")
BILDER = ["anna-haertelt-portraet.jpg", "studio-aah-gruenderin-anna-haertelt.webp"]


def maske(sitzung, bild):
    x = np.asarray(bild.resize((1024, 1024), Image.LANCZOS), dtype=np.float32) / 255.0 - 0.5
    vorhersage = sitzung.run(None, {sitzung.get_inputs()[0].name: x.transpose(2, 0, 1)[None]})[0][0, 0]
    vorhersage = (vorhersage - vorhersage.min()) / (vorhersage.max() - vorhersage.min())
    return Image.fromarray((vorhersage * 255).astype(np.uint8)).resize(bild.size, Image.LANCZOS)


def main():
    if len(sys.argv) < 2:
        sys.exit("Aufruf: python3 werkzeuge/grafiken/freistellen.py PFAD/isnet-general-use.onnx")
    sitzung = ort.InferenceSession(sys.argv[1], providers=["CPUExecutionProvider"])
    ZIEL.mkdir(parents=True, exist_ok=True)
    for datei in BILDER:
        bild = ImageOps.exif_transpose(Image.open(QUELLE / datei)).convert("RGB")
        alpha = maske(sitzung, bild)
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
