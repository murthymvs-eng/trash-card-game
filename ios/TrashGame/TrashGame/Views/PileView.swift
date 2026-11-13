import SwiftUI

struct PileView: View {
    let theme: Theme
    let top: Card?
    let count: Int
    let label: String
    let cardW: CGFloat
    let drawable: Bool
    let action: () -> Void

    var body: some View {
        VStack(spacing: 3) {
            ZStack {
                if count > 0 {
                    if let top { CardFaceView(card: top, theme: theme) } else { CardBackView(theme: theme) }
                } else {
                    RoundedRectangle(cornerRadius: 6)
                        .fill(theme.slotColor())
                        .overlay(RoundedRectangle(cornerRadius: 6).strokeBorder(theme.slotColor(edge: true), lineWidth: 1))
                }
            }
            .frame(width: cardW, height: cardW * 1.4)
            .overlay(RoundedRectangle(cornerRadius: 6).strokeBorder(theme.accent, lineWidth: drawable ? 2 : 0))
            Text(label).font(.system(size: max(9, cardW * 0.2))).foregroundColor(theme.bannerInk)
            Text("\(count)").font(.system(size: max(9, cardW * 0.2), weight: .bold)).foregroundColor(theme.bannerInk.opacity(0.85))
        }
        .contentShape(Rectangle())
        .onTapGesture { if drawable { action() } }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(label), \(count) card\(count == 1 ? "" : "s")")
    }
}