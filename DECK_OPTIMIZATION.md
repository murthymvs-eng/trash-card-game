# Deck Asset Scaling for Web Play

Goal: get the eight art decks to load fast over the web without visible
quality loss, and stop paying for ~1.7 GB of print-resolution PNGs in the repo.

**Status: DONE (2026-11-10).** Results are recorded at the bottom of this file.

## Current state (measured 2026-11-10)

| Deck | Faces | Format | On disk | Tracked in git |
|---|---|---|---|---|
| `avengers_deck` | 52 | PNG 1500×2100 | 356 MB | yes |
| `hp_card_deck` | 52 | PNG 1500×2100 | 331 MB | yes |
| `minion_deck` | 52 | PNG 1500×2100 | 312 MB | yes |
| `starwars_deck` | 52 | PNG 1500×2100 | 329 MB | yes |
| `taylor_swift_tours_deck` | 52 | PNG 1500×2100 | 371 MB | yes |
| `coco_deck` | 52 | PNG + JPEG 400px | 48 MB | JPEG only (PNG gitignored) |
| `princess_deck` | 52 | PNG + JPEG 400px | 48 MB | JPEG only |
| `spiderman_deck` | 52 | PNG + JPEG 400px | 47 MB | JPEG only |

- Working tree: **912 MB**; `.git`: **333 MB**; GitHub remote: **1.7 GB**
  (API `size` = 1,737,651 KB).
- Every card face averages **6–7 MB** in the five PNG decks.
- The PNGs are 1500×2100 — print resolution (2.5×3.5 in @ 600 DPI).

## The key insight: we are already shipping far more pixels than we display

CSS caps a card at `clamp(46px, 8.2vw, 80px)` wide; the hand is
`clamp(56px, 8.6vw, 86px)`. Even on a 2× DPR phone that is **~180 device px**.
The existing 400 px JPEG decks (`coco`, `princess`, `spiderman`) are therefore
**~4.4× oversampled at 1× and ~2.2× at 2×** — already proven in production.

So 400 px is the correct target width, and the five PNG decks simply never got
## Measured results (tool: `_optimize_decks.py`, validated on `minion_deck`)

| Source | Output | Size |
|---|---|---|
| PNG 1504×2096, 7.07 MB | JPEG 400px q80 progressive | **61 KB** |
| " | WebP 400px q80 | **54 KB** |
| " | AVIF 400px q55 | **40 KB** |
| " | WebP 320px q78 | **31 KB** |

Whole-deck run on `minion_deck`: **312.5 MB → 2.61 MB** (49 KB/card avg),
**10 seconds** with 8-way parallelism.

Projected across all five decks: **1,699 MB of PNG → ~13 MB of JPEG.**
That is a **~99% reduction**, and it takes the working tree from 912 MB to
roughly **35 MB**.

Quality check: original vs. 400 px JPEG cropped side by side at render scale —
indistinguishable (fine filigree, hairline gold borders and small index
numerals all survive; only the extreme fine grain in the background wash
softens, and it is never visible at ≤90 CSS px).

## Plan

### Phase 1 — Normalize the five PNG decks (the big win)

1. Convert every face to **400 px wide JPEG, q80, progressive** — the exact
   contract the three shipped decks already use. ~10 s per deck.
2. Update `.gitignore` to exclude `*_deck/*.png` for all decks, not just the
   three that already do it.
3. `git rm --cached` the 260 tracked PNGs, then `git add` the new JPEGs.
4. Update `index.html` `imgTheme(...)` calls so the five decks pass `'jpg'`
   instead of the default `'png'`.
5. Keep the source PNGs on disk (they are ignored, not deleted) so the art can
   still be re-exported at another size later.

Result: repo tracks ~13 MB of card faces instead of ~1.7 GB.

### Phase 2 — Reclaim git history

Rewriting history is required to drop the 1.7 GB already pushed. `git-filter-repo`
is installed for this.

```
git filter-repo --path-glob '*_deck/*.png' --invert-paths
git push --force origin main
```

This removes the PNG blobs from all 19 commits. The remote should drop from
### Phase 4 — Optional further wins

- **WebP/AVIF via `<picture>`**: AVIF is 40 KB vs JPEG 61 KB (a further 35% off
  the ~13 MB). Requires emitting `.avif`/`.webp` alongside the JPEG and
  changing `imgFace()` to emit a `<picture>` element with a JPEG fallback.
  Roughly a third of the remaining bytes.
- **Sprite sheet per deck**: one WebP atlas per deck (13 ranks × 4 suits) plus
  a JSON index — `minion_deck` atlas is **2.15 MB in a single request** vs 52
  separate files. Cuts request count from 52 to 1 and lets the whole deck be
  cached as one object. Requires changing `imgFace()` to use
  `background-position` on a shared sheet.
- **Cap DPR**: add `srcset` at 1×/2× so 400 px is served deliberately rather
  than by assumption.
- `bg/` is already 3.4 MB total and `backs/` 1.1 MB — both fine, no action.

## Verification

- `python3 _optimize_decks.py --report` — per-deck before/after.
- Playwright: load `index.html`, open Settings, count image requests and total
  transferred bytes; assert no request exceeds ~150 KB and the theme grid
  issues no PNG requests.
- Visual: `_build_review.py` regenerates `_theme_review.html` — the contact
  sheet renders every rank of every theme over its own background, so it is
  the fastest way to eyeball all eight decks at once for any downscale
  artifact.
- Check `index.html` `imgTheme` calls all point at `.jpg`; a missing file
  shows as a broken image, so grep for `imgTheme(` and confirm the extension
  argument on each of the eight art decks.

## Notes / risks

- `sips` on this machine cannot write WebP (`Error 13`) — WebP/AVIF encoding
  must go through Pillow (`pip3 install --user pillow`; Pillow here has both
  WebP and AVIF support). Pillow is not currently a declared dependency, so
  Phase 1 uses `sips` (already installed, JPEG only) and needs no new deps.
- The three existing JPEG decks were exported at 400 px from *different* source
  art than the PNG decks, so after conversion the five converted decks will
  match them in resolution but not necessarily in JPEG quantization quality.
  Matching them exactly would mean re-encoding the three shipped decks too —
  optional, and only worth it for byte-level consistency.
- `.git/refs/heads/main 2` is a stray broken ref in this clone (from a Finder
  copy). It makes `git show-ref` and `git rev-list --all` error out, but does
  not affect `refs/heads/main` or the build. Worth deleting.
- The `.mov` screen recording at the repo root is **58 MB** and is tracked.
  Removing it from tracking (keeping it locally) is a free additional win.

1.7 GB to roughly 30–40 MB. **This rewrites history** — every existing clone
must be re-cloned, and any open PRs break. It is a one-time operation.

### Phase 3 — Fix the runtime load burst

Right now `buildThemeGrid()` renders a live card face for **every** theme at
once, so opening Settings fires ~16 large face images in parallel — the
heaviest single moment in the app. After Phase 1 this drops from ~7 MB each to
~50 KB each, which largely solves it. Two cheap follow-ups:

- Add `loading="lazy"` + `decoding="async"` to the theme-grid preview faces so
  off-screen ones never fetch.
- Add `loading="lazy"` to the card faces rendered into slots/hands, so the
  initial paint only fetches the cards actually on screen.

converted.

## What was actually done

### Phase 1 — Convert the five PNG decks ✅

All five decks converted to **400 px wide progressive JPEG q80**, matching the
contract `coco`/`princess`/`spiderman` already used:

| Deck | PNG before | JPEG after |
|---|---|---|
| `avengers_deck` | 355.9 MB | 3.09 MB (58 KB/card) |
| `hp_card_deck` | 331.3 MB | 2.84 MB (53 KB/card) |
| `minion_deck` | 312.5 MB | 2.61 MB (49 KB/card) |
| `starwars_deck` | 328.6 MB | 2.78 MB (52 KB/card) |
| `taylor_swift_tours_deck` | 371.3 MB | 3.47 MB (65 KB/card) |
| **Total** | **1,699.5 MB** | **14.79 MB** |

`.gitignore` now excludes `*_deck/*.png` for every deck (not just three), and
the source PNGs stay on disk so the art can still be re-exported at any size.
`_optimize_decks.py` regenerates the JPEGs in ~10 s per deck (8-way parallel).

### Phase 2 — Reclaim history ✅

```
git filter-repo --path-glob '*_deck/*.png' --path-glob '*.mov' --invert-paths --force
git push --force origin main
```

- Local `.git`: **1.8 GB → 37 MB** (single pack, 585 objects).
- All 22 commits preserved (hashes rewritten), working tree untouched.
- The 58 MB `.mov` was dropped from history as well.
- Remote `main` now points at `c33f6bc`; GitHub Pages rebuilt automatically.
- The old PNG paths now return **404** on the live site.

### Phase 3 — Runtime load burst ✅

- `imgFace()` now emits `decoding="async"`.
- Theme-picker preview faces are `loading="lazy"`, so opening Settings no
  longer fires every deck's images at once — the grid issues **8 card requests
  instead of 16**, and only for the visible row.
- `imgTheme()` default extension changed `png` → `jpg` (the three decks that
  already passed `'jpg'` are unaffected).

### Verification

- All 8 decks resolve to 400 px faces, **zero broken images** (checked locally
  and on the live site).
- Full 1-player game played to completion on the deployed site — 19 slots
  filled, 25/25 card images loaded, all `.jpg`, no `.png` requests.
- Live sizes per card face: minion 49 KB, hp 69 KB, avengers 71 KB,
  starwars 68 KB, taylor 65 KB, princess 118 KB, coco 135 KB, spiderman 137 KB.
- The theme contact sheet (`_theme_review.html`) renders all 13 ranks of all
  8 decks over their own backgrounds — no visible downscale artifacts.

### Still available (optional, not done)

- **WebP/AVIF via `<picture>`**: AVIF is 40 KB vs JPEG 61 KB, so ~35% off the
  remaining 14.8 MB. Needs Pillow (`pip3 install --user pillow`) — `sips` on
  this machine cannot write WebP (`Error 13`).
- **Sprite sheet per deck**: one WebP atlas per deck (13 ranks × 4 suits) plus
  a JSON index — `minion_deck` atlas is **2.15 MB in a single request** vs 52
  files. Cuts request count 52 → 1 per deck.
- **srcset at 1×/2×** so 400 px is served deliberately rather than by
  assumption.
- `bg/` (3.4 MB) and `backs/` (1.1 MB) are fine as-is.

## Notes / risks

- `sips` on this machine cannot write WebP (`Error 13`) — WebP/AVIF encoding
  must go through Pillow (`pip3 install --user pillow`; Pillow here has both
  WebP and AVIF support). Pillow is not currently a declared dependency, so
  the shipped JPEGs use `sips`/Pillow only as a build-time tool with no runtime
  dependency.
- The three pre-existing JPEG decks were exported from *different* source art
  than the five converted decks, so the five converted decks match them in
  resolution but not necessarily in JPEG quantization quality. Matching exactly
  would mean re-encoding the three shipped decks too — optional.
- The history rewrite means **every existing clone must be re-cloned**; the old
  commit hashes are gone.
- A stray broken ref `.git/refs/heads/main 2` (from a Finder copy) was removed;
  it made `git show-ref` and `git rev-list --all` error out.
- The `.mov` screen recording is no longer tracked but still on disk locally.
