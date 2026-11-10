MINIONS DECK — 52 playing cards
====================================================
Generated with local ComfyUI + Qwen-Image 2.1 Turbo.

Dimensions : 1500 x 2100 px each (exact 5:7) = 2.5 x 3.5 in @ 600 DPI
Filenames  : <suit>_<rank>.png  (A,2,3,4,5,6,7,8,9,10,J,Q,K)
Manifest   : manifest.json (card -> house, character, seed)

SUITE -> MINION MAPPING (classic Minion faces are the pips):
  Hearts   = BOB     (crimson red & yellow, the group leader)
  Spades   = STUART  (dark green & yellow, the spiky-haired rebel)
  Clubs    = KARL    (royal blue & yellow, the muscle)
  Diamonds = SPEEDY  (golden yellow & red, the fastest)

COURT / ACE CHARACTERS:
  Hearts  A Bob            | K Gru            | Q Lucy Wilde      | J Margo
  Spades  A Stuart         | K El Macho Stuart| Q Scarlet Overkill| J Vector
  Clubs   A Karl           | K Balthrak       | Q Velma           | J Dr. Nefario
  Diamonds A Speedy        | K Minion King    | Q Edith           | J Agnes

Number cards (2-10) show a big portrait of the suite Minion with classic
Minion-face pips in a traditional pip pattern.

Regenerate: python_embeded\python.exe deck_gen.py minions <start> <end> [--force]
(indices: hearts=0-12, spades=13-25, clubs=26-38, diamonds=39-51)
