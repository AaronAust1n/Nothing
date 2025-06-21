import random

ORIGINS = [
    "was once a teapot until a wizard sneezed on it",
    "hatched from a giant, sparkling jellybean",
    "escaped from a child's unfinished drawing",
    "is the result of a magical laundry mishap",
    "arrived on a misplaced meteor",
    "was wished into existence by a lonely gnome",
    "spontaneously generated in a library's fiction section",
    "used to be a cloud, but got bored",
    "is looking for the ultimate sandwich"
]

ANECDOTES = [
    "believes it's a renowned detective, despite all evidence to the contrary",
    "once accidentally started a tiny, harmless cult",
    "is on a quest to find the world's softest pillow",
    "can often be found attempting to teach pigeons philosophy",
    "secretly dreams of becoming a professional yodeler",
    "is convinced that reflections are its long-lost twin",
    "tries to make friends with garden gnomes, with mixed results",
    "has a surprisingly good singing voice, but only sings when no one is listening"
]

def generate_backstory():
    """Generates a short, whimsical backstory."""
    story_parts = [random.choice(ORIGINS)]
    if random.random() < 0.7: # 70% chance of adding an anecdote
        story_parts.append(random.choice(ANECDOTES))

    return ". ".join(story_parts) + "."

if __name__ == '__main__':
    for _ in range(3):
        print(generate_backstory())
