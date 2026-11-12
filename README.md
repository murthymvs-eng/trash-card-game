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

Eight themes use full **art decks** instead — 52 generated card faces each (5:7), one folder per
deck alongside `index.html`:

| Theme         | Deck folder                |
|---------------|----------------------------|
| Minions       | `minion_deck/`             |
| Harry Potter  | `hp_card_deck/`            |
| Marvel Avengers | `avengers_deck/`         |
| Star Wars     | `starwars_deck/`           |
| Taylor Swift  | `taylor_swift_tours_deck/` |
| Spider-Man    | `spiderman_deck/`          |
| Coco          | `coco_deck/`               |
| Princess      | `princess_deck/`           |
| Moana         | `moana_deck/`              |
| Toy Story     | `toystory_deck/`           |

The two newest decks — **Moana** and **Toy Story** — are generated end-to-end by
`_gen_deck.py` (art direction in `_deck_specs.py`): 52 card faces per deck, four
character "houses" mapped to the four suits, court cards carrying a name plate
and the number cards reusing the house's lead character inside a true pip layout.
Both ship as 400 px JPEG faces plus a `manifest.json` recording each card's
house, character and seed.

Two details are worth knowing if you regenerate them:

- **Pips are composited, not painted.** The image model cannot count (asked for
  "two heart pips" it draws four), so the model paints the card art with the
  field left clear and `_pips.py` overlays mathematically correct pips
  afterwards — a "7" always shows seven.
- **Faces ship at exactly 400×560 (5:7).** The board draws cards into a
  `aspect-ratio:5/7` box, so the source is centre-cropped to 5:7 before
  downscaling; these decks have 0 % aspect deviation.

Run `python3 _verify_decks.py` to check every deck for missing faces, wrong
width, unreadable files and manifest coverage.

Every deck ships **400 px-wide JPEG card faces (49–137 KB each)** — the display renders a card at
most ~90 CSS px wide, so 400 px is roughly 2× headroom at 2× DPR. The five older art decks were
generated at 1500×2100 and downscaled (those PNG sources stay on disk, out of git; regenerate
their JPEGs with `python3 _optimize_decks.py --jpg`) — that took the tracked art from
**1.7 GB to 15 MB**. The Moana and Toy Story decks are instead generated **directly at 400×560**
by `_gen_deck.py` — no print-resolution pass, no downscale (~14× fewer latent pixels, ~10 s per
card). See `DECK_OPTIMIZATION.md` for the full measurements and rationale.

Card backs are **AI-generated per theme** — `backs/<themeId>.jpg` (343×480 JPEG, ~80 KB each) — with
the original hand-drawn SVG backs kept as an automatic fallback if a file is missing, so a deck is
never broken.

### Theme backgrounds

Each theme also ships a full-bleed environment photo — `bg/<themeId>.jpg`, 1600×896 JPEG q82,
AI-generated via ComfyUI (Qwen-Image 2.1 Turbo). See `BACKGROUNDS.md` for the prompt set, seeds
and the legibility spec. A fixed scrim plus a blurred, darkened copy of the art masked over the
card zone keeps the middle calm while edges stay alive, and the felt/slot/accent colours re-tint
per theme. A missing file silently falls back to the theme's felt gradient — themes ship
independently.

## Tech

Vanilla HTML/CSS/JS in one file — pointer-based drag & drop, a shared face-up discard pile,
canvas confetti, WebAudio sound effects, and a small state-driven renderer. No frameworks,
no network calls.
