import re

class LinguisticAnalyzer:
    """
    Analyzes a word or phrase to extract linguistic features.
    These features will influence the generation of "Word-Flowers."
    """

    def __init__(self):
        # Simple sentiment dictionary (can be expanded)
        self.positive_words = {"joy", "love", "happy", "bright", "good", "fun", "beauty"}
        self.negative_words = {"sad", "hate", "dark", "bad", "pain", "fear"}
        self.rare_chars = {'x', 'z', 'q', 'j'} # Define rare characters

    def _normalize_word(self, word: str) -> str:
        """Lowercase and remove non-alphabetic characters for analysis."""
        return re.sub(r'[^a-z]', '', word.lower())

    def analyze(self, text_input: str) -> dict:
        """
        Analyzes the input text (word or phrase) and returns its linguistic features.

        Args:
            text_input: The word or phrase to analyze.

        Returns:
            A dictionary of linguistic features.
            Example: {'sentiment_score': 0.8, 'length': 5, 'vowel_ratio': 0.4, 'has_rare_char': False, 'word_count': 1}
        """
        if not text_input.strip():
            return {
                'sentiment_score': 0.0,  # Neutral for empty
                'length': 0,
                'vowel_ratio': 0.0,
                'has_rare_char': False,
                'word_count': 0,
                'cleaned_words': []
            }

        words = text_input.split()
        cleaned_words = [self._normalize_word(w) for w in words if self._normalize_word(w)] # store cleaned words for further use

        if not cleaned_words: # if all words were non-alphabetic
             return {
                'sentiment_score': 0.0,
                'length': sum(len(w) for w in words), # Original length of non-alpha words
                'vowel_ratio': 0.0,
                'has_rare_char': False,
                'word_count': len(words),
                'cleaned_words': []
            }

        # For simplicity, sentiment is averaged over words.
        # A more complex phrase-level sentiment might be better but harder.
        sentiment_score = 0
        num_sentiment_words = 0
        for word in cleaned_words:
            if word in self.positive_words:
                sentiment_score += 1
                num_sentiment_words +=1
            elif word in self.negative_words:
                sentiment_score -= 1
                num_sentiment_words +=1

        # Average sentiment score, ranging roughly from -1 to 1.
        # If no sentiment words, it's neutral (0).
        # Add 0.5 to shift range to 0 to 1 for easier color mapping later? Or keep -1 to 1.
        # Let's keep it -1 to 1 for now, and map it to 0-1 in the flower engine if needed.
        # Default to 0 (neutral) if no words with sentiment value were found
        avg_sentiment_score = (sentiment_score / num_sentiment_words) if num_sentiment_words > 0 else 0.0


        # Aggregate features from all cleaned words
        total_length = sum(len(w) for w in cleaned_words)
        total_vowels = sum(1 for w in cleaned_words for char in w if char in "aeiou")

        vowel_ratio = (total_vowels / total_length) if total_length > 0 else 0.0

        has_rare_char = any(char in self.rare_chars for w in cleaned_words for char in w)

        return {
            'sentiment_score': avg_sentiment_score,
            'length': total_length, # Total length of alphabetic characters
            'vowel_ratio': vowel_ratio,
            'has_rare_char': has_rare_char,
            'word_count': len(cleaned_words),
            'cleaned_words': cleaned_words # Useful for the Garden to iterate over actual words
        }

if __name__ == '__main__':
    analyzer = LinguisticAnalyzer()

    test_phrases = [
        "joyful love",
        "sad dark fear",
        "neutral statement",
        "complex xylophone",
        "quizzical jaguar",
        "  ",
        "!@#$%^",
        "goodbad", # one word
        "good bad", # two words, should average to 0
        "Z",
        "a"
    ]

    for phrase in test_phrases:
        features = analyzer.analyze(phrase)
        print(f"Phrase: \"{phrase}\"")
        print(f"Features: {features}\n")

    # Example of expected output for "joyful love"
    # 'joyful' -> 'joy' (positive), length 3, vowels 1 (o)
    # 'love' -> 'love' (positive), length 4, vowels 2 (o,e)
    # Sentiment: (1+1)/2 = 1
    # Length: 3+4 = 7
    # Vowels: 1+2 = 3
    # Vowel ratio: 3/7 approx 0.428
    # Rare char: false
    # Word count: 2
    print("Expected for 'joyful love': {'sentiment_score': 1.0, 'length': 7, 'vowel_ratio': 0.428..., 'has_rare_char': False, 'word_count': 2}")
    features_joy_love = analyzer.analyze("joyful love")
    assert features_joy_love['sentiment_score'] == 1.0
    assert features_joy_love['length'] == 7
    assert abs(features_joy_love['vowel_ratio'] - 3/7) < 0.001
    assert not features_joy_love['has_rare_char']
    assert features_joy_love['word_count'] == 2

    # Example for "good bad"
    # 'good' (positive), 'bad' (negative)
    # Sentiment: (1-1)/2 = 0
    features_good_bad = analyzer.analyze("good bad")
    assert features_good_bad['sentiment_score'] == 0.0

    # Example for empty string
    features_empty = analyzer.analyze("   ")
    assert features_empty['sentiment_score'] == 0.0
    assert features_empty['length'] == 0
    assert features_empty['word_count'] == 0

    # Example for non-alphabetic
    features_non_alpha = analyzer.analyze("!@#$")
    assert features_non_alpha['sentiment_score'] == 0.0
    assert features_non_alpha['length'] == 0 # Length of original non-alpha characters
    assert features_non_alpha['word_count'] == 0 # Number of original "words"
    assert not features_non_alpha['cleaned_words']

    print("All basic assertions passed.")
