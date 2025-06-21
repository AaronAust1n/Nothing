import random

PREFIXES = [
    "Zibber", "Zobber", "Floof", "Wobble", "Glim", "Snug", "Flutter", "Zizzle",
    "Blob", "Boing", "Chirp", "Doodle", "Fuddle", "Giggle", "Hoot", "Jumble",
    "Klonk", "Lumble", "Mimsy", "Noodle", "Ooble", "Piffle", "Quib", "Rumble",
    "Scribb", "Tootle", "Umble", "Vizzle", "Wom", "Xylo", "Yaffle", "Zumble"
]

SUFFIXES = [
    "noodle", "glee", "beast", "gong", "wing", "fin", "snout", "horn",
    "doodle", "bop", "clump", "drop", "fizz", "flump", "goop", "huff",
    "jig", "kibble", "lump", "munch", "nubble", "plonk", "quatch", "ruff",
    "squeak", "tronk", "uffle", "vroom", "wump", "xorph", "yodel", "zoom"
]

ROOTS = [ # Optional middle parts or standalone names
    "Wisp", "Blob", "Fuzz", "Spark", "Puff", "Critter", "Thingamajig",
    "Snickle", "Frob", "Glumph", "Bramble", "Chortle", "Dingle", "Flit",
    "Grin", "Hoo", "Jape", "Lark", "Mirth", "Nudge", "Pootle", "Quirk",
    "Romp", "Smidgen", "Trill", "Urchin", "Verve", "Whiff", "Yip", "Zest"
]

def generate_name():
    """Generates a whimsical creature name."""
    name_parts = []
    if random.random() < 0.7: # 70% chance of having a prefix
        name_parts.append(random.choice(PREFIXES))

    if random.random() < 0.5 or not name_parts: # 50% chance of a root, or always if no prefix
        name_parts.append(random.choice(ROOTS))

    if random.random() < 0.7 and name_parts: # 70% chance of a suffix, if there's already a part
        name_parts.append(random.choice(SUFFIXES))
    elif not name_parts: # Ensure at least one part if all random checks fail
        name_parts.append(random.choice(ROOTS))

    if len(name_parts) > 1 and random.random() < 0.5:
        return "-".join(name_parts)
    else:
        return "".join(name_parts)

if __name__ == '__main__':
    for _ in range(10):
        print(generate_name())
