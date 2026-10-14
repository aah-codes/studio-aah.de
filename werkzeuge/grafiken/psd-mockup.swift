// Setzt eine Website-Aufnahme in ein Photoshop-Mockup (PSD mit „Smart Object“ für den Bildschirm) – ohne Photoshop (Anna 14.10.2026).
// Liest die Ebenen der PSD, mischt sie mit ihren Modi (Normal, Multiplizieren, Ineinanderkopieren, Linear abwedeln …) und ersetzt
// die angegebene Platzhalter-Ebene durch das eigene Bild, perspektivisch verzerrt nach ihren vier Eckpunkten.
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/psd-mockup.swift MOCKUP.psd BILD.jpg AUS.jpg --ziel "PUT YOUR DESIGN HERE" [--breite 2400]
//        [--weglassen "REMOVE THIS LAYER,smart object"] [--liste]
// --liste zeigt nur die Ebenen. Lizenz der Mockups beachten: das leere Mockup nie ins Repository, nur fertige Bilder.
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

struct Kanal { let id: Int16; let laenge: UInt32 }
final class Ebene {
    var name = "", oben = 0, links = 0, unten = 0, rechts = 0, kanaele: [Kanal] = [], modus = "norm", deckkraft = 255
    var schnitt = false, versteckt = false, gruppe = 0, platziert: [Double]? = nil, daten: [Int16: [UInt8]] = [:]
    var maske: (o: Int, l: Int, u: Int, r: Int, standard: UInt8)? = nil  // Ebenenmaske (Kanal -2)
    var breite: Int { rechts - links }; var hoehe: Int { unten - oben }
}

let a = CommandLine.arguments
func option(_ n: String) -> String? { a.firstIndex(of: n).map { a[$0 + 1] } }
guard a.count >= 2 else { print("Aufruf: MOCKUP.psd BILD.jpg AUS.jpg --ziel EBENE [--breite 2400] [--weglassen A,B] [--liste]"); exit(1) }
let nurListe = a.contains("--liste")
let d = try! Data(contentsOf: URL(fileURLWithPath: a[1]), options: .alwaysMapped)
var p = 0
func u8() -> Int { defer { p += 1 }; return Int(d[p]) }
func u16() -> Int { defer { p += 2 }; return Int(d[p]) << 8 | Int(d[p + 1]) }
func i16() -> Int16 { Int16(bitPattern: UInt16(u16())) }
func u32() -> UInt32 { defer { p += 4 }; return UInt32(d[p]) << 24 | UInt32(d[p + 1]) << 16 | UInt32(d[p + 2]) << 8 | UInt32(d[p + 3]) }
func i32() -> Int { Int(Int32(bitPattern: u32())) }
func f64() -> Double { var b: UInt64 = 0; for _ in 0..<8 { b = b << 8 | UInt64(u8()) }; return Double(bitPattern: b) }
func text(_ n: Int) -> String { defer { p += n }; return String(bytes: d[p..<p + n], encoding: .isoLatin1) ?? "" }

guard text(4) == "8BPS", u16() == 1 else { print("Keine PSD (PSB wird nicht unterstützt)"); exit(1) }
p += 6; _ = u16(); let H = Int(u32()), W = Int(u32()); let tiefe = u16(); _ = u16()
guard tiefe == 8 else { print("Nur 8 Bit pro Kanal"); exit(1) }
p += Int(u32()); p += Int(u32()); _ = u32(); _ = u32()
let anzahl = abs(Int(i16()))
var ebenen: [Ebene] = []
for _ in 0..<anzahl {
    let e = Ebene(); e.oben = i32(); e.links = i32(); e.unten = i32(); e.rechts = i32()
    for _ in 0..<u16() { e.kanaele.append(Kanal(id: i16(), laenge: u32())) }
    p += 4; e.modus = text(4); e.deckkraft = u8(); e.schnitt = u8() == 1; e.versteckt = (u8() & 2) != 0; p += 1
    let extraLaenge = Int(u32()); let ende = p + extraLaenge
    let mlen = Int(u32()); let mstart = p
    if mlen >= 18 { let mo = i32(), ml = i32(), mu = i32(), mr = i32(); e.maske = (mo, ml, mu, mr, UInt8(u8())) }
    p = mstart + mlen; p += Int(u32())
    let nl = u8(); e.name = text(nl); p += (4 - (nl + 1) % 4) % 4
    while p < ende {
        p += 4; let schluessel = text(4); let ln = Int(u32()); let start = p
        if schluessel == "lsct" { let typ = Int(u32()); e.gruppe = typ; if ln >= 12 { p += 4; e.modus = text(4) } }
        if schluessel == "PlLd" { p += 8; let n = u8(); p += n; p += 16; e.platziert = (0..<8).map { _ in f64() } }
        p = start + ln + (ln % 2)
    }
    p = ende; ebenen.append(e)
}
// Gruppen: Trennmarke (3) unten, Kopf (1/2) oben; Sichtbarkeit erbt sich
var stapel: [Int] = []; var eltern = [Int?](repeating: nil, count: ebenen.count)
for (i, e) in ebenen.enumerated() {
    eltern[i] = stapel.last
    if e.gruppe == 3 { stapel.append(i) } else if e.gruppe == 1 || e.gruppe == 2 { if let s = stapel.popLast() { eltern[s] = stapel.last; ebenen[s].versteckt = e.versteckt; eltern[i] = stapel.last } }
}
func sichtbar(_ i: Int) -> Bool { var j: Int? = i; while let k = j { if ebenen[k].versteckt { return false }; j = eltern[k] }; return true }
if nurListe {
    for (i, e) in ebenen.enumerated() { print(i, e.name, e.modus, e.deckkraft, e.schnitt ? "geschnitten" : "", sichtbar(i) ? "" : "versteckt", e.platziert != nil ? "Smart Object" : "", e.links, e.oben, e.breite, e.hoehe) }
    exit(0)
}
let ziele = Set((option("--ziel") ?? "").split(separator: ",").map(String.init)); let weg = Set((option("--weglassen") ?? "").split(separator: ",").map(String.init))
let ausBreite = Int(option("--breite") ?? "2400")!; let s = CGFloat(ausBreite) / CGFloat(W)
// Kanaldaten lesen (nur für benötigte Ebenen entpacken)
for e in ebenen {
    for k in e.kanaele {
        let ende = p + Int(k.laenge); let komp = u16(); let m = e.maske
        let w = k.id == -2 ? (m.map { $0.r - $0.l } ?? 0) : e.breite, h = k.id == -2 ? (m.map { $0.u - $0.o } ?? 0) : e.hoehe
        if w > 0 && h > 0 && k.id >= -2 {
            var buf = [UInt8](repeating: 0, count: w * h)
            if komp == 0 { buf.withUnsafeMutableBufferPointer { b in d.copyBytes(to: b, from: p..<p + w * h) } }
            else if komp == 1 {
                var zl: [Int] = []; for _ in 0..<h { zl.append(u16()) }
                var o = 0
                for z in 0..<h {
                    var q = p; let zende = p + zl[z]; var x = 0
                    while q < zende && x < w {
                        let n = Int(Int8(bitPattern: d[q])); q += 1
                        if n >= 0 { let c = min(n + 1, w - x); for t in 0..<c { buf[o + x + t] = d[q + t] }; q += n + 1; x += c }
                        else if n > -128 { let c = min(1 - n, w - x); let v = d[q]; for t in 0..<c { buf[o + x + t] = v }; q += 1; x += c }
                    }
                    p = zende; o += w
                }
            } else { print("Kompression \(komp) nicht unterstützt (Ebene \(e.name))") }
            e.daten[k.id] = buf
        }
        p = ende
    }
}
let farbraum = CGColorSpace(name: CGColorSpace.sRGB)!
let rahmen = CGRect(x: 0, y: 0, width: CGFloat(W) * s, height: CGFloat(H) * s)
func bild(_ e: Ebene) -> CIImage? {
    guard let r = e.daten[0], let g = e.daten[1], let b = e.daten[2] else { return nil }
    let al = e.daten[-1]; let n = e.breite * e.hoehe; var px = [UInt8](repeating: 0, count: n * 4)
    for i in 0..<n { let aa = al?[i] ?? 255; let f = Int(aa); px[i * 4] = UInt8(Int(r[i]) * f / 255); px[i * 4 + 1] = UInt8(Int(g[i]) * f / 255); px[i * 4 + 2] = UInt8(Int(b[i]) * f / 255); px[i * 4 + 3] = aa }
    let prov = CGDataProvider(data: Data(px) as CFData)!
    let cg = CGImage(width: e.breite, height: e.hoehe, bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: e.breite * 4, space: farbraum,
                     bitmapInfo: CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue), provider: prov, decode: nil, shouldInterpolate: true, intent: .defaultIntent)!
    var ci = CIImage(cgImage: cg).transformed(by: CGAffineTransform(scaleX: s, y: s))
    ci = ci.transformed(by: CGAffineTransform(translationX: CGFloat(e.links) * s, y: CGFloat(H - e.unten) * s))
    if e.deckkraft < 255 { ci = ci.applyingFilter("CIColorMatrix", parameters: ["inputAVector": CIVector(x: 0, y: 0, z: 0, w: CGFloat(e.deckkraft) / 255)]) }
    return ci
}
func maskenbild(_ e: Ebene) -> CIImage? {
    guard let m = e.maske, let md = e.daten[-2] else { return nil }
    let w = m.r - m.l, h = m.u - m.o; var px = [UInt8](repeating: 0, count: w * h * 4)
    for i in 0..<(w * h) { let v = md[i]; px[i * 4] = v; px[i * 4 + 1] = v; px[i * 4 + 2] = v; px[i * 4 + 3] = v }
    let cg = CGImage(width: w, height: h, bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: w * 4, space: farbraum,
                     bitmapInfo: CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue), provider: CGDataProvider(data: Data(px) as CFData)!, decode: nil, shouldInterpolate: true, intent: .defaultIntent)!
    var ci = CIImage(cgImage: cg).transformed(by: CGAffineTransform(scaleX: s, y: s)).transformed(by: CGAffineTransform(translationX: CGFloat(m.l) * s, y: CGFloat(H - m.u) * s))
    if m.standard > 127 { ci = ci.composited(over: CIImage(color: CIColor(red: 1, green: 1, blue: 1)).cropped(to: rahmen).applyingFilter("CISourceOutCompositing", parameters: [kCIInputBackgroundImageKey: ci.cropped(to: ci.extent)])) }
    return ci
}
let modi = ["norm": "CISourceOverCompositing", "mul ": "CIMultiplyBlendMode", "scrn": "CIScreenBlendMode", "over": "CIOverlayBlendMode", "lbrn": "CILinearBurnBlendMode",
            "lddg": "CILinearDodgeBlendMode", "lLit": "CILinearLightBlendMode", "sLit": "CISoftLightBlendMode", "hLit": "CIHardLightBlendMode", "dark": "CIDarkenBlendMode", "lite": "CILightenBlendMode"]
var gesamt = CIImage(color: CIColor(red: 1, green: 1, blue: 1)).cropped(to: rahmen)
var schnittBasis: CIImage? = nil
for (i, e) in ebenen.enumerated() where e.gruppe == 0 && sichtbar(i) && !weg.contains(e.name) {
    var ebene: CIImage? = nil
    if ziele.contains(e.name), let c = e.platziert, a.count > 3 {
        // eigenes Bild perspektivisch auf die vier Ecken des Smart Objects legen
        let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, nil)!; let quelle = CIImage(cgImage: CGImageSourceCreateImageAtIndex(src, 0, nil)!)
        let pt = { (x: Double, y: Double) in CIVector(x: CGFloat(x) * s, y: CGFloat(Double(H) - y) * s) }
        let breiteO = hypot(c[2] - c[0], c[3] - c[1]), hoeheO = hypot(c[6] - c[0], c[7] - c[1])
        let qb = quelle.extent.width, qh = min(quelle.extent.height, qb * CGFloat(hoeheO / breiteO))
        let oben = quelle.cropped(to: CGRect(x: 0, y: quelle.extent.height - qh, width: qb, height: qh))
        ebene = oben.applyingFilter("CIPerspectiveTransform", parameters: ["inputTopLeft": pt(c[0], c[1]), "inputTopRight": pt(c[2], c[3]), "inputBottomRight": pt(c[4], c[5]), "inputBottomLeft": pt(c[6], c[7])])
    } else if e.platziert != nil { continue } else { ebene = bild(e) }
    // Ebenenmaske anwenden (z. B. runde Bildschirmecken)
    if let n = ebene, let mb = maskenbild(e) { ebene = n.applyingFilter("CISourceInCompositing", parameters: [kCIInputBackgroundImageKey: mb]) }
    guard var neu = ebene else { if !e.schnitt { schnittBasis = nil }; continue }
    if e.schnitt, let basis = schnittBasis { neu = neu.applyingFilter("CISourceInCompositing", parameters: [kCIInputBackgroundImageKey: basis]) }
    else if !e.schnitt { schnittBasis = neu }
    let f = modi[e.modus] ?? "CISourceOverCompositing"
    gesamt = neu.applyingFilter(f, parameters: [kCIInputBackgroundImageKey: gesamt]).cropped(to: rahmen)
}
let ctx = CIContext(options: [.workingColorSpace: farbraum])
let cg = ctx.createCGImage(gesamt, from: rahmen, format: .RGBA8, colorSpace: farbraum)!
let aus = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[3]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(aus, cg, [kCGImageDestinationLossyCompressionQuality: 0.8] as CFDictionary); CGImageDestinationFinalize(aus)
print(a[3], cg.width, cg.height)
