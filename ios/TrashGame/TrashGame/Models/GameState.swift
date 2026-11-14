import Foundation

/// The three phases of a turn. Mirrors the web build's `phase` field.
enum TurnPhase: String, Equatable {
    /// Waiting for the current player to draw.
    case awaiting
    /// The player has drawn and must place or discard the card.
    case acting
}

/// One participant in a game — human or CPU.
struct Player: Identifiable, Equatable {
    let id: Int
    var name: String
    var isAI: Bool
    var hand: [Card]
    /// 10 trash slots; index 0 is Ace, index 9 is Ten. `nil` = empty.
    var slots: [Card?]
    /// Advanced mode only: the face-down cover over each slot. Covered ⟺ the
    /// slot is empty. Placing a card flips the cover into the player's hand.
    /// Classic mode: all nil.
    var covers: [Card?]

    init(id: Int, name: String, isAI: Bool) {
        self.id = id
        self.name = name
        self.isAI = isAI
        self.hand = []
        self.slots = Array(repeating: nil, count: GameRules.slotCount)
        self.covers = Array(repeating: nil, count: GameRules.slotCount)
    }

    /// Number of filled slots (equivalent to the web build's `placed` counter).
    var placed: Int { slots.compactMap { $0 }.count }
}

/// The full, single-source-of-truth game state (mirrors the web build's `G` object).
struct GameState {
    var players: [Player]
    var deck: [Card]
    /// Shared face-up discard pile.
    var center: [Card]
    var turn: Int
    var phase: TurnPhase
    var placedThisTurn: Int
    var mode: Int
    /// Advanced mode: slots start covered; placement flips the cover into the
    /// player's hand and the turn continues.
    var advanced: Bool
    var over: Bool
    var winner: [Int]
    var fast: Bool
    var lastDrawn: (player: Int, hand: Int)?
    var lastPlaced: (player: Int, slot: Int)?
    var turnDrawnCard: Card?
    var title: String
    var subtitle: String

    init(players: [Player],
         deck: [Card],
         center: [Card] = [],
         turn: Int = 0,
         phase: TurnPhase = .awaiting,
         placedThisTurn: Int = 0,
         mode: Int = 1,
         over: Bool = false,
         winner: [Int] = [],
         fast: Bool = false,
         advanced: Bool = false,
         lastDrawn: (player: Int, hand: Int)? = nil,
         lastPlaced: (player: Int, slot: Int)? = nil,
         turnDrawnCard: Card? = nil,
         title: String = "",
         subtitle: String = "") {
        self.players = players
        self.deck = deck
        self.center = center
        self.turn = turn
        self.phase = phase
        self.placedThisTurn = placedThisTurn
        self.mode = mode
        self.advanced = advanced
        self.over = over
        self.winner = winner
        self.fast = fast
        self.lastDrawn = lastDrawn
        self.lastPlaced = lastPlaced
        self.turnDrawnCard = turnDrawnCard
        self.title = title
        self.subtitle = subtitle
    }

    static let empty = GameState(players: [], deck: [])
}

/// Static rule constants — ported verbatim from `index.html`.
enum GameRules {
    /// Every card rank in the deck (ascending, A last).
    static let ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    /// The slot a card of each rank must go into (index 0 = Ace … 9 = Ten).
    static let slotOrder = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    static let slotCount = 10
}