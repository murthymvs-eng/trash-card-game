import XCTest
@testable import TrashGame

@MainActor
final class TrashGameTests: XCTestCase {

    var engine: GameEngine!

    override func setUp() {
        super.setUp()
        engine = GameEngine()
        engine.useSynchronousTimers = true
        engine.onSound = { _ in }
        engine.onWin = {}
    }

    override func tearDown() {
        engine = nil
        super.tearDown()
    }

    // MARK: - Deck

    func testDeckHas52UniqueCards() {
        let d = engine.makeDeck()
        XCTAssertEqual(d.count, 52)
        XCTAssertEqual(Set(d).count, 52, "deck must contain no duplicates")
    }

    func testDeckContainsFullRankSuitMatrix() {
        let d = engine.makeDeck()
        for r in GameRules.ranks {
            for s in Card.Suit.allCases {
                XCTAssertTrue(d.contains(Card(rank: r, suit: s)), "missing \(r)\(s)")
            }
        }
    }

    // MARK: - newGame setup

    func testOnePlayerGameCreatesYouAndCPU() {
        engine.newGame(mode: 1)
        XCTAssertEqual(engine.state.players.count, 2)
        XCTAssertFalse(engine.state.players[0].isAI)
        XCTAssertTrue(engine.state.players[1].isAI)
        XCTAssertEqual(engine.state.players[1].name, "CPU")
        XCTAssertEqual(engine.state.deck.count, 52)
        XCTAssertEqual(engine.state.mode, 1)
        XCTAssertEqual(engine.state.phase, .awaiting)
        XCTAssertEqual(engine.state.turn, 0)
    }

    func testHotseatGameCreatesNPlayersNoAI() {
        engine.newGame(mode: 4)
        XCTAssertEqual(engine.state.players.count, 4)
        XCTAssertTrue(engine.state.players.allSatisfy { !$0.isAI })
        XCTAssertEqual(engine.state.players[2].name, "P3")
    }

    func testSlotsStartEmpty() {
        engine.newGame(mode: 2)
        for p in engine.state.players {
            XCTAssertEqual(p.slots.count, GameRules.slotCount)
            XCTAssertTrue(p.slots.allSatisfy { $0 == nil })
            XCTAssertEqual(p.placed, 0)
            XCTAssertTrue(p.hand.isEmpty)
        }
    }

    // MARK: - Placement rules

    func testCanPlaceRankExactMatch() {
        let ace = Card(rank: "A", suit: .spades)
        XCTAssertTrue(engine.canPlaceRank(ace, rank: "A"))
        XCTAssertFalse(engine.canPlaceRank(ace, rank: "2"))
    }

    func testJackIsWildcard() {
        let j = Card(rank: "J", suit: .clubs)
        for r in GameRules.slotOrder {
            XCTAssertTrue(engine.canPlaceRank(j, rank: r))
        }
    }

    func testQueenAndKingNeverPlaceable() {
        for r in GameRules.slotOrder {
            XCTAssertFalse(engine.canPlaceRank(Card(rank: "Q", suit: .hearts), rank: r))
            XCTAssertFalse(engine.canPlaceRank(Card(rank: "K", suit: .hearts), rank: r))
        }
    }

    func testFindSlotMapsRankToIndex() {
        engine.newGame(mode: 2)
        var p = engine.state.players[0]
        XCTAssertEqual(engine.findSlot(p, Card(rank: "A", suit: .spades)), 0)
        XCTAssertEqual(engine.findSlot(p, Card(rank: "10", suit: .spades)), 9)
        XCTAssertNil(engine.findSlot(p, Card(rank: "Q", suit: .spades)))
        // Jack fills the first empty slot.
        p.slots[0] = Card(rank: "2", suit: .hearts)
        XCTAssertEqual(engine.findSlot(p, Card(rank: "J", suit: .spades)), 1)
    }

    func testCannotPlaceIntoOccupiedSlot() {
        engine.newGame(mode: 2)
        var p = engine.state.players[0]
        p.slots[0] = Card(rank: "A", suit: .hearts)
        XCTAssertFalse(engine.canPlaceInSlot(p, Card(rank: "A", suit: .spades), 0))
    }

    // MARK: - Move flow (deterministic with synchronous timers)

    func testDrawFromDeckGivesPlayableCard() {
        engine.newGame(mode: 1)
        engine.state.deck = [Card(rank: "A", suit: .spades)]
        engine.doDraw(0, source: "deck")
        XCTAssertEqual(engine.state.phase, .acting)
        XCTAssertEqual(engine.state.players[0].hand, [Card(rank: "A", suit: .spades)])
        XCTAssertEqual(engine.state.turnDrawnCard, Card(rank: "A", suit: .spades))
    }

    func testUnplayableDrawAutoDiscardsAndAdvances() {
        engine.newGame(mode: 2)
        engine.state.deck = [Card(rank: "3", suit: .clubs), Card(rank: "K", suit: .spades)]
        engine.doDraw(0, source: "deck")
        // King is unplayable -> timer fires synchronously -> auto-discard + endTurn.
        XCTAssertTrue(engine.state.players[0].hand.isEmpty)
        XCTAssertEqual(engine.state.center.last, Card(rank: "K", suit: .spades))
        XCTAssertEqual(engine.state.turn, 1)
        XCTAssertEqual(engine.state.phase, .awaiting)
    }

    func testDiscardMovesToCenterAndEndsTurn() {
        engine.newGame(mode: 2)
        engine.state.deck = [Card(rank: "7", suit: .diamonds), Card(rank: "2", suit: .hearts)]
        engine.doDraw(0, source: "deck")
        engine.discardCard(0, hand: 0)
        XCTAssertEqual(engine.state.players[0].hand.count, 0)
        XCTAssertEqual(engine.state.center.last, Card(rank: "2", suit: .hearts))
        XCTAssertEqual(engine.state.turn, 1)
        XCTAssertEqual(engine.state.phase, .awaiting)
    }

    func testJackPlacesIntoAnyEmptySlot() {
        engine.newGame(mode: 2)
        let j = Card(rank: "J", suit: .diamonds)
        var p0 = engine.state.players[0]
        p0.hand = [j]
        engine.state.players[0] = p0
        XCTAssertTrue(engine.placeCard(0, hand: 0, slot: 3))
        XCTAssertEqual(engine.state.players[0].slots[3], j)
        XCTAssertTrue(engine.state.players[0].hand.isEmpty)
    }

    func testQueenCannotBePlaced() {
        engine.newGame(mode: 2)
        let q = Card(rank: "Q", suit: .spades)
        var p0 = engine.state.players[0]
        p0.hand = [q]
        engine.state.players[0] = p0
        XCTAssertFalse(engine.placeCard(0, hand: 0))
        XCTAssertEqual(engine.state.players[0].hand, [q])
        XCTAssertNil(engine.state.players[0].slots[0])
    }

    // MARK: - Win detection

    func testFillingTenthSlotWins() {
        engine.newGame(mode: 2)
        var p0 = engine.state.players[0]
        for i in 0..<9 {
            p0.slots[i] = Card(rank: GameRules.slotOrder[i], suit: .spades)
        }
        p0.hand = [Card(rank: "10", suit: .hearts)]
        engine.state.players[0] = p0
        engine.placeCard(0, hand: 0)
        XCTAssertTrue(engine.state.over)
        XCTAssertEqual(engine.state.winner, [0])
    }

    func testDeckExhaustionPicksMostPlaced() {
        engine.newGame(mode: 2)
        var a = engine.state.players[0]
        a.slots[0] = Card(rank: "A", suit: .spades)
        a.slots[1] = Card(rank: "2", suit: .spades)
        a.slots[2] = Card(rank: "3", suit: .spades)
        a.hand = [Card(rank: "K", suit: .spades)]
        engine.state.players[0] = a
        var b = engine.state.players[1]
        b.slots[0] = Card(rank: "A", suit: .hearts)
        engine.state.players[1] = b
        engine.state.deck = []
        engine.discardCard(0, hand: 0)   // -> endTurn -> deck empty -> score
        XCTAssertTrue(engine.state.over)
        XCTAssertEqual(engine.state.winner, [0])
    }

    // MARK: - Advanced mode

    func testAdvancedDealCoversAllSlots() {
        engine.newGame(mode: 2, advanced: true)
        XCTAssertTrue(engine.state.advanced)
        XCTAssertEqual(engine.state.deck.count, 52 - 20)
        for p in engine.state.players {
            XCTAssertEqual(p.covers.compactMap { $0 }.count, 10)
            XCTAssertTrue(p.slots.allSatisfy { $0 == nil })
            XCTAssertTrue(p.hand.isEmpty)
        }
    }

    func testClassicHasNoCovers() {
        engine.newGame(mode: 2)
        XCTAssertFalse(engine.state.advanced)
        XCTAssertEqual(engine.state.deck.count, 52)
        for p in engine.state.players {
            XCTAssertTrue(p.covers.allSatisfy { $0 == nil })
        }
    }

    func testAdvancedCoverGoesToHandOnPlace() {
        engine.newGame(mode: 1, advanced: true)
        let cover = Card(rank: "4", suit: .hearts)
        var p0 = engine.state.players[0]
        p0.hand = [Card(rank: "A", suit: .spades)]
        p0.covers[0] = cover
        engine.state.players[0] = p0
        engine.state.phase = .acting   // simulate a mid-turn placement
        let deckBefore = engine.state.deck.count
        XCTAssertTrue(engine.placeCard(0, hand: 0, slot: 0))
        // The card is placed, the cover flips into the hand, and the turn
        // continues (no new draw, still in the acting phase).
        XCTAssertEqual(engine.state.players[0].slots[0], Card(rank: "A", suit: .spades))
        XCTAssertEqual(engine.state.players[0].hand, [cover])
        XCTAssertNil(engine.state.players[0].covers[0])
        XCTAssertEqual(engine.state.turn, 0)
        XCTAssertEqual(engine.state.phase, .acting)
        XCTAssertEqual(engine.state.deck.count, deckBefore)
    }

    func testAdvancedDiscardEndsTurnAndDumpsHand() {
        engine.newGame(mode: 2, advanced: true)
        var p0 = engine.state.players[0]
        p0.hand = [Card(rank: "Q", suit: .spades), Card(rank: "K", suit: .hearts)]
        engine.state.players[0] = p0
        engine.discardCard(0, hand: 0)
        XCTAssertEqual(engine.state.turn, 1)
        XCTAssertEqual(engine.state.players[0].hand.count, 0)
        // The discarded card is on the bottom, the dumped hand on top.
        XCTAssertEqual(engine.state.center.last, Card(rank: "K", suit: .hearts))
        XCTAssertTrue(engine.state.center.contains(Card(rank: "Q", suit: .spades)))
    }

    func testAdvancedUnplayableAutoDiscardsAndDumpsHand() {
        engine.newGame(mode: 1, advanced: true)
        engine.state.deck = [Card(rank: "K", suit: .spades)]
        var p0 = engine.state.players[0]
        p0.hand = [Card(rank: "Q", suit: .clubs)]
        engine.state.players[0] = p0
        engine.doDraw(0, source: "deck")
        // Nothing playable -> auto-discard: the unplayable card is dumped, and the
        // CPU then plays its own turn, so it is back at player 0.
        XCTAssertEqual(engine.state.players[0].hand.count, 0)
        XCTAssertEqual(engine.state.players[1].hand.count, 0)
        XCTAssertTrue(engine.state.center.contains(Card(rank: "Q", suit: .clubs)))
        XCTAssertTrue(engine.state.center.contains(Card(rank: "K", suit: .spades)))
        XCTAssertEqual(engine.state.turn, 0)
        XCTAssertEqual(engine.state.phase, .awaiting)
        XCTAssertFalse(engine.state.over)
    }

    func testAdvancedWinOnTenthPlacement() {
        engine.newGame(mode: 2, advanced: true)
        var p0 = engine.state.players[0]
        for i in 0..<9 {
            p0.slots[i] = Card(rank: GameRules.slotOrder[i], suit: .spades)
            p0.covers[i] = nil
        }
        p0.hand = [Card(rank: "10", suit: .hearts)]
        engine.state.players[0] = p0
        engine.placeCard(0, hand: 0, slot: 9)
        XCTAssertTrue(engine.state.over)
        XCTAssertEqual(engine.state.winner, [0])
    }

    func testAdvancedScoreGameOverWhenBothPilesEmpty() {
        engine.newGame(mode: 2, advanced: true)
        engine.state.deck = []
        engine.state.center = []
        var p0 = engine.state.players[0]
        p0.slots[0] = Card(rank: "A", suit: .spades)
        p0.covers[0] = nil
        p0.hand = [Card(rank: "2", suit: .hearts)]
        engine.state.players[0] = p0
        var p1 = engine.state.players[1]
        p1.slots[0] = Card(rank: "A", suit: .hearts)
        p1.slots[1] = Card(rank: "2", suit: .spades)
        p1.covers[0] = nil
        p1.covers[1] = nil
        engine.state.players[1] = p1
        // Placing the last card leaves nothing to draw -> game over by score (tie).
        engine.placeCard(0, hand: 0, slot: 1)
        XCTAssertTrue(engine.state.over)
        XCTAssertEqual(engine.state.winner, [0, 1])
    }

    func testAdvancedFullAIGameCompletes() {
        engine.newGame(mode: 1, advanced: true)
        var steps = 0
        while !engine.state.over && steps < 5000 {
            steps += 1
            guard engine.state.turn == 0, !engine.state.players[0].isAI else { break }
            if engine.state.phase == .awaiting {
                engine.doDraw(0, source: engine.state.deck.isEmpty ? "center" : "deck")
            } else if let hi = engine.findPlayable(0) {
                engine.placeCard(0, hand: hi)
            } else {
                let hi = engine.state.players[0].hand.firstIndex {
                    !engine.canPlaceAnywhere(engine.state.players[0], $0)
                } ?? 0
                engine.discardCard(0, hand: hi)
            }
        }
        XCTAssertTrue(engine.state.over, "advanced game should end (after \(steps) driver steps)")
        XCTAssertFalse(engine.state.winner.isEmpty)
    }
}
