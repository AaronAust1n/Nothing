import random

PRIMARY_ABILITIES = [
    "can burp rainbows", "tells excellent jokes (incomprehensibly)", "changes color based on mood",
    "can only be seen by people named Kevin", "levitates slightly when happy",
    "attracts small, shiny objects", "can talk to squirrels, but only about nuts",
    "leaves a trail of glitter", "sweats lemonade", "can predict the weather, but is always wrong",
    "glows faintly in the dark", "can mimic any sound, but always too loudly",
    "eats shadows for sustenance", "can turn invisible, but only its left foot",
    "understands advanced calculus but can't tie its shoes (if it had any)"
]

QUIRKY_HABITS = [
    "collects lost socks and builds nests from them", "hums off-key opera at dawn",
    "sleeps upside down in chandeliers", "communicates exclusively through interpretive dance on Tuesdays",
    "tries to pay for things with buttons", "arranges pebbles into complex geometric patterns",
    "chases its own tail (even if it doesn't have one)", "gives surprisingly good financial advice",
    "apologizes to inanimate objects when it bumps into them", "writes tiny poems on leaves",
    "attempts to fly using only sheer willpower", "hides valuable items in other people's pockets"
]

PERSONALITY_TRAITS = [
    "perpetually confused", "overly enthusiastic", "grumpy before its morning dew",
    "surprisingly wise", "a natural leader (of other, smaller imaginary things)",
    "extremely shy, blushes easily", "a hopeless romantic", "fiercely loyal to its favorite rock",
    "easily distracted by butterflies", "thinks it's a renowned detective", "a bit of a prankster",
    "always optimistic, even when stuck in a jar"
]

def generate_characteristics():
    """Generates characteristics for the creature."""
    return {
        "primary_ability": random.choice(PRIMARY_ABILITIES),
        "quirky_habit": random.choice(QUIRKY_HABITS),
        "personality_trait": random.choice(PERSONALITY_TRAITS)
    }

if __name__ == '__main__':
    for _ in range(3):
        print(generate_characteristics())
