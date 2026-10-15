// ausschnitt EIN AUS X Y B H ZIELBREITE QUALITÄT  (Koordinaten in Quellpixeln, oben links)
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
let a = CommandLine.arguments
let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!
let bild = CGImageSourceCreateImageAtIndex(src, 0, nil)!
let r = CGRect(x: Int(a[3])!, y: Int(a[4])!, width: Int(a[5])!, height: Int(a[6])!)
let teil = bild.cropping(to: r)!
let zb = min(Int(a[7])!, teil.width); let zh = Int(Double(teil.height) * Double(zb) / Double(teil.width))
let ctx = CGContext(data: nil, width: zb, height: zh, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
ctx.interpolationQuality = .high; ctx.draw(teil, in: CGRect(x: 0, y: 0, width: zb, height: zh))
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, ctx.makeImage()!, [kCGImageDestinationLossyCompressionQuality: Double(a[8])!] as CFDictionary); CGImageDestinationFinalize(d)
print(a[2], zb, zh)
