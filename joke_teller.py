import random

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the bicycle fall over? Because it was two tired!"
]

def tell_joke():
    """Selects and prints a random joke."""
    joke = random.choice(jokes)
    print_ascii_art()
    print(joke)

def print_ascii_art():
    """Prints a laughing face ASCII art."""
    art = """
    😂 LOL 😂
      \\   /
       \\ /
      -----
     / o o \\
    |   ^   |
     \\  ~  /
      -----
    """
    print(art)

if __name__ == "__main__":
    while True:
        tell_joke()
        user_input = input("Press Enter for another joke, or type 'q' to quit: ")
        if user_input.lower() == 'q':
            break
