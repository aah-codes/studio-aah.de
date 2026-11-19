import PDFKit; import AppKit
let a = CommandLine.arguments; let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
for i in 0..<doc.pageCount { let p = doc.page(at: i)!; let r = p.bounds(for: .mediaBox); let s = CGFloat(Double(a[3])!)
  let img = NSImage(size: NSSize(width: r.width*s, height: r.height*s)); img.lockFocus()
  NSColor.white.set(); NSRect(x:0,y:0,width:r.width*s,height:r.height*s).fill()
  let c = NSGraphicsContext.current!.cgContext; c.scaleBy(x: s, y: s); p.draw(with: .mediaBox, to: c); img.unlockFocus()
  let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!; try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "\(a[2])/seite-\(i+1).png")) }
