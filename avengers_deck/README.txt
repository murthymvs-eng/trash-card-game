MARVEL AVENGERS DECK — 52 playing cards
====================================================
Generated with local ComfyUI + Qwen-Image 2.1 Turbo.

Dimensions : 1500 x 2100 px each (exact 5:7) = 2.5 x 3.5 in @ 600 DPI
Filenames  : <suit>_<rank>.png  (A,2,3,4,5,6,7,8,9,10,J,Q,K)
Manifest   : manifest.json (card -> house, character, seed)

SUITE -> THEME MAPPING:
  Hearts   = Captain America & the Classic Avengers (red & gold, star shield)
  Spades   = Thanos & the Dark Nemesis (black & silver, Infinity Gauntlet)
  Clubs    = the Guardians of the Galaxy (cosmic blue & silver, the Galaxy ship)
  Diamonds = the Mystic Sorcerers (emerald & gold, Eye of Agamotto)

COURT / ACE CHARACTERS:
  Hearts  A Captain America | K Iron Man   | Q Black Widow  | J Hawkeye
  Spades  A Thanos          | K Loki       | Q Hela         | J Ultron
  Clubs   A Star-Lord       | K Groot      | Q Gamora       | J Rocket Raccoon
  Diamonds A Doctor Strange | K Wong       | Q Scarlet Witch| J Vision

Number cards (2-10) keep true suit pips in each theme's colors around a
large themed emblem (star shield / Infinity Gauntlet / Galaxy / mystic eye).

Regenerate: python_embeded\python.exe deck_gen.py avengers <start> <end> [--force]
(indices: hearts=0-12, spades=13-25, clubs=26-38, diamonds=39-51)
