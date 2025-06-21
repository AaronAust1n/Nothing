# world.py - Defines the game world, rooms, items, and characters

# Basic data structures (will be expanded)

# Room:
#   name: str
#   description: str
#   exits: dict (e.g., {"north": "room_id_2"})
#   items: list of item objects
#   characters: list of character objects

# Item:
#   name: str
#   description: str
#   properties: dict (e.g., {"can_take": True, "is_weapon": False})

# Character:
#   name: str
#   description: str
#   dialogue: str or function to generate dialogue

# Example room structure
rooms = {
    "start_room": {
        "name": "The Compiler's Cradle",
        "description": "You are in a brightly lit room, humming with the gentle whir of unseen processes. Code snippets flicker on the walls like digital hieroglyphs. This is where new adventures are compiled. A narrow passage leads north.",
        "exits": {"north": "glitchy_grove_entry"},
        "items": ["debug_leaflet"], # Item IDs
        "characters": ["guidance_gnome"] # Character IDs
    },
    "glitchy_grove_entry": {
        "name": "Entrance to the Glitchy Grove",
        "description": "The air shimmers strangely here. Twisted trees made of tangled cables rise around you. Their leaves are flickering bits of deprecated code. A path leads south back to the Cradle, and another deeper into the grove to the east.",
        "exits": {"south": "start_room", "east": "murmuring_node"},
        "items": [],
        "characters": []
    },
    "murmuring_node": {
        "name": "Murmuring Node",
        "description": "Sunlight dapples through the canopy of a colossal, ancient `for` loop. Strange, melodic beeps emanate from a central node covered in glowing moss. Paths lead west and north.",
        "exits": {"west": "glitchy_grove_entry", "north": "syntax_swamp_edge"},
        "items": ["syntax_sugar_cube"],
        "characters": []
    },
     "syntax_swamp_edge": {
        "name": "Edge of the Syntax Swamp",
        "description": "The ground becomes marshy and unstable here, with pools of bubbling, undefined variables. The air is thick with the croaking of boolean frogs. A narrow, rickety bridge of semicolons leads east. The path back south is clearer.",
        "exits": {"south": "murmuring_node", "east": "rickety_bridge"}, # "east" will be the puzzle
        "items": [],
        "characters": ["bug_mascot"]
    },
    "rickety_bridge": {
        "name": "Rickety Semicolon Bridge",
        "description": "You are on a shaky bridge made of oversized semicolons, spanning a chasm of infinite loops. It doesn't look very safe. You could try to cross east or go back west.",
        "exits": {"west": "syntax_swamp_edge", "east": "library_of_babel"}, # Crossing might have a condition later
        "items": [],
        "characters": []
    },
    "library_of_babel": {
        "name": "The Library of Babel (Compact Edition)",
        "description": "Rows upon rows of servers hum quietly, each containing every possible combination of code. Most of it is nonsense, but somewhere in here is the answer to everything... and a way back west.",
        "exits": {"west": "rickety_bridge"},
        "items": ["lost_docstring"],
        "characters": []
    }
}

# Item database
items_db = {
    "debug_leaflet": {
        "name": "Debug Leaflet",
        "description": "A small, shimmering leaflet. It reads: 'When lost in execution, observe your surroundings. Variables may hold the key.'",
        "properties": {"can_take": True, "readable": True}
    },
    "syntax_sugar_cube": {
        "name": "Syntax Sugar Cube",
        "description": "A sparkling cube that smells faintly of vanilla and abstraction. It looks delicious but might have side effects.",
        "properties": {"can_take": True, "edible": True} # "edible" is a custom property
    },
    "lost_docstring": {
        "name": "Lost Docstring Scroll",
        "description": "A dusty scroll containing a fragment of a forgotten function's documentation. It seems important.",
        "properties": {"can_take": True, "readable": True}
    },
    "pointer_pearl": {
        "name": "Pointer Pearl",
        "description": "A beautiful, iridescent pearl that seems to point towards whatever you desire most... or the nearest null pointer exception.",
        "properties": {"can_take": True}
    }
}

# Character database
characters_db = {
    "guidance_gnome": {
        "name": "Guidance Gnome",
        "description": "A tiny gnome wearing spectacles made of magnifying glasses, constantly muttering about 'best practices'.",
        "dialogue": [
            "Welcome, adventurer! To begin your journey, try typing 'look' or 'help'.",
            "Remember, well-structured code is happy code!",
            "Don't forget to check your inventory using 'i' or 'inventory'."
        ],
        "dialogue_index": 0 # To cycle through dialogue
    },
    "bug_mascot": {
        "name": "Buggy the Code Grub",
        "description": "A surprisingly cute, six-legged grub with large, expressive compound eyes. It chirps and clicks, pointing a tiny antenna towards the Syntax Swamp.",
        "dialogue": [
            "Chirp! Click-whirr... (It seems to be indicating that the bridge ahead is tricky.)",
            "Buzzz... (It nudges a loose semicolon on the ground, then looks at you expectantly.)"
        ],
        "dialogue_index": 0
    }
}


def get_room_data(room_id):
    """Returns the data for a given room ID."""
    return rooms.get(room_id)

def get_item_data(item_id):
    """Returns the data for a given item ID."""
    return items_db.get(item_id)

def get_character_data(char_id):
    """Returns the data for a given character ID."""
    return characters_db.get(char_id)
