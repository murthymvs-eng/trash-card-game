#!/usr/bin/env python3
"""Generate one themed art deck (52 card faces) on the ComfyUI Qwen-Image server.

The engine shells out to the comfyui-image-gen skill CLI one image at a time
(one workflow in flight -> no VRAM pressure), then encodes every PNG to the
400 px JPEG contract the game ships (see DECK_OPTIMIZATION.md).

Usage:
  python3 _gen_deck.py moana              # all 52 cards of the moana deck
  python3 _gen_deck.py moana --only hearts_A   # single card (test)
  python3 _gen_deck.py moana --force      # regenerate even if the file exists
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import time

import _pips

ROOT = os.path.dirname(os.path.abspath(__file__))
CLI = os.path.expanduser("~/.cline/skills/comfyui-image-gen/qwen_image.py")
SUITS = ["hearts", "diamonds", "clubs", "spades"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
COURTS = ["A", "J", "Q", "K"]          # cards that carry a name plate
PIP_NAME = {"hearts": "heart", "diamonds": "diamond",
            "clubs": "club", "spades": "spade"}

NEG_CARD = ("blurry, lowres, jpeg artifacts, deformed, extra limbs, extra fingers, "
            "modern photograph, watermark, signature, jumbled letters, garbled text, "
            "duplicate, tilted, skewed perspective, cropped, muddy, cluttered, oversaturated")

# Cards are generated DIRECTLY at the shipping size. The board never shows a
# card wider than ~90 CSS px (~180 device px on a 2x phone), every deck ships
# 400x560 JPEG, and both 400 and 560 divide by the Qwen VAE's 16-px patch, so
# the VAE decodes exactly 400x560 -- no print-resolution pass, no downscale,
# ~14x fewer latent pixels per render.
WIDTH, HEIGHT = 400, 560


def load_spec(name):
    mod = importlib.import_module("_deck_specs")
    if name not in mod.DECKS:
        sys.exit("unknown deck %r (have: %s)" % (name, ", ".join(mod.DECKS)))
    return mod.DECKS[name]


def card_prompt(deck, suit, rank, house):
    """Build the prompt for one card face."""
    style = deck.get("style", "")
    if rank in COURTS:
        name, desc = house["characters"][rank]
        subject = ("Centered waist-up portrait of %s (%s) inside an oval gold "
                   "filigree medallion. A small gold name plate banner at the "
                   "bottom reads \"%s\"." % (name, desc, name))
        plate = ""
    else:
        # Number cards reuse the house's lead character. The model cannot count
        # pips, so it is told to leave the field clear and _pips.py overlays
        # mathematically correct pips afterwards.
        name, desc = house["main"]
        subject = ("Centered waist-up portrait of %s (%s) inside an oval gold "
                   "filigree medallion. The flat area of the card around the "
                   "medallion is plain ornate empty card face."
                   % (name, desc))
        plate = (" No suit pips, no hearts, no spades, no clubs, no diamonds "
                 "anywhere on the card, no name plate, no banner, no lettering "
                 "other than the rank numeral and small suit symbol in the "
                 "upper-left corner.")
    return ("Ornate collectible playing card face, the %s of %s. %s "
            "A %s crest emblem above the medallion, the rank numeral and the %s "
            "suit symbol printed in the upper-left corner. %s %s "
            "%s Hand-painted illustration, high detail, elegant, vertical 5:7 "
            "composition." % (rank, PIP_NAME[suit], subject, house["crest"],
                              PIP_NAME[suit], house["frame"], house["bg"] + plate,
                              style))


def generate(prompt, negative, seed, outdir, prefix, attempts=3):
    """Generate one image, retrying on transient network/timeout failures.

    The ComfyUI box occasionally drops the socket while streaming a 7 MB PNG
    back to the Mac; the work is simply re-submitted on the next attempt.
    """
    last = ""
    for attempt in range(1, attempts + 1):
        cmd = [sys.executable, CLI, prompt,
               "--negative-prompt", negative,
               "--width", str(WIDTH), "--height", str(HEIGHT),
               "--seed", str(seed), "-o", outdir, "--prefix", prefix, "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        for line in reversed(proc.stdout.strip().splitlines()):
            if line.startswith("{"):
                return json.loads(line)["files"][0]
        last = proc.stdout[-600:] + proc.stderr[-600:]
        print("[retry %d/%d] %s" % (attempt, attempts, last.strip()[-200:]),
              flush=True)
        time.sleep(5)
    raise RuntimeError("generation failed after %d attempts:\n%s"
                       % (attempts, last))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--only", help="one card, e.g. hearts_A")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--seed-base", type=int, default=770000)
    args = ap.parse_args()

    spec = load_spec(args.deck)
    outdir = os.path.join(ROOT, spec["dir"])
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, "_raw")
    os.makedirs(tmp, exist_ok=True)

    manifest_path = os.path.join(outdir, "manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path))

    index = 0
    for suit in SUITS:
        house = spec["houses"][suit]
        for rank in RANKS:
            index += 1
            key = "%s_%s" % (suit, rank)
            if args.only and key != args.only:
                continue
            jpg = os.path.join(outdir, key + ".jpg")
            png = os.path.join(outdir, key + ".png")
            if os.path.exists(jpg) and not args.force:
                print("[skip] %s" % key)
                continue
            seed = args.seed_base + index
            print("[gen ] %s  seed=%d" % (key, seed), flush=True)
            prompt = card_prompt(spec, suit, rank, house)
            raw = generate(prompt, NEG_CARD, seed, tmp, "%s_%s" % (spec["dir"], key))
            # The model cannot count pips, so exact pips are composited here.
            _pips.draw_pips(raw, suit, rank)
            normalize_png(raw)
            to_jpeg(raw, jpg)
            if os.path.exists(png):
                os.remove(png)
            os.replace(raw, png)
            manifest[key + ".jpg"] = {
                "suit": suit, "rank": rank, "house": house["house"],
                "character": house["characters"][rank][0] if rank in COURTS else None,
                "seed": seed,
            }
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=1, sort_keys=True)
    print("[done] %s -> %s" % (spec["dir"], outdir))


def to_jpeg(src, dst):
    """Normalize to the repo's exact delivery contract: 400x560 (5:7) JPEG.

    The latent is requested at exactly 400x560, so the decode normally already
    matches and these guards are no-ops; they only exist in case the server
    ever snaps the size (other decks ship exactly 400x560, and the board draws
    every slot with `aspect-ratio:5/7` + `object-fit:cover`, so a mismatched
    source gets its edges shaved).
    """
    from PIL import Image
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        target = 5 / 7
        if abs(w / h - target) > 1e-4:
            if w / h > target:          # too wide -> trim the sides
                nw = int(round(h * target))
                left = (w - nw) // 2
                im = im.crop((left, 0, left + nw, h))
            else:                       # too tall -> trim top/bottom
                nh = int(round(w / target))
                top = (h - nh) // 2
                im = im.crop((0, top, w, top + nh))
        im = im.resize((400, 560), Image.LANCZOS)
        im.save(dst, "JPEG", quality=80, optimize=True, progressive=True)


def normalize_png(src):
    """Snap a generated PNG to exactly 400x560 (the on-disk source size)."""
    from PIL import Image
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        target = 5 / 7
        if abs(w / h - target) > 1e-4:
            if w / h > target:
                nw = int(round(h * target))
                left = (w - nw) // 2
                im = im.crop((left, 0, left + nw, h))
            else:
                nh = int(round(w / target))
                top = (h - nh) // 2
                im = im.crop((0, top, w, top + nh))
        if im.size != (400, 560):
            im = im.resize((400, 560), Image.LANCZOS)
            im.save(src, "PNG")
    return src


if __name__ == "__main__":
    sys.exit(main())
