// QR-Code als PNG mit dem eingebauten Core-Image-Filter von macOS (nichts aus dem Netz).
// Aufruf: swift werkzeuge/grafiken/qr-code.swift "https://studio-aah.de/ki-arbeits-setup/" ziel.png [Pixel je Modul]
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else { print("Aufruf: qr-code.swift TEXT ZIEL.png [SKALA]"); exit(1) }
let skala = args.count > 3 ? CGFloat(Double(args[3]) ?? 20) : 20
let filter = CIFilter(name: "CIQRCodeGenerator")!
filter.setValue(args[1].data(using: .utf8), forKey: "inputMessage")
filter.setValue("M", forKey: "inputCorrectionLevel")
let bild = filter.outputImage!.transformed(by: CGAffineTransform(scaleX: skala, y: skala))
let rep = NSBitmapImageRep(ciImage: bild)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))
print(args[2], Int(bild.extent.width), "px")
