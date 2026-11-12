TOY STORY DECK — 52 playing cards
====================================================
Generated with ComfyUI + Qwen-Image 2.1 Turbo (see _gen_deck.py).

Dimensions : 400 x 560 px each (exact 5:7) -- generated directly at shipping size
Filenames  : <suit>_<rank>.jpg  (A,2,3,4,5,6,7,8,9,10,J,Q,K)
Manifest   : manifest.json (card -> house, character, seed)
Shipped    : 400 px-wide JPEG (~50-70 KB each); a matching 400x560 PNG source
             stays on disk but is gitignored (see DECK_OPTIMIZATION.md).

SUITE -> HOUSE MAPPING (house crest + colours theme each suite):
  Hearts   = Woody and Andy's Round-Up crew (primary red/yellow/blue, sheriff star crest)
  Diamonds = The Pizza Planet aliens and the Sunnyside crew (lime & teal, rocket crest)
  Clubs    = Toy Story 2 and the toys of Al's Toy Barn (mustard & denim, suitcase crest)
  Spades   = Toy Story 4 and the carnival of broken toys (carnival magenta & gold, carousel crest)

COURT / ACE CHARACTERS:
  Hearts   A Woody        | K Buzz Lightyear | Q Jessie     | J Rex
  Diamonds A The Aliens   | K Lotso           | Q Mr. Potato Head | J Slinky Dog
  Clubs    A Wheezy       | K Stinky Pete     | Q Al         | J The Childcare Robot
  Spades   A Forky        | K Bo Peep         | Q Dusty      | J Gabby Gabby

Number cards (2-10) reuse the house's lead character, ringed by true suit pips
arranged in the classic pip pattern around the portrait medallion.

Regenerate: python3 _gen_deck.py toystory [--force]
Deck art direction lives in _deck_specs.py.
