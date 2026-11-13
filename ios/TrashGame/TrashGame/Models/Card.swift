import Foundation

/// A single playing card in the Trash game.
struct Card: Equatable, Hashable, Identifiable {
    /// The four suits — `C/D/H/S` to match the web build's mapping.
    enum Suit: String, CaseIterable, Codable, Hashable {
        case clubs = "C"
        case diamonds = "D"
        case hearts = "H"
        case spades = "S"

        /// Lowercase name used by the image decks (`hearts_A.jpg`).
        var fileName: String {
            switch self {
            case .clubs: return "clubs"
            case .diamonds: return "diamonds"
            case .hearts: return "hearts"
            case .spades: return "spades"
            }
        }

        /// Suit glyph (♣ ♦ ♥ ♠).
        var glyph: String {
            switch self {
            case .clubs: return "♣"
            case .diamonds: return "♦"
            case .hearts: return "♥"
            case .spades: return "♠"
            }
        }

        var isRed: Bool { self == .hearts || self == .diamonds }
    }

    let rank: String   // "A", "2"..."10", "J", "Q", "K"
    let suit: Suit

    var id: String { "\(rank)\(suit.rawValue)" }
    var isJack: Bool { rank == "J" }
    var isFace: Bool { rank == "J" || rank == "Q" || rank == "K" }
}