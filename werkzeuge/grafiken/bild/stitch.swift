// stitch AUS BREITE QUELLE y1 y2 [QUELLE y1 y2 ...] (y in Quellpixeln)
import Foundation; import CoreGraphics; import ImageIO; import UniformTypeIdentifiers
let a = CommandLine.arguments; let bw = Int(a[2])!; var teile: [(CGImage, CGFloat)] = []; var gesamt: CGFloat = 0; var i = 3
while i + 2 < a.count { let s = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[i]) as CFURL, nil)!; let im = CGImageSourceCreateImageAtIndex(s, 0, nil)!
  let t = im.cropping(to: CGRect(x: 0, y: Int(a[i+1])!, width: im.width, height: Int(a[i+2])! - Int(a[i+1])!))!; let h = CGFloat(t.height) * CGFloat(bw) / CGFloat(t.width); teile.append((t, h)); gesamt += h; i += 3 }
let c = CGContext(data: nil, width: bw, height: Int(gesamt), bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
c.interpolationQuality = .high; var y = gesamt
for (t, h) in teile { y -= h; c.draw(t, in: CGRect(x: 0, y: y, width: CGFloat(bw), height: h)) }
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, c.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.62] as CFDictionary); CGImageDestinationFinalize(d); print(a[1], bw, Int(gesamt))
