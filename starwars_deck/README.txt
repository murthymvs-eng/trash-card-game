STAR WARS DECK — 52 playing cards
====================================================
Generated with local ComfyUI + Qwen-Image 2.1 Turbo.

Dimensions : 1500 x 2100 px each (exact 5:7) = 2.5 x 3.5 in @ 600 DPI
Filenames  : <suit>_<rank>.png  (A,2,3,4,5,6,7,8,9,10,J,Q,K)
Manifest   : manifest.json (card -> house, character, seed)

SUITE -> FACTION MAPPING:
  Hearts   = the Jedi Order (red & gold, lightsaber)
  Spades   = the Sith and the Dark Side (black & purple, double-bladed saber)
  Clubs    = the Rebel Alliance (blue & silver, Rebel starbird)
  Diamonds = the Scoundrels and Gamblers of the Galaxy (gold, bounty hunter)

COURT / ACE CHARACTERS:
  Hearts  A Yoda           | K Obi-Wan Kenobi  | Q Ahsoka Tano  | J Anakin Skywalker
  Spades  A Darth Vader    | K Emperor Palpatine| Q Asajj Ventress | J Count Dooku
  Clubs   A Princess Leia  | K Mon Mothma      | Q Hera Syndulla| J General Rieekan
  Diamonds A Han Solo      | K Boba Fett       | Q Sabine Wren  | J Chewbacca

Number cards (2-10) keep true suit pips in each faction's colors around a
large themed emblem (lightsaber / Sith saber / Rebel starbird / bounty hunter).

Regenerate: python_embeded\python.exe deck_gen.py starwars <start> <end> [--force]
(indices: hearts=0-12, spades=13-25, clubs=26-38, diamonds=39-51)
