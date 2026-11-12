MOANA DECK — 52 playing cards
====================================================
Generated with ComfyUI + Qwen-Image 2.1 Turbo (see _gen_deck.py).

Dimensions : 400 x 560 px each (exact 5:7) -- generated directly at shipping size
Filenames  : <suit>_<rank>.jpg  (A,2,3,4,5,6,7,8,9,10,J,Q,K)
Manifest   : manifest.json (card -> house, character, seed)
Shipped    : 400 px-wide JPEG (~50-70 KB each); a matching 400x560 PNG source
             stays on disk but is gitignored (see DECK_OPTIMIZATION.md).

SUITE -> HOUSE MAPPING (house crest + colours theme each suite):
  Hearts   = Motunui Village and the Chief's family (crimson & gold, canoe crest)
  Diamonds = Maui and the Demigod of the Fishhook (ocean blue & turquoise, fishhook crest)
  Clubs    = Te Fiti and the spirits of the ancestors (emerald & gold, leaf crest)
  Spades   = The monster, the storm and the island of the dead (charcoal & ember, shadow crest)

COURT / ACE CHARACTERS:
  Hearts   A Moana        | K Chief Tui    | Q Sina         | J Gramma Tala
  Diamonds A Maui         | K Maui's brothers| Q Maui's mother| J Hei Hei
  Clubs    A Te Fiti      | K The Ancestors | Q The Ocean    | J Nainoa
  Spades   A Te Ka        | K The Storm    | Q The Dark Island | J Monster's Eye

Number cards (2-10) reuse the house's lead character, ringed by true suit pips
arranged in the classic pip pattern around the portrait medallion.

Regenerate: python3 _gen_deck.py moana [--force]
Deck art direction lives in _deck_specs.py.
