// Schneidet ein Bild oben auf eine Höhe zu und verkleinert es auf eine Breite (JPEG) – für Aufnahmen aus seiten-aufnahme.py.
// Braucht nur macOS (keine Installation). Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/zuschnitt.swift EIN.jpg AUS.jpg BREITE [HÖHE_IM_ERGEBNIS] [QUALITÄT 0–1]
// HÖHE_IM_ERGEBNIS: 0 oder weggelassen = ganze Höhe (nur verkleinern)
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 4, let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil),
      let bild = CGImageSourceCreateImageAtIndex(src, 0, nil) else { print("Aufruf: EIN AUS BREITE [HÖHE] [QUALITÄT]"); exit(1) }
let breite = Int(a[3])!
let faktor = Double(breite) / Double(bild.width)
let wunsch = a.count > 4 ? Int(a[4])! : 0
let hoehe = wunsch > 0 ? min(wunsch, Int(Double(bild.height) * faktor)) : Int(Double(bild.height) * faktor)
let quelle = bild.cropping(to: CGRect(x: 0, y: 0, width: bild.width, height: Int(Double(hoehe) / faktor)))!
let ctx = CGContext(data: nil, width: breite, height: hoehe, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
ctx.interpolationQuality = .high
ctx.draw(quelle, in: CGRect(x: 0, y: 0, width: breite, height: hoehe))
let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(ziel, ctx.makeImage()!, [kCGImageDestinationLossyCompressionQuality: a.count > 5 ? Double(a[5])! : 0.72] as CFDictionary)
CGImageDestinationFinalize(ziel)
print(a[2], breite, hoehe)
