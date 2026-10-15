// Wortmarke als Bild (PNG, transparent) aus einer Systemschrift, z. B. „@JANA_VOIGTMANN“ in Helvetica (Jana, Anna 15.10.2026: Instagram-Name als Logo)
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/wortmarke.swift "TEXT" SCHRIFT.ttc#INDEX AUS.png FARBE_HEX [GRÖSSE]
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 5 else { print("Aufruf: TEXT SCHRIFT#INDEX AUS FARBE [GRÖSSE]"); exit(1) }
let teile = a[2].components(separatedBy: "#"), nr = teile.count > 1 ? Int(teile[1])! : 0
let d = (CTFontManagerCreateFontDescriptorsFromURL(URL(fileURLWithPath: teile[0]) as CFURL) as! [CTFontDescriptor])[nr]
let groesse = CGFloat(a.count > 5 ? Double(a[5])! : 120)
let font = CTFontCreateWithFontDescriptor(d, groesse, nil)
let v = Int(a[4].replacingOccurrences(of: "#", with: ""), radix: 16)!
let farbe = CGColor(red: CGFloat((v >> 16) & 255) / 255, green: CGFloat((v >> 8) & 255) / 255, blue: CGFloat(v & 255) / 255, alpha: 1)
let attr = [kCTFontAttributeName: font, kCTForegroundColorAttributeName: farbe] as CFDictionary
let linie = CTLineCreateWithAttributedString(CFAttributedStringCreate(nil, a[1] as CFString, attr))
let r = CTLineGetImageBounds(linie, nil)
let rand: CGFloat = groesse * 0.1
let B = Int(ceil(r.width + 2 * rand)), H = Int(ceil(r.height + 2 * rand))
let ctx = CGContext(data: nil, width: B, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.textPosition = CGPoint(x: rand - r.minX, y: rand - r.minY)
CTLineDraw(linie, ctx)
let ziel = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[3]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(ziel, ctx.makeImage()!, nil); CGImageDestinationFinalize(ziel)
print(a[3], B, H)
