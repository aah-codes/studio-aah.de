// anonym EIN AUS BREITE RADIUS: verkleinern und ganz weichzeichnen (Inhalte unlesbar, Aufbau bleibt)
import Foundation; import CoreImage; import ImageIO; import UniformTypeIdentifiers
let a = CommandLine.arguments
let q = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!; let s = Double(a[3])! / q.extent.width
let k = q.transformed(by: CGAffineTransform(scaleX: s, y: s)); let r = k.extent
let w = k.clampedToExtent().applyingGaussianBlur(sigma: Double(a[4])!).cropped(to: r)
let c = CIContext(); let cg = c.createCGImage(w, from: r)!
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, cg, [kCGImageDestinationLossyCompressionQuality: 0.8] as CFDictionary); CGImageDestinationFinalize(d); print(a[2], cg.width, cg.height)
