// Bildwelt A (KI-Themenbilder, voll gebrandet): macht aus einem KI-Rohbild ein Asset-Set in allen Formaten.
// Bildkonzept: graue Szene, genau ein Gegenstand in Blau, eine große Bauhaus-Form, sichtbare Kennzeichnung „Bild: KI-generiert“.
// Braucht nur macOS (keine Installation). Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/bildwelt-a.swift ROH.png ZIELORDNER NAME FORM [FORMFARBE]
//   FORM: kreis | halbkreis | dreieck   FORMFARBE: blau (Standard) | creme | weiss
//   FORM keine = Branchenbilder (Anna, 17.11.2026, Vorbild ZDF-Kategorien): keine Form, alles außer Blau wird Schwarz-Weiß, Blau soll 40–60 % der Fläche tragen
// Ergebnis: ZIELORDNER/NAME-titel.png (1200×800), -vorschau.png (1200×630), -quadrat.png (1080×1080), -hoch.png (1080×1350);
// danach mit cwebp in WebP umwandeln (siehe bildwelt-a.sh). Das Rohbild selbst bleibt unverändert (Herkunftsdaten bleiben dort erhalten).
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 5, let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil),
      let roh = CGImageSourceCreateImageAtIndex(src, 0, nil) else {
    print("Aufruf: ROH ZIELORDNER NAME FORM [FORMFARBE]"); exit(1)
}
let ziel = a[2], name = a[3], form = a[4], formfarbe = a.count > 5 ? a[5] : "blau"
let sRGB = CGColorSpace(name: CGColorSpace.sRGB)!
let sw = form == "keine" // Schwarz-Weiß-Modus ohne Form

// Markenfarben
let BLAU: (CGFloat, CGFloat, CGFloat) = (42 / 255, 95 / 255, 230 / 255)   // #2a5fe6
let CREME: (CGFloat, CGFloat, CGFloat) = (238 / 255, 236 / 255, 231 / 255) // #eeece7
let ZIEL_FARBTON = 223.1 // Farbton (hue) von #2a5fe6 in Grad

// 1. Rohbild in einen bearbeitbaren Puffer holen
let W = roh.width, H = roh.height
let ctx0 = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4, space: sRGB,
                     bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx0.draw(roh, in: CGRect(x: 0, y: 0, width: W, height: H))
let px = ctx0.data!.bindMemory(to: UInt8.self, capacity: W * H * 4)

// 2. Blaue Flächen auf Markenblau ziehen (nur Farbton, Helligkeit und Sättigung bleiben) und Schwerpunkt des Blau-Objekts finden
var sx = 0.0, sy = 0.0, n = 0.0, tonSumme = 0.0
for y in 0..<H {
    for x in 0..<W {
        let i = (y * W + x) * 4
        let r = Double(px[i]) / 255, g = Double(px[i + 1]) / 255, b = Double(px[i + 2]) / 255
        let mx = max(r, g, b), mn = min(r, g, b), d = mx - mn
        let grau = UInt8(min(255, (0.2126 * r + 0.7152 * g + 0.0722 * b) * 255))
        func entfaerben() { if sw { px[i] = grau; px[i + 1] = grau; px[i + 2] = grau } }
        guard mx > 0, d / mx > 0.28, d > 0.12 else { entfaerben(); continue }
        var h: Double
        if mx == r { h = 60 * ((g - b) / d).truncatingRemainder(dividingBy: 6) }
        else if mx == g { h = 60 * ((b - r) / d + 2) }
        else { h = 60 * ((r - g) / d + 4) }
        if h < 0 { h += 360 }
        guard h > 185, h < 265 else { entfaerben(); continue }
        tonSumme += h; sx += Double(x); sy += Double(y); n += 1
        // Farbton ersetzen (HSV), Wert und Sättigung behalten
        let s = d / mx, v = mx, hh = ZIEL_FARBTON / 60
        let c = v * s, xx = c * (1 - abs(hh.truncatingRemainder(dividingBy: 2) - 1)), m = v - c
        var (nr, ng, nb) = (0.0, 0.0, 0.0)
        switch Int(hh) { case 3: (nr, ng, nb) = (0, xx, c); default: (nr, ng, nb) = (xx, 0, c) }
        px[i] = UInt8(min(255, (nr + m) * 255)); px[i + 1] = UInt8(min(255, (ng + m) * 255)); px[i + 2] = UInt8(min(255, (nb + m) * 255))
    }
}
let anteil = n / Double(W * H)
let fx = n > 0 ? sx / n / Double(W) : 0.5
let fy = n > 0 ? 1 - sy / n / Double(H) : 0.5 // CoreGraphics zählt y von unten
print(String(format: "%@: Blau-Anteil %.1f %%, mittlerer Farbton vorher %.0f° (Ziel %.0f°), Schwerpunkt x %.2f y %.2f",
             name, anteil * 100, n > 0 ? tonSumme / n : 0, ZIEL_FARBTON, fx, 1 - fy))
if anteil < 0.004 { print("WARNUNG: kaum Blau gefunden – Motiv prüfen") }
if sw && (anteil < 0.35 || anteil > 0.65) { print(String(format: "HINWEIS: Blau-Anteil %.0f %% – Ziel für Branchen 40–60 %%", anteil * 100)) }
let bild = ctx0.makeImage()!

// 3. Formate zuschneiden (Schwerpunkt des Blau-Objekts bleibt im Bild), Form und Kennzeichnung setzen
let formate: [(String, Int, Int)] = [("titel", 1200, 800), ("vorschau", 1200, 630), ("quadrat", 1080, 1080), ("hoch", 1080, 1350)]
for (endung, bw, bh) in formate {
    let zielQuote = Double(bw) / Double(bh), quote = Double(W) / Double(H)
    var cw = Double(W), ch = Double(H)
    if zielQuote < quote { cw = Double(H) * zielQuote } else { ch = Double(W) / zielQuote }
    // Motiv leicht aus der Mitte (Drittel), damit auf der anderen Seite Platz für die Form bleibt
    let wunschX = sw ? fx - cw / Double(W) * 0.5 : (fx < 0.5 ? fx - cw / Double(W) * 0.62 : fx - cw / Double(W) * 0.38)
    let cx = min(max(0, wunschX * Double(W)), Double(W) - cw)
    let wunschY = fy - ch / Double(H) * 0.5
    let cy = min(max(0, wunschY * Double(H)), Double(H) - ch)
    let ausschnitt = bild.cropping(to: CGRect(x: cx, y: Double(H) - cy - ch, width: cw, height: ch))!
    let c = CGContext(data: nil, width: bw, height: bh, bitsPerComponent: 8, bytesPerRow: 0, space: sRGB,
                      bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    c.interpolationQuality = .high
    c.draw(ausschnitt, in: CGRect(x: 0, y: 0, width: bw, height: bh))

    // Lage des Motivs im Ausschnitt; Form auf die ruhige Seite
    let mx = (fx * Double(W) - cx) / cw
    let links = mx > 0.5
    let fw = Double(bw), fh = Double(bh), kurz = min(fw, fh)
    let farbe: (CGFloat, CGFloat, CGFloat) = formfarbe == "creme" ? CREME : (formfarbe == "weiss" ? (1, 1, 1) : BLAU)
    if !sw {
    c.saveGState()
    c.setBlendMode(.normal); c.setFillColor(red: farbe.0, green: farbe.1, blue: farbe.2, alpha: 0.94) // flach wie Bauhaus; multiplizieren wurde auf dunklem Grund schmutzig
    let pfad = CGMutablePath()
    switch form {
    case "halbkreis": // auf der Unterkante stehend
        let r = kurz * 0.42, mitteX = links ? fw * 0.22 : fw * 0.78
        pfad.addArc(center: CGPoint(x: mitteX, y: 0), radius: r, startAngle: 0, endAngle: .pi, clockwise: false)
        pfad.closeSubpath()
    case "dreieck": // gleichseitig, Spitze nach oben, Grundlinie auf der Unterkante, angeschnitten am Rand
        let s = kurz * 0.92, h = s * 0.866, mitteX = links ? fw * 0.12 : fw * 0.88
        pfad.move(to: CGPoint(x: mitteX - s / 2, y: 0)); pfad.addLine(to: CGPoint(x: mitteX + s / 2, y: 0))
        pfad.addLine(to: CGPoint(x: mitteX, y: h)); pfad.closeSubpath()
    default: // kreis, am Rand angeschnitten
        let r = kurz * 0.40, mitteX = links ? fw * 0.08 : fw * 0.92
        pfad.addEllipse(in: CGRect(x: mitteX - r, y: fh * 0.62 - r, width: 2 * r, height: 2 * r))
    }
    c.addPath(pfad); c.fillPath()
    c.restoreGState()
    }

    // Kennzeichnung (EU AI Act Art. 50): kleine Zeile unten rechts
    let text = "Bild: KI-generiert"
    let groesse = max(13, kurz * 0.016)
    let schrift = CTFontCreateWithName("HelveticaNeue-Medium" as CFString, groesse, nil)
    let attr = NSAttributedString(string: text, attributes: [
        NSAttributedString.Key(kCTFontAttributeName as String): schrift,
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): CGColor(red: 1, green: 1, blue: 1, alpha: 1)])
    let zeile = CTLineCreateWithAttributedString(attr)
    let tb = CTLineGetBoundsWithOptions(zeile, .useOpticalBounds)
    let pad = groesse * 0.55, rand = groesse * 1.1
    let box = CGRect(x: fw - rand - tb.width - 2 * pad, y: rand, width: tb.width + 2 * pad, height: groesse + pad * 1.2)
    c.setFillColor(red: 14 / 255, green: 16 / 255, blue: 17 / 255, alpha: 0.62)
    c.addPath(CGPath(roundedRect: box, cornerWidth: box.height / 2, cornerHeight: box.height / 2, transform: nil)); c.fillPath()
    c.textPosition = CGPoint(x: box.minX + pad, y: box.minY + (box.height - groesse) / 2 + groesse * 0.22)
    CTLineDraw(zeile, c)

    let url = URL(fileURLWithPath: "\(ziel)/\(name)-\(endung).png")
    let dest = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(dest, c.makeImage()!, nil)
    CGImageDestinationFinalize(dest)
}
