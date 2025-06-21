# Core misinterpretation engine for the Universal Miscommunication Device
import random
import re

# A small dictionary of homophones and similar sounding words
HOMOPHONE_MAP = {
    "their": ["there", "they're"],
    "there": ["their", "they're"],
    "they're": ["their", "there"],
    "to": ["too", "two"],
    "too": ["to", "two"],
    "two": ["to", "too"],
    "your": ["you're"],
    "you're": ["your"],
    "presents": ["presence"],
    "presence": ["presents"],
    "here": ["hear"],
    "hear": ["here"],
    "see": ["sea"],
    "sea": ["see"],
    "sun": ["son"],
    "son": ["sun"],
    "ate": ["eight"],
    "eight": ["ate"],
    "buy": ["by", "bye"],
    "by": ["buy", "bye"],
    "bye": ["buy", "by"],
    "know": ["no"],
    "no": ["know"],
    "knight": ["night"],
    "night": ["knight"],
    "write": ["right", "rite"],
    "right": ["write", "rite"],
    "rite": ["write", "right"],
    "is": ["fizz", "his"], # Added for more fun
    "a": ["hay", "eh"],
    "world": ["whirled", "word"],
    "hello": ["jello", "hallow"],
}

def lexical_substituter(text: str) -> str:
    """
    Replaces words in the text with their homophones or similar words.
    """
    words = re.findall(r"[\w']+|[.,!?;]", text.lower()) # Keep punctuation
    substituted_words = []
    for word in words:
        # Attempt to substitute with a certain probability to make it less predictable
        if word in HOMOPHONE_MAP and random.random() < 0.7: # 70% chance of substitution if word is in map
            substituted_words.append(random.choice(HOMOPHONE_MAP[word]))
        else:
            substituted_words.append(word)

    # Basic re-capitalization for 'i' and start of sentence
    if substituted_words:
        substituted_words[0] = substituted_words[0].capitalize()
        for i in range(len(substituted_words)):
            if substituted_words[i] == "i":
                substituted_words[i] = "I"
            # Capitalize after sentence-ending punctuation
            if i > 0 and substituted_words[i-1] in ['.','!','?'] and i < len(substituted_words):
                 # Check if the current word is not a punctuation itself
                if substituted_words[i] not in [',','.','!','?',';',"'"]:
                    substituted_words[i] = substituted_words[i].capitalize()


    return " ".join(substituted_words).replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?").replace(" ;", ";")


def syntactic_scrambler(text: str) -> str:
    """
    Scrambles the order of words in a sentence, but tries to keep punctuation at the end.
    """
    words = text.split()
    if not words:
        return ""

    # Separate punctuation at the end of the sentence
    last_word = words[-1]
    punctuation = ""
    if last_word and last_word[-1] in ".!?":
        punctuation = last_word[-1]
        words[-1] = last_word[:-1]
        if not words[-1]: # if the last word was only punctuation
            words.pop()
            if not words: # if sentence was only punctuation
                return punctuation

    random.shuffle(words)

    scrambled_sentence = " ".join(words)
    if scrambled_sentence and not scrambled_sentence[0].isalnum(): # handle cases where shuffle puts punc first
        scrambled_sentence = scrambled_sentence.lstrip()

    # Re-capitalize the first word
    if scrambled_sentence:
         # Find the first actual word to capitalize
        word_list = list(scrambled_sentence)
        for i in range(len(word_list)):
            if word_list[i].isalpha():
                word_list[i] = word_list[i].upper()
                break
        scrambled_sentence = "".join(word_list)


    return scrambled_sentence + punctuation


def misinterpret_text(text: str) -> str:
    """
    Applies a series of misinterpretations to the input text.
    """
    # Step 1: Literal Interpretation (New)
    text_after_literal = literal_interpreter(text)

    # Step 2: Lexical Substitution
    text_after_lexical = lexical_substituter(text_after_literal)

    # Step 3: Syntactic Scrambling
    # We'll apply scrambling sentence by sentence if there are multiple sentences.
    # Simple sentence split (can be improved with more robust sentence tokenization)
    sentences = re.split(r'(?<=[.!?])\s+', text_after_lexical)
    scrambled_sentences = [syntactic_scrambler(s) for s in sentences if s.strip()]

    final_text = " ".join(scrambled_sentences)

    return final_text

# --- New Literal Interpretation Module ---
LITERAL_IDIOMS_MAP = {
    r"it's raining cats and dogs": "actual felines and canines are falling from the sky",
    r"break a leg": "literally fracture a lower limb",
    r"bite the bullet": "actually sink your teeth into a piece of ammunition",
    r"spill the beans": "cause legumes to tumble out",
    r"piece of cake": "a literal slice of baked dessert",
    r"costs an arm and a leg": "requires the surgical removal of appendages for payment",
    r"let the cat out of the bag": "allow a feline to escape from a sack",
    r"kill two birds with one stone": "achieve the demise of a pair of avians using a single rock",
    r"speak of the devil": "you mentioned the archfiend, and so he appeared", # A bit more narrative
    r"once in a blue moon": "on the rare occasion the moon is visibly blue",
    r"throw in the towel": "hurl a piece of absorbent fabric",
}

def literal_interpreter(text: str) -> str:
    """
    Replaces common idioms with their literal, absurd interpretations.
    Uses case-insensitive matching.
    """
    interpreted_text = text
    for idiom, literal_meaning in LITERAL_IDIOMS_MAP.items():
        # Using re.IGNORECASE for case-insensitive replacement
        # Using a word boundary \b to avoid matching parts of words, e.g., "cat" in "caterpillar"
        # but need to be careful with idioms that might start/end with non-alphanumeric for \b
        # For simplicity now, we'll assume idioms are space-bounded or sentence bounded.
        # A simple regex replace should work for many cases.

        # We need to handle the regex compilation for each idiom.
        # To ensure whole phrase matching and ignore case:
        try:
            # (?i) makes the regex case-insensitive
            interpreted_text = re.sub(r"(?i)\b" + idiom + r"\b", literal_meaning, interpreted_text)
        except re.error as e:
            # This might happen if an idiom itself contains special regex characters
            # For this map, it should be fine.
            print(f"Regex error with idiom '{idiom}': {e}")
            pass # Keep original text for this idiom if regex fails

    return interpreted_text

if __name__ == '__main__':
    # Example usage
    test_phrases = [
        "Hello, world!",
        "I see their presents here.",
        "You're going to write two letters.",
        "This is a test sentence. And this is another one!",
        "What is the meaning of life?",
        "It's raining cats and dogs.",
        "This task is a piece of cake.",
        "Good luck on your exam, break a leg!",
        "I had to bite the bullet and tell him the news.",
        "Don't spill the beans about the surprise party."
    ]

    for original_text in test_phrases:
        # Test case insensitivity for idioms
        if "cats and dogs" in original_text:
            original_text = original_text.replace("it's", "IT'S") # Mix case

        print(f"Original: {original_text}")
        misinterpreted_text = misinterpret_text(original_text)
        print(f"Misinterpreted: {misinterpreted_text}\n")

    print("\n--- Interactive Test ---")
    interactive_tests = [
        "I am writing a long sentence to see how well it scrambles everything and if the punctuation stays in the right place.",
        "Is this working? I hope so!",
        "He decided to throw in the towel.",
        "Wow, that new car costs an arm and a leg, but it's beautiful."
    ]
    for test_input in interactive_tests:
        print(f"\nInput: {test_input}")
        print(f"Output: {misinterpret_text(test_input)}")
