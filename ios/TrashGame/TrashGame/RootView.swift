import SwiftUI
import UIKit

struct RootView: View {
    @StateObject private var engine = GameEngine()
    @AppStorage("trashTheme") private var themeID = "classic"
    @AppStorage("trashName") private var name = "You"
    @AppStorage("muted") private var muted = false
    @State private var inGame = false
    @State private var showSettings = false

    private var currentTheme: Theme { theme(themeID) }

    var body: some View {
        GeometryReader { geo in
            ZStack {
                background(geo.size)
                if inGame {
                    GameView(engine: engine, theme: currentTheme)
                } else {
                    StartView(
                        theme: currentTheme,
                        muted: muted,
                        onMute: { muted.toggle() },
                        onStart: start,
                        onSettings: { showSettings = true }
                    )
                }
                if inGame && engine.state.over {
                    OverlayView(
                        engine: engine,
                        theme: currentTheme,
                        onAgain: { engine.newGame(mode: engine.state.mode) },
                        onChangeMode: { inGame = false }
                    )
                    if engine.state.winner.count == 1 { ConfettiView() }
                }
            }
            // Lay the content out on the FULL screen: iPads reserve an asymmetric
            // safe area for the front camera in landscape, which would otherwise
            // push the board off-centre.
            .frame(width: geo.size.width, height: geo.size.height)
            // Exit to the main screen. Anchored to the screen frame (not to the
            // board) so it always sits in the visible corner of the display.
            .overlay(alignment: .topTrailing) {
                if inGame {
                    HStack(spacing: 8) {
                        settingsChip
                        exitChip
                    }
                    .padding(.top, 6 + screenInsets.top)
                    .padding(.trailing, 16 + screenInsets.right)
                }
            }
        }
        .ignoresSafeArea()
        .onAppear {
            wireEngine()
            if ProcessInfo.processInfo.arguments.contains("--autoplay") {
                // Demo: auto-play a full 1P game (both players) for screen-recording.
                engine.isAutoPlaying = true
                engine.newGame(mode: 1)
                inGame = true
                engine.aiTurnStart()
            } else {
                // Demo/debug: launch with `-startMode N` (or `--demo`) to auto-start a game.
                let demoMode = ProcessInfo.processInfo.arguments.contains("--demo") ? 1
                    : UserDefaults.standard.integer(forKey: "startMode")
                if demoMode >= 1 && !inGame {
                    // Start after the launch rotation has settled, otherwise the
                    // board can end up in a state where touches are dropped.
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) { start(demoMode) }
                }
            }
            if ProcessInfo.processInfo.arguments.contains("--landscape") {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
                    if let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene {
                        scene.requestGeometryUpdate(.iOS(interfaceOrientations: .landscapeRight))
                        scene.keyWindow?.rootViewController?.setNeedsUpdateOfSupportedInterfaceOrientations()
                    }
                }
            }
            MusicEngine.shared.setMuted(muted)
            MusicEngine.shared.play(theme: themeID, mode: inGame ? .game : .menu)
        }
        .onChange(of: name) { _, newName in engine.userName = newName.isEmpty ? "You" : newName }
        .onChange(of: muted) { _, m in SoundEngine.shared.setMuted(m); MusicEngine.shared.setMuted(m) }
        .onChange(of: inGame) { _, playing in MusicEngine.shared.play(theme: themeID, mode: playing ? .game : .menu) }
        .onChange(of: themeID) { _, _ in MusicEngine.shared.play(theme: themeID, mode: inGame ? .game : .menu) }
        .sheet(isPresented: $showSettings) {
            SettingsSheet(
                theme: currentTheme,
                engine: engine,
                themeID: $themeID,
                name: $name,
                muted: $muted,
                // Only offered in-game: restart the current mode from scratch.
                onStartOver: inGame ? {
                    showSettings = false
                    Haptics.tap()
                    engine.newGame(mode: engine.state.mode)
                } : nil
            )
        }
    }

    /// Matches the web background: full-bleed cover image, slightly darkened
    /// and saturated, under the same radial scrim as index.html (a light veil
    /// in the centre, darker toward the screen edges).
    private func background(_ size: CGSize) -> some View {
        ZStack {
            currentTheme.feltGradient
            if let img = bundleImage("bg_\(currentTheme.id)") {
                Image(uiImage: img)
                    .resizable()
                    .scaledToFill()
                    .brightness(-0.18)
                    .saturation(1.06)
                    .overlay(
                        RadialGradient(
                            gradient: Gradient(stops: [
                                .init(color: .black.opacity(0.38), location: 0),
                                .init(color: .black.opacity(0.28), location: 0.32),
                                .init(color: .black.opacity(0.10), location: 0.56),
                                .init(color: .black.opacity(0.55), location: 1.0)
                            ]),
                            center: .center,
                            startRadius: 0,
                            endRadius: max(size.width, size.height) * 0.75
                        )
                    )
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    /// Floating chip that leaves the game and returns to the main screen.
    private var exitChip: some View {
        Button {
            Haptics.tap()
            exitToMenu()
        } label: {
            HStack(spacing: 3) {
                Image(systemName: "chevron.left").font(.system(size: 10, weight: .bold))
                Text("Menu").font(.system(size: 12, weight: .semibold))
            }
            .foregroundColor(.white)
            .padding(.horizontal, 9)
            .padding(.vertical, 5)
            .background(Capsule().fill(Color.black.opacity(0.45)))
        }
        .buttonStyle(.plain)
        .accessibilityIdentifier("exit-button")
        .accessibilityLabel("Exit to main screen")
    }

    /// Floating chip that opens the in-game settings (theme / start over).
    private var settingsChip: some View {
        Button {
            Haptics.tap()
            showSettings = true
        } label: {
            HStack(spacing: 3) {
                Image(systemName: "gearshape.fill").font(.system(size: 10, weight: .bold))
                Text("Settings").font(.system(size: 12, weight: .semibold))
            }
            .foregroundColor(.white)
            .padding(.horizontal, 9)
            .padding(.vertical, 5)
            .background(Capsule().fill(Color.black.opacity(0.45)))
        }
        .buttonStyle(.plain)
        .accessibilityIdentifier("settings-button")
        .accessibilityLabel("Open settings")
    }

    /// Safe-area insets of the real window (the app ignores the safe area, so
    /// `GeometryReader` reports zero).
    private var screenInsets: UIEdgeInsets {
        let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene
        return scene?.keyWindow?.safeAreaInsets ?? .zero
    }

    /// Leaves the game and returns to the main screen.
    private func exitToMenu() {
        inGame = false
        engine.abortGame()
    }

    private func start(_ mode: Int) {
        engine.newGame(mode: mode)
        inGame = true
    }

    private func wireEngine() {
        engine.onSound = { SoundEngine.shared.play($0, theme: themeID) }
        engine.onWin = { Haptics.win() }
        engine.userName = name.isEmpty ? "You" : name
        SoundEngine.shared.setMuted(muted)
    }
}