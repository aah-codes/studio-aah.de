// Setzt eine Website-Aufnahme in den geraden (frontalen) Bildschirm eines Foto-Mockups ein (Anna 15.10.2026: nur echte Mockups).
// Schneidet das Foto zu, vergrößert es um FAKTOR (damit die Seite im Bildschirm scharf ist) und legt die Aufnahme genau in das
// Bildschirm-Rechteck, mit einem leichten Glanz von oben links. Koordinaten in Pixeln des Originalfotos, von oben links.
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/bildschirm-einsetzen.swift FOTO.jpg SEITE.jpg AUS.jpg  ZX ZY ZB ZH  BX BY BB BH  [FAKTOR] [QUALITÄT]
//   Z… = Zuschnitt des Fotos, B… = Bildschirm im Foto
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 12 else { print("Aufruf: FOTO SEITE AUS ZX ZY ZB ZH BX BY BB BH [FAKTOR] [QUALITÄT]"); exit(1) }
func laden(_ p: String) -> CGImage { CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: p) as CFURL, nil)!, 0, nil)! }
let foto = laden(a[1]), seite = laden(a[2])
let z = (4...7).map { CGFloat(Double(a[$0])!) }, b = (8...11).map { CGFloat(Double(a[$0])!) }
let f = a.count > 12 ? CGFloat(Double(a[12])!) : 2, q = a.count > 13 ? Double(a[13])! : 0.86
let W = Int(z[2] * f), H = Int(z[3] * f)
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
ctx.interpolationQuality = .high
// Foto: Zuschnitt (CG zählt von unten)
let teil = foto.cropping(to: CGRect(x: z[0], y: z[1], width: z[2], height: z[3]))!
ctx.draw(teil, in: CGRect(x: 0, y: 0, width: W, height: H))
// Bildschirm-Rechteck im Ergebnis
let r = CGRect(x: (b[0] - z[0]) * f, y: CGFloat(H) - (b[1] - z[1] + b[3]) * f, width: b[2] * f, height: b[3] * f)
ctx.draw(seite, in: r)
// leichter Glanz von oben links
ctx.saveGState(); ctx.clip(to: r)
let glanz = CGGradient(colorsSpace: CGColorSpace(name: CGColorSpace.sRGB)!, colors: [CGColor(gray: 1, alpha: 0.10), CGColor(gray: 1, alpha: 0)] as CFArray, locations: [0, 1])!
ctx.drawLinearGradient(glanz, start: CGPoint(x: r.minX, y: r.maxY), end: CGPoint(x: r.minX + r.width * 0.45, y: r.maxY - r.height * 0.8), options: [])
ctx.restoreGState()
let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[3]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(ziel, ctx.makeImage()!, [kCGImageDestinationLossyCompressionQuality: q] as CFDictionary)
CGImageDestinationFinalize(ziel)
print(a[3], W, H)
