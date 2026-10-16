// Schriftstufen als Bild (PNG, transparent) – für Schriften, deren Lizenz keine Weitergabe der Datei erlaubt (Satoshi, Helvetica):
// Aufbau wie das Designsystem bei Bauer (Anna 16.10.2026: „auf allen Referenzseiten so die Typo abbilden“) – je Zeile Stufe und Maß klein,
// darunter die Probe in der echten Schrift, Größe und Zeilenabstand wie auf der Website. Die Schriftdateien bleiben außerhalb des Repositorys.
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/schriftstufen.swift STUFEN.json AUS.png
// STUFEN.json: {"breite": 1100, "massstab": 2, "zeilen": [{"stufe": "H1", "mass": "86 / 86 · 700", "schrift": "PFAD.otf" oder "PFAD.ttc#1",
//   "groesse": 86, "zeilenhoehe": 1.0, "sperrung": -1.12, "farbe": "#2A1E2B", "text": "…", "versal": false,
//   "knopf": {"grund": "#FF5000", "radius": 999, "innen": [10, 22]}}]}
// Mit "einzeln": true entsteht je Stufe nur die Probe als eigenes Bild (AUS-1.png, AUS-2.png …).
// Mit "nur_aa": {"schrift": …, "farbe": …, "groesse": 200} entsteht stattdessen nur „Aa“ (für die Schriftkarte).
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 3, let daten = try? JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath: a[1]))) as? [String: Any]
else { print("Aufruf: STUFEN.json AUS.png"); exit(1) }
let m = CGFloat((daten["massstab"] as? Double) ?? 2)
func schrift(_ angabe: String, _ groesse: CGFloat) -> CTFont {
    let teile = angabe.components(separatedBy: "#"), nr = teile.count > 1 ? Int(teile[1])! : 0
    let d = (CTFontManagerCreateFontDescriptorsFromURL(URL(fileURLWithPath: teile[0]) as CFURL) as! [CTFontDescriptor])[nr]
    return CTFontCreateWithFontDescriptor(d, groesse, nil)
}
func farbe(_ hex: String) -> CGColor {
    let v = Int(hex.replacingOccurrences(of: "#", with: ""), radix: 16)!
    return CGColor(red: CGFloat((v >> 16) & 255) / 255, green: CGFloat((v >> 8) & 255) / 255, blue: CGFloat(v & 255) / 255, alpha: 1)
}
func text(_ s: String, _ f: CTFont, _ c: CGColor, sperrung: CGFloat = 0, zeilenhoehe: CGFloat? = nil) -> NSAttributedString {
    var stil = [CTParagraphStyleSetting]()
    var zh = zeilenhoehe ?? 0
    if zeilenhoehe != nil {
        withUnsafeBytes(of: &zh) { _ in }
        stil.append(CTParagraphStyleSetting(spec: .minimumLineHeight, valueSize: MemoryLayout<CGFloat>.size, value: &zh))
        stil.append(CTParagraphStyleSetting(spec: .maximumLineHeight, valueSize: MemoryLayout<CGFloat>.size, value: &zh))
    }
    let absatz = CTParagraphStyleCreate(stil, stil.count)
    return NSAttributedString(string: s, attributes: [kCTFontAttributeName as NSAttributedString.Key: f, kCTForegroundColorAttributeName as NSAttributedString.Key: c,
        kCTKernAttributeName as NSAttributedString.Key: sperrung, kCTParagraphStyleAttributeName as NSAttributedString.Key: absatz])
}
func hoehe(_ t: NSAttributedString, _ breite: CGFloat) -> CGFloat {
    let fs = CTFramesetterCreateWithAttributedString(t)
    return ceil(CTFramesetterSuggestFrameSizeWithConstraints(fs, CFRange(location: 0, length: 0), nil, CGSize(width: breite, height: .greatestFiniteMagnitude), nil).height)
}
func zeichne(_ ctx: CGContext, _ t: NSAttributedString, _ x: CGFloat, _ yOben: CGFloat, _ breite: CGFloat, _ h: CGFloat, _ gesamt: CGFloat) {
    let fs = CTFramesetterCreateWithAttributedString(t)
    let pfad = CGPath(rect: CGRect(x: x, y: gesamt - yOben - h, width: breite, height: h), transform: nil)
    CTFrameDraw(CTFramesetterCreateFrame(fs, CFRange(location: 0, length: 0), pfad, nil), ctx)
}
func speichere(_ ctx: CGContext) {
    let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(ziel, ctx.makeImage()!, nil); CGImageDestinationFinalize(ziel); print(a[2], ctx.width, ctx.height)
}
let raum = CGColorSpace(name: CGColorSpace.sRGB)!
if let aa = daten["nur_aa"] as? [String: Any] {   // nur „Aa“ für die Schriftkarte
    let g = CGFloat(aa["groesse"] as! Double) * m
    let t = text("Aa", schrift(aa["schrift"] as! String, g), farbe(aa["farbe"] as! String), sperrung: -0.04 * g)
    let b = Int(ceil(CTLineGetTypographicBounds(CTLineCreateWithAttributedString(t), nil, nil, nil))) + Int(4 * m), h = Int(ceil(g * 0.95))
    let ctx = CGContext(data: nil, width: b, height: h, bitsPerComponent: 8, bytesPerRow: 0, space: raum, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.textPosition = CGPoint(x: 0, y: g * 0.2); CTLineDraw(CTLineCreateWithAttributedString(t), ctx); speichere(ctx); exit(0)
}
let breite = CGFloat((daten["breite"] as? Double) ?? 1100) * m, rand = 28 * m, innen = breite - 2 * rand
let klein = schrift("/System/Library/Fonts/Menlo.ttc", 11 * m), grau = farbe("#6B6F71"), linie = farbe("#D6D8D9")
struct Zeile { let kopf: NSAttributedString; let mass: NSAttributedString; let probe: NSAttributedString; let hp: CGFloat; let knopf: [String: Any]?; let pb: CGFloat }
var zeilen = [Zeile]()
for z in daten["zeilen"] as! [[String: Any]] {
    let g = CGFloat(z["groesse"] as! Double) * m, zh = CGFloat((z["zeilenhoehe"] as? Double) ?? 1.2) * g
    var s = z["text"] as! String; if (z["versal"] as? Bool) == true { s = s.uppercased() }
    let probe = text(s, schrift(z["schrift"] as! String, g), farbe((z["farbe"] as? String) ?? "#0E1011"), sperrung: CGFloat((z["sperrung"] as? Double) ?? 0) * m, zeilenhoehe: zh)
    let knopf = z["knopf"] as? [String: Any]
    let innenAbstand = (knopf?["innen"] as? [Double]).map { CGFloat($0[1]) * m } ?? 0
    let pb = knopf != nil ? ceil(CTLineGetTypographicBounds(CTLineCreateWithAttributedString(probe), nil, nil, nil)) + 2 * innenAbstand : innen
    // Umbruchbreite: Spaltenbreite, aber nie schmaler als das längste Wort (sonst bricht „Workplaces.“ mitten im Wort)
    let wortmax = s.split(separator: " ").map { w -> CGFloat in
        let l = CTLineCreateWithAttributedString(text(String(w), schrift(z["schrift"] as! String, g), farbe("#000000"), sperrung: CGFloat((z["sperrung"] as? Double) ?? 0) * m))
        return CGFloat(CTLineGetTypographicBounds(l, nil, nil, nil)) }.max() ?? 0
    let wb = max(innen, ceil(wortmax) + 2 * m)
    zeilen.append(Zeile(kopf: text((z["stufe"] as! String).uppercased(), klein, farbe("#0E1011"), sperrung: 0.6 * m),
                        mass: text(z["mass"] as! String, klein, grau), probe: probe, hp: hoehe(probe, knopf != nil ? .greatestFiniteMagnitude : wb), knopf: knopf, pb: knopf != nil ? pb : wb))
}
if (daten["einzeln"] as? Bool) == true {   // je Stufe nur die Probe als eigenes Bild (AUS-1.png …); Stufe und Maß setzt die Website als Text
    for (n, z) in zeilen.enumerated() {
        let iv = (z.knopf?["innen"] as? [Double]).map { CGFloat($0[0]) * m } ?? 0, ih = (z.knopf?["innen"] as? [Double]).map { CGFloat($0[1]) * m } ?? 0
        // Breite = längste Zeile (sonst verkleinert die Website das Bild), unten Platz für Unterlängen bei engem Zeilenabstand
        var maxw: CGFloat = 0
        let fr = CTFramesetterCreateFrame(CTFramesetterCreateWithAttributedString(z.probe), CFRange(location: 0, length: 0), CGPath(rect: CGRect(x: 0, y: 0, width: z.pb, height: z.hp), transform: nil), nil)
        for l in CTFrameGetLines(fr) as! [CTLine] { maxw = max(maxw, CGFloat(CTLineGetTypographicBounds(l, nil, nil, nil)) - CGFloat(CTLineGetTrailingWhitespaceWidth(l))) }
        let unten: CGFloat = z.knopf != nil ? 0 : ceil((CTFontGetDescent(z.probe.attribute(kCTFontAttributeName as NSAttributedString.Key, at: 0, effectiveRange: nil) as! CTFont)) * 0.9)
        let b = Int(z.knopf != nil ? z.pb : ceil(maxw) + 4 * m), h = Int(z.hp + 2 * iv + unten)
        let c = CGContext(data: nil, width: b, height: h, bitsPerComponent: 8, bytesPerRow: 0, space: raum, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
        if let k = z.knopf {
            let rad = min(CGFloat((k["radius"] as? Double) ?? 4) * m, CGFloat(h) / 2)
            c.addPath(CGPath(roundedRect: CGRect(x: 0, y: 0, width: b, height: h), cornerWidth: rad, cornerHeight: rad, transform: nil)); c.setFillColor(farbe(k["grund"] as! String)); c.fillPath()
        }
        zeichne(c, z.probe, ih, iv, z.knopf != nil ? CGFloat(b) : z.pb, z.hp, CGFloat(h))
        let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2].replacingOccurrences(of: ".png", with: "-\(n + 1).png")) as CFURL, UTType.png.identifier as CFString, 1, nil)!
        CGImageDestinationAddImage(ziel, c.makeImage()!, nil); CGImageDestinationFinalize(ziel); print(n + 1, b, h)
    }
    exit(0)
}
let kh = 16 * m, abstand = 10 * m, zeilenRand = 22 * m
var gesamt: CGFloat = 0
for z in zeilen { let iv = (z.knopf?["innen"] as? [Double]).map { CGFloat($0[0]) * m } ?? 0; gesamt += zeilenRand + kh * 2 + abstand + z.hp + 2 * iv + zeilenRand }
let ctx = CGContext(data: nil, width: Int(breite), height: Int(gesamt), bitsPerComponent: 8, bytesPerRow: 0, space: raum, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
var y: CGFloat = 0
for (i, z) in zeilen.enumerated() {
    y += zeilenRand
    zeichne(ctx, z.kopf, rand, y, innen, kh, gesamt); y += kh
    zeichne(ctx, z.mass, rand, y, innen, kh, gesamt); y += kh + abstand
    if let k = z.knopf {
        let iv = (k["innen"] as? [Double]).map { CGFloat($0[0]) * m } ?? 0, ih = (k["innen"] as? [Double]).map { CGFloat($0[1]) * m } ?? 0
        let r = CGRect(x: rand, y: gesamt - y - z.hp - 2 * iv, width: z.pb, height: z.hp + 2 * iv)
        let rad = min(CGFloat((k["radius"] as? Double) ?? 4) * m, r.height / 2)
        ctx.addPath(CGPath(roundedRect: r, cornerWidth: rad, cornerHeight: rad, transform: nil)); ctx.setFillColor(farbe(k["grund"] as! String)); ctx.fillPath()
        zeichne(ctx, z.probe, rand + ih, y + iv, z.pb, z.hp, gesamt); y += z.hp + 2 * iv
    } else { zeichne(ctx, z.probe, rand, y, innen, z.hp, gesamt); y += z.hp }
    y += zeilenRand
    if i < zeilen.count - 1 { ctx.setFillColor(linie); ctx.fill(CGRect(x: rand, y: gesamt - y - m, width: innen, height: m)) }
}
speichere(ctx)
