import random

HEAD_SHAPES = ["round", "pointy", "square-ish", "cloud-like", "flat", "egg-shaped", "star-shaped"]
NUM_EYES_OPTIONS = [1, 2, 3, 4, 5, "many", "a cluster of"] # "many" can be interpreted in ASCII
MOUTH_STYLES = ["toothy grin", "tiny beak", "pursed lips", "wide gape", "smirk", "no visible mouth"]

BODY_SHAPES = ["plump", "serpentine", "boxy", "amorphous", "flat", "spindly", "orb-like"]
BODY_TEXTURES = ["fluffy", "scaly", "slimy", "glittery", "smooth", "rough", "mossy", "metallic"]

LEG_STYLES = ["tiny tiptoe feet", "springy coils", "wiggly tentacles", "rolling orbs", "sturdy stumps", "no legs (slithers)"]
NUM_LEGS_OPTIONS = [0, 2, 4, 6, 8, "many"] # 0 means no legs

WING_TYPES = ["feathery", "leathery", "insect-like", "made of cheese", "shadowy", "clockwork", "gossamer"]
WING_SPANS = ["tiny", "medium", "wide", "majestic"] # For description

TAIL_FORMS = ["bushy", "prehensile", "spiky", "emits sparks", "stubby", "long and whip-like", "fluffy pom-pom"]

COLORS_PRIMARY = [
    "Sparkling Magenta", "Gloomy Green", "Surprisingly Orange", "Electric Blue",
    "Cosmic Lilac", "Sunshine Yellow", "Midnight Indigo", "Forest Green",
    "Ruby Red", "Sapphire Blue", "Emerald Green", "Amethyst Purple",
    "Obsidian Black", "Pearl White", "Goldenrod", "Turquoise"
]
COLORS_ACCENT = [
    "Silver", "Gold", "Bronze", "Iridescent", "Matte Black", "Neon Pink",
    "Lime Green", "Sky Blue", "Crimson", "Lavender"
]


def generate_body_details():
    """Generates details about the creature's body."""
    details = {}

    details["head_shape"] = random.choice(HEAD_SHAPES)
    details["num_eyes"] = random.choice(NUM_EYES_OPTIONS)
    details["mouth_style"] = random.choice(MOUTH_STYLES)

    details["body_shape"] = random.choice(BODY_SHAPES)
    details["body_texture"] = random.choice(BODY_TEXTURES)

    has_legs = random.choice([True, True, False]) # Higher chance of having legs
    if has_legs:
        details["leg_style"] = random.choice(LEG_STYLES)
        if details["leg_style"] == "no legs (slithers)":
             details["num_legs"] = 0
        else:
            details["num_legs"] = random.choice(NUM_LEGS_OPTIONS)
            if details["num_legs"] == 0 and details["leg_style"] != "no legs (slithers)": # Avoid "sturdy stumps" with 0 legs
                details["leg_style"] = "no legs (slithers)"

    else:
        details["leg_style"] = "no legs (slithers)" # or hovers, floats
        details["num_legs"] = 0

    if random.random() < 0.6: # 60% chance of having wings
        details["wing_type"] = random.choice(WING_TYPES)
        details["wing_span"] = random.choice(WING_SPANS)
    else:
        details["wing_type"] = None
        details["wing_span"] = None

    if random.random() < 0.7: # 70% chance of having a tail
        details["tail_form"] = random.choice(TAIL_FORMS)
    else:
        details["tail_form"] = None

    details["primary_color"] = random.choice(COLORS_PRIMARY)
    details["accent_color1"] = random.choice(COLORS_ACCENT)
    if random.random() < 0.5:
        details["accent_color2"] = random.choice([c for c in COLORS_ACCENT if c != details["accent_color1"]])
    else:
        details["accent_color2"] = None

    return details

if __name__ == '__main__':
    for _ in range(3):
        print(generate_body_details())
