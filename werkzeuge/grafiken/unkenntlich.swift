// Personen in Website-Aufnahmen unkenntlich machen (Anna 14.10.2026: „Mitarbeiter bitte nicht zeigen“).
// Zeichnet die angegebenen Rechtecke stark weichgezeichnet (Gauß) neu; der Rest des Bildes bleibt unverändert.
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/unkenntlich.swift EIN.jpg AUS.jpg X,Y,B,H [X,Y,B,H …]
// Koordinaten in Pixeln von oben links. Stärke: Radius = 4 % der kürzeren Rechteckseite, mindestens 18 px.
import Foundation; import CoreImage; import CoreGraphics; import ImageIO; import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 4 else { print("Aufruf: EIN.jpg AUS.jpg X,Y,B,H …"); exit(1) }
let bild = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!, 0, nil)!
let w = bild.width, h = bild.height
let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
ctx.draw(bild, in: CGRect(x: 0, y: 0, width: w, height: h))
let ci = CIContext(), quelle = CIImage(cgImage: bild)
for r in a[3...] {
    let z = r.split(separator: ",").map { Double($0)! }
    // CoreImage und CoreGraphics zählen von unten
    let rect = CGRect(x: z[0], y: Double(h) - z[1] - z[3], width: z[2], height: z[3])
    let radius = max(18, min(z[2], z[3]) * 0.04)
    let weich = quelle.clampedToExtent().applyingGaussianBlur(sigma: radius).cropped(to: rect)
    if let teil = ci.createCGImage(weich, from: rect) { ctx.draw(teil, in: rect) }
}
let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(ziel, ctx.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.8] as CFDictionary)
CGImageDestinationFinalize(ziel)
print(a[2], w, h)
