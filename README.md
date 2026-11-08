# 🗑️ Trash — The Card Game (Web)

A fast, faithful web port of the classic **Trash** card game — the easy-to-learn card race
where you fill your trash pile with **A, 2, 3, 4, 5, 6, 7, 8, 9, 10**.

Single file (`index.html`) — no build step, no dependencies. Open it anywhere.

## Rules

- Every player is dealt **4 cards**. In front of you sit **10 trash slots** — one for each
  rank A through 10 (any suit).
- On your turn: **click the deck to draw 1 card**, then **drag** up to 2 cards from your
  hand onto matching empty slots.
- A card fits only in its own rank's slot — **except the Jack (J), a wildcard that fits any
  empty slot**. **Queens and Kings are useless** and can never be placed.
- First to fill all **10 slots** wins instantly. If the deck runs out first, the player with
  the **most cards placed** wins.

## Play

- **1 Player** — you vs. the CPU.
- **2–4 Players** — pass & play hotseat.
- Click the deck to draw; drag cards to place. Keyboard: `D` = draw, `Enter` / `E` = end turn.

## Tech

Vanilla HTML/CSS/JS in one file — pointer-based drag & drop, canvas confetti, WebAudio sound
effects, and a small state-driven renderer. No frameworks, no network calls.
