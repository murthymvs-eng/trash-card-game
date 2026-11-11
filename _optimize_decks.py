#!/usr/bin/env python3
"""Scale the art decks down for web play.

The five high-fidelity decks (avengers, hp, minion, starwars, taylor) are
1500x2100 PNGs, ~6-7 MB each -> ~450 MB of PNGs tracked in git and a 1.7 GB
remote repo. The three later decks (coco, princess, spiderman) already ship
400 px JPEG card faces; this script brings the other five to the same
contract and optionally emits WebP for a <picture> fallback.

Usage:
  python3 _optimize_decks.py --report          # measure only, change nothing
  python3 _optimize_decks.py --jpg              # write <suit>_<rank>.jpg (400px q80)
  python3 _optimize_decks.py --webp             # write <suit>_<rank>.webp (400px q80)
  python3 _optimize_decks.py --atlas out.webp   # one sprite sheet per deck
"""
import os, sys, json, argparse
from multiprocessing import Pool
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
# Decks still on PNG (the ones that need scaling down). The jpg-only decks are
# skipped so their existing assets are never touched.
PNG_DECKS = ['avengers_deck', 'hp_card_deck', 'minion_deck',
             'starwars_deck', 'taylor_swift_tours_deck']
# Cards are drawn at most ~90 CSS px wide (2x DPR => ~180 device px), so 400 px
# is a ~2x headroom margin. Matches the shipped coco/princess/spiderman decks.
DEFAULT_WIDTH = 400
DEFAULT_QUALITY = 80
def card_files(deck):
    """Yield (rank, suit, src_png_path) for a deck, in a stable order."""
    for suit in SUITS:
        for rank in RANKS:
            p = os.path.join(ROOT, deck, f'{suit}_{rank}.png')
            if os.path.exists(p):
                yield rank, suit, p


def _convert_one(job):
    (deck, rank, suit, src, args_w, args_q, do_jpg, do_webp) = job
    out = {'src_bytes': os.path.getsize(src), 'jpg_bytes': 0}
    with Image.open(src) as im:
        im = im.convert('RGB')
        h = round(im.height * args_w / im.width)
        small = im.resize((args_w, h), Image.LANCZOS)
        stem = os.path.join(ROOT, deck, f'{suit}_{rank}')
        if do_jpg:
            dst = f'{stem}.jpg'
            small.save(dst, 'JPEG', quality=args_q, optimize=True, progressive=True)
            out['jpg_bytes'] = os.path.getsize(dst)
        if do_webp:
            small.save(f'{stem}.webp', 'WEBP', quality=args_q, method=6)
    return out


def convert(deck, args):
    jobs = [(deck, rank, suit, src, args.width, args.quality,
             args.jpg, args.webp) for rank, suit, src in card_files(deck)]
    results = [_convert_one(j) for j in jobs] if len(jobs) < 4 else \
        Pool(min(8, len(jobs))).map(_convert_one, jobs)
    out = {'deck': deck, 'files': len(results), 'src_bytes': 0, 'dst_bytes': 0}
    for r in results:
        out['src_bytes'] += r['src_bytes']
        out['dst_bytes'] += r['jpg_bytes']
    return out


def build_atlas(deck, dest, args):
    """One sprite sheet per deck: 13 ranks (cols) x 4 suits (rows)."""
    cols, rows = len(RANKS), len(SUITS)
    cw, ch = args.width, round(args.width * 7 / 5)
    sheet = Image.new('RGB', (cols * cw, rows * ch), (255, 255, 255))
    index = {}
    for ci, rank in enumerate(RANKS):
        for ri, suit in enumerate(SUITS):
            src = os.path.join(ROOT, deck, f'{suit}_{rank}.png')
            if not os.path.exists(src):
                continue
            with Image.open(src) as im:
                sheet.paste(im.convert('RGB').resize((cw, ch), Image.LANCZOS),
                            (ci * cw, ri * ch))
            index[f'{suit}_{rank}'] = {'x': ci * cw, 'y': ri * ch, 'w': cw, 'h': ch}
    sheet.save(dest, 'WEBP', quality=args.quality, method=6)
    with open(dest + '.json', 'w') as f:
        json.dump(index, f, indent=1)
    return dest, os.path.getsize(dest)



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jpg', action='store_true')
    ap.add_argument('--webp', action='store_true')
    ap.add_argument('--atlas', metavar='FILE')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--width', type=int, default=DEFAULT_WIDTH)
    ap.add_argument('--quality', type=int, default=DEFAULT_QUALITY)
    ap.add_argument('--decks', nargs='*', default=PNG_DECKS)
    args = ap.parse_args()
    if not (args.jpg or args.webp or args.atlas or args.report):
        ap.print_help()
        return 0

    total_png = 0
    for deck in args.decks:
        d = os.path.join(ROOT, deck)
        if args.atlas:
            dest = args.atlas
            if not dest.endswith('.webp'):
                dest = os.path.join(ROOT, dest, deck + '.webp')
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            path, size = build_atlas(deck, dest, args)
            print(f'{deck:26} atlas {size/1e6:6.2f} MB -> {path}')
            continue
        if args.report:
            pngs = [f for f in os.listdir(d) if f.endswith('.png')]
            jpgs = [f for f in os.listdir(d) if f.endswith('.jpg')]
            src = sum(os.path.getsize(os.path.join(d, f)) for f in pngs)
            total_png += src
            print(f'{deck:26} {len(pngs)} png {src/1e6:7.1f} MB'
                  + (f'   {len(jpgs)} jpg' if jpgs else ''))
            continue
        r = convert(deck, args)
        avg = r['dst_bytes'] / max(r['files'], 1) / 1024
        print(f"{deck:26} {r['files']} cards  png {r['src_bytes']/1e6:7.1f} MB"
              f" -> jpg {r['dst_bytes']/1e6:6.2f} MB (avg {avg:.0f} KB/card)")
    if args.report:
        print(f'{"TOTAL":26} png {total_png/1e6:.1f} MB')
    return 0


if __name__ == '__main__':
    sys.exit(main())
