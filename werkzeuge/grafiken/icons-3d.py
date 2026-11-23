"""3D-Fassung der Bauhaus-Icons.

Läuft in Blender (kostenlos, auf dem MacBook in ~/Applications/Blender.app), nicht mit dem normalen Python.
Aufruf vom Repository-Ordner aus über das Hilfsskript:
    bash werkzeuge/grafiken/icons-3d.sh ZIELORDNER website/bilder/formen/brand.svg [weitere.svg …]
Für jedes SVG entsteht ZIELORDNER/<name>-3d.png (1024 × 1024, transparenter Hintergrund mit weichem Kontaktschatten).

Alle Werte sind für jedes Icon gleich, damit das Set wie aus einem Guss wirkt:
Tiefe 13 % der Breite, leicht abgerundete Kanten (nach innen, damit die Fugen offen bleiben), mattes Material wie Satin-Kunststoff,
Kamera gerade von vorn und 12° von oben, Icon steht auf dem Boden, Linien (stroke) werden vorher zu Flächen,
ein weiches Licht von oben links, Farben exakt aus der Farbtafel (Blau berührt nie Schwarz: die Fugen der SVGs bleiben echte Spalten).
"""
import math
import os
import pathlib
import sys

import addon_utils
import bpy
from mathutils import Vector

FARBEN = {  # sRGB-Werte der Marke (tokens.json)
    'blau': (0x2a, 0x5f, 0xe6), 'schwarz': (0x0e, 0x10, 0x11), 'weiss': (0xff, 0xff, 0xff), 'gelb': (0xff, 0xe6, 0x00),
}
TIEFE, FASE, NEIGUNG, AUFLOESUNG, SAMPLES = 0.26, 0.025, 12, 1024, 96  # Tiefe 13 % der Breite (Breite = 2)
# Ohne Schatten; nur mit SCHATTEN=1 kommt der Kontaktschatten zurück
SCHATTEN = os.environ.get('SCHATTEN') == '1'
# Neigung 12° statt 20°: bei 20° verdeckte die Oberseite der unteren Form die Fuge, Blau schien Schwarz zu berühren


def linear(c):
    """sRGB (0–255) → linearer Farbwert für Blender."""
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def naechste_markenfarbe(rgb):
    """Farbe aus dem SVG auf die nächste Markenfarbe ziehen (der Import liefert leicht andere Werte)."""
    def abstand(a, b): return sum((x - y) ** 2 for x, y in zip(a, b))
    return min(FARBEN, key=lambda n: abstand([linear(v) for v in FARBEN[n]], rgb))


def material(name):
    m = bpy.data.materials.get('marke-' + name) or bpy.data.materials.new('marke-' + name)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = [linear(v) for v in FARBEN[name]] + [1]
    p.inputs['Roughness'].default_value = 0.55          # matt wie Satin
    if 'Specular IOR Level' in p.inputs: p.inputs['Specular IOR Level'].default_value = 0.25
    if 'Coat Weight' in p.inputs: p.inputs['Coat Weight'].default_value = 0.0
    return m


def szene_leeren():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon_utils.enable('io_curve_svg', default_set=True)


def _clip(poly, x0, y0, x1, y1):
    """Vieleck auf ein Rechteck beschneiden (Sutherland-Hodgman)."""
    for innen, schnitt in (
        (lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
        (lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
        (lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
        (lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1)),
    ):
        neu = []
        for i, b in enumerate(poly):
            a = poly[i - 1]
            if innen(b):
                if not innen(a): neu.append(schnitt(a, b))
                neu.append(b)
            elif innen(a):
                neu.append(schnitt(a, b))
        poly = neu
        if not poly: break
    return poly


def linien_zu_flaechen(svg, ordner):
    """Blender übernimmt nur Flächen. Gerade Linien (stroke, z. B. Haken, Briefumschlag) werden zu Flächen,
    beschnitten auf die Form darunter (in 2D liegt der Überstand weiß auf Weiß, in 3D stünde er heraus)."""
    import re
    import xml.etree.ElementTree as ET
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    baum = ET.parse(svg)
    wurzel = baum.getroot()
    if not any(e.get('stroke') for e in wurzel.iter()):
        return svg
    rahmen = []  # Rahmen der gefüllten Formen, in Reihenfolge
    for e in list(wurzel):
        tag = e.tag.split('}')[-1]
        if tag == 'rect':
            x, y = float(e.get('x', 0)), float(e.get('y', 0))
            rahmen.append((x, y, x + float(e.get('width')), y + float(e.get('height'))))
        elif tag == 'circle':
            cx, cy, r = (float(e.get(a)) for a in ('cx', 'cy', 'r'))
            rahmen.append((cx - r, cy - r, cx + r, cy + r))
        if tag != 'path' or not e.get('stroke'):
            continue
        punkte = [tuple(map(float, p)) for p in re.findall(r'(-?[\d.]+)[ ,](-?[\d.]+)', e.get('d'))]
        w = float(e.get('stroke-width', 1)) / 2
        eckig = e.get('stroke-linecap') == 'square'
        unter = next((r for r in reversed(rahmen) if all(r[0] <= px <= r[2] and r[1] <= py <= r[3] for px, py in punkte)), None)
        idx = list(wurzel).index(e)
        wurzel.remove(e)
        # eine geschlossene Fläche mit Gehrung (miter) an den Gelenken, damit kein Stoß sichtbar ist
        richt = []
        for (ax, ay), (bx, by) in zip(punkte, punkte[1:]):
            lg = math.hypot(bx - ax, by - ay)
            richt.append(((bx - ax) / lg, (by - ay) / lg))

        def seite(sg):
            aus = []
            for k, (px, py) in enumerate(punkte):
                if k in (0, len(punkte) - 1):
                    ux, uy = richt[0] if k == 0 else richt[-1]
                    v = (-w if k == 0 else w) if eckig else 0
                    aus.append((px + ux * v - uy * w * sg, py + uy * v + ux * w * sg))
                    continue
                (u1x, u1y), (u2x, u2y) = richt[k - 1], richt[k]
                p1 = (px - u1y * w * sg, py + u1x * w * sg)
                p2 = (px - u2y * w * sg, py + u2x * w * sg)
                det = u1x * -u2y - u1y * -u2x
                t = ((p2[0] - p1[0]) * -u2y - (p2[1] - p1[1]) * -u2x) / det
                aus.append((p1[0] + u1x * t, p1[1] + u1y * t))
            return aus

        poly = seite(1) + seite(-1)[::-1]
        if unter: poly = _clip(poly, *unter)
        d = 'M ' + ' L '.join(f'{px:.2f} {py:.2f}' for px, py in poly) + ' Z'
        wurzel.insert(idx, ET.Element('path', {'d': d, 'fill': e.get('stroke')}))
    ziel = ordner / ('_flaechen-' + svg.name)
    baum.write(ziel)
    return ziel


def icon_bauen(svg):
    bpy.ops.import_curve.svg(filepath=str(svg))
    teile = [o for o in bpy.context.scene.objects if o.type == 'CURVE']
    # Größe normieren: breiteste Seite = 2 Einheiten, Mitte im Ursprung
    ecken = [o.matrix_world @ Vector(c) for o in teile for c in o.bound_box]
    xs, ys = [e.x for e in ecken], [e.y for e in ecken]
    breite, hoehe = max(xs) - min(xs), max(ys) - min(ys)
    f = 2 / max(breite, hoehe)
    mitte = Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0))
    kaesten = []  # 2D-Rahmen der bisherigen Formen, um Überlappung zu erkennen
    for i, o in enumerate(teile):
        # Maße in echten Einheiten: Kurvenpunkte direkt skalieren (transform_apply greift im Hintergrundbetrieb nicht)
        for sp in o.data.splines:
            for bp in sp.bezier_points:
                bp.co, bp.handle_left, bp.handle_right = bp.co * f, bp.handle_left * f, bp.handle_right * f
            for pp in sp.points:
                pp.co = (pp.co.x * f, pp.co.y * f, pp.co.z * f, pp.co.w)
        o.location = (o.location - mitte) * f
        d = o.data
        d.dimensions = '2D'
        d.fill_mode = 'BOTH'
        # die Fase wächst sonst nach außen und schließt die Fugen: Umriss um die Fase verkleinern, Tiefe ebenso
        d.extrude = TIEFE / 2 - FASE
        d.offset = -FASE
        d.bevel_depth = FASE
        d.bevel_resolution = 4
        # spätere SVG-Formen, die auf einer früheren liegen (weißer Ring, schwarzer Punkt), ein Stück nach vorn wie aufgesetzt;
        # Formen nebeneinander (Balken, Fugen) bleiben auf einer Ebene, damit die Fuge sichtbar bleibt
        # Rahmen aus den Kurvenpunkten (bound_box ist im Hintergrundbetrieb noch nicht aktualisiert)
        pk = [Vector(bp.co[:2]) for sp in o.data.splines for bp in sp.bezier_points] + \
             [Vector(pp.co[:2]) for sp in o.data.splines for pp in sp.points]
        lx, ly = o.location.x, o.location.y
        k = (min(e.x for e in pk) + lx, min(e.y for e in pk) + ly, max(e.x for e in pk) + lx, max(e.y for e in pk) + ly)
        ebene = 0
        for (k2, e2) in kaesten:
            if k[0] < k2[2] - 1e-3 and k[2] > k2[0] + 1e-3 and k[1] < k2[3] - 1e-3 and k[3] > k2[1] + 1e-3:
                ebene = max(ebene, e2 + 1)
        kaesten.append((k, ebene))
        o.location.z += ebene * 0.06
        alt = o.active_material
        farbe = naechste_markenfarbe(tuple(alt.diffuse_color[:3])) if alt else 'schwarz'
        d.materials.clear()
        d.materials.append(material(farbe))
    # aufstellen: Icon steht senkrecht und schaut zur Kamera
    leer = bpy.data.objects.new('icon', None)
    bpy.context.scene.collection.objects.link(leer)
    for o in teile: o.parent = leer
    leer.rotation_euler = (math.radians(90), 0, 0)
    leer.location.z = hoehe * f / 2 + FASE              # steht auf dem Boden (Unterkante berührt ihn)
    return leer


def buehne(mitte_z):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    try:
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'
        sc.cycles.device = 'GPU'
    except Exception:
        pass
    sc.render.resolution_x = sc.render.resolution_y = AUFLOESUNG
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'          # Farben wie in der Marke, kein Filmlook
    # Boden fängt nur den Schatten (abgeschaltet, Icons schweben frei)
    if SCHATTEN:
        bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
        boden = bpy.context.active_object
        boden.is_shadow_catcher = True
    # Licht: groß und weich von oben links, dazu helle Umgebung
    licht = bpy.data.lights.new('studio', 'AREA')
    licht.energy, licht.size = 900, 2.5                  # kleiner und höher: kurzer Kontaktschatten statt grauer Fläche
    lo = bpy.data.objects.new('studio', licht)
    sc.collection.objects.link(lo)
    lo.location = (-1, -3, 9)
    lo.rotation_euler = (Vector((0, 0, 1)) - lo.location).to_track_quat('-Z', 'Y').to_euler()
    welt = bpy.data.worlds.new('welt')
    welt.use_nodes = True
    welt.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35 if SCHATTEN else 0.6  # ohne Boden fehlt dessen Aufhellung: Blau sonst zu dunkel
    welt.node_tree.nodes['Background'].inputs['Color'].default_value = (1, 1, 1, 1)
    sc.world = welt
    # Kamera: gerade von vorn, 12° von oben, leichte Tele-Brennweite gegen Verzerrung
    cam = bpy.data.cameras.new('kamera')
    cam.lens = 100
    co = bpy.data.objects.new('kamera', cam)
    sc.collection.objects.link(co)
    abstand = 8.5
    co.location = (0, -abstand * math.cos(math.radians(NEIGUNG)), mitte_z + abstand * math.sin(math.radians(NEIGUNG)))
    co.rotation_euler = (Vector((0, 0, mitte_z)) - co.location).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = co


def main():
    argv = sys.argv[sys.argv.index('--') + 1:]
    ziel = pathlib.Path(argv[0])
    ziel.mkdir(parents=True, exist_ok=True)
    for svg in map(pathlib.Path, argv[1:]):
        szene_leeren()
        quelle = linien_zu_flaechen(svg.resolve(), ziel)
        icon = icon_bauen(quelle)
        if quelle != svg.resolve(): quelle.unlink()
        buehne(icon.location.z)
        bpy.context.scene.render.filepath = str(ziel / f'{svg.stem}-3d.png')
        bpy.ops.render.render(write_still=True)
        print('3D-Icon geschrieben:', svg.stem)


main()
