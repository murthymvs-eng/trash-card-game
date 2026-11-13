import SwiftUI

func animalEmoji(_ rank: String) -> String {
    switch rank {
    case "A": return "🐭"; case "2": return "🐹"; case "3": return "🐰"; case "4": return "🐱"
    case "5": return "🐶"; case "6": return "🐼"; case "7": return "🦁"; case "8": return "🐯"
    case "9": return "🦊"; case "10": return "🐲"; case "J": return "🦖"; case "Q": return "🦄"
    default: return "🐉"
    }
}

func fairyEmoji(_ rank: String) -> String {
    switch rank {
    case "A": return "👑"; case "2": return "🕊️"; case "3": return "🌹"; case "4": return "⭐"
    case "5": return "🔮"; case "6": return "☕"; case "7": return "🗝️"; case "8": return "🌙"
    case "9": return "🪄"; case "10": return "🏰"; case "J": return "🛡️"; case "Q": return "👸"
    default: return "🤴"
    }
}

/// A procedurally drawn card face for the five non-image themes.
struct NativeCardFace: View {
    let card: Card
    let style: FaceStyle

    private var ink: Color {
        if style == .classic { return card.suit.isRed ? Color(hex: "c81e26") : Color(hex: "1a1a22") }
        switch (style, card.suit) {
        case (.emoji, .spades): return Color(hex: "3b5fd9")
        case (.emoji, .clubs): return Color(hex: "2f8a3c")
        case (.emoji, .hearts): return Color(hex: "d93b5c")
        case (.emoji, .diamonds): return Color(hex: "e8862a")
        case (.neon, .spades): return Color(hex: "37e6ff")
        case (.neon, .hearts): return Color(hex: "ff4f9a")
        case (.neon, .diamonds): return Color(hex: "c46bff")
        case (.neon, .clubs): return Color(hex: "47ff9e")
        default: return Color(hex: "5a3a1e")
        }
    }

    private var faceColor: Color {
        switch style {
        case .classic: return Color(hex: "fffdf4")
        case .emoji: return Color.white.opacity(0.94)
        case .fairy: return Color(hex: "f3c6de").opacity(0.55)
        case .neon: return Color(hex: "0d0a26")
        case .wood: return Color(hex: "d9b98a")
        case .image: return Color.white
        }
    }

    private var centerEmoji: String? {
        switch style {
        case .emoji: return animalEmoji(card.rank)
        case .fairy: return fairyEmoji(card.rank)
        default: return nil
        }
    }

    var body: some View {
        GeometryReader { geo in
            let w = geo.size.width
            let h = geo.size.height
            ZStack {
                faceColor
                RoundedRectangle(cornerRadius: w * 0.06)
                    .strokeBorder(Color.black.opacity(0.18), lineWidth: max(0.4, w * 0.008))
                CornerIndex(card: card, color: ink, size: w * 0.15)
                    .position(x: w * 0.16, y: h * 0.12)
                CornerIndex(card: card, color: ink, size: w * 0.15)
                    .rotationEffect(.degrees(180))
                    .position(x: w * 0.84, y: h * 0.88)
                center(size: w * 0.58)
                    .position(x: w * 0.5, y: h * 0.5)
            }
        }
    }

    @ViewBuilder
    private func center(size: CGFloat) -> some View {
        if let emoji = centerEmoji {
            Text(emoji).font(.system(size: size))
        } else if card.isFace && style == .classic {
            VStack(spacing: size * 0.08) {
                Text(card.rank).font(.system(size: size * 0.8, weight: .bold)).foregroundColor(ink)
                Text(card.suit.glyph).font(.system(size: size * 0.4)).foregroundColor(ink)
            }
        } else {
            Text(card.suit.glyph)
                .font(.system(size: size))
                .foregroundColor(ink)
                .shadow(color: style == .neon ? ink.opacity(0.9) : .clear, radius: size * 0.14)
        }
    }
}

/// Corner rank + suit index.
struct CornerIndex: View {
    let card: Card
    let color: Color
    let size: CGFloat

    var body: some View {
        VStack(spacing: size * 0.05) {
            Text(card.rank).font(.system(size: size * 0.85, weight: .bold)).foregroundColor(color)
            Text(card.suit.glyph).font(.system(size: size * 0.7)).foregroundColor(color)
        }
        .lineLimit(1)
        .minimumScaleFactor(0.5)
    }
}