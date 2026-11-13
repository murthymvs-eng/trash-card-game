import SwiftUI
import UIKit
import Combine

/// The game board — responsive: sizes cards to fit the screen, side-by-side in
/// landscape, stacked in portrait. The drawn card is shown in the center.
struct GameView: View {
    @ObservedObject var engine: GameEngine
    let theme: Theme
    /// Drag state lives outside the engine so a drag does not re-render the board
    /// on every frame — only the ghost follows the finger.
    @StateObject private var drag = DragState()

    var body: some View {
        GeometryReader { geo in
            let W = geo.size.width, H = geo.size.height
            let landscape = W > H
            let rows = rowIndices
            let cw = cardWidth(W: W, H: H, landscape: landscape, rows: rows)
            ZStack {
                Group {
                    if landscape {
                        HStack(spacing: 6) {
                            zonesColumn(rows.0, cw: cw)
                            center(cw: cw, landscape: true)
                            zonesColumn(rows.1, cw: cw)
                        }
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                        .padding(.horizontal, edgeInset)
                    } else {
                        VStack(spacing: 6) {
                            zonesRow(rows.0, cw: cw)
                            center(cw: cw, landscape: false)
                            zonesRow(rows.1, cw: cw)
                        }
                        .frame(width: W, height: H)
                        .padding(.horizontal, 8)
                    }
                }
                // Ghost card tracking the finger (separate observer: the board does
                // not re-render on every drag frame).
                DragGhostView(drag: drag, theme: theme, size: CGSize(width: cw, height: cw * 1.4))
            }
            .frame(width: W, height: H)
            // One shared space for the drag gesture, the slot frames and the ghost.
            .coordinateSpace(name: "board")
            .onPreferenceChange(SlotFrameKey.self) { frames in
                var byPlayer: [Int: [Int: CGRect]] = [:]
                for (id, frame) in frames {
                    byPlayer[id.player, default: [:]][id.slot] = frame
                }
                // Publish outside the current view update to avoid mutating state
                // while SwiftUI is laying out.
                DispatchQueue.main.async { engine.slotFrames = byPlayer }
            }
        }
    }

    private var rowIndices: ([Int], [Int]) {
        let n = engine.state.players.count
        if engine.state.mode == 1 { return ([1], [0]) }
        if n == 2 { return ([0], [1]) }
        if n == 3 { return ([0, 1], [2]) }
        return ([0, 1], [2, 3])
    }

    /// iPads inset one side for the front camera in landscape; keep the board
    /// clear of it symmetrically so the layout stays centred.
    private var edgeInset: CGFloat {
        let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene
        let insets = scene?.keyWindow?.safeAreaInsets ?? .zero
        return max(insets.left, insets.right, 0)
    }

    private func cardWidth(W: CGFloat, H: CGFloat, landscape: Bool, rows: ([Int], [Int])) -> CGFloat {
        let pad: CGFloat = 12, gap: CGFloat = 4, hgap: CGFloat = 6
        let headerH: CGFloat = 18, labelH: CGFloat = 28, ratio: CGFloat = 1.4
        let usable = max(W - 2 * edgeInset, 220)
        let v: CGFloat
        if landscape {
            let cwH = (usable - pad - 2 * hgap - 8 * gap) / 11.6
            let cwV = (H - pad - 2 * headerH - 3 * gap) / (2 * ratio)
            v = min(cwH, cwV)
        } else {
            let perRow = CGFloat(max(rows.0.count, rows.1.count))
            let cwH = (usable - pad - (perRow - 1) * hgap - perRow * 4 * gap) / (perRow * 5)
            let cwV = (H - pad - 2 * headerH - 3 * gap - 2 * labelH) / (5 * ratio)
            v = min(cwH, cwV)
        }
        return max(20, min(v, 96) * 0.9)
    }

    private func zonesRow(_ idxs: [Int], cw: CGFloat) -> some View {
        HStack(alignment: .top, spacing: 10) {
            ForEach(idxs, id: \.self) { i in
                PlayerZoneView(engine: engine, playerIndex: i, theme: theme, cardW: cw)
            }
        }
    }

    private func zonesColumn(_ idxs: [Int], cw: CGFloat) -> some View {
        VStack(spacing: 10) {
            ForEach(idxs, id: \.self) { i in
                PlayerZoneView(engine: engine, playerIndex: i, theme: theme, cardW: cw)
            }
        }
    }

    @ViewBuilder
    private func center(cw: CGFloat, landscape: Bool) -> some View {
        if landscape {
            VStack(spacing: 8) {
                PileView(theme: theme, top: nil, count: engine.state.deck.count, label: "Deck", cardW: cw, drawable: deckDrawable) {
                    Haptics.tap(); engine.doDraw(engine.state.turn, source: "deck")
                }
                drawnCardView(cw: cw)
                Text(banner).font(.system(size: max(9, cw * 0.2))).multilineTextAlignment(.center).foregroundColor(theme.bannerInk).frame(width: cw * 1.6)
                PileView(theme: theme, top: engine.state.center.last, count: engine.state.center.count, label: "Discard", cardW: cw, drawable: centerDrawable) {
                    Haptics.tap(); engine.doDraw(engine.state.turn, source: "center")
                }
            }
            .frame(width: cw * 1.6)
        } else {
            HStack(alignment: .center, spacing: 10) {
                PileView(theme: theme, top: nil, count: engine.state.deck.count, label: "Deck", cardW: cw, drawable: deckDrawable) {
                    Haptics.tap(); engine.doDraw(engine.state.turn, source: "deck")
                }
                VStack(spacing: 4) {
                    drawnCardView(cw: cw)
                    Text(banner).font(.system(size: max(10, cw * 0.22))).multilineTextAlignment(.center).foregroundColor(theme.bannerInk)
                }
                .frame(maxWidth: .infinity)
                PileView(theme: theme, top: engine.state.center.last, count: engine.state.center.count, label: "Discard", cardW: cw, drawable: centerDrawable) {
                    Haptics.tap(); engine.doDraw(engine.state.turn, source: "center")
                }
            }
        }
    }

    private func drawnCardView(cw: CGFloat) -> some View {
        let t = engine.state.turn
        let p = engine.state.players[t]
        return Group {
            if !p.isAI, !engine.state.over, engine.state.phase == .acting, let c = p.hand.first {
                CardFaceView(card: c, theme: theme)
                    .frame(width: cw, height: cw * 1.4)
                    .shadow(radius: 3)
                    .gesture(dragGesture(card: c, player: t))
                    .accessibilityIdentifier("hand-card")
                    .accessibilityLabel("\(c.rank) of \(c.suit.fileName); drag onto a slot, tap to discard")
            } else {
                Color.clear.frame(width: cw, height: cw * 1.4)
            }
        }
    }

    /// Immediate drag: the card follows the finger from touch-down — no long press.
    /// Release over one of your slots places it; a tap without movement discards it.
    private func dragGesture(card c: Card, player t: Int) -> some Gesture {
        DragGesture(minimumDistance: 0, coordinateSpace: .named("board"))
            .onChanged { value in
                guard canAct(t) else { return }
                let moved = abs(value.translation.width) > 3 || abs(value.translation.height) > 3
                drag.card = moved ? c : nil
                drag.point = moved ? value.location : nil
            }
            .onEnded { value in
                guard canAct(t) else { return }
                let moved = abs(value.translation.width) > 8 || abs(value.translation.height) > 8
                drag.card = nil
                drag.point = nil
                if !moved {
                    Haptics.discard()
                    engine.discardCard(t, hand: 0)
                    return
                }
                if let slot = hitSlot(player: t, at: value.location) {
                    if engine.placeCard(t, hand: 0, slot: slot) {
                        Haptics.place()
                    } else {
                        Haptics.error()
                    }
                } else {
                    Haptics.error()
                }
            }
    }

    /// The slot of `player` that contains `point` (board space), if any.
    private func hitSlot(player: Int, at point: CGPoint) -> Int? {
        engine.slotFrames[player]?.first(where: { $0.value.contains(point) })?.key
    }

    private func canAct(_ t: Int) -> Bool {
        guard !engine.state.over, engine.state.phase == .acting, engine.state.turn == t else { return false }
        return !engine.state.players[t].isAI
    }

    private var deckDrawable: Bool {
        engine.state.phase == .awaiting && !engine.state.over &&
        !engine.state.players[engine.state.turn].isAI && engine.state.deck.count > 0
    }
    private var centerDrawable: Bool {
        engine.state.phase == .awaiting && !engine.state.over &&
        !engine.state.players[engine.state.turn].isAI && engine.state.center.count > 0
    }

    private var banner: String {
        if engine.state.over { return "Game over" }
        let p = engine.state.players[engine.state.turn]
        if p.isAI { return "CPU is thinking…" }
        let who = engine.state.mode == 1 ? "" : "P\(engine.state.turn + 1): "
        var t = engine.state.phase == .awaiting
            ? "\(who)Your turn — draw from the deck or discard"
            : "\(who)Drag it to a slot — or tap to discard"
        if engine.state.deck.isEmpty { t += " • deck empty" }
        return t
    }
}

/// Live drag state. Kept separate from the engine so that dragging does not
/// re-render the whole board on every frame — only the ghost follows the finger.
final class DragState: ObservableObject {
    @Published var card: Card?
    @Published var point: CGPoint?
}

/// The card that follows the finger while dragging.
struct DragGhostView: View {
    @ObservedObject var drag: DragState
    let theme: Theme
    let size: CGSize

    var body: some View {
        GeometryReader { _ in
            if let card = drag.card, let pt = drag.point {
                CardFaceView(card: card, theme: theme)
                    .frame(width: size.width, height: size.height)
                    .scaleEffect(1.07)
                    .rotationEffect(.degrees(2.5))
                    .shadow(radius: 10, y: 6)
                    .position(pt)
                    .allowsHitTesting(false)
            }
        }
        .allowsHitTesting(false)
    }
}