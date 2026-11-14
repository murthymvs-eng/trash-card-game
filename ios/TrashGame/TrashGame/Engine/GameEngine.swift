import Foundation
import Combine

/// State machine for the Trash card game — ported from the web build's JS loop
/// (`newGame`/`doDraw`/`placeCard`/`discardCard`/`endTurn` + CPU AI), with
/// `after(ms, fn)` timeouts replaced by `Task.sleep`.
@MainActor
final class GameEngine: ObservableObject {

    /// Single source of truth; SwiftUI views observe this.
    @Published var state: GameState

    /// Wired by the app layer to play sound ("draw"/"place"/"err"/"discard"/"win").
    var onSound: ((String) -> Void)?
    /// Wired by the app layer to trigger the confetti/win animation.
    var onWin: (() -> Void)?

    /// When true, `after` runs its continuation synchronously (deterministic tests).
    var useSynchronousTimers = false

    /// When true, the human player is also driven automatically (demo/autoplay recording).
    var isAutoPlaying = false

    /// Player 0's display name (mirrors the web build's `userName()`).
    var userName: String = "You"

    /// Bumped on every `newGame` to invalidate in-flight timers from a previous game.
    private var generation = 0

    /// Frames of the trash slots in the board coordinate space (drop hit-testing).
    @Published var slotFrames: [Int: [Int: CGRect]] = [:]

    init() {
        state = .empty
    }

    // MARK: - Setup

    func makeDeck() -> [Card] {
        var d: [Card] = []
        for r in GameRules.ranks {
            for s in Card.Suit.allCases {
                d.append(Card(rank: r, suit: s))
            }
        }
        d.shuffle()
        return d
    }

    /// Cancels the running game (the player left mid-game). In-flight timers are
    /// invalidated and the state is cleared so the main screen starts fresh.
    func abortGame() {
        generation += 1
        state = .empty
    }

    func newGame(mode n: Int, advanced: Bool = false) {
        generation += 1
        let total = n == 1 ? 2 : n
        var players: [Player] = []
        for i in 0..<total {
            let name: String
            if i == 0 {
                name = userName.isEmpty ? "You" : userName
            } else if n == 1 {
                name = "CPU"
            } else {
                name = "P\(i + 1)"
            }
            let isAI = n == 1 && i == 1
            players.append(Player(id: i, name: name, isAI: isAI))
        }
        var deck = makeDeck()
        // Advanced: deal 10 face-down cover cards per player (one per slot).
        for i in 0..<players.count where advanced {
            let covers = Array(deck.prefix(GameRules.slotCount))
            deck.removeFirst(GameRules.slotCount)
            players[i].covers = covers
        }
        state = GameState(
            players: players,
            deck: deck,
            center: [],
            turn: 0,
            phase: .awaiting,
            placedThisTurn: 0,
            mode: n,
            over: false,
            winner: [],
            fast: false,
            advanced: advanced
        )
        // Debug/test hook: force the card that will be drawn next, e.g. "-forceCard 4".
        if let i = ProcessInfo.processInfo.arguments.firstIndex(of: "-forceCard"),
           i + 1 < ProcessInfo.processInfo.arguments.count {
            let rank = ProcessInfo.processInfo.arguments[i + 1]
            if GameRules.ranks.contains(rank), !state.deck.isEmpty {
                state.deck[state.deck.count - 1] = Card(rank: rank, suit: .hearts)
            }
        }
    }

    // MARK: - Placement rules

    func canPlaceRank(_ c: Card, rank: String) -> Bool {
        c.rank == "J" || c.rank == rank
    }

    func canPlaceInSlot(_ p: Player, _ c: Card, _ s: Int) -> Bool {
        guard s >= 0, s < GameRules.slotCount else { return false }
        return p.slots[s] == nil && canPlaceRank(c, rank: GameRules.slotOrder[s])
    }

    func canPlaceAnywhere(_ p: Player, _ c: Card) -> Bool {
        p.slots.indices.contains { canPlaceInSlot(p, c, $0) }
    }

    /// The slot a card should go into, if any.
    func findSlot(_ p: Player, _ c: Card) -> Int? {
        if c.rank == "J" {
            return p.slots.firstIndex { $0 == nil }
        }
        guard let idx = GameRules.slotOrder.firstIndex(of: c.rank) else { return nil }
        return p.slots[idx] == nil ? idx : nil
    }

    /// Index into player i's hand of a playable card (non-Jacks first).
    func findPlayable(_ i: Int) -> Int? {
        let p = state.players[i]
        if let j = p.hand.firstIndex(where: { $0.rank != "J" && findSlot(p, $0) != nil }) {
            return j
        }
        return p.hand.firstIndex(where: { findSlot(p, $0) != nil })
    }

    // MARK: - Turn actions

    func doDraw(_ pIdx: Int, source: String) {
        guard !state.over, state.phase == .awaiting else { return }
        // Advanced: nobody left to draw from — end the game on score.
        if state.advanced, state.deck.isEmpty, state.center.isEmpty {
            gameOverByScore()
            return
        }

        var card: Card?
        if source == "center", let top = state.center.popLast() {
            card = top
        } else if source == "deck", let top = state.deck.popLast() {
            card = top
        } else if let top = state.deck.popLast() {
            card = top
        } else if let top = state.center.popLast() {
            card = top
        }
        guard let card else { return }

        var p = state.players[pIdx]
        p.hand.append(card)
        state.players[pIdx] = p

        state.phase = .acting
        state.placedThisTurn = 0
        state.lastPlaced = nil
        state.turnDrawnCard = card
        state.lastDrawn = (player: pIdx, hand: p.hand.count - 1)
        playSound("draw")

        if p.isAI || isAutoPlaying {
            aiStep(pIdx)
        } else if findPlayable(pIdx) == nil {
            after(1200) { [weak self] in
                guard let self, !self.state.over,
                      self.state.turn == pIdx, self.state.phase == .acting else { return }
                self.autoEnd(pIdx)
            }
        }
    }

    // MARK: - Placing & discarding

    @discardableResult
    func placeCard(_ pIdx: Int, hand hi: Int, slot sIdx: Int? = nil) -> Bool {
        guard !state.over else { return false }
        let p = state.players[pIdx]
        guard hi < p.hand.count else { return false }
        let c = p.hand[hi]

        let target = sIdx ?? findSlot(p, c)
        guard let s = target, canPlaceInSlot(p, c, s) else {
            playSound("err")
            return false
        }

        var pc = p
        pc.slots[s] = c
        pc.hand.remove(at: hi)
        if state.advanced, let cover = p.covers[s] {
            // Unlock: the face-down cover flips into the player's hand.
            pc.covers[s] = nil
            pc.hand.append(cover)
        }
        state.players[pIdx] = pc
        state.placedThisTurn += 1
        state.lastDrawn = nil
        state.lastPlaced = (player: pIdx, slot: s)
        playSound("place")

        if pc.placed >= GameRules.slotCount {
            gameOverWin(pIdx)
            return true
        }
        if state.placedThisTurn >= 1 {
            after(450) { [weak self] in
                guard let self, !self.state.over else { return }
                if self.state.advanced { self.continueTurn(pIdx) } else { self.endTurn() }
            }
        }
        return true
    }

    func discardCard(_ pIdx: Int, hand hi: Int) {
        guard !state.over else { return }
        var p = state.players[pIdx]
        guard hi < p.hand.count else { return }
        let c = p.hand.remove(at: hi)
        state.players[pIdx] = p
        state.center.append(c)
        if state.advanced {
            // The rest of the hand (unplayed covers) is dumped into the discard.
            state.center.append(contentsOf: p.hand)
            state.players[pIdx].hand.removeAll()
        }
        state.lastDrawn = nil
        playSound("discard")
        endTurn()
    }

    // MARK: - Turn advancement & AI

    func endTurn() {
        guard !state.over else { return }

        // If nothing was placed this turn, the just-drawn card is auto-discarded.
        if state.placedThisTurn == 0 {
            let turn = state.turn
            var p = state.players[turn]
            if let drawn = state.turnDrawnCard, let di = p.hand.firstIndex(of: drawn) {
                p.hand.remove(at: di)
                state.center.append(drawn)
                state.players[turn] = p
            }
        }

        if state.advanced
            ? (state.deck.isEmpty && state.center.isEmpty)
            : state.deck.isEmpty {
            gameOverByScore()
            return
        }

        state.turn = (state.turn + 1) % state.players.count
        state.phase = .awaiting
        state.placedThisTurn = 0
        state.lastDrawn = nil
        state.lastPlaced = nil
        state.turnDrawnCard = nil

        if state.players[state.turn].isAI || isAutoPlaying {
            aiTurnStart()
        }
    }

    func aiChooseDrawSource() -> String {
        let p = state.players[state.turn]
        if !state.center.isEmpty, !state.deck.isEmpty {
            if let top = state.center.last, findSlot(p, top) != nil { return "center" }
            return "deck"
        }
        return state.center.isEmpty ? "deck" : "center"
    }

    func aiTurnStart() {
        after(900) { [weak self] in
            guard let self, !self.state.over, (self.state.players[self.state.turn].isAI || self.isAutoPlaying) else { return }
            self.doDraw(self.state.turn, source: self.aiChooseDrawSource())
        }
    }

    func aiStep(_ i: Int) {
        let ok: () -> Bool = { [weak self] in
            guard let self else { return false }
            return !self.state.over && self.state.turn == i && (self.state.players[i].isAI || self.isAutoPlaying)
        }
        guard ok(), state.phase == .acting else { return }

        if let hi = findPlayable(i) {
            after(750) { [weak self] in
                guard let self, ok(), self.state.phase == .acting else { return }
                self.placeCard(i, hand: hi)
            }
        } else {
            after(750) { [weak self] in
                guard let self, ok(), self.state.phase == .acting else { return }
                self.autoEnd(i)
            }
        }
    }

    /// Auto-end for the current player: classic auto-discards the just-drawn
    /// card; advanced discards the first unplayable card and dumps the rest
    /// of the hand into the discard pile.
    func autoEnd(_ pIdx: Int) {
        if state.advanced {
            let p = state.players[pIdx]
            let hi = p.hand.firstIndex { !canPlaceAnywhere(p, $0) } ?? 0
            discardCard(pIdx, hand: hi)
        } else {
            endTurn()
        }
    }

    /// Advanced: after a placement, the turn does NOT go back to the draw
    /// phase (only one draw per turn). The revealed cover stays in the hand —
    /// keep placing to continue, or tap a card to discard and end the turn.
    func continueTurn(_ pIdx: Int) {
        guard !state.over, state.turn == pIdx else { return }
        if state.deck.isEmpty && state.center.isEmpty {
            gameOverByScore()
            return
        }
        state.placedThisTurn = 0
        state.lastDrawn = nil
        state.lastPlaced = nil
        state.turnDrawnCard = nil
        if state.players[pIdx].isAI || isAutoPlaying {
            aiStep(pIdx)
            return
        }
        // Human: if nothing left to play, the turn ends on its own.
        if findPlayable(pIdx) == nil {
            after(1200) { [weak self] in
                guard let self, !self.state.over,
                      self.state.turn == pIdx, self.state.phase == .acting else { return }
                self.autoEnd(pIdx)
            }
        }
    }

    // MARK: - Game over

    func gameOverWin(_ i: Int) {
        state.over = true
        state.winner = [i]
        state.title = winTitle(i) + (state.mode == 1 && i == 0 ? " 🎉" : "")
        state.subtitle = "All 10 slots filled — trash pile complete!"
        playSound("win")
        onWin?()
    }

    func gameOverByScore() {
        state.over = true
        let mx = state.players.map { $0.placed }.max() ?? 0
        state.winner = state.players.indices.filter { state.players[$0].placed == mx }
        if state.winner.count > 1 {
            state.title = "It's a tie!"
        } else if let w = state.winner.first {
            state.title = winTitle(w)
        }
        state.subtitle = "The deck ran out — most cards placed wins."
        if state.winner.count == 1 {
            playSound("win")
            onWin?()
        } else {
            playSound("place")
        }
    }

    private func winTitle(_ i: Int) -> String {
        let n = state.players[i].name
        return n == "You" ? "You win!" : "\(n) wins!"
    }

    // MARK: - Helpers

    private func playSound(_ kind: String) {
        onSound?(kind)
    }

    /// Executes `fn` after `ms` milliseconds (0 in fast mode), invalidated if a
    /// new game starts first.
    private func after(_ ms: Int, _ fn: @escaping () -> Void) {
        if useSynchronousTimers {
            fn()
            return
        }
        let gen = generation
        let delay: Int
        if state.fast {
            delay = 0
        } else if isAutoPlaying {
            delay = max(ms / 4, 60)
        } else {
            delay = ms
        }
        Task {
            try? await Task.sleep(for: .milliseconds(delay))
            guard gen == generation else { return }
            fn()
        }
    }
}