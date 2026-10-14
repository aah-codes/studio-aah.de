// Unternehmenspräsentation als Heft (Anna 14.10.2026): Seiten in Heft-Reihenfolge, leere Seiten, Kapitel-Doppelseite mit Foto
// über beide Seiten, neue Seitenzahlen. Schreibt ein PDF (Vektor, Originalseiten bleiben scharf) und auf Wunsch JPGs für die Website.
// Aufruf vom Repository-Ordner aus:
//   swift werkzeuge/grafiken/heft-druck.swift QUELLE.pdf FOTO.jpg SCHRIFT.woff2 AUS.pdf "2,-,-,1,3,…" [JPG-ORDNER BREITE]
// Reihenfolge: Seitennummern der Quelle, "-" = leere Seite, "F" = Hälfte der Foto-Doppelseite (zweimal hintereinander).
// Die erste Seite (Umschlag) und die letzte (Rückseite) bekommen keine Seitenzahl, leere Seiten auch nicht.
// Seitenzahlfeld der Vorlage: gelbes Schrägfeld unten rechts (gemessen an der Vorlage vom 02.10.2026, 1920 × 1080 pt); im Heft steht es immer außen.
import Foundation; import CoreGraphics; import ImageIO; import UniformTypeIdentifiers; import CoreText

let a = CommandLine.arguments
guard a.count >= 6 else { print("Aufruf: QUELLE.pdf FOTO.jpg SCHRIFT.woff2 AUS.pdf REIHENFOLGE [JPG-ORDNER BREITE]"); exit(1) }
let quelle = CGPDFDocument(URL(fileURLWithPath: a[1]) as CFURL)!
let foto = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, nil)!, 0, nil)!
let schriftDesc = (CTFontManagerCreateFontDescriptorsFromURL(URL(fileURLWithPath: a[3]) as CFURL) as! [CTFontDescriptor])[0]
let reihe = a[5].split(separator: ",").map { String($0).trimmingCharacters(in: .whitespaces) }
let box = quelle.page(at: 1)!.getBoxRect(.mediaBox); let W = box.width, H = box.height
let blau = CGColor(red: 0, green: 0.2, blue: 0.4, alpha: 1), gelb = CGColor(red: 0.984, green: 0.835, blue: 0.165, alpha: 1)

func schrift(_ gr: CGFloat, _ gewicht: CGFloat) -> CTFont {
    let wght = 2003265652  // Achse 'wght' der variablen Inter
    let d = CTFontDescriptorCreateCopyWithAttributes(schriftDesc, [kCTFontVariationAttribute: [wght: gewicht]] as CFDictionary)
    return CTFontCreateWithFontDescriptor(d, gr, nil)
}
// Text mit oberem linken Punkt in Seitenkoordinaten von oben (wie in der Vorlage gemessen)
func text(_ c: CGContext, _ s: String, _ x: CGFloat, _ yGrund: CGFloat, _ f: CTFont, _ farbe: CGColor, sperren: CGFloat = 0) {
    let att = NSAttributedString(string: s, attributes: [NSAttributedString.Key(kCTFontAttributeName as String): f,
                                                          NSAttributedString.Key(kCTForegroundColorAttributeName as String): farbe,
                                                          NSAttributedString.Key(kCTKernAttributeName as String): sperren])
    c.textPosition = CGPoint(x: x, y: H - yGrund); CTLineDraw(CTLineCreateWithAttributedString(att), c)
}
func seitenzahl(_ c: CGContext, _ n: Int, _ seite: CGPDFPage? = nil) {
    // Seitenzahl immer außen (Anna 14.10.2026): rechte Seiten (ungerade) unten rechts, linke Seiten (gerade) unten links.
    // Linke Seiten: altes Feld unten rechts verschwindet – die Seite wird dort, nur in diesem Rechteck, um 62 pt versetzt
    // noch einmal gezeichnet (der Inhalt direkt darüber füllt die Stelle, bleibt Vektor)
    let links = n % 2 == 0
    if links, let p = seite {
        c.saveGState(); c.clip(to: CGRect(x: 1846, y: H - 1006, width: W - 1846, height: 60))
        c.translateBy(x: 0, y: -62); c.drawPDFPage(p); c.restoreGState()
    }
    c.setFillColor(gelb); c.beginPath()
    if links {
        c.move(to: CGPoint(x: 0, y: H - 953)); c.addLine(to: CGPoint(x: W - 1858, y: H - 953)); c.addLine(to: CGPoint(x: W - 1871, y: H - 997)); c.addLine(to: CGPoint(x: 0, y: H - 997))
    } else {
        c.move(to: CGPoint(x: 1858, y: H - 953)); c.addLine(to: CGPoint(x: W, y: H - 953)); c.addLine(to: CGPoint(x: W, y: H - 997)); c.addLine(to: CGPoint(x: 1871, y: H - 997))
    }
    c.closePath(); c.fillPath()
    let s = String(format: "%02d", n), f = schrift(19, 700)
    let att = NSAttributedString(string: s, attributes: [NSAttributedString.Key(kCTFontAttributeName as String): f, NSAttributedString.Key(kCTForegroundColorAttributeName as String): blau,
                                                          NSAttributedString.Key(kCTKernAttributeName as String): 1.5])
    let l = CTLineCreateWithAttributedString(att); let b = CTLineGetBoundsWithOptions(l, .useGlyphPathBounds)
    let mitte: CGFloat = links ? W - 1894 : 1894
    c.textPosition = CGPoint(x: mitte - b.width / 2, y: H - 982); CTLineDraw(l, c)
}
func fotoHaelfte(_ c: CGContext, rechts: Bool) {
    // Foto über beide Seiten: Streifen 32:9 aus der Mitte (etwas tiefer, Stützen und Kran bleiben im Bild).
    // Foto, Blautönung und Verlauf erst in eine Bitmap rechnen: im PDF würden der beschnittene JPEG und der
    // durchsichtige Verlauf sonst falsch (ungeschnitten bzw. deckend) ausgegeben
    let fw = CGFloat(foto.width), fh = fw * H / (2 * W), fy = (CGFloat(foto.height) - fh) * 0.55
    let bw = 3840, bh = Int(Double(bw) * Double(H) / Double(2 * W))
    let bm = CGContext(data: nil, width: bw, height: bh, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    bm.interpolationQuality = .high
    bm.draw(foto.cropping(to: CGRect(x: 0, y: fy, width: fw, height: fh))!, in: CGRect(x: 0, y: 0, width: bw, height: bh))
    bm.setFillColor(CGColor(red: 0, green: 0.2, blue: 0.4, alpha: 0.3)); bm.fill(CGRect(x: 0, y: 0, width: bw, height: bh))
    let verlauf = CGGradient(colorsSpace: CGColorSpace(name: CGColorSpace.sRGB), colors: [CGColor(red: 0, green: 0.2, blue: 0.4, alpha: 0.7), CGColor(red: 0, green: 0.2, blue: 0.4, alpha: 0)] as CFArray, locations: [0, 1])!
    bm.drawLinearGradient(verlauf, start: CGPoint(x: 0, y: 0), end: CGPoint(x: 0, y: CGFloat(bh) * 0.55), options: [])
    // als JPEG einbetten (sonst landet die Bitmap unkomprimiert im PDF, rund 25 MB je Seite)
    let daten = NSMutableData(); let ziel = CGImageDestinationCreateWithData(daten, UTType.jpeg.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(ziel, bm.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.9] as CFDictionary); CGImageDestinationFinalize(ziel)
    let streifen = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithData(daten, nil)!, 0, nil)!
    c.saveGState(); c.clip(to: CGRect(x: 0, y: 0, width: W, height: H))
    c.draw(streifen, in: CGRect(x: rechts ? -W : 0, y: 0, width: 2 * W, height: H))
    c.restoreGState()
    if !rechts {
        c.setFillColor(gelb); c.fill(CGRect(x: 85, y: H - 748, width: 40, height: 6))
        text(c, "AKTUELLE BAUPROJEKTE", 140, 754, schrift(24, 600), gelb, sperren: 2.4)
        text(c, "Was gerade auf unseren", 85, 866, schrift(86, 700), CGColor(gray: 1, alpha: 1), sperren: -1.2)
        text(c, "Baustellen passiert.", 85, 952, schrift(86, 700), CGColor(gray: 1, alpha: 1), sperren: -1.2)
        text(c, "WOLFGANG BAUER INGENIEURBAU   ·   REFERENZEN", 85, 1031, schrift(15, 600), CGColor(gray: 1, alpha: 0.85), sperren: 1.8)
    }
}

var mb = CGRect(x: 0, y: 0, width: W, height: H)
let pdf = CGContext(URL(fileURLWithPath: a[4]) as CFURL, mediaBox: &mb, nil)!
var fotoSeite = 0
for (i, r) in reihe.enumerated() {
    pdf.beginPDFPage(nil)
    pdf.setFillColor(CGColor(gray: 1, alpha: 1)); pdf.fill(mb)
    let heftSeite = i + 1, rand = i == 0 || i == reihe.count - 1
    if r == "F" { fotoHaelfte(pdf, rechts: fotoSeite == 1); fotoSeite += 1; if fotoSeite == 2 { seitenzahl(pdf, heftSeite) } }
    else if r != "-" { let p = quelle.page(at: Int(r)!)!; pdf.drawPDFPage(p); if !rand { seitenzahl(pdf, heftSeite, p) } }
    pdf.endPDFPage()
}
pdf.closePDF()
print("Heft: \(reihe.count) Seiten → \(a[4])")

// JPGs für die Website (h01.jpg …)
if a.count >= 8 {
    let doc = CGPDFDocument(URL(fileURLWithPath: a[4]) as CFURL)!, breite = Double(a[7])!
    for n in 1...doc.numberOfPages {
        let p = doc.page(at: n)!, s = breite / Double(W), w = Int(Double(W) * s), h = Int(Double(H) * s)
        let c = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
        c.setFillColor(CGColor(gray: 1, alpha: 1)); c.fill(CGRect(x: 0, y: 0, width: w, height: h)); c.interpolationQuality = .high; c.scaleBy(x: s, y: s); c.drawPDFPage(p)
        let z = CGImageDestinationCreateWithURL(URL(fileURLWithPath: String(format: "%@/h%02d.jpg", a[6], n)) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
        CGImageDestinationAddImage(z, c.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.8] as CFDictionary); CGImageDestinationFinalize(z)
    }
    print("JPGs: \(doc.numberOfPages) → \(a[6])")
}
