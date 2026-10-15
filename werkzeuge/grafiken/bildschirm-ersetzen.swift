// Ersetzt den Bildschirminhalt eines Foto-Mockups durch eine Website-Aufnahme (Anna 16.10.2026, Jana: MacBook mit fremder Seite).
// Ersetzt wird die Fläche zwischen den vier Ecken mit geglätteten Kanten; nur dunkle Pixel des Fotos in einem Saum am Rand bleiben stehen,
// so bleiben Rahmen, Kerbe (Notch) und Rundungen aus dem Foto erhalten. Die Seite wird perspektivisch auf die vier Ecken gelegt.
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/bildschirm-ersetzen.swift FOTO.jpg SEITE.jpg AUS.jpg SAUM SCHWELLE UNUSED  OLx OLy ORx ORy URx URy ULx ULy [HELLIGKEIT] [QUALITÄT]
import Foundation
import CoreImage
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 15 else { print("Aufruf: FOTO SEITE AUS SAUM SCHWELLE UNUSED OLx OLy ORx ORy URx URy ULx ULy [HELLIGKEIT] [QUALITÄT]"); exit(1) }
let fotoCG = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!, 0, nil)!
let W = fotoCG.width, H = fotoCG.height
let hell = a.count > 15 ? Double(a[15])! : 0.95, q = a.count > 16 ? Double(a[16])! : 0.88
func bitmap(_ bild: CGImage) -> [UInt8] {
  let c = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
  c.draw(bild, in: CGRect(x: 0, y: 0, width: W, height: H))
  return Array(UnsafeBufferPointer(start: c.data!.bindMemory(to: UInt8.self, capacity: W * H * 4), count: W * H * 4))
}
var foto = bitmap(fotoCG)
// 1. Maske: Viereck der Ecken; im Saum (Abstand zum Rand < SAUM) bleiben dunkle Foto-Pixel stehen (Kerbe, Rahmen, Rundung)
let saum = Double(a[4])!, schwelle = Int(a[5])!
let e = (7...14).map { Double(a[$0])! }
let ecken = [(e[0], e[1]), (e[2], e[3]), (e[4], e[5]), (e[6], e[7])]
func abstand(_ x: Double, _ y: Double) -> Double {   // > 0 innen: kleinster Abstand zu den vier Kanten
  var m = Double.infinity
  for i in 0..<4 { let (x1, y1) = ecken[i], (x2, y2) = ecken[(i + 1) % 4]
    let d = ((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) / hypot(x2 - x1, y2 - y1); m = min(m, d) }
  return m
}
// 2. Seite perspektivisch auf die Ecken legen
// Seite etwas größer als das Viereck, damit der überstehende Saum gefüllt ist
let roh = (7...14).map { CGFloat(Double(a[$0])!) }
let mx = (roh[0] + roh[2] + roh[4] + roh[6]) / 4, my = (roh[1] + roh[3] + roh[5] + roh[7]) / 4
let p = roh.enumerated().map { (i, v) in i % 2 == 0 ? mx + (v - mx) * 1.006 : my + (v - my) * 1.006 }
func pkt(_ x: CGFloat, _ y: CGFloat) -> CIVector { CIVector(x: x, y: CGFloat(H) - y) }
var seite = CIImage(contentsOf: URL(fileURLWithPath: a[2]))!
seite = seite.applyingFilter("CIColorControls", parameters: [kCIInputBrightnessKey: hell - 1])
seite = seite.applyingFilter("CIPerspectiveTransform", parameters: ["inputTopLeft": pkt(p[0], p[1]), "inputTopRight": pkt(p[2], p[3]),
  "inputBottomRight": pkt(p[4], p[5]), "inputBottomLeft": pkt(p[6], p[7])])
let leer = CIImage(color: CIColor(red: 0, green: 0, blue: 0, alpha: 0)).cropped(to: CGRect(x: 0, y: 0, width: W, height: H))
let ctx = CIContext()
let seiteCG = ctx.createCGImage(seite.composited(over: leer), from: CGRect(x: 0, y: 0, width: W, height: H))!
let s = bitmap(seiteCG)
let q2 = roh.enumerated().map { (i, v) in i % 2 == 0 ? mx + (v - mx) * 1.0025 : my + (v - my) * 1.0025 }   // Maske einen Hauch größer: kein Saum der alten Farbe
// 3. Weiche Maske (Kantenglättung): weiße Fläche in Seitengröße auf dieselben Ecken verzerrt; in der Kerbe/den Rundungen
//    (dunkle Foto-Pixel im Saum am Rand) bleibt das Foto stehen
let weiss = CIImage(color: CIColor(red: 1, green: 1, blue: 1)).cropped(to: CIImage(contentsOf: URL(fileURLWithPath: a[2]))!.extent)
  .applyingFilter("CIPerspectiveTransform", parameters: ["inputTopLeft": pkt(q2[0], q2[1]), "inputTopRight": pkt(q2[2], q2[3]),
    "inputBottomRight": pkt(q2[4], q2[5]), "inputBottomLeft": pkt(q2[6], q2[7])])
let mCG = ctx.createCGImage(weiss.composited(over: leer), from: CGRect(x: 0, y: 0, width: W, height: H))!
let mk = bitmap(mCG)
for y in 0..<H { for x in 0..<W {
  let k = y * W + x, i = k * 4
  var al = Double(mk[i + 3]) / 255; if al <= 0 { continue }
  let r = Int(foto[i]), g = Int(foto[i + 1]), bl = Int(foto[i + 2])
  // Kerbe/Rahmen: dunkel UND grau (ohne Farbe) – die alte Seite ist farbig und wird immer ersetzt
  let d = abstand(Double(x), Double(y)), dunkel = (r + g + bl) / 3 < schwelle && max(r, g, bl) - min(r, g, bl) < 40
  if d < saum && dunkel { al = 0 }
  for c in 0..<3 { foto[i + c] = UInt8(Double(s[i + c]) * al + Double(foto[i + c]) * (1 - al)) } } }
let aus = CGContext(data: &foto, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[3]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(ziel, aus.makeImage()!, [kCGImageDestinationLossyCompressionQuality: q] as CFDictionary)
CGImageDestinationFinalize(ziel)
print(a[3], W, H)
