# 🗑️ Trash — The Classic Card Game (Web)

A fast, faithful web port of the classic **Trash** card game — the easy-to-learn card race
where you fill your trash pile with **all the 2s, then all the 3s**.

Single file (`index.html`) — no build step, no dependencies. Open it anywhere.

## Rules

- Every player is dealt **4 cards**. In front of you sit **8 trash slots**:
  top row `2♣ 2♦ 2♥ 2♠`, bottom row `3♣ 3♦ 3♥ 3♠`.
- On your turn: **draw 1 card**, then **place up to 2** cards from your hand into matching
  empty slots (any order).
- First to fill all **8 slots** wins instantly. If the deck runs out first, the player with
  the **most cards placed** wins.

## Play

- **1 Player** — you vs. the CPU.
- **2–4 Players** — pass & play hotseat.
- Keyboard: `D` = draw, `Enter` / `E` = end turn.

## Tech

Vanilla HTML/CSS/JS in one file — canvas confetti, WebAudio sound effects, and a small
state-driven renderer. No frameworks, no network calls.
