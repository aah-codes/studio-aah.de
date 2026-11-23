// Nachschritt für icons-3d.sh: sehr schwachen Schattenschleier (graue Fläche) entfernen, Kontaktschatten behalten.
// Pixel mit geringer Deckkraft (unter SCHWELLE) werden durchsichtig, darüber wird die Deckkraft weich angehoben.
// Aufruf: swift icons-3d-schatten.swift DATEI.png [weitere.png …] (überschreibt die Dateien)
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
let SCHWELLE = 0.10
for pfad in CommandLine.arguments.dropFirst() {
  let url = URL(fileURLWithPath: pfad)
  guard let src = CGImageSourceCreateWithURL(url as CFURL, nil), let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { print("nicht lesbar:", pfad); continue }
  let w = img.width, h = img.height
  let cs = CGColorSpace(name: CGColorSpace.sRGB)!
  let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
  ctx.draw(img, in: CGRect(x: 0, y: 0, width: w, height: h))
  let p = ctx.data!.bindMemory(to: UInt8.self, capacity: w * h * 4)
  for i in stride(from: 0, to: w * h * 4, by: 4) {
    let a = Double(p[i + 3]) / 255
    if a >= 0.999 || a == 0 { continue }
    let neu = max(0, (a - SCHWELLE) / (1 - SCHWELLE))
    let f = a > 0 ? neu / a : 0
    for k in 0..<3 { p[i + k] = UInt8(min(255, Double(p[i + k]) * f)) }
    p[i + 3] = UInt8(neu * 255)
  }
  let dest = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil)!
  CGImageDestinationAddImage(dest, ctx.makeImage()!, nil); CGImageDestinationFinalize(dest)
}
