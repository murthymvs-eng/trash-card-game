"""Deck definitions for the generated art decks (Moana + Toy Story).

Each deck maps the four suits to four "houses" (character groups), the way the
Harry Potter deck maps suits to Hogwarts houses. Every house carries:

  house      - the group name recorded in manifest.json
  palette    - dominant colour scheme of that house's cards
  frame      - the card border treatment
  crest      - the emblem that sits above the portrait medallion
  bg         - the scene behind the portrait
  main       - (name, description) of the character shown on the number cards
  characters - {A, J, Q, K} court characters, each (name, description)

Descriptions are written to be self-contained: the image model is given the
character name *and* a visual description so it renders the right face.
"""

DECKS = {}

# --------------------------------------------------------------------------
# MOANA (2016)
# --------------------------------------------------------------------------
DECKS["moana"] = {
    "dir": "moana_deck",
    "style": "stylized 2D animated feature-film style, warm cinematic lighting",
    "houses": {
        "hearts": {
            "house": "Motunui Village and the Chief's family",
            "palette": "crimson and coral red with gold trim, woven tapa-cloth texture",
            "frame": "Crimson tapa-cloth card border with gold woven edging and a red feather motif at each corner",
            "crest": "golden outrigger canoe with a triangular sail",
            "bg": "Motunui tropical shore behind, palm trees and a turquoise lagoon",
            "main": ("MOANA",
                     "a teenage Polynesian girl with long wavy black hair, wearing a "
                     "red top and a cream tapa skirt, holding a wooden oar over her "
                     "shoulder, confident smile"),
            "characters": {
                "A": ("MOANA",
                      "a teenage Polynesian girl with long wavy black hair, wearing a "
                      "red top and a cream tapa skirt, holding a wooden oar over her "
                      "shoulder, confident smile"),
                "K": ("CHIEF TUI",
                      "a large broad-shouldered Polynesian chief with a thick black "
                      "beard, wearing an ornate red and orange feathered cloak, proud "
                      "regal expression"),
                "Q": ("SINA",
                      "a warm Polynesian mother with long dark hair, wearing a coral "
                      "red patterned skirt, gentle loving expression"),
                "J": ("GRAMMA TALA",
                      "an elderly Polynesian grandmother with short grey hair, deeply "
                      "lined kind face, wearing a green and red island shawl, wise "
                      "expression"),
            },
        },
        "diamonds": {
            "house": "Maui and the Demigod of the Fishhook",
            "palette": "deep ocean blue and turquoise with gold trim",
            "frame": "Deep blue lacquer card border with turquoise wave scrollwork and gold shell corners",
            "crest": "giant golden fishhook crossed over a nautilus shell",
            "bg": "Open turquoise ocean behind with a dramatic glowing horizon",
            "main": ("MAUI",
                     "a muscular Polynesian demigod with long curly black hair, wearing "
                     "a red patterned sash, holding a giant golden fishhook, broad "
                     "mischievous grin"),
            "characters": {
                "A": ("MAUI",
                      "a muscular Polynesian demigod with long curly black hair, wearing "
                      "a red patterned sash, holding a giant golden fishhook, broad "
                      "mischievous grin"),
                "K": ("MAUI'S BROTHERS",
                      "a row of six identical muscular Polynesian brothers in "
                      "red patterned sashes with long curly black hair, laughing "
                      "together"),
                "Q": ("MAUI'S MOTHER",
                      "a dignified Polynesian woman in a red tapa dress with long "
                      "black hair, stern disapproving expression"),
                "J": ("HEI HEI",
                      "a comically plump cream and tan rooster with a huge red comb "
                      "and googly eyes, panicked expression"),
            },
        },
        "clubs": {
            "house": "Te Fiti and the spirits of the ancestors",
            "palette": "lush emerald green and gold, leaf-vein filigree",
            "frame": "Emerald green leaf-veined card border with gold fern scrollwork and polished shell corners",
            "crest": "glowing green heart-shaped island leaf of life",
            "bg": "Lush glowing green island grove behind with shafts of sunlight",
            "main": ("TE FITI",
                     "a radiant green goddess of nature with a woman's face, her body "
                     "a swirl of vines, flowers and glowing green light, serene "
                     "expression"),
            "characters": {
                "A": ("TE FITI",
                      "a radiant green goddess of nature with a woman's face, her body "
                      "a swirl of vines, flowers and glowing green light, serene "
                      "expression"),
                "K": ("THE ANCESTORS",
                      "a group of ancestral Polynesian spirit figures in white tapa "
                      "robes with glowing outlines, solemn and watchful"),
                "Q": ("THE OCEAN",
                      "a vast sentient ocean spirit made of swirling deep blue water "
                      "and white foam, vast and watchful"),
                "J": ("NAINOA",
                      "an ancient Polynesian navigator with a weathered tattooed face "
                      "and grey beard, wearing a woven cloak, wise expression"),
            },
        },
        "spades": {
            "house": "The monster, the storm and the island of the dead",
            "palette": "volcanic magenta, deep charcoal and ember orange",
            "frame": "Charcoal card border cracked with glowing ember veins and blackened coral edges",
            "crest": "a snarling black shadow monster silhouette wreathed in flame",
            "bg": "A stormy night sea behind with lightning and swirling dark waves",
            "main": ("TE KA",
                     "a colossal terrifying shadow monster of black smoke and lava "
                     "cracks with burning orange eyes and a roaring fanged mouth"),
            "characters": {
                "A": ("TE KA",
                      "a colossal terrifying shadow monster of black smoke and lava "
                      "cracks with burning orange eyes and a roaring fanged mouth"),
                "K": ("THE STORM",
                      "a roaring black tornado storm cloud with swirling wind bands "
                      "and forked lightning, furious expression"),
                "Q": ("THE DARK ISLAND",
                      "a bleak island of black jagged cliffs swallowed by violet "
                      "shadow and mist, ominous"),
                "J": ("MONSTER'S EYE",
                      "a single huge glowing orange eye burning in the darkness, "
                      "surrounded by cracked lava rock"),
            },
        },
    },
}

# --------------------------------------------------------------------------
# TOY STORY (1995)
# --------------------------------------------------------------------------
DECKS["toystory"] = {
    "dir": "toystory_deck",
    "style": "Pixar-style 3D CGI character portrait, soft global illumination, shallow depth of field",
    "houses": {
        "hearts": {
            "house": "Woody and Andy's Round-Up crew",
            "palette": "bright primary red, yellow and blue with warm wood tones",
            "frame": "Red and gold toy-box card border with painted wood grain, yellow star corners and a stitched felt edge",
            "crest": "a sheriff star badge over a pull-string cowboy",
            "bg": "A sunny child's bedroom behind with wooden shelves and a poster wall",
            "main": ("WOODY",
                     "a vintage pull-string cowboy doll with a yellow plaid shirt, "
                     "cow-print vest, red bandana and brown cowboy hat, friendly "
                     "determined smile"),
            "characters": {
                "A": ("WOODY",
                      "a vintage pull-string cowboy doll with a yellow plaid shirt, "
                      "cow-print vest, red bandana and brown cowboy hat, friendly "
                      "determined smile"),
                "K": ("BUZZ LIGHTYEAR",
                      "a space ranger action figure in a white and green spacesuit "
                      "with a purple visor helmet, translucent wings and a plastic "
                      "jetpack, heroic pose"),
                "Q": ("JESSIE",
                      "a vintage yodeling cowgirl doll with red yarn hair in braids, "
                      "cow-print chaps and a wide-brimmed hat, joyful grin"),
                "J": ("REX",
                      "a small green plastic tyrannosaurus rex toy with tiny arms "
                      "and wide anxious eyes, timid expression"),
            },
        },
        "diamonds": {
            "house": "The Pizza Planet aliens and the Sunnyside crew",
            "palette": "lime green, teal and candy pink",
            "frame": "Purple and teal alien-lounge card border with chrome rocket fins and glowing green porthole corners",
            "crest": "a chrome Pizza Planet rocket ship with a hanging claw",
            "bg": "A toy store shelf behind with pizza boxes and claw machine glow",
            "main": ("THE ALIENS",
                     "a trio of small lime green three-eyed alien toys in matching "
                     "purple space suits, standing shoulder to shoulder, wide-eyed "
                     "and amazed"),
            "characters": {
                "A": ("THE ALIENS",
                      "a trio of small lime green three-eyed alien toys in matching "
                      "purple space suits, standing shoulder to shoulder, wide-eyed "
                      "and amazed"),
                "K": ("LOTSO",
                      "a chubby pink and lavender strawberry-scented teddy bear with "
                      "a smug scowl and stubby plush paws"),
                "Q": ("MR. POTATO HEAD",
                      "a mismatched plastic potato head toy with detachable ears, a "
                      "mustache and a plug-in nose, silly grin"),
                "J": ("SLINKY DOG",
                      "a spring-bodied metal and fabric dachshund toy with a long "
                      "coiled silver spring torso, happy panting expression"),
            },
        },
        "clubs": {
            "house": "Toy Story 2 and the toys of Al's Toy Barn",
            "palette": "dusty mustard, denim blue and aged cardboard tan",
            "frame": "Weathered brown card border with peeling toy-box print, postage-stamp corners and a frayed cloth edge",
            "crest": "a battered child's suitcase stamped with travel stickers",
            "bg": "A dusty antique toy barn shelf behind with old boxes and cobwebs",
            "main": ("WHEEZY",
                     "a squeaky red tin man toy with a bent antenna, chipped white "
                     "paint and a round speaker chest, earnest expression"),
            "characters": {
                "A": ("WHEEZY",
                      "a squeaky red tin man toy with a bent antenna, chipped white "
                      "paint and a round speaker chest, earnest expression"),
                "K": ("STINKY PETE",
                      "a velvety ventriloquist dummy with a cream cloth face, purple "
                      "velvet suit and a broad unsettling smile"),
                "Q": ("AL",
                      "a small one-eyed green alien toy with a metal speaking tube "
                      "mouth, sly mischievous expression"),
                "J": ("THE CHILDCARE ROBOT",
                      "a round white and blue dome robot toy with a headset, a "
                      "friendly screen face and stubby arms"),
            },
        },
        "spades": {
            "house": "Toy Story 4 and the carnival of broken toys",
            "palette": "carnival magenta, sunlit gold and teal canvas stripes",
            "frame": "Carnival tent-striped card border in magenta and gold with wooden post corners and bulb lights",
            "crest": "a wooden carousel horse with a golden pole",
            "bg": "A travelling carnival midway behind with striped tents and strings of bulbs",
            "main": ("FORKY",
                     "a small white plastic spork toy with mismatched googly eyes, a "
                     "pipe-cleaner mustache and a bent tine arm, anxious hopeful "
                     "expression"),
            "characters": {
                "A": ("FORKY",
                      "a small white plastic spork toy with mismatched googly eyes, a "
                      "pipe-cleaner mustache and a bent tine arm, anxious hopeful "
                      "expression"),
                "K": ("BO PEEP",
                      "a porcelain shepherdess figurine in a blue and white floral "
                      "dress holding a gold crook, serene noble expression"),
                "Q": ("DUSTY",
                      "a worn grey cleaning-rag horse toy with a patched cloth body "
                      "and a lumpy stitched face, gentle weary smile"),
                "J": ("GABBY GATTY",
                      "a plush lavender cat toy with a glittery purple floral "
                      "pattern and enormous sparkly blue eyes, delighted expression"),
            },
        },
    },
}
