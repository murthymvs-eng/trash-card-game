TOY STORY DECK — 52 playing cards
====================================================
Generated with ComfyUI + Qwen-Image 2.1 Turbo (see _gen_deck.py).

Dimensions : 400 x 560 px each (exact 5:7) -- generated directly at shipping size
Filenames  : <suit>_<rank>.jpg  (A,2,3,4,5,6,7,8,9,10,J,Q,K)
Manifest   : manifest.json (card -> house, character, seed)
Shipped    : 400 px-wide JPEG (~50-70 KB each); a matching 400x560 PNG source
             stays on disk but is gitignored (see DECK_OPTIMIZATION.md).

SUITE -> HOUSE MAPPING (house crest + colours theme each suite):
  Hearts   = Woody and the Round-Up gang (sheriff gold on warm crimson)
  Diamonds = the Pizza Planet crew (lime green on deep space indigo)
  Clubs    = the vintage toys of Al's Toy Barn (mustard gold & denim blue)
  Spades   = the new toys of Bonnie's room (carnival magenta & gold)

COURT / ACE CHARACTERS:
  Hearts   A Woody        | K Buzz Lightyear | Q Jessie     | J Rex
  Diamonds A The Aliens   | K Lotso           | Q Hamm       | J Slinky Dog
  Clubs    A Wheezy       | K Stinky Pete     | Q Mr. Potato Head | J Bullseye
  Spades   A Forky        | K Duke Caboom     | Q Bo Peep    | J Gabby Gabby

v2 prompts: every card is a FLAT FULL-BLEED 2D card face (no environment, no
photograph of a card) and characters follow their canonical movie designs.

Number cards (2-10) reuse the house's lead character, ringed by true suit pips
arranged in the classic pip pattern around the portrait medallion.

Regenerate: python3 _gen_deck.py toystory [--force]
Deck art direction lives in _deck_specs.py.
