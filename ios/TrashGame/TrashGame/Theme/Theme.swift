import SwiftUI

/// How a theme draws its card faces.
enum FaceStyle: Equatable {
    case classic
    case emoji
    case fairy
    case neon
    case wood
    case image(deckDir: String)
}

/// Per-theme look, ported from the web build's `LOOK` palette.
struct Theme: Identifiable {
    let id: String
    let name: String
    let subtitle: String
    let face: FaceStyle
    let felt: [Color]
    let accent: Color
    let accentDeep: Color
    let accentLite: Color
    let bannerInk: Color

    var feltGradient: LinearGradient {
        LinearGradient(colors: felt, startPoint: .top, endPoint: .bottom)
    }

    func slotColor(edge: Bool = false) -> Color {
        Color.black.opacity(edge ? 0.55 : 0.34)
    }
}

extension Color {
    init(hex: String, alpha: Double = 1) {
        let h = hex.trimmingCharacters(in: CharacterSet(charactersIn: "#"))
        var v: UInt64 = 0
        Scanner(string: h).scanHexInt64(&v)
        let r = Double((v >> 16) & 0xFF) / 255
        let g = Double((v >> 8) & 0xFF) / 255
        let b = Double(v & 0xFF) / 255
        self.init(red: r, green: g, blue: b, opacity: alpha)
    }
}

private func ink(_ hex: String) -> Color { Color(hex: hex) }

let allThemes: [Theme] = [
    Theme(id: "classic", name: "Classic", subtitle: "Timeless cream", face: .classic,
          felt: [ink("2f9a6a"), ink("1f7a52"), ink("12583a"), ink("0a3521")],
          accent: ink("ffd24d"), accentDeep: ink("a5701a"), accentLite: ink("ffe08a"), bannerInk: ink("eafff2")),
    Theme(id: "animal", name: "Emoji Party", subtitle: "Cute critters", face: .emoji,
          felt: [ink("8fd6a8"), ink("4f9e78"), ink("2a5e46"), ink("153326")],
          accent: ink("ffc94d"), accentDeep: ink("a8700f"), accentLite: ink("ffe49a"), bannerInk: ink("f2fff4")),
    Theme(id: "minion", name: "Minions", subtitle: "The yellow crew", face: .image(deckDir: "minion_deck"),
          felt: [ink("c9a63a"), ink("8a6d18"), ink("4d3c0c"), ink("2a2006")],
          accent: ink("ffd24d"), accentDeep: ink("8a6a12"), accentLite: ink("ffe98a"), bannerInk: ink("eafff2")),
    Theme(id: "fairy", name: "Fairytale", subtitle: "Storybook sparkle", face: .fairy,
          felt: [ink("cbb4f2"), ink("8f74c4"), ink("4f3d78"), ink("2a2045")],
          accent: ink("ffd9f2"), accentDeep: ink("a04f8f"), accentLite: ink("ffeafb"), bannerInk: ink("fdf3ff")),
    Theme(id: "neon", name: "Neon Night", subtitle: "Cyber glow", face: .neon,
          felt: [ink("2a2350"), ink("191540"), ink("0d0a26"), ink("06040f")],
          accent: ink("37e6ff"), accentDeep: ink("0d7f96"), accentLite: ink("b6f5ff"), bannerInk: ink("e6fbff")),
    Theme(id: "wood", name: "Woodblock", subtitle: "Vintage print", face: .wood,
          felt: [ink("d9b98a"), ink("a37f4e"), ink("6b502e"), ink("3c2b18")],
          accent: ink("f0d090"), accentDeep: ink("8a6a2a"), accentLite: ink("fbe6bd"), bannerInk: ink("eafff2")),
    Theme(id: "hp", name: "Harry Potter", subtitle: "The House Deck", face: .image(deckDir: "hp_card_deck"),
          felt: [ink("7a2a36"), ink("4a1620"), ink("2a0d13"), ink("15060a")],
          accent: ink("f0c96a"), accentDeep: ink("8a6416"), accentLite: ink("fbe6ab"), bannerInk: ink("fff2d6")),
    Theme(id: "avengers", name: "Marvel Avengers", subtitle: "Assemble!", face: .image(deckDir: "avengers_deck"),
          felt: [ink("a8323c"), ink("6b1620"), ink("3d0c13"), ink("1e0508")],
          accent: ink("ffd98a"), accentDeep: ink("a5701a"), accentLite: ink("ffeec4"), bannerInk: ink("eafff2")),
    Theme(id: "starwars", name: "Star Wars", subtitle: "Galaxy far away", face: .image(deckDir: "starwars_deck"),
          felt: [ink("2c3a5c"), ink("182240"), ink("0d1326"), ink("05070f")],
          accent: ink("ffe81f"), accentDeep: ink("8a7a10"), accentLite: ink("fff9a8"), bannerInk: ink("fdfbe6")),
    Theme(id: "spiderman", name: "Spider-Man", subtitle: "Far From Home", face: .image(deckDir: "spiderman_deck"),
          felt: [ink("2b4bd9"), ink("16255e"), ink("0c1435"), ink("05081c")],
          accent: ink("ff4d5e"), accentDeep: ink("8a1020"), accentLite: ink("ff9aa4"), bannerInk: ink("ffe8ea")),
    Theme(id: "coco", name: "Coco", subtitle: "Day of the Dead", face: .image(deckDir: "coco_deck"),
          felt: [ink("b8701f"), ink("7a4410"), ink("4a2809"), ink("261403")],
          accent: ink("ffcf4d"), accentDeep: ink("a35c12"), accentLite: ink("ffe6a6"), bannerInk: ink("fff3dc")),
    Theme(id: "princess", name: "Princess", subtitle: "Once Upon a Time", face: .image(deckDir: "princess_deck"),
          felt: [ink("b98bb4"), ink("7d5080"), ink("4c2f4f"), ink("281829")],
          accent: ink("ffd7ea"), accentDeep: ink("a8548f"), accentLite: ink("ffeaf6"), bannerInk: ink("fdf1f8")),
    Theme(id: "taylor", name: "Taylor Swift", subtitle: "The Eras Tour", face: .image(deckDir: "taylor_swift_tours_deck"),
          felt: [ink("c25d92"), ink("7e3560"), ink("451b35"), ink("250d1c")],
          accent: ink("ffe89a"), accentDeep: ink("a5701a"), accentLite: ink("fff4c8"), bannerInk: ink("eafff2")),
    Theme(id: "moana", name: "Moana", subtitle: "The Wayfinders", face: .image(deckDir: "moana_deck"),
          felt: [ink("1f8fb0"), ink("146b8a"), ink("0b3f55"), ink("05212e")],
          accent: ink("ffd24d"), accentDeep: ink("a5701a"), accentLite: ink("ffe08a"), bannerInk: ink("eafaff")),
    Theme(id: "toystory", name: "Toy Story", subtitle: "Andys Playroom", face: .image(deckDir: "toystory_deck"),
          felt: [ink("c9452f"), ink("8f2a1c"), ink("521410"), ink("2b0a07")],
          accent: ink("ffd24d"), accentDeep: ink("a5701a"), accentLite: ink("ffe08a"), bannerInk: ink("fff3dc")),
    Theme(id: "mario", name: "Mario", subtitle: "Mushroom Kingdom", face: .image(deckDir: "mario_deck"),
          felt: [ink("4a7fe0"), ink("2a52b8"), ink("15307a"), ink("0a1740")],
          accent: ink("e5392f"), accentDeep: ink("8f1a14"), accentLite: ink("ff8a7a"), bannerInk: ink("fff4e8")),
    Theme(id: "frozen", name: "Frozen", subtitle: "Into the Unknown", face: .image(deckDir: "frozen_deck"),
          felt: [ink("4f9fd8"), ink("2f6ba3"), ink("1c4569"), ink("0c2136")],
          accent: ink("8fd8f5"), accentDeep: ink("2f6ba3"), accentLite: ink("d6f3ff"), bannerInk: ink("eaf8ff"))
]

func theme(_ id: String?) -> Theme {
    guard let id, let t = allThemes.first(where: { $0.id == id }) else { return allThemes[0] }
    return t
}