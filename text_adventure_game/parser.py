# parser.py - Handles parsing of player input

def normalize_input(player_input_str: str) -> list[str]:
    """
    Normalizes player input.
    - Converts to lowercase.
    - Splits into words.
    - Removes common "noise" words (articles, prepositions) that don't affect meaning.
    """
    if not player_input_str:
        return []

    words = player_input_str.lower().split()
    # Define a list of common noise words to ignore.
    # This list can be expanded as needed.
    noise_words = [
        "a", "an", "the", "to", "at", "in", "on", "of", "for", "with",
        "go", "move", "travel", "walk", "proceed", "head",
        "get", "take", "grab", "pick", "up",
        "drop", "leave",
        "look", "examine", "inspect", "see", "view",
        "talk", "speak", "ask", "tell",
        "my", "me"
    ]

    # Filter out noise words, but keep essential verbs if they are not followed by a direction/object
    # For example, "go" by itself might be valid, or "look" by itself.
    # This simple filter might need refinement.

    # A more robust approach would be to identify verb, noun, preposition etc.
    # For now, a simpler filter:
    cleaned_words = [word for word in words if word not in noise_words or word in ["go", "look", "talk"]] # Keep some core verbs

    # If cleaned_words is empty but original words had content, it might be a command like "go" or "look"
    if not cleaned_words and words:
        # Try to retain the first word if it's a primary command verb
        potential_verb = words[0]
        if potential_verb in ["go", "look", "inventory", "quit", "help", "i", "l", "q", "h", "take", "drop", "talk"]:
             return [potential_verb] + [w for w in words[1:] if w not in noise_words]


    # This is still very basic. A real parser would use more sophisticated techniques
    # like identifying parts of speech (verb, noun, adjective) and sentence structure.
    # For now, we'll keep it simple.

    # If the first word is a known verb, keep it and then filter the rest
    if words:
        verb = words[0]
        # Common verbs that might be followed by arguments
        if verb in ["go", "take", "drop", "look", "examine", "talk", "use", "open", "read"]:
            # Reconstruct a simplified command: verb + (significant part of the rest)
            significant_others = [w for w in words[1:] if w not in ["to", "at", "the", "a", "an", "my"]]
            return [verb] + significant_others

    # Fallback to just splitting and lowercasing if the above logic doesn't simplify well
    return player_input_str.lower().split()


def parse_command(player_input_str: str) -> tuple[str | None, str | None]:
    """
    Parses the player's input string into a command and an argument.
    Returns a tuple (command, argument).
    E.g., "go north" -> ("go", "north")
          "take sword" -> ("take", "sword")
          "look" -> ("look", None)
          "quit" -> ("quit", None)
    """
    words = normalize_input(player_input_str) # Use the more advanced normalize_input

    if not words:
        return None, None

    command = words[0]
    argument = None

    # Mapping synonyms or shorthand to a canonical command
    if command in ["n", "north"]:
        return "go", "north"
    if command in ["s", "south"]:
        return "go", "south"
    if command in ["e", "east"]:
        return "go", "east"
    if command in ["w", "west"]:
        return "go", "west"
    if command in ["u", "up"]:
        return "go", "up"
    if command in ["d", "down"]:
        return "go", "down"

    if command in ["l", "look", "examine", "inspect"]:
        # "look at <something>" vs "look"
        if len(words) > 1 and words[1] == "at" and len(words) > 2: # "look at X"
            return "look_at", " ".join(words[2:])
        elif len(words) > 1: # "look X"
            return "look_at", " ".join(words[1:])
        return "look", None # Just "look"

    if command in ["i", "inv", "inventory"]:
        return "inventory", None

    if command in ["q", "quit", "exit"]:
        return "quit", None

    if command in ["get", "take", "grab", "pickup"]:
        command = "take" # Canonical verb
        if len(words) > 1:
            argument = " ".join(words[1:])
        else:
            return "take", None # "take" without argument, prompt for what to take

    if command in ["drop", "leave"]:
        command = "drop" # Canonical verb
        if len(words) > 1:
            argument = " ".join(words[1:])
        else:
            return "drop", None # "drop" without argument

    if command in ["talk", "speak", "ask"]:
        command = "talk"
        if len(words) > 1 and words[1] == "to" and len(words) > 2: # "talk to X"
             argument = " ".join(words[2:])
        elif len(words) > 1: # "talk X"
             argument = " ".join(words[1:])
        else:
            return "talk", None # "talk" without argument

    # If we haven't matched a multi-word command structure above,
    # and there are multiple words, assume it's command + argument.
    if len(words) > 1 and argument is None: # Ensure argument wasn't set by specific logic above
        argument = " ".join(words[1:])

    return command, argument

if __name__ == '__main__':
    # Test cases for the parser
    test_inputs = [
        "go north", "n",
        "take the shiny key", "get key",
        "look", "l",
        "look at the old chest", "examine chest",
        "drop sword",
        "inventory", "i",
        "quit", "q",
        "talk to the old man", "ask gnome",
        "use potion on self",
        "north" # should be "go north"
    ]
    print("Testing parser.py...")
    for test_input in test_inputs:
        cmd, arg = parse_command(test_input)
        print(f"Input: '{test_input}' -> Command: '{cmd}', Argument: '{arg}'")

    print("\nTesting normalize_input...")
    test_normalize = [
        "take the red potion",
        "go to the north",
        "look",
        "use the key on the door",
        "talk to guard"
    ]
    for test_input in test_normalize:
        norm = normalize_input(test_input)
        print(f"Input: '{test_input}' -> Normalized: '{norm}'")
