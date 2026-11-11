# Deck Asset Scaling for Web Play

Goal: get the eight art decks to load fast over the web without visible
quality loss, and stop paying for ~1.7 GB of print-resolution PNGs in the repo.

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
