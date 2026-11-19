// Fächert die gerenderten Seiten 1, 2, 3, 7, 8 des Musterberichts auf (Anna 20.11.2026: alle Blätter sichtbar).
// Aufruf: swift werkzeuge/grafiken/pruefbericht/faecher.swift ZIEL.png ORDNER_MIT_seite-N.png
// Danach mit sips verkleinern (2400, 1200, 640 px) und mit cwebp nach website/bilder/website-check/pruefbericht-mockup*.webp.
import AppKit
// Fächer: Blätter von links (hinten) nach rechts (vorn), jedes deutlich sichtbar
let a = CommandLine.arguments; let ziel = a[1]; let ordner = a[2]
let seiten = [1, 2, 3, 7, 8]; let winkel: [CGFloat] = [-4, 2, -2, 3, -1.5]
let B: CGFloat = 4000, H: CGFloat = 1800, hoehe: CGFloat = 1400, abstand: CGFloat = 700
let breite = hoehe * 210 / 297
let cs = CGColorSpaceCreateDeviceRGB()
let ctx = CGContext(data: nil, width: Int(B), height: Int(H), bitsPerComponent: 8, bytesPerRow: 0, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
let start = (B - (breite + abstand * CGFloat(seiten.count - 1))) / 2
for (i, s) in seiten.enumerated() {
  let bild = NSImage(contentsOfFile: "\(ordner)/seite-\(s).png")!.cgImage(forProposedRect: nil, context: nil, hints: nil)!
  let mx = start + breite / 2 + abstand * CGFloat(i), my = H / 2 + (i % 2 == 0 ? 10 : -10)
  ctx.saveGState()
  ctx.translateBy(x: mx, y: my); ctx.rotate(by: winkel[i] * .pi / 180)
  ctx.setShadow(offset: CGSize(width: 0, height: -26), blur: 60, color: CGColor(red: 0.05, green: 0.06, blue: 0.07, alpha: 0.28))
  ctx.draw(bild, in: CGRect(x: -breite / 2, y: -hoehe / 2, width: breite, height: hoehe))
  ctx.restoreGState()
}
let rep = NSBitmapImageRep(cgImage: ctx.makeImage()!)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: ziel))
