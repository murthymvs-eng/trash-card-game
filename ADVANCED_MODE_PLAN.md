# Advanced Mode — Plan

> Status: **draft, pending sign-off** (2026-11-13)
> Scope: new game mode alongside the existing 1–4 player modes, in **both** the web build
> (`index.html`) and the iOS app (`ios/TrashGame`). Classic mode stays byte-for-byte identical.

## 1. Rules — "Advanced" (FINAL — user-confirmed 2026-11-13)

- **Setup:** same 52-card deck. Every player is dealt **10 cards face down, one per trash
  slot** (a "cover" on each). The deck keeps the rest: 52 − 10·players
  (2P → 32, 3P → 22, 4P → 12 cards in the deck).
- **Your turn (a chain of draws + placements):**
  1. **Draw 1** — from the **deck** or the top of the **discard** (your choice, as today).
  2. **Place** any card in your hand that fits an open slot (rank A–10, or **J** into any
     open slot). Placing it **unlocks the cover** on that slot: the face-down card flips
     **into your hand**.
  3. After placing, **draw again** — your turn continues.
  4. **End your turn by discarding:** tap any card in hand to discard it — the discarded
     card **plus every card left in hand** (unplayed covers) goes to the **discard pile**.
  5. If **nothing in hand fits** an open slot, you must discard (auto after a short beat).
- **Winning:** unchanged — first player to fill all 10 slots wins. If it's someone's turn
  to draw and **both** the deck and the discard are empty, the game ends and the player
  with the most placed cards wins (tie possible). Classic keeps its current
  "deck empty → score" rule.
- Slot positions/ranks unchanged (A … 10 left to right); a cover hides the slot's rank
  ghost. Covered ⟺ slot is empty (kept in sync the whole game).
- Covers live in the **hand** (not the discard): placing a card flips its cover into
  the hand and you resolve it the same turn (place it if it fits). **One draw per turn** —
  a turn is a single draw followed by a chain of placements, so the active hand is a
  single card at a time.

### Final decisions (user-confirmed)
- **Cover fate = Option 3:** flipped cover goes to the **player's hand**; you chain it
  (place if it fits, discard to end the turn). Leftover hand at turn end → discard pile.
- **Placement optional** — you may always tap a card to discard and end your turn early.
- **1/2/3/4-player Advanced** — mirrors the classic button grid.
- **No new assets** — unlock animation reuses existing pop/flip styling; SFX reuses
  place/draw (a dedicated flip sound is an optional later add).

## 2. Engine changes (web `index.html` first, then iOS mirror)

### Shared logic
- `G`/`GameState`: add `advanced: Bool`. Per player: `covers: (Card|null)[10]`
  (all nil in classic). Covered ⟺ slot empty (kept in sync).
- `newGame(mode, advanced)`: after shuffling, pop 10 cards per player into `covers`
  (deck shrinks by 10·players).
- `placeCard`: on success, if `advanced` → the slot's **cover flips into the player's
  hand** (`covers[s]` → `hand`, `covers[s]=null`, `lastUnlocked` for animation). Win check
  as today. Then **instead of `endTurn`**, schedule (≈450 ms) a *continue-turn* step:
  - guard: if deck **and** center empty → `gameOverByScore`;
  - else **stay in the acting phase** (one draw per turn — no re-draw): reset `placedThisTurn`,
    clear `turnDrawnCard`/`lastDrawn`, render; if AI → `aiStep()` (place the next card,
     or auto-discard); for a human the turn auto-ends after ≈1200 ms if nothing is
     playable, else they place to continue or tap to discard.
- `discardCard`: classic = as today. Advanced: the discarded card **plus every card left
  in hand** goes to the discard pile, then `endTurn`.
- Auto-end: unified `handHasPlayable(p)` check (classic hand is just the drawn card, so
  behaviour is unchanged). Nothing playable → after ≈1200 ms auto-discard
  (advanced: `discardCard` dumps the hand; classic: `endTurn` auto-discard).
- `doDraw` / `endTurn`: safety guard — both piles empty → `gameOverByScore` (advanced).
  Classic's deck-empty → score rule untouched.
- AI: `aiStep`/`aiTurnStart` structure unchanged — in advanced the
  place → continue-turn → aiStep chain runs (drawing only once) until the AI has
  nothing to place and discards (dumping its hand).
### Web specifics
- `newGame(n)` → `newGame(n, advanced=false)`; `G.advanced`; start-screen wiring
  (`data-adv`), "Play Again" (`newGame(G.mode, G.advanced)`).
- Start screen: keep the 4 classic buttons; add an **"Advanced"** labeled row of 4
  buttons (1 Player / 2 / 3 / 4, subtitle "Covered slots — draw until you must discard").
- `renderZone`: a covered slot renders the **card back** (`.slot.covered`) instead of the
  rank ghost; unlock = flip/pop animation via `lastUnlocked`.
- Banner text for advanced ("Keep drawing — place it, or tap to end your turn").
- How-to-play modal: new "Advanced mode" section.

### iOS specifics (`ios/TrashGame`)
- `GameState`: `advanced: Bool`; `Player.covers: [Card?]` (default all nil — keeps
  existing tests green).
- `GameEngine.newGame(mode:advanced:)` + the same engine changes (continue-turn step,
  guards, AI fall-through).
- `StartView`: "Advanced" group — 4 `ModeButton`s; `onStart: (Int, Bool)` through
  `RootView`; "Play Again" passes `state.advanced`.
- `PlayerZoneView`/slot: covered slots render the card back with a flip-on-unlock
  animation (animate on `covers` change).
- `GameView` banner: advanced variant text.
- Tests (`TrashGameTests`, existing style with synchronous timers):
  1. Advanced deal: covers dealt 10/player, deck = 52 − 10n, no placements.
  2. Placement unlocks: cover → discard, slot filled, `covers[s] == nil`.
  3. Turn continues after placement (phase back to `.awaiting`, same player,
     `placedThisTurn == 0`).
  4. Explicit discard ends the turn.
  5. Unplayable draw auto-discards and ends the turn.
  6. Win on 10th placement.
  7. Score game-over when both piles empty (and not before).
  8. AI plays a full advanced game to completion (synchronous timers, terminates).
  9. Regression: classic behaviour unchanged (existing suite must pass untouched).
- Optional UI test: launch → tap Advanced 1P → assert covered slots + deck count 32.

## 3. Docs & deployment
- Web: `README.md` + How-to modal; push to `main` → GitHub Pages auto-deploys.
- iOS: run full test suite; `xcodebuild` Release; install on the iPad
  (UDID `00008122-000629383E61801C`, check `devicectl list` first).
- `IOS_APP_PLAN.md` note + memory-bank updates (`progress.md`, `activeContext.md`).

## 4. Risks / edge cases
- **4-player advanced:** only 12 deck cards → game almost always ends by score. Fine;
  note it in the How-to text.
- Discard pile grows fast (covers + Q/K) → late draws skew random. That's the point of
  the mode; deck-count UI already shows the state.
- Timer/AI chaining must respect existing invalidation (web `G.timers` / iOS
  `generation`) so "Start Over"/exiting mid-chain can't double-advance.
- Keep every change gated on `advanced` so the classic path and its tests are untouched.

## 5. Build order
1. Web engine + UI + how-to → manual playthrough.
2. iOS models + engine + tests green.
3. iOS views (start group, covers, banner) → UI test.
4. Deploy: Pages push + iPad build.
5. Docs + memory bank.

