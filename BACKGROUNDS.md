# Theme Backgrounds (`bg/`)

One landscape JPEG per theme, rendered behind the board as "environment, not picture".

## Contract

- File: `bg/<themeId>.jpg` — lowercase, exact match (GitHub Pages is case-sensitive).
- Format: JPEG q82, 1600×896 (Qwen rounds 900→896; `background-size:cover` absorbs it).
- Subject: environment only — no people, hands, cards, or text. Busy detail belongs at
  the frame edges; the middle hosts the card zone.
- Missing file ⇒ automatic silent fallback to the theme's felt gradient
  (`preloadBg()` marks it `missing` → `applyTheme()` switches to plain felt).
  No HTML change ever needed to add/replace a background — just drop the file in
  and refresh.

## Generation recipe (ComfyUI, Qwen-Image 2.1 Turbo)

CLI: `~/.cline/skills/comfyui-image-gen/qwen_image.py` · server `100.120.166.95:8000`
Always `curl -4` the server (its IPv6 address is unroutable from this Mac).

Settings, same for every theme (fixed seed = series coherence):

```
--width 1600 --height 896 --seed 2127 --steps 8 --cfg 1.0
--negative-prompt "text, watermark, logo, signature, letters, numbers, playing cards,
hands, people, faces, blurry, lowres, jpeg artifacts, deformed, cluttered center,
bright center, washed out, oversaturated"
```

Prompt scaffold (suffix identical for all 15):

```
<scene>, empty center, no people, no hands, no text, no cards,
cinematic, wide establishing shot, shallow depth of field, bokeh,
dramatic rim lighting, vignette, dark moody color grade, highly detailed, 8k
```

Scenes:

| Theme | Scene | Palette |
|---|---|---|
| classic | Aged green baize card table, brass banker's lamp, dark wood study, cigar-box leather, dust motes | green / brass |
| animal | Pastel woodland clearing, giant mushrooms, falling leaves, storybook moss, peach dawn light | mint / peach |
| minion | Yellow industrial construction lab, girder steel, crates, harsh work lights, steel-blue shadows | yellow / steel |
| fairy | Moonlit garden, fireflies, gilded vines, glowing toadstools, lavender mist, willows | lavender / gold |
| neon | Cyberpunk rooftop, holographic signage, wet reflective parapet, megacity towers | magenta / cyan |
| wood | Japanese woodblock room, tatami table, ink-wash mountains past shoji, sepia lantern light | sepia / indigo |
| hp | Candlelit grand library, floating books, gothic arches, oxblood leather, gold leaf | oxblood / gold |
| avengers | Glass penthouse command floor at night, city skyline, hex-pattern tech, chrome | crimson / gold |
| starwars | Desert cantina doorway at dusk, twin suns over dunes, chrome doorframes, amber haze | amber / blue |
| spiderman | NYC rooftop at dusk, water tower, fire-escape lattice, glinting silk, navy skyline | navy / crimson |
| coco | Ofrenda at night, marigold petals, papel picado, candle glow | marigold / magenta |
| princess | Gilded ballroom, gold columns, stained-glass windows, chandeliers, rose petals | rose / gold |
| taylor | Stadium stage in haze, confetti, pink/gold beams, rigging bokeh | pink / gold |
| moana | Sunset over a tropical lagoon, black sand beach, palm trees, outrigger canoe | turquoise / gold |
| toystory | Sunlit child's playroom, wooden floorboards, stacked toy boxes, alphabet rug | primary red / gold |

Pipeline per image: generate PNG → `sips -s format jpeg -s formatOptions 82 <png> --out bg/<id>.jpg`.
Run ONE generation at a time (VRAM rule from the skill); a sequential loop is fine.

## Legibility guarantee (design invariant)

Measured reality: diffusion models reliably put the busiest, brightest content
mid-frame, regardless of "empty center" prompting (princess seed-2127 raw art:
center gradient energy 77.6 vs edges 41.5 — inverted). The game therefore enforces
calm in CSS, not in the art:

1. `--scrim` over photo themes veils the center: `rgba(0,0,0,.38) 0% → .28 32% → .10 56% → .55 100%`.
2. `#bgLayer::after` — a blurred (14px), darkened (×0.72) copy of the art masked
   to the card zone softens whatever lands mid-frame.

Effective environment (art × scrim × blur) for princess, 1280×800 probe:
center luma 0.056 / energy 5.2, edges energy 22.4 (4.3× busier) — all acceptance
gates PASS; card-vs-background contrast ≈ 8.5:1.

## Acceptance gates (`luma.py` probe, center box 30–70% vs edge ring)

1. center mean luma ≤ 0.40 (dark middle)
2. center gradient energy ≤ edge gradient energy (calm middle)
3. edge energy ≥ 1.1× center (meaningful periphery)
4. center luminance stdev ≤ 0.18 (low local contrast)

Raw-art failures of gates 2–4 are acceptable (CSS compensates); raw gate-1 failures
(bright hot spots the veil can't tame) get one seed re-roll (+1).

---

# Card backs (`backs/`)

One back per theme, 5:7 portrait, AI-generated with the same server and seed family as the
backgrounds (seed **4242**, so the back art reads as a separate series).

```
--width 640 --height 896 --seed 4242 --steps 8 --cfg 1.0
--negative-prompt "text, letters, numbers, watermark, logo, signature, hands, people, faces,
blurry, lowres, jpeg artifacts, tilted, angled, perspective, asymmetric, off-center, cluttered,
harsh shadows"
```

Prompt suffix (identical for all 15):

```
<scene>, playing card back design, flat front facing view, vertical mirror symmetry,
ornate rectangular border frame, centered emblem, repeating pattern,
no text, no letters, no numbers, highly detailed, crisp illustration
```

| Theme | Scene |
|---|---|
| classic | green & gold damask, baroque scrollwork, gold rosette medallion |
| animal | pastel woodland, leaves & mushrooms, paw-print medallion |
| minion | yellow/steel-blue industrial, hazard stripes, goggle-lens emblem |
| fairy | lavender & gold garden, gilded vines, fireflies, crescent medallion |
| neon | magenta/cyan holo circuit grid, hexagon chip emblem |
| wood | sepia/indigo woodblock, seigaiha waves, ink-wash mountains, red sun disc |
| hp | oxblood & gold gothic leather, gold filigree, owl & starry circle |
| avengers | crimson & gold hex-tech lattice, triangular arc-reactor emblem |
| starwars | deep blue & amber chrome panels, twin-sun emblem |
| spiderman | navy & crimson, full radial web, spider emblem |
| coco | marigold & magenta papel picado, sugar-skull medallion |
| princess | rose & gold castle filigree, crown & rose medallion |
| taylor | pink & gold glitter, confetti, stage beams, starburst emblem |
| moana | turquoise & gold lagoon, nautilus-shell medallion, wave pattern |
| toystory | primary toy-box colours, alphabet blocks, golden sheriff-star medallion |

Shipped at **343×480 JPEG q80** (56–130 KB each, 1.1 MB total) — ~4× the largest on-screen
render, so no visible softness. Re-encode with `sips -Z 480 -s format jpeg -s formatOptions 80`.

**Wiring + fallback.** `THEMES[id].back()` now returns an `<img class="face-svg cardimg">`; the
previous hand-drawn SVG is kept as `THEMES[id]._backFallback` and is swapped in by `backFail()`
if the JPG is missing or fails to load (verified by blocking the request — the legacy SVG
renders instead). Deck piles, the hand and the review sheet all use the same path.

**Validation.** Mirror-symmetry score 0.70–0.88 across the set (no asymmetric outliers); every
back has a legible central emblem (center stdev 0.09–0.33); all 13 load in-game and in
`_theme_review.html`; the deck pile re-renders on theme switch.

> Gotcha: ComfyUI names outputs `<prefix>_<counter>_.png` with a **server-global** counter — never
> assume `_00001_`; pick the newest matching file (`ls -t <prefix>_*.png | head -1`).
