import SwiftUI

struct OverlayView: View {
    let engine: GameEngine
    let theme: Theme
    let onAgain: () -> Void
    let onChangeMode: () -> Void

    private var ranked: [(index: Int, name: String, placed: Int)] {
        engine.state.players.enumerated()
            .map { (index: $0.offset, name: $0.element.name, placed: $0.element.placed) }
            .sorted { $0.placed > $1.placed }
    }

    var body: some View {
        ZStack {
            Color.black.opacity(0.55).ignoresSafeArea()
            VStack(spacing: 12) {
                Text(engine.state.title).font(.title.bold())
                Text(engine.state.subtitle).font(.subheadline).opacity(0.85)
                VStack(spacing: 8) {
                    ForEach(ranked, id: \.index) { r in
                        HStack {
                            Text(r.name + (engine.state.winner.contains(r.index) ? " 🏆" : ""))
                            Spacer()
                            Text("\(r.placed)/10").monospacedDigit()
                        }
                        .padding(.horizontal, 12).padding(.vertical, 8)
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(engine.state.winner.contains(r.index) ? theme.accent.opacity(0.25) : Color.white.opacity(0.06))
                        )
                    }
                }
                .frame(maxWidth: 320)
                HStack(spacing: 12) {
                    Button("Play Again", action: onAgain)
                        .buttonStyle(.borderedProminent).tint(theme.accentDeep)
                    Button("Change Mode", action: onChangeMode)
                        .buttonStyle(.bordered)
                }
                .padding(.top, 6)
            }
            .padding(24)
            .frame(maxWidth: 360)
            .background(RoundedRectangle(cornerRadius: 20).fill(.regularMaterial))
            .padding(.horizontal, 16)
        }
    }
}