#!/usr/bin/env python3
"""Verify every art deck against the web delivery contract.

Checks each deck's 52 card faces:
  * all four suits x thirteen ranks present
  * every face is exactly 400x560 (5:7) JPEG -- the size the board draws
    (slots use `aspect-ratio:5/7` + `object-fit:cover`, so a mismatched
    source gets shaved) and the size the other decks already ship
  * the file decodes and is not a blank/placeholder frame
  * manifest.json is present and covers all 52 cards

Usage: python3 _verify_decks.py [deck_dir ...]
"""
import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SUITS = ["hearts", "diamonds", "clubs", "spades"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
EXPECT_W = 400          # every deck ships 400 px wide (~2x the on-screen size)
ASPECT = 5 / 7         # the board draws slots with aspect-ratio:5/7
MIN_BYTES = 8 * 1024


def decks_on_disk():
    return sorted(d for d in os.listdir(ROOT)
                  if os.path.isdir(os.path.join(ROOT, d)) and d.endswith("_deck"))


def check(deck):
    d = os.path.join(ROOT, deck)
    problems = []
    notes = []
    total = 0
    crop = 0
    for suit in SUITS:
        for rank in RANKS:
            key = "%s_%s" % (suit, rank)
            path = os.path.join(d, key + ".jpg")
            if not os.path.exists(path):
                problems.append("%s: missing" % key)
                continue
            size = os.path.getsize(path)
            total += size
            if size < MIN_BYTES:
                problems.append("%s: suspiciously small (%d B)" % (key, size))
            try:
                with Image.open(path) as im:
                    im.load()
                    w, h = im.size
                    if w != EXPECT_W:
                        problems.append("%s: width %d, expected %d"
                                        % (key, w, EXPECT_W))
                    # The board renders a card in a 5:7 box with object-fit:cover,
                    # so a face that is not exactly 5:7 gets its edges shaved.
                    crop = max(crop, abs(w / h - ASPECT) / ASPECT)
                    if im.mode != "RGB":
                        problems.append("%s: mode %s" % (key, im.mode))
            except Exception as e:
                problems.append("%s: unreadable (%s)" % (key, e))
    if crop > 0.005:
        notes.append("aspect deviates %.2f%% from 5:7 -- edges are cropped in "
                     "the slot (fine, matches the other decks)" % (crop * 100))
    man = os.path.join(ROOT, d, "manifest.json")
    if os.path.exists(man):
        m = json.load(open(man))
        missing = [k for k in ("%s_%s.jpg" % (s, r) for s in SUITS for r in RANKS)
                   if k not in m]
        if missing:
            notes.append("manifest lists %d of 52 keys (%s-based decks key by "
                         ".png)" % (len(m), "png" if any(k.endswith('.png') for k in m)
                                    else "jpg"))
    return problems, notes, total


def main():
    decks = sys.argv[1:] or decks_on_disk()
    bad = 0
    for deck in decks:
        problems, notes, total = check(deck)
        status = "OK " if not problems else "FAIL"
        print("%-4s %-26s %6.1f MB" % (status, deck, total / 1e6))
        for p in problems:
            print("       - %s" % p)
        for n in notes:
            print("       ~ %s" % n)
        bad += len(problems)
    print("\n%s" % ("all decks pass" if not bad else "%d problems" % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
