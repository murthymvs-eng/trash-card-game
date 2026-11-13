import SwiftUI

/// Looping confetti rain drawn on a canvas (non-interactive overlay).
struct ConfettiView: View {
    private let colors: [Color] = [
        Color(hex: "f5c518"), Color(hex: "ff5d5d"), Color(hex: "5dd3ff"),
        Color(hex: "7bff7b"), Color(hex: "c77bff"), .white
    ]

    var body: some View {
        TimelineView(.animation) { timeline in
            Canvas { ctx, size in
                let t = timeline.date.timeIntervalSinceReferenceDate
                for i in 0..<170 {
                    let seed = Double(i)
                    let speed = 30 + seed.truncatingRemainder(dividingBy: 50)
                    let x = ((seed * 265.4435761).truncatingRemainder(dividingBy: size.width))
                    let y = ((t * speed) + seed * 17).truncatingRemainder(dividingBy: size.height + 60) - 30
                    let w = 6 + seed.truncatingRemainder(dividingBy: 6)
                    let rect = CGRect(x: x < 0 ? x + size.width : x, y: y, width: w, height: w * 1.5)
                    ctx.fill(Path(ellipseIn: rect), with: .color(colors[i % colors.count].opacity(0.9)))
                }
            }
        }
        .allowsHitTesting(false)
        .ignoresSafeArea()
    }
}