import SwiftUI

struct StartView: View {
    let theme: Theme
    let muted: Bool
    let onMute: () -> Void
    let onStart: (Int) -> Void
    let onSettings: () -> Void

    var body: some View {
        VStack(spacing: 20) {
            Spacer(minLength: 8)
            ZStack {
                CardFaceView(card: Card(rank: "A", suit: .spades), theme: theme).offset(x: -34)
                CardFaceView(card: Card(rank: "K", suit: .hearts), theme: theme)
                CardFaceView(card: Card(rank: "J", suit: .clubs), theme: theme).offset(x: 34)
            }
            .frame(height: 168)
            .shadow(radius: 8, y: 4)

            Text("Fill your trash pile to win")
                .font(.title2.bold())
                .foregroundColor(theme.bannerInk)
            Text("No hands — draw 1 card a turn and place or dump it. Collect A, 2 … 10; the Jack is wild, Queens and Kings are useless.")
                .font(.subheadline)
                .multilineTextAlignment(.center)
                .foregroundColor(theme.bannerInk.opacity(0.92))

            VStack(spacing: 10) {
                ModeButton(title: "1 Player", subtitle: "You vs the CPU", accent: theme.accent) { onStart(1) }
                ModeButton(title: "2 Players", subtitle: "Pass & play", accent: theme.accent) { onStart(2) }
                ModeButton(title: "3 Players", subtitle: "Pass & play", accent: theme.accent) { onStart(3) }
                ModeButton(title: "4 Players", subtitle: "Pass & play", accent: theme.accent) { onStart(4) }
            }
            .padding(.horizontal, 4)

            HStack(spacing: 16) {
                Button(action: onSettings) {
                    Label("Settings", systemImage: "gearshape.fill")
                        .foregroundColor(theme.bannerInk)
                }
                Button(action: onMute) {
                    Text(muted ? "🔇" : "🔊").font(.title3)
                }
            }
            Spacer(minLength: 8)
        }
        // Keep the menu readable on wide screens (iPad) instead of stretching it.
        .frame(maxWidth: 440)
        .frame(maxWidth: .infinity)
        .padding(.vertical, 16)
    }
}

struct ModeButton: View {
    let title: String
    let subtitle: String
    let accent: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack {
                Text(title).bold()
                Spacer()
                Text(subtitle).font(.caption).opacity(0.75)
            }
            .padding(.vertical, 12).padding(.horizontal, 16)
            .frame(maxWidth: .infinity)
            .background(accent.opacity(0.14))
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .overlay(RoundedRectangle(cornerRadius: 12).strokeBorder(accent.opacity(0.45), lineWidth: 1))
        }
        .buttonStyle(.plain)
        .accessibilityLabel(title)
        .accessibilityHint(subtitle)
    }
}

struct SettingsSheet: View {
    let theme: Theme
    @ObservedObject var engine: GameEngine
    @Binding var themeID: String
    @Binding var name: String
    @Binding var muted: Bool
    /// Restart the current game (only offered while a game is in progress).
    var onStartOver: (() -> Void)? = nil
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Section("Your name") {
                    TextField("You", text: $name)
                        .onChange(of: name) { _, newValue in
                            let cleaned = newValue.replacingOccurrences(of: "\\s+", with: " ", options: .regularExpression)
                            name = String(cleaned.prefix(14))
                        }
                }
                Section("Card theme") {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 12) {
                            ForEach(allThemes) { t in
                                Button { themeID = t.id } label: {
                                    VStack(spacing: 4) {
                                        RoundedRectangle(cornerRadius: 10)
                                            .fill(t.feltGradient)
                                            .frame(width: 60, height: 60)
                                            .overlay(
                                                RoundedRectangle(cornerRadius: 10)
                                                    .strokeBorder(themeID == t.id ? Color.accentColor : .clear, lineWidth: 2.5)
                                            )
                                        Text(t.name).font(.caption2).lineLimit(1).frame(width: 72)
                                    }
                                }
                                .buttonStyle(.plain)
                            }
                        }
                    }
                }
                if let startOver = onStartOver {
                    Section("Game") {
                        Button("Start Over", action: startOver)
                        Text("Reshuffles the deck and resets the current game.")
                            .font(.footnote)
                            .foregroundColor(.secondary)
                    }
                }
                Section {
                    Toggle("Sound effects", isOn: $muted.toggling())
                }
                Section("Debug") {
                    Toggle("Fast A.I.", isOn: Binding(
                        get: { engine.state.fast },
                        set: { engine.state.fast = $0 }
                    ))
                }
            }
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
        .presentationDetents([.medium, .large])
    }
}

/// Inverts a Bool for a Toggle bound to a "muted" flag.
extension Binding where Value == Bool {
    func toggling() -> Binding<Bool> {
        Binding<Bool>(
            get: { !wrappedValue },
            set: { wrappedValue = !$0 }
        )
    }
}