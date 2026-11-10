HARRY POTTER — THE HOUSE DECK (52 playing cards)
====================================================
HP HOUSE DECK — 52 playing cards
Generated with local ComfyUI + Qwen-Image 2.1 Turbo.

Dimensions : 1500 x 2100 px each (exact 5:7 ratio)
             = 2.5 x 3.5 inches @ 600 DPI (standard poker-card size,
             print-ready)
Filenames  : <suit>_<rank>.png  (A,2,3,4,5,6,7,8,9,10,J,Q,K)
Manifest   : manifest.json (card -> house, character, seed)

SUITE -> HOUSE MAPPING (house crest + colors theme each suite):
  Hearts   = Gryffindor  (crimson & gold, lion crest)
  Spades   = Slytherin   (dark green & silver, serpent crest)
  Clubs    = Ravenclaw   (bronze & blue, eagle crest)
  Diamonds = Hufflepuff  (yellow & black, badger crest)

COURT / ACE CHARACTERS (house founders as Aces):
  Hearts  A Godric Gryffindor | K Albus Dumbledore | Q Minerva McGonagall | J Harry Potter
  Spades  A Salazar Slytherin | K Lord Voldemort   | Q Bellatrix Lestrange| J Draco Malfoy
  Clubs   A Rowena Ravenclaw  | K Gilderoy Lockhart| Q Cho Chang          | J Luna Lovegood
  Diamonds A Helga Hufflepuff | K Cedric Diggory   | Q Nymphadora Tonks   | J Newt Scamander

Number cards (2-10) keep the true suit pips (heart/spade/club/diamond)
arranged in classic pip pattern around a large house emblem, so the
deck plays as a normal 52-card deck.

Regenerate a card:  C:\Users\rogi73090\ComfyUI_windows_portable\python_embeded\python.exe C:\Users\rogi73090\ComfyUI_windows_portable\hp_deck_gen.py <start> <end> --force
(indices: hearts=0-12, spades=13-25, clubs=26-38, diamonds=39-51;
rank order A,2,3,4,5,6,7,8,9,10,J,Q,K)
Note: the generator produces 1504x2096 (VAE alignment); resize_deck.py
normalizes every card to exactly 1500x2100.
