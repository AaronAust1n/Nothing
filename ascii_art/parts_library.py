"""
This library stores ASCII art snippets for various creature parts.
Each part is a list of strings, representing lines of ASCII art.
The engine will attempt to combine these parts.

General conventions:
- Try to keep parts somewhat centered if they are meant to be stacked.
- Widths can vary; the engine will handle padding.
- Some parts are designed to be "connectors" or sit adjacent.
"""

HEADS = {
    "default": [ # Fallback
        " /---\\",
        "| o o |",
        " \\---/"
    ],
    "round": [
        "  .--.  ",
        " /    \\ ",
        "| o  o |",
        " \\    / ",
        "  `--'  "
    ],
    "pointy": [
        "   /\\   ",
        "  /  \\  ",
        " |o  o| ",
        " /----\\ ",
        " `----' "
    ],
    "square-ish": [
        ".------.",
        "| o  o |",
        "|      |",
        "'------'"
    ],
    "cloud-like": [
        "  .--~~-.",
        " / o  o  \\",
        "(   ☁    )",
        " `-----' "
    ],
    "flat": [
        " _______ ",
        "| o   o |",
        "--------- " # Note the space for potential asymmetry
    ],
    "egg-shaped": [
        "  .--.  ",
        " /    \\ ",
        "|  o o |",
        " \\    / ",
        "  `--'  "
    ],
    "star-shaped": [ # Very abstract
        "   ☆   ",
        "  / \\  ",
        " |o o| ",
        "  \\ /  ",
        "   v   "
    ]
}

# For dynamic eye placement (a bit more advanced, might simplify for V1 of engine)
HEAD_TEMPLATES_FOR_EYES = {
    "round_base": [ # Template where 'E' can be replaced by eye chars
        "  .--.  ",
        " /EEEE\\ ", # EEEE allows for 1 to 4 eyes or a cluster
        "| E  E |", # Backup if EEEE is too much
        " \\    / ",
        "  `--'  "
    ],
}

BODIES = {
    "default": [
        "|     |",
        "|     |",
        "|_____|"
    ],
    "plump": [
        " /-----\\",
        "(       )",
        "(       )",
        " \\-----/"
    ],
    "serpentine": [
        "  .--.  ",
        " /    \\ ",
        " \\    / ",
        "  \\  /  ",
        "   `'   "
    ],
    "boxy": [
        "+-------+",
        "|       |",
        "|       |",
        "+-------+"
    ],
    "amorphous": [ # A bit of a blob
        "  .--.  ",
        " /    \\ ",
        "(  ☁   )",
        " \\    / ",
        "  `--'  "
    ],
    "flat_wide": [ # Meant for things that might be wide and not tall
        "-------------",
        "_____________"
    ],
    "spindly": [
        "   |   ",
        "  / \\  ",
        " |   | ",
        "  \\ /  ",
        "   |   "
    ],
    "orb-like": [
        "  .--.  ",
        " /    \\ ",
        "(      )",
        " \\    / ",
        "  `--'  "
    ]
}

LEGS_SETS = {
    "default_two": [ # Two legs
        " / \\ ",
        "|   |",
        "'-'-'"
    ],
    "default_four": [ # Four legs
        "/| |\\",
        "||_||",
        "\" \" \""
    ],
    "tiny_tiptoe_feet_two": [
        "  v v  ",
        "  \" \"  "
    ],
    "tiny_tiptoe_feet_many": [
        " v v v v",
        " \" \" \" \""
    ],
    "springy_coils_two": [
        " (~) (~)",
        " /_/ /_/"
    ],
    "springy_coils_many": [ # Added
        "(~)(~)(~)",
        "/_ /_ /_/"
    ],
    "wiggly_tentacles_many": [
        "~^~^~^~",
        "/ / / /"
    ],
    "rolling_orbs_two": [ # Two orbs
        " (O) (O)",
    ],
    "rolling_orbs_many": [
        "(O)(O)(O)"
    ],
    "sturdy_stumps_two": [
        "[___] [___]",
    ],
    "sturdy_stumps_four": [
        "|_| |_|",
        "|_| |_|"
    ],
    "sturdy_stumps_many": [ # Added
        "|_||_||_|",
        "|_||_||_|"
    ],
    "no_legs_slithers_base": [ # For creatures that slither
        "~~~~~~~~~~~",
    ],
    "no_legs_flat_base": [
        "-----------",
    ]
}

WINGS = { # Designed to be attached to the sides of a body
    "default_small_left":  ["<--"],
    "default_small_right": ["-->"],
    "feathery_small_left": ["<~~~"],
    "feathery_small_right": ["~~~>"],
    "feathery_large_left": [
        "  .-- ",
        " /   )",
        "(___/"
    ],
    "feathery_large_right": [
        " --.  ",
        "(   \\ ",
        " \\___)"
    ],
    "leathery_small_left": ["<\\"],
    "leathery_small_right": ["/>"],
    "leathery_large_left": [
        "  /\\ ",
        " /  )",
        "/__/"
    ],
    "leathery_large_right": [
        " /\\  ",
        "(  \\ ",
        "\\__\\"
    ],
    "insect_like_left": ["<))"],
    "insect_like_right": ["(("],
    "made_of_cheese_left": ["<🧀"], # Fun!
    "made_of_cheese_right": ["🧀>"],
}

TAILS = { # Designed to be attached to the rear/bottom of a body
    "default_stubby": [
        " -="
    ],
    "bushy": [
        "  .--~~.",
        " (      )",
        "  `----'"
    ],
    "prehensile": [
        "  /",
        " /",
        "(_)",
    ],
    "spiky": [
        " ---<"
    ],
    "emits_sparks": [
        " --**"
    ],
    "long_whip_like": [
        "  `.",
        "   `.",
        "    `--"
    ],
    "fluffy_pom_pom": [
        "   .--.",
        "  (    )",
        "   `--'"
    ]
}

# Special characters or small elements
EXTRAS = {
    "sparkle": ["✨"],
    "eye_default": "o",
    "eye_large": "O",
    "eye_slit": "-",
    "eye_star": "*",
}

# For aligning parts, height of common configurations
# This is more of a guide for the engine or manual assembly
# Engine might calculate this dynamically
PART_TYPICAL_HEIGHTS = {
    "head": 3, # average
    "body": 4, # average
    "legs": 2  # average
}
