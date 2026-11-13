# Trash → Native iOS (SwiftUI) — Conversion Plan

> Source: `trash-card-game` (single-file web game, `index.html` 1015 lines, no deps).
> Target: native SwiftUI app. No WebView, no runtime reuse of web code — only the **rules engine** logic is ported (as reference); everything renders in SwiftUI.

## Todo Checklist (living — updated as work proceeds)

Progress is tracked here; check items off as each lands.

- [x] **M1 · Project scaffold** — ✅ project created (`ios/TrashGame`, SwiftUI, XCTest), iOS-constrained (iOS 17+, iPhone+iPad), iPhone 17 sim; ✅ 550 JPEG assets bundled (namespaced `deck_suit_rank.jpg` + `back_<id>.jpg` + `bg_<id>.jpg`).
- [x] **M2 · Engine port + tests** — ✅ `Card`, `Player`, `GameState`, `GameEngine` (rules + AI + win detection); 17 `XCTest` cases, all passing on simulator (deck uniqueness, J wildcard, Q/K blocked, auto-discard, exhaustion scoring, full-slot win).
- [ ] **M3 · Native card faces (faithful port)** — re-draw the 5 SVG themes in SwiftUI: Classic, Emoji Party, Fairytale, Neon Night, Woodblock; + `CardFaceView` dispatcher for image decks.
- [ ] **M4 · Screens** — StartView (mode picker 1–4, hero fan, how-to-play), GameView (board rows + deck/discard/banner), PlayerZoneView (10 slots + hand), OverlayView (win screen), SettingsView + ThemePickerView.
- [x] **M3 · Native card faces** — ✅ `NativeCardFace` for Classic/Emoji/Fairytale/Neon/Woodblock + image-deck loader + per-theme backs. Note: classic court cards render letter+glyph (full `portrait()` art not yet re-drawn).
- [x] **M4 · Screens** — ✅ StartView (mode picker 1–4, hero fan), GameView (rows + deck/discard/banner), PlayerZoneView (10 slots + hand), OverlayView, SettingsSheet + theme picker, RootView.
- [x] **M5 · Input** — ✅ tap deck/discard to draw, tap card to discard, **drag-to-slot with immediate finger tracking** (custom `DragGesture` + per-slot frame hit-testing in a shared `"board"` coordinate space — no long-press arming), AI timers.
- [x] **M6 · FX & persistence** — ✅ ConfettiView + SoundEngine (synthesized draw/place/err/discard/win) + `@AppStorage` name/theme/mute + haptics; ✅ per-theme background = felt gradient + blurred/darkened art masked to center (bright felt edges, verified via pixel sampling); ✅ card pop (scale transition) + shake-on-invalid-drop.
- [x] **M7 · Polish** — ✅ haptics, iPad max-width board, accessibility labels (mode buttons, piles, zones, slots, hand card), "Fast A.I." debug toggle in Settings.
- [x] **M8 · Validate** — ✅ full `xcodebuild test` green: 17 unit tests + 1 UI smoke test (launch → "1 Player" → board); ✅ build/install/launch verified; render verified via pixel sampling (felt `#2f9a6a` edges, darkened art center).
- [x] **M9 · Per-theme music** — ✅ `MusicEngine` synthesizes per-theme menu + gameplay loops (key/tempo/timbre per theme), wired to theme/mute/game-state; ✅ licensed-track loader: drop `music_<theme>_<menu|game>.<ext>` into `ios/TrashGame/TrashGame/Music/` and it overrides the synth (see `ios/MUSIC.md`).
- [x] **M10 · Mario deck** — ✅ 52 faces generated at 400×560 (avg 56 KB, same contract as the other decks) + AI card back; 4 houses (Mushroom Kingdom / Luigi's Mansion / Yoshi's Island / Bowser's Castle) with per-house palettes/frames/crests and court characters (Toad, Peach, Bowser, Toadette, Rosalina, Bowser Jr., Lemuki, Goomba, Koopa Troopa, Shy Guy, Dry Bones); theme registered in app + web; `_verify_decks.py` → all decks pass.
- [x] **M11 · iPad layout + deployment** — ✅ landscape-only, responsive board sized to the screen, start screen constrained to a readable 440 pt column, hero fan rebuilt without negative HStack spacing, **iPad camera safe-area asymmetry fixed** (content now centred on the screen: margins 138/137 px, board 312/312 px); built + installed + running on the iPad Air 11" (M3) via `DEVELOPMENT_TEAM=XS9CUNT486` (personal team) with auto-provisioned profile.

## What we are converting

- **Game engine** (~180 lines pure logic): `makeDeck`, `newGame(n)`, `doDraw(source)`, `placeCard`, `discardCard`, `endTurn`, AI (`aiChooseDrawSource`/`aiTurnStart`/`aiStep`), win detection. State: `players[]`, `deck[]`, `center[]`, `turn`, `phase`, `placedThisTurn`, `over`, `winner[]`.
- **Modes:** 1P (vs CPU) and 2–4P hotseat.
- **15 themes:** 5 procedural SVG faces (classic, emoji/animal, fairy, neon, wood) + 10 image decks (52 JPEG faces each, 400 px wide). Per-theme AI card backs (`backs/*.jpg`), full-bleed backgrounds (`bg/*.jpg`), `LOOK` palette (felt/slot/accent).
- **UI:** start screen, settings (name + theme grid), game board, win overlay, how-to-play modal.
- **Input:** pointer drag-to-slot, tap-to-discard, keyboard `D/C/X`.
- **FX:** canvas confetti, WebAudio synthesized SFX.
- **Persistence:** `localStorage` name/theme/mute.
- **Assets:** 550 JPEGs ≈ 44 MB (PNG sources gitignored).

## Architecture mapping (JS → Swift)

| Web | iOS |
|---|---|
| `G` global + `render()` string templating | `@MainActor final class GameEngine: ObservableObject` with `@Published` state; SwiftUI views bind (no HTML strings) |
| `newGame/doDraw/placeCard/discardCard/endTurn/AI` | `GameEngine` methods, ported ~1:1 (pure logic) |
| `after(ms, fn)` timeouts + `fast` flag | `Task { try? await Task.sleep(...) }`, coalesced per move; `fast` honored |
| Pointer drag & drop | `DragGesture` + global-coordinate hit-test vs slot frames; tap = discard |
| Canvas confetti | SwiftUI `Canvas` + `TimelineView` |
| WebAudio oscillators | `AVAudioEngine`/`AVAudioSourceNode` synthesized tones |
| `localStorage` | `@AppStorage("name"/"theme"/"sound")` |
| `THEMES` + `LOOK` | `Theme` struct (id, name, subtitle, palette, face style, deck dir, back, bg) |

## Proposed project structure

```
ios/TrashGame/
├── TrashGameApp.swift
├── Models/        Card.swift, Player.swift, GameState.swift (enum TurnPhase)
├── Engine/        GameEngine.swift, SoundEngine.swift
├── Theme/         Theme.swift (15-theme registry + LOOK palettes)
├── Views/
│   ├── StartView.swift
│   ├── GameView.swift
│   ├── PlayerZoneView.swift
│   ├── CardView.swift (+ CardFaceView)
│   ├── PileView.swift
│   ├── OverlayView.swift
│   ├── ThemePickerView.swift (+ SettingsView)
│   └── Effects/ConfettiView.swift
└── Resources/     (10 deck folders ×52 JPG + backs/ + bg/, as folder refs)
```

## Asset strategy

- Import **only committed JPEGs** (~44 MB) — fine for a bundle. Use Xcode **folder references** for `*_deck/`, `backs/`, `bg/` so filenames map 1:1 to `<suit>_<rank>.jpg` (no renames).
- 10 image themes → `Image(...)`; 5 procedural themes → native SwiftUI face (faithful port).

## Milestones (build order)

1. **Scaffold** — SwiftUI project, import assets, `Theme` registry.
2. **Engine + tests** — port rules/AI/win logic with `XCTest` (deck uniqueness, J wildcard, Q/K blocking, deck-exhaustion scoring).
3. **Native cards** — Classic first, then Emoji/Fairytale/Neon/Woodblock (faithful re-draw of the SVG art).
4. **Screens** — start, settings, theme picker, game board, win overlay.
5. **Input** — tap-to-draw/discard, drag-to-slot with highlighting.
6. **FX** — confetti, synthesized SFX, per-theme background + palette, pop/shake animations.
7. **Polish** — haptics, iPad/landscape, accessibility.
8. **Validate** — build/run on simulator, playtest parity vs web.

## Decisions (locked)

- Native SwiftUI (not WebView).
- **Faithful native port of the 5 SVG card arts** (per user).
- iOS 17+, package all 15 themes + art as-is.

## Risks / notes

- The 5 SVG face themes are the bulk of the fiddly work (`portrait()`/`cornerSet()`/pip layouts → SwiftUI `Path`s).
- Public remote `murthymvs-eng/trash-card-game` — keep tokens/secrets out; JPEGs already committed (no history bloat).
- App Store review may flag trademarked fan-art IP (Minions, Marvel, Star Wars, Harry Potter, etc.) — user to confirm distribution intent.

## Open items

- Project location: `ios/TrashGame/` inside this repo (decided) — confirm committing to the public remote.
## Debug / test hooks (launch arguments)

| Argument | Effect |
|---|---|
| `-startMode N` / `--demo` | Auto-start a game in mode N (starts 0.4 s after launch so the window rotation has settled) |
| `--autoplay` | Both players play automatically — for screen recording |
| `-forceCard <rank>` | Forces the next card drawn (e.g. `-forceCard 4`) — used by the UI tests |
| `-trashTheme <id>` | Force a theme (e.g. `mario`) |

Accessibility identifiers used by the UI tests: `hand-card`, `slot-<player>-<slot>`.

- App name/bundle id: `TrashGame` / `com.<you>.trashgame` (TBD).