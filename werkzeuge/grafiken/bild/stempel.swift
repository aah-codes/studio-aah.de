// stempel EIN AUS dx dy X Y B H [weich]: kopiert das Rechteck (X+dx, Y+dy, B, H) weich überblendet nach (X, Y) – Koordinaten von oben links
import Foundation; import CoreGraphics; import ImageIO; import UniformTypeIdentifiers
let a = CommandLine.arguments
let im = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!, 0, nil)!
let W = im.width, H = im.height, dx = Int(a[3])!, dy = Int(a[4])!, X = Int(a[5])!, Y = Int(a[6])!, B = Int(a[7])!, HH = Int(a[8])!, w = a.count > 9 ? Double(a[9])! : 12
let c = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
c.draw(im, in: CGRect(x: 0, y: 0, width: W, height: H))
let p = c.data!.bindMemory(to: UInt8.self, capacity: W * H * 4)
var kopie = [UInt8](repeating: 0, count: W * H * 4); for i in 0..<(W * H * 4) { kopie[i] = p[i] }
for y in Y..<(Y + HH) { for x in X..<(X + B) {
  let rand = Double(min(x - X, X + B - 1 - x, y - Y, Y + HH - 1 - y)); let al = min(1, max(0, rand / w))
  let sx = x + dx, sy = y + dy; guard sx >= 0, sx < W, sy >= 0, sy < H else { continue }
  // Speicher zählt von oben (CGContext-Daten), Koordinaten auch von oben
  let d = (y * W + x) * 4, s = (sy * W + sx) * 4
  for k in 0..<3 { p[d + k] = UInt8(Double(kopie[s + k]) * al + Double(kopie[d + k]) * (1 - al)) } } }
let z = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(z, c.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.85] as CFDictionary); CGImageDestinationFinalize(z); print(a[2])
