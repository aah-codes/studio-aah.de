// Setzt eine Website-Aufnahme perspektivisch in einen schräg stehenden Bildschirm eines Foto-Mockups (Anna 16.10.2026, Jana:
// Atelier-Foto mit Monitor). Ecken in Pixeln des Fotos, von oben links: oben-links, oben-rechts, unten-rechts, unten-links.
// Die Seite wird leicht an das Foto angeglichen (Helligkeit, minimale Unschärfe) und bekommt einen zarten Glanz.
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/bildschirm-perspektive.swift FOTO.jpg SEITE.jpg AUS.jpg  OLx OLy ORx ORy URx URy ULx ULy [HELLIGKEIT 0–1] [QUALITÄT]
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 12 else { print("Aufruf: FOTO SEITE AUS OLx OLy ORx ORy URx URy ULx ULy [HELLIGKEIT] [QUALITÄT]"); exit(1) }
let foto = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
var seite = CIImage(contentsOf: URL(fileURLWithPath: a[2]))!
let H = foto.extent.height
let p = (4...11).map { CGFloat(Double(a[$0])!) }
let hell = a.count > 12 ? Double(a[12])! : 0.94, q = a.count > 13 ? Double(a[13])! : 0.88
func pkt(_ x: CGFloat, _ y: CGFloat) -> CIVector { CIVector(x: x, y: H - y) }   // CoreImage zählt von unten
seite = seite.applyingFilter("CIColorControls", parameters: [kCIInputBrightnessKey: hell - 1, kCIInputSaturationKey: 0.95])
seite = seite.applyingFilter("CIPerspectiveTransform", parameters: [
  "inputTopLeft": pkt(p[0], p[1]), "inputTopRight": pkt(p[2], p[3]), "inputBottomRight": pkt(p[4], p[5]), "inputBottomLeft": pkt(p[6], p[7])])
seite = seite.applyingFilter("CIGaussianBlur", parameters: [kCIInputRadiusKey: 0.6]).cropped(to: seite.extent)
// zarter Glanz von oben links über der Seite
let glanz = CIFilter(name: "CILinearGradient", parameters: ["inputPoint0": pkt(p[0], p[1]), "inputPoint1": pkt((p[0] + p[4]) / 2, (p[1] + p[5]) / 2),
  "inputColor0": CIColor(red: 1, green: 1, blue: 1, alpha: 0.12), "inputColor1": CIColor(red: 1, green: 1, blue: 1, alpha: 0)])!.outputImage!
let maske = CIImage(color: CIColor(red: 1, green: 1, blue: 1)).cropped(to: CIImage(color: .white).extent)
  .applyingFilter("CIPerspectiveTransform", parameters: ["inputTopLeft": pkt(p[0], p[1]), "inputTopRight": pkt(p[2], p[3]), "inputBottomRight": pkt(p[4], p[5]), "inputBottomLeft": pkt(p[6], p[7])])
let glanzSeite = glanz.cropped(to: seite.extent).applyingFilter("CISourceInCompositing", parameters: [kCIInputBackgroundImageKey: seite])
var bild = glanzSeite.composited(over: seite).composited(over: foto).cropped(to: foto.extent)
_ = maske
let ctx = CIContext()
let cg = ctx.createCGImage(bild, from: foto.extent)!
let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[3]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(ziel, cg, [kCGImageDestinationLossyCompressionQuality: q] as CFDictionary)
CGImageDestinationFinalize(ziel)
print(a[3], cg.width, cg.height)
