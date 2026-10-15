// Kontaktbogen: kontakt.swift AUS.jpg SPALTEN BREITE BILD…  (Beschriftung = Dateiname)
import Foundation; import CoreGraphics; import ImageIO; import UniformTypeIdentifiers; import CoreText
let a = CommandLine.arguments; let sp = Int(a[2])!, bw = CGFloat(Double(a[3])!)
let dateien = Array(a[4...]); let bilder = dateien.map { CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: $0) as CFURL, nil)!, 0, nil)! }
let maxH: CGFloat = bw * 1.2, beschr: CGFloat = 22, luecke: CGFloat = 10
let zeilen = (bilder.count + sp - 1) / sp
var zh = [CGFloat](repeating: 0, count: zeilen)
for (i, b) in bilder.enumerated() { let h = min(maxH, bw * CGFloat(b.height) / CGFloat(b.width)); zh[i / sp] = max(zh[i / sp], h) }
let W = Int(CGFloat(sp) * (bw + luecke) + luecke), H = Int(zh.reduce(0, +) + CGFloat(zeilen) * (beschr + luecke) + luecke)
let c = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
c.setFillColor(CGColor(gray: 0.85, alpha: 1)); c.fill(CGRect(x: 0, y: 0, width: W, height: H)); c.interpolationQuality = .high
var y = CGFloat(H) - luecke
for z in 0..<zeilen {
  for s in 0..<sp { let i = z * sp + s; if i >= bilder.count { break }
    let b = bilder[i]; let h = bw * CGFloat(b.height) / CGFloat(b.width); let x = luecke + CGFloat(s) * (bw + luecke)
    let sichtbar = min(h, zh[z])
    c.saveGState(); c.clip(to: CGRect(x: x, y: y - beschr - sichtbar, width: bw, height: sichtbar))
    c.draw(b, in: CGRect(x: x, y: y - beschr - h, width: bw, height: h)); c.restoreGState()
    let name = (dateien[i] as NSString).lastPathComponent.replacingOccurrences(of: ".jpg", with: "")
    let att = NSAttributedString(string: name, attributes: [NSAttributedString.Key(kCTFontAttributeName as String): CTFontCreateWithName("Helvetica-Bold" as CFString, 14, nil)])
    c.textPosition = CGPoint(x: x, y: y - 16); CTLineDraw(CTLineCreateWithAttributedString(att), c) }
  y -= zh[z] + beschr + luecke }
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, c.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.75] as CFDictionary); CGImageDestinationFinalize(d)
print(a[1], W, H)
