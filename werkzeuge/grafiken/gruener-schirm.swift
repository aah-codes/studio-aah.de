// Foto-Mockup mit grünem Bildschirm (z. B. aus Canva) für die Website vorbereiten (Anna 14.10.2026).
// - verkleinert das Foto auf BREITE, dunkelt grüne Ränder ab und speichert es als JPEG
// - schreibt eine Maske (PNG, durchsichtig, wo der Bildschirm ist): das Foto liegt mit der Maske über der Seite,
//   so verdecken Hand, Seitenumschlag oder Rahmen die Seite richtig
// - findet die grünen Flächen (größte zuerst) und gibt je Fläche die vier Ecken und die matrix3d aus, mit der eine
//   Seite von SW × SH CSS-Pixeln genau hineinpasst
// Aufruf: swift werkzeuge/grafiken/gruener-schirm.swift FOTO AUS.jpg MASKE.png BREITE SW SH
import Foundation; import CoreGraphics; import ImageIO; import UniformTypeIdentifiers
let a = CommandLine.arguments
guard a.count >= 7 else { print("Aufruf: FOTO AUS.jpg MASKE.png BREITE SW SH"); exit(1) }
let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!
let orig = CGImageSourceCreateImageAtIndex(src, 0, nil)!
let w = Int(a[4])!, h = Int(Double(orig.height) * Double(w) / Double(orig.width))
let rgb = CGColorSpace(name: CGColorSpace.sRGB)!
let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: rgb, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.interpolationQuality = .high; ctx.draw(orig, in: CGRect(x: 0, y: 0, width: w, height: h))
let d = ctx.data!.assumingMemoryBound(to: UInt8.self)
let mctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: rgb, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
let m = mctx.data!.assumingMemoryBound(to: UInt8.self)
// Speicher läuft von oben nach unten (Zeile 0 = oben im Bild)
var gruen = [Bool](repeating: false, count: w * h)
for i in 0..<(w * h) {
    let o = i * 4; let r = Int(d[o]), g = Int(d[o + 1]), b = Int(d[o + 2])
    let stark = g > 120 && g > r + 60 && g > b + 60, rand = g > r + 22 && g > b + 22
    gruen[i] = stark
    let alpha: UInt8 = stark ? 0 : (rand ? 0 : 255)
    if rand { d[o] = 20; d[o + 1] = 22; d[o + 2] = 24 }
    m[o] = 255 * UInt8(alpha / 255); m[o + 1] = m[o]; m[o + 2] = m[o]; m[o + 3] = alpha
}
func schreibe(_ c: CGContext, _ pfad: String, _ typ: CFString) {
    let z = CGImageDestinationCreateWithURL(URL(fileURLWithPath: pfad) as CFURL, typ, 1, nil)!
    CGImageDestinationAddImage(z, c.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.8] as CFDictionary); CGImageDestinationFinalize(z)
}
schreibe(ctx, a[2], UTType.jpeg.identifier as CFString); schreibe(mctx, a[3], UTType.png.identifier as CFString)
// zusammenhängende grüne Flächen
var marke = [Int32](repeating: 0, count: w * h); var flaechen: [(n: Int, tl: (Int, Int, Int), tr: (Int, Int, Int), br: (Int, Int, Int), bl: (Int, Int, Int))] = []
var stapel: [Int] = []
for s in 0..<(w * h) where gruen[s] && marke[s] == 0 {
    let id = Int32(flaechen.count + 1); marke[s] = id; stapel = [s]
    var f = (n: 0, tl: (0, 0, Int.max), tr: (0, 0, Int.min), br: (0, 0, Int.min), bl: (0, 0, Int.max))
    while let i = stapel.popLast() {
        let x = i % w, y = i / w; f.n += 1
        if x + y < f.tl.2 { f.tl = (x, y, x + y) }; if x - y > f.tr.2 { f.tr = (x, y, x - y) }
        if x + y > f.br.2 { f.br = (x, y, x + y) }; if x - y < f.bl.2 { f.bl = (x, y, x - y) }
        for j in [i - 1, i + 1, i - w, i + w] where j >= 0 && j < w * h && gruen[j] && marke[j] == 0 && abs(j % w - x) <= 1 { marke[j] = id; stapel.append(j) }
    }
    flaechen.append(f)
}
let sw = Double(a[5])!, sh = Double(a[6])!
func matrix(_ e: [(Double, Double)]) -> String {
    let von = [(0.0, 0.0), (sw, 0.0), (sw, sh), (0.0, sh)]; var A = [[Double]](), B = [Double]()
    for i in 0..<4 { let (x, y) = von[i], (u, v) = e[i]
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u); A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v) }
    for c in 0..<8 { var mx = c; for r in c..<8 where abs(A[r][c]) > abs(A[mx][c]) { mx = r }; A.swapAt(c, mx); B.swapAt(c, mx)
        for r in 0..<8 where r != c { let f = A[r][c] / A[c][c]; for k in c..<8 { A[r][k] -= f * A[c][k] }; B[r] -= f * B[c] } }
    let q = (0..<8).map { B[$0] / A[$0][$0] }
    return String(format: "matrix3d(%.10g,%.10g,0,%.10g,%.10g,%.10g,0,%.10g,0,0,1,0,%.10g,%.10g,0,1)", q[0], q[3], q[6], q[1], q[4], q[7], q[2], q[5])
}
print("Foto \(w)×\(h)")
for f in flaechen.sorted(by: { $0.n > $1.n }).prefix(3) where f.n > w * h / 400 {
    let e = [f.tl, f.tr, f.br, f.bl].map { (Double($0.0), Double($0.1)) }
    print("Fläche \(f.n) px: Ecken", e.map { "\(Int($0.0))|\(Int($0.1))" }.joined(separator: " "), "→", matrix(e))
}
