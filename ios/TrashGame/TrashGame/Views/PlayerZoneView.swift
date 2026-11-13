import SwiftUI

/// Identifies one slot on the board (player + slot index) for drop hit-testing.
struct SlotID: Hashable {
    let player: Int
    let slot: Int
}

/// Collects every slot's frame in the "board" coordinate space.
struct SlotFrameKey: PreferenceKey {
    static var defaultValue: [SlotID: CGRect] = [:]
    static func reduce(value: inout [SlotID: CGRect], nextValue: () -> [SlotID: CGRect]) {
        value.merge(nextValue()) { _, new in new }
    }
}

struct PlayerZoneView: View {
    @ObservedObject var engine: GameEngine
    let playerIndex: Int
    let theme: Theme
    let cardW: CGFloat

    private var player: Player? {
        // The engine can be aborted (players cleared) while this view is still
        // on screen — never index blindly.
        engine.state.players.indices.contains(playerIndex) ? engine.state.players[playerIndex] : nil
    }
    private var slotH: CGFloat { cardW * 7.0 / 5.0 }
    private var active: Bool { engine.state.turn == playerIndex }

    var body: some View {
        if let p = player {
            zoneView(p: p)
        } else {
            EmptyView()
        }
    }

    private func zoneView(p: Player) -> some View {
        VStack(spacing: 4) {
            HStack(spacing: 6) {
                Text(p.name)
                    .font(.system(size: max(11, cardW * 0.24), weight: .bold))
                    .lineLimit(1)
                if active {
                    Text("TURN")
                        .font(.system(size: max(8, cardW * 0.16), weight: .bold))
                        .padding(.horizontal, 5).padding(.vertical, 2)
                        .background(theme.accent)
                        .foregroundColor(.black.opacity(0.8))
                        .clipShape(Capsule())
                }
                Spacer(minLength: 0)
                Text("\(p.placed)/10")
                    .font(.system(size: max(10, cardW * 0.2), weight: .bold))
                    .monospacedDigit()
            }
            .foregroundColor(theme.bannerInk)
            .accessibilityElement(children: .combine)
            .accessibilityLabel("\(p.name), \(p.placed) of 10 slots filled")

            LazyVGrid(columns: Array(repeating: GridItem(.fixed(cardW), spacing: 4), count: 5), spacing: 4) {
                ForEach(0..<10, id: \.self) { s in
                    SlotView(
                        card: p.slots[s],
                        playerIndex: playerIndex,
                        slotIndex: s,
                        theme: theme,
                        ghost: GameRules.slotOrder[s],
                        size: CGSize(width: cardW, height: slotH)
                    )
                }
            }
            .animation(.spring(response: 0.38, dampingFraction: 0.62), value: p.slots.compactMap { $0?.id })
        }
        .fixedSize()
    }
}

struct SlotView: View {
    let card: Card?
    let playerIndex: Int
    let slotIndex: Int
    let theme: Theme
    let ghost: String
    let size: CGSize

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 5)
                .fill(theme.slotColor())
                .overlay(RoundedRectangle(cornerRadius: 5).strokeBorder(theme.slotColor(edge: true), lineWidth: 1))
            if let card {
                CardFaceView(card: card, theme: theme)
                    .id(card.id)
                    .transition(.scale(scale: 0.6).combined(with: .opacity))
            } else {
                Text(ghost)
                    .font(.system(size: max(9, size.width * 0.24), weight: .semibold))
                    .foregroundColor(.white.opacity(0.5))
            }
        }
        .frame(width: size.width, height: size.height)
        .background(
            GeometryReader { geo in
                Color.clear.preference(key: SlotFrameKey.self,
                                      value: [SlotID(player: playerIndex, slot: slotIndex): geo.frame(in: .named("board"))])
            }
        )
        .accessibilityIdentifier("slot-\(playerIndex)-\(slotIndex)")
        .accessibilityLabel(card != nil ? "\(card!.rank) of \(card!.suit.fileName)" : "Empty slot for \(ghost)")
    }
}