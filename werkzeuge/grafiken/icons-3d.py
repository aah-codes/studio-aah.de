"""3D-Fassung der Bauhaus-Icons (Formensprache STUDIO AAH!, Anna 18.11.2026: „2D führt, 3D als Akzent“).

Läuft in Blender (kostenlos, auf dem MacBook in ~/Applications/Blender.app), nicht mit dem normalen Python.
Aufruf vom Repository-Ordner aus über das Hilfsskript:
    bash werkzeuge/grafiken/icons-3d.sh ZIELORDNER website/bilder/formen/brand.svg [weitere.svg …]
Für jedes SVG entsteht ZIELORDNER/<name>-3d.png (1024 × 1024, transparenter Hintergrund mit weichem Kontaktschatten).

Alle Werte sind für jedes Icon gleich, damit das Set wie aus einem Guss wirkt (Regeln: Betrieb Studio AAH/Bildwelten/icon-system/formensprache.md, Abschnitt 5):
Tiefe 15 % der Breite, leicht abgerundete Kanten, mattes Material wie Satin-Kunststoff, Kamera gerade von vorn und 20° von oben,
ein weiches Licht von oben links, Farben exakt aus der Farbtafel (Blau berührt nie Schwarz: die Fugen der SVGs bleiben echte Spalten).
"""
import math
import pathlib
import sys

import addon_utils
import bpy
from mathutils import Vector

FARBEN = {  # sRGB-Werte der Marke (tokens.json)
    'blau': (0x2a, 0x5f, 0xe6), 'schwarz': (0x0e, 0x10, 0x11), 'weiss': (0xff, 0xff, 0xff), 'gelb': (0xff, 0xe6, 0x00),
}
TIEFE, FASE, NEIGUNG, AUFLOESUNG, SAMPLES = 0.3, 0.03, 20, 1024, 96  # Tiefe 15 % der Breite (Breite = 2)


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


def icon_bauen(svg):
    bpy.ops.import_curve.svg(filepath=str(svg))
    teile = [o for o in bpy.context.scene.objects if o.type == 'CURVE']
    # Größe normieren: breiteste Seite = 2 Einheiten, Mitte im Ursprung
    ecken = [o.matrix_world @ Vector(c) for o in teile for c in o.bound_box]
    xs, ys = [e.x for e in ecken], [e.y for e in ecken]
    breite, hoehe = max(xs) - min(xs), max(ys) - min(ys)
    f = 2 / max(breite, hoehe)
    mitte = Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0))
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
        d.extrude = TIEFE / 2
        d.bevel_depth = FASE
        d.bevel_resolution = 4
        # spätere SVG-Formen liegen oben (weißer Ring, schwarzer Punkt): je Ebene ein Stück nach vorn, wie aufgesetzt
        o.location.z += i * 0.06
        alt = o.active_material
        farbe = naechste_markenfarbe(tuple(alt.diffuse_color[:3])) if alt else 'schwarz'
        d.materials.clear()
        d.materials.append(material(farbe))
    # aufstellen: Icon steht senkrecht und schaut zur Kamera
    leer = bpy.data.objects.new('icon', None)
    bpy.context.scene.collection.objects.link(leer)
    for o in teile: o.parent = leer
    leer.rotation_euler = (math.radians(90), 0, 0)
    leer.location.z = 1 + TIEFE                          # steht auf dem Boden
    return leer


def buehne():
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
    # Boden fängt nur den Schatten
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    boden = bpy.context.active_object
    boden.is_shadow_catcher = True
    # Licht: groß und weich von oben links, dazu helle Umgebung
    licht = bpy.data.lights.new('studio', 'AREA')
    licht.energy, licht.size = 650, 5
    lo = bpy.data.objects.new('studio', licht)
    sc.collection.objects.link(lo)
    lo.location = (-4, -4, 6)
    lo.rotation_euler = (Vector((0, 0, 1)) - lo.location).to_track_quat('-Z', 'Y').to_euler()
    welt = bpy.data.worlds.new('welt')
    welt.use_nodes = True
    welt.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
    welt.node_tree.nodes['Background'].inputs['Color'].default_value = (1, 1, 1, 1)
    sc.world = welt
    # Kamera: gerade von vorn, 20° von oben, leichte Tele-Brennweite gegen Verzerrung
    cam = bpy.data.cameras.new('kamera')
    cam.lens = 100
    co = bpy.data.objects.new('kamera', cam)
    sc.collection.objects.link(co)
    abstand = 8.5
    co.location = (0, -abstand * math.cos(math.radians(NEIGUNG)), 1 + TIEFE + abstand * math.sin(math.radians(NEIGUNG)))
    co.rotation_euler = (Vector((0, 0, 1 + TIEFE)) - co.location).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = co


def main():
    argv = sys.argv[sys.argv.index('--') + 1:]
    ziel = pathlib.Path(argv[0])
    ziel.mkdir(parents=True, exist_ok=True)
    for svg in map(pathlib.Path, argv[1:]):
        szene_leeren()
        icon_bauen(svg.resolve())
        buehne()
        bpy.context.scene.render.filepath = str(ziel / f'{svg.stem}-3d.png')
        bpy.ops.render.render(write_still=True)
        print('3D-Icon geschrieben:', svg.stem)


main()
