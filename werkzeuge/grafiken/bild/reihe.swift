// reihe AUS.jpg HÖHE BILD… : Bilder nebeneinander auf gleiche Höhe
import Foundation; import CoreGraphics; import ImageIO; import UniformTypeIdentifiers
let a = CommandLine.arguments; let H = CGFloat(Double(a[2])!)
let b = a[3...].map { CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: $0) as CFURL, nil)!, 0, nil)! }
let ws = b.map { H * CGFloat($0.width) / CGFloat($0.height) }; let W = Int(ws.reduce(0, +) + CGFloat(b.count + 1) * 10)
let c = CGContext(data: nil, width: W, height: Int(H) + 20, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
c.setFillColor(CGColor(gray: 0.8, alpha: 1)); c.fill(CGRect(x: 0, y: 0, width: W, height: Int(H) + 20)); c.interpolationQuality = .high
var x: CGFloat = 10; for (i, im) in b.enumerated() { c.draw(im, in: CGRect(x: x, y: 10, width: ws[i], height: H)); x += ws[i] + 10 }
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, c.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.8] as CFDictionary); CGImageDestinationFinalize(d)
