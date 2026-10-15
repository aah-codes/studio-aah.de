// Schriftmuster als Bild (PNG, transparent) – für Schriften, deren Lizenz keine Weitergabe der Schriftdatei erlaubt
// (z. B. Satoshi bei Deinetwegen, Anna 15.10.2026: Repository nur SIL OFL). Die Schriftdateien bleiben außerhalb des Repositorys.
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/schriftmuster.swift REGULAR.otf BOLD.otf AUS.png NAME FARBE_HEX
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 6 else { print("Aufruf: REGULAR BOLD AUS NAME FARBE"); exit(1) }
func schrift(_ pfad: String, _ groesse: CGFloat) -> CTFont {
    let d = (CTFontManagerCreateFontDescriptorsFromURL(URL(fileURLWithPath: pfad) as CFURL) as! [CTFontDescriptor])[0]
    return CTFontCreateWithFontDescriptor(d, groesse, nil)
}
let hex = a[5].replacingOccurrences(of: "#", with: "")
let v = Int(hex, radix: 16)!
let farbe = CGColor(red: CGFloat((v >> 16) & 255) / 255, green: CGFloat((v >> 8) & 255) / 255, blue: CGFloat(v & 255) / 255, alpha: 1)
let B = 1600, H = 900
let ctx = CGContext(data: nil, width: B, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
func zeile(_ text: String, _ font: CTFont, _ x: CGFloat, _ y: CGFloat) {
    let attr = [kCTFontAttributeName: font, kCTForegroundColorAttributeName: farbe] as CFDictionary
    let linie = CTLineCreateWithAttributedString(CFAttributedStringCreate(nil, text as CFString, attr))
    ctx.textPosition = CGPoint(x: x, y: CGFloat(H) - y)
    CTLineDraw(linie, ctx)
}
zeile("Aa", schrift(a[2], 360), 40, 340)
zeile(a[4], schrift(a[2], 72), 760, 150)
zeile("Regular · Italic · Bold · Bold Italic", schrift(a[1], 34), 760, 214)
zeile("ABCDEFGHIJKLMNOPQRSTUVWXYZ", schrift(a[1], 46), 60, 560)
zeile("abcdefghijklmnopqrstuvwxyzäöüß", schrift(a[1], 46), 60, 630)
zeile("ABCDEFGHIJKLMNOPQRSTUVWXYZ", schrift(a[2], 46), 60, 760)
zeile("abcdefghijklmnopqrstuvwxyz 0123456789", schrift(a[2], 46), 60, 830)
let bild = ctx.makeImage()!
let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[3]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(ziel, bild, nil)
CGImageDestinationFinalize(ziel)
print(a[3])
