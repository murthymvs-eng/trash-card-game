# 🗑️ Trash — The Card Game (Web)

A fast, faithful web port of the classic **Trash** card game — the easy-to-learn card race
where you fill your trash pile with **A, 2, 3, 4, 5, 6, 7, 8, 9, 10**.

Single file (`index.html`) — no build step, no dependencies. Open it anywhere.

## Rules

- No hands! All **52 cards** start in the **deck**. In front of each player sit **10 trash
  slots** — one for each rank A through 10 (any suit).
- On your turn: **draw 1 card** — from the **deck** or the top of the **discard pile** —
  then either **place it** by dragging it to a matching empty slot, or **discard it**
  (tap the card, or press `X`) into the **discard pile**. Nothing is kept — there is no
  buffer to save cards in.
- A card fits only in its own rank's slot — **except the Jack (J), a wildcard that fits any
  empty slot**. **Queens and Kings are useless** and can never be placed.
- First to fill all **10 slots** wins instantly. If the deck runs out first, the player with
  the **most cards placed** wins.

## Play

- **1 Player** — you vs. the CPU.
- **2–4 Players** — pass & play hotseat.
- Click the deck or the discard pile to draw; drag a card to place it, tap it (or press `X`)
  to discard it. Keyboard: `D` = draw from deck, `C` = draw from discard, `X` = discard.

## Visuals

Every card face is drawn in **SVG** (crisp at any size, no images): classic corner indices,
solid suit pips, stylized illustrated **J / Q / K court cards**, and ornamental card backs —
all laid on a green felt table with lighting and texture.

Five themes use full **art decks** instead — 52 generated PNG card faces each (print-quality
1500×2100, 5:7), one folder per deck alongside `index.html`:

| Theme         | Deck folder                |
|---------------|----------------------------|
| Minions       | `minion_deck/`             |
| Harry Potter  | `hp_card_deck/`            |
| Marvel Avengers | `avengers_deck/`         |
| Star Wars     | `starwars_deck/`           |
| Taylor Swift  | `taylor_swift_tours_deck/` |

Card backs stay SVG (the decks ship faces only).

## Tech

Vanilla HTML/CSS/JS in one file — pointer-based drag & drop, a shared face-up discard pile,
canvas confetti, WebAudio sound effects, and a small state-driven renderer. No frameworks,
no network calls.
