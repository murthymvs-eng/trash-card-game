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
# TOY STORY (1995) — v2 prompts
# --------------------------------------------------------------------------
# v2 rules: the card face IS the whole image (flat, full-bleed, straight-on --
# scene language turns every card into a photo of a card standing in a room),
# and characters are described by their canonical movie designs, never as
# physical toys/figurines/objects.
DECKS["toystory"] = {
    "dir": "toystory_deck",
    "style": ("polished 3D animated feature-film character art, smooth studio-grade "
              "CGI shading, soft even key light, vivid saturated colours, appealing "
              "expressive cartoon faces"),
    "houses": {
        "hearts": {
            "house": "Woody and the Round-Up gang",
            "palette": "sheriff gold on warm crimson",
            "frame": "a flat deep-crimson border band with a thin gold rope inner line and small gold stars printed in the corners",
            "crest": "gold five-point sheriff star badge emblem",
            "bg": "flat warm crimson card-face background with a subtle gold rope-swirl damask pattern, no scenery, no objects",
            "main": ("WOODY",
                     "a cheerful cowboy character with a brown cowboy hat, yellow checked "
                     "shirt, black-and-white cow-hide vest with a gold sheriff star badge, "
                     "blue jeans and a confident friendly smile"),
            "characters": {
                "A": ("WOODY",
                      "a cheerful cowboy character with a brown cowboy hat, yellow checked "
                      "shirt, black-and-white cow-hide vest with a gold sheriff star badge, "
                      "blue jeans and a confident friendly smile"),
                "K": ("BUZZ LIGHTYEAR",
                      "a heroic space-ranger character in a white, lime-green and purple "
                      "spacesuit with a clear dome helmet, green chest control panel and "
                      "neatly folded white wings, strong cleft chin, proud heroic pose"),
                "Q": ("JESSIE",
                      "an energetic cowgirl character with a red yarn ponytail braid tied "
                      "with a yellow bow, white cowgirl hat, crisp white long-sleeve shirt, "
                      "blue jeans under cow-print chaps, big joyful grin"),
                "J": ("REX",
                      "a big friendly green tyrannosaurus dinosaur character with tiny arms, "
                      "large worried amber eyes, rounded snout and a nervous open-mouth smile"),
            },
        },
        "diamonds": {
            "house": "the Pizza Planet crew",
            "palette": "lime green on deep space indigo",
            "frame": "a flat deep-indigo border band with a thin teal inner line and small gold rocket fins printed in the corners",
            "crest": "gold rocket-ship emblem on a round purple disc",
            "bg": "flat deep-indigo card-face background with a subtle tiny gold star pattern, no scenery, no objects",
            "main": ("THE ALIENS",
                     "three little lime-green alien characters standing shoulder to "
                     "shoulder, each with three round black eyes in a row, wearing "
                     "matching deep-blue one-piece suits, mouths open in amazed wonder"),
            "characters": {
                "A": ("THE ALIENS",
                      "three little lime-green alien characters standing shoulder to "
                      "shoulder, each with three round black eyes in a row, wearing "
                      "matching deep-blue one-piece suits, mouths open in amazed wonder"),
                "K": ("LOTSO",
                      "a big fluffy pink teddy-bear character with a paler pink belly, "
                      "heavy brow, grumpy scowl and a small bamboo cane"),
                "Q": ("HAMM",
                      "a pink piggy-bank character with glossy pink glaze, perky little "
                      "ears, a curly tail and a cork stopper, wry knowing smile"),
                "J": ("SLINKY DOG",
                      "a friendly dachshund dog character with a head and tail connected "
                      "by a long coiled metal spring body, floppy tan ears, happy panting "
                      "smile"),
            },
        },
        "clubs": {
            "house": "the vintage toys of Al's Toy Barn",
            "palette": "mustard gold and denim blue",
            "frame": "a flat mustard-gold border band with a stitched denim-blue inner line and small gold rosettes printed in the corners",
            "crest": "gold barn-star rosette emblem inside a rope circle",
            "bg": "flat mustard-gold card-face background with subtle denim-blue swirl damask, no scenery, no objects",
            "main": ("WHEEZY",
                     "a little red rubber penguin character with a bright orange beak, "
                     "red bow tie and rosy cheeks, endearing hopeful smile"),
            "characters": {
                "A": ("WHEEZY",
                      "a little red rubber penguin character with a bright orange beak, "
                      "red bow tie and rosy cheeks, endearing hopeful smile"),
                "K": ("STINKY PETE",
                      "a stern old prospector character with a bushy white beard and "
                      "mustache, wide-brimmed brown mining hat with a head lamp, red "
                      "plaid shirt and brown vest, arms crossed, gruff but kindly look"),
                "Q": ("MR. POTATO HEAD",
                      "a comical brown potato-shaped character with big expressive eyes, "
                      "a black mustache, pink ears, white-gloved hands on hips and a "
                      "sassy smirk"),
                "J": ("BULLSEYE",
                      "a sturdy chestnut-brown horse character with a cream mane and "
                      "tail, dark gentle eyes and a loyal attentive expression"),
            },
        },
        "spades": {
            "house": "the new toys of Bonnie's room",
            "palette": "carnival magenta and sunlit gold",
            "frame": "a flat magenta border band with thin gold-and-cream stripe lines and small gold rosette medallions printed in the corners",
            "crest": "gold sunburst rosette medallion emblem",
            "bg": "flat deep-magenta card-face background with fine gold filigree curls, no scenery, no objects",
            "main": ("FORKY",
                     "a wobbly handmade character made of a white plastic spork with "
                     "mismatched googly eyes, a red wax mouth, red pipe-cleaner arms "
                     "and popsicle-stick feet, arms spread in anxious wonder"),
            "characters": {
                "A": ("FORKY",
                      "a wobbly handmade character made of a white plastic spork with "
                      "mismatched googly eyes, a red wax mouth, red pipe-cleaner arms "
                      "and popsicle-stick feet, arms spread in anxious wonder"),
                "K": ("DUKE CABOOM",
                      "a daring stunt-rider character in a glossy white jumpsuit and "
                      "white crash helmet with a bold black mustache and confident "
                      "grin, seated on a white and red toy motorcycle"),
                "Q": ("BO PEEP",
                      "a graceful porcelain shepherdess character with rosy cheeks, a "
                      "light-blue dress with white lace trim, a pink hooded cape and a "
                      "tall light-blue shepherd's crook staff, gentle brave smile"),
                "J": ("GABBY GABBY",
                      "a vintage 1950s doll character with auburn ringlet curls, big "
                      "green eyes, rosy freckled cheeks and a pale pink dress, wistful "
                      "hopeful smile"),
            },
        },
    },
}


# --------------------------------------------------------------------------
# MARIO (Super Mario Bros. video game)
# --------------------------------------------------------------------------
DECKS["mario"] = {
    "dir": "mario_deck",
    "style": ("classic 16-bit pixel art video game sprite style, crisp hard-edged "
              "pixels, saturated primary colors, bold black outlines, chunky "
              "1990s side-scrolling platformer game artwork"),
    "houses": {
        "hearts": {
            "house": "Mushroom Kingdom",
            "palette": "bright red, white and blue with gold trim",
            "frame": "Red and white mushroom-themed card border with gold rivets",
            "crest": "a red mushroom cap with big white spots",
            "bg": "green warp pipe and checkered flag landscape behind",
            "main": ("MARIO",
                     "a short sturdy cartoon plumber hero with a red cap bearing a "
                     "white circle emblem, bushy black mustache, big round nose, red "
                     "long-sleeve shirt, blue overalls with two yellow buttons, white "
                     "gloves and brown boots, cheerful grin"),
            "characters": {
                "A": ("MARIO",
                      "a short sturdy cartoon plumber hero with a red cap bearing a "
                      "white circle emblem, bushy black mustache, big round nose, red "
                      "long-sleeve shirt, blue overalls with two yellow buttons, "
                      "white gloves and brown boots, cheerful grin"),
                "J": ("TOAD",
                      "a small cheerful mushroom-headed character with a red and "
                      "white spotted cap, enormous white eyes, tiny stubby body"),
                "Q": ("PRINCESS PEACH",
                      "a princess with long golden blonde hair in big curls, a gold "
                      "crown set with blue and red jewels, a flowing pink gown with "
                      "long white gloves, gentle serene smile"),
                "K": ("BOWSER",
                      "a huge muscular cartoon turtle king with a spiked green "
                      "shell, orange scaled skin, small horns on his head, white "
                      "fangs and a fiery mane, roaring furiously"),
            },
        },
        "diamonds": {
            "house": "Luigi's Mansion",
            "palette": "deep green, black and violet with silver trim",
            "frame": "Green and black haunted-mansion card border with silver rivets",
            "crest": "a tall green warp pipe",
            "bg": "dark haunted mansion hallway lit by green ghost flames behind",
            "main": ("LUIGI",
                     "a tall lanky cartoon plumber hero with a dark green cap "
                     "bearing a white circle emblem, thin black mustache, long nose, "
                     "green long-sleeve shirt, blue overalls with two yellow "
                     "buttons, white gloves and brown boots, nervous grin"),
            "characters": {
                "A": ("LUIGI",
                      "a tall lanky cartoon plumber hero with a dark green cap "
                      "bearing a white circle emblem, thin black mustache, long nose, "
                      "green long-sleeve shirt, blue overalls with two yellow "
                      "buttons, white gloves and brown boots, nervous grin"),
                "J": ("TOADETTE",
                      "a small cheerful mushroom-headed character with a pink and "
                      "white spotted cap and a pink bow, enormous white eyes, tiny "
                      "stubby body"),
                "Q": ("ROSALINA",
                      "a tall elegant cosmic princess with long platinum blonde hair "
                      "in a high ponytail, a pale teal gown, a serene expression, "
                      "faint star sparkles around her"),
                "K": ("BOWSER JR.",
                      "a small boss turtle with a spiked green shell, orange skin, "
                      "a spiky orange hair tuft and small fangs, scolding glare"),
            },
        },
        "clubs": {
            "house": "Yoshi's Island",
            "palette": "leaf green, orange and cream with warm gold trim",
            "frame": "Cream and orange rounded card border with gold leaf scrollwork",
            "crest": "a large white egg with green spots",
            "bg": "bright Yoshi's Island jungle with round fruit trees behind",
            "main": ("YOSHI",
                     "a friendly cartoon dinosaur with a rounded snout, big round "
                     "white eyes, green body, white belly, orange saddle-like shoes "
                     "and a cheerful open-mouthed smile"),
            "characters": {
                "A": ("YOSHI",
                      "a friendly cartoon dinosaur with a rounded snout, big round "
                      "white eyes, green body, white belly, orange saddle-like shoes "
                      "and a cheerful open-mouthed smile"),
                "J": ("TOAD",
                      "a small cheerful mushroom-headed character with a red and "
                      "white spotted cap, enormous white eyes, tiny stubby body"),
                "Q": ("LEMUKI",
                      "a chubby cheerful cartoon lemur with a tall tuft of hair on "
                      "its head, orange shirt, big smile and round friendly eyes"),
                "K": ("GOOMBA",
                      "a grumpy brown walking cartoon mushroom enemy with thick "
                      "angry eyebrows, a wide scowl and stubby feet"),
            },
        },
        "spades": {
            "house": "Bowser's Castle",
            "palette": "charcoal grey, crimson red and molten gold",
            "frame": "Dark stone and crimson card border with gold spike studs",
            "crest": "a spiked green turtle shell",
            "bg": "Bowser's Castle lava dungeon with glowing lava below behind",
            "main": ("BOWSER",
                     "a huge muscular cartoon turtle king with a spiked green shell, "
                     "orange scaled skin, small horns on his head, white fangs and a "
                     "fiery mane, roaring furiously"),
            "characters": {
                "A": ("BOWSER",
                      "a huge muscular cartoon turtle king with a spiked green "
                      "shell, orange scaled skin, small horns on his head, white "
                      "fangs and a fiery mane, roaring furiously"),
                "J": ("KOOPA TROOPA",
                      "a tall cartoon turtle enemy with a green shell, yellow skin, "
                      "a scowl and sharp white claws"),
                "Q": ("SHY GUY",
                      "a small shy cartoon ghost with a rounded white body, tiny "
                      "black eyes, a wavy hem and a nervous expression"),
                "K": ("DRY BONES",
                      "a lanky cartoon skeletal turtle with a white skull, dark eye "
                      "sockets, a green shell and bony thin limbs"),
            },
        },
    },
}
