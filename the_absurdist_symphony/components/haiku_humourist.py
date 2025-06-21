import json
import random
import os

class HaikuHumourist:
    """
    Generates whimsical or absurd haikus based on a mood vector.
    Aims for 5-7-5 syllable structure, with creative liberties.
    """
    def __init__(self, vocab_file_path=None):
        if vocab_file_path is None:
            # Construct path relative to this file's directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            vocab_file_path = os.path.join(base_dir, '..', 'data', 'haiku_vocab.json')

        self.vocab = self._load_vocab(vocab_file_path)
        self.mood_vector = {}

    def _load_vocab(self, vocab_file_path: str) -> dict:
        """Loads vocabulary from a JSON file."""
        try:
            with open(vocab_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Vocabulary file not found at {vocab_file_path}")
            # Fallback to a very basic internal vocab if file is missing
            return {
                "general_nouns_1_syllable": ["cat", "dog", "sky"],
                "general_verbs_1_syllable": ["runs", "jumps", "sleeps"],
                "general_adjectives_1_syllable": ["red", "big", "small"],
                "connectors_1_syllable": ["a", "the", "is"],
                "fillers_1_syllable": ["oh"],
            }
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {vocab_file_path}")
            return {} # Or raise an error

    def _get_words_by_syllables(self, target_syllables: int, word_type_prefixes: list[str]) -> list[str]:
        """
        Gets words with a specific syllable count from given categories.
        Example prefixes: ["general_nouns_", "mood_joy_words_"]
        """
        words = []
        for prefix in word_type_prefixes:
            key = f"{prefix}{target_syllables}_syllable"
            if key in self.vocab:
                words.extend(self.vocab[key])
            # For 2 and 3 syllables, also try "syllables" (plural)
            if target_syllables > 1:
                key_plural = f"{prefix}{target_syllables}_syllables"
                if key_plural in self.vocab:
                    words.extend(self.vocab[key_plural])
        return list(set(words)) # Unique words

    def _get_random_word(self, available_syllables: int, base_categories: list[str], mood_categories: list[str], mood_influence: float) -> tuple[str, int]:
        """
        Selects a random word, considering mood influence.
        Returns (word, syllable_count_of_word) or (None, 0) if no suitable word is found.
        Tries to match available_syllables, then less, then 1.
        """

        possible_syllables = list(range(1, available_syllables + 1))
        random.shuffle(possible_syllables) # Try different syllable counts

        for s_count in [available_syllables] + [s for s in possible_syllables if s != available_syllables]: # Prioritize exact match
            if s_count <= 0: continue

            words = []
            # Higher mood_influence means higher chance of picking mood words
            if random.random() < mood_influence and mood_categories:
                words = self._get_words_by_syllables(s_count, mood_categories)

            if not words: # If no mood words found or mood_influence is low
                words = self._get_words_by_syllables(s_count, base_categories)

            if words:
                return random.choice(words), s_count

        # Fallback: try any 1-syllable connector/filler if nothing else fits
        fallback_words = self._get_words_by_syllables(1, ["connectors_", "fillers_"])
        if fallback_words:
            return random.choice(fallback_words), 1

        return None, 0


    def _build_line(self, target_syllables: int, is_first_line: bool = False) -> str:
        """
        Builds a line of haiku with approximately target_syllables.
        """
        line_words = []
        syllables_left = target_syllables

        # Determine primary mood for this line/haiku (can be simplified)
        # This is a very basic way to pick a dominant mood for word selection
        mood_strengths = {
            'joy': self.mood_vector.get('joy', 0.0),
            'gloom': self.mood_vector.get('gloom', 0.0),
            'chaos': self.mood_vector.get('chaos', 0.0),
            'serenity': self.mood_vector.get('serenity', 0.0),
            'mystery': self.mood_vector.get('mystery', 0.0),
            'energy': self.mood_vector.get('energy', 0.0),
        }
        # Select top two moods or one if others are too low
        sorted_moods = sorted(mood_strengths.items(), key=lambda item: item[1], reverse=True)

        mood_cats_to_use = []
        mood_influence_factor = 0.0

        if sorted_moods[0][1] > 0.3: # Primary mood is strong enough
            mood_cats_to_use.append(f"mood_{sorted_moods[0][0]}_words_")
            mood_influence_factor = sorted_moods[0][1]
            if len(sorted_moods) > 1 and sorted_moods[1][1] > 0.2: # Secondary mood
                 mood_cats_to_use.append(f"mood_{sorted_moods[1][0]}_words_")
                 # Average influence if two moods
                 mood_influence_factor = (mood_influence_factor + sorted_moods[1][1]) / 2


        word_count = 0
        max_words_per_line = 5 # Avoid overly long lines of 1-syllable words

        while syllables_left > 0 and word_count < max_words_per_line:
            base_cats = ["general_nouns_", "general_verbs_", "general_adjectives_"]
            if word_count > 0 : # Allow connectors/fillers after the first word
                base_cats.extend(["connectors_", "fillers_"])

            # Add more nouns/adjectives at start, more verbs/connectors later? (simple heuristic)
            if word_count == 0: # First word often a noun or adjective
                 current_base_cats = ["general_nouns_", "general_adjectives_"]
            elif word_count == 1 and syllables_left > 2 : # Second word often a verb
                 current_base_cats = ["general_verbs_"]
            else: # Mix it up
                 current_base_cats = base_cats

            # Chaos factor: sometimes pick from ANY category
            if self.mood_vector.get('chaos', 0.0) > 0.7 and random.random() < 0.3:
                all_prefixes = list(set(k.split('_')[0] + "_" + k.split('_')[1] + "_" for k in self.vocab.keys()))
                current_base_cats = random.sample(all_prefixes, min(len(all_prefixes), 3))

            # "Mood Contradiction" for high chaos
            mood_contradiction_active = False
            if self.mood_vector.get('chaos', 0.0) > 0.75 and random.random() < 0.2: # 20% chance for a contradictory word
                print("HAIKU HUMOURIST: Engaging mood contradiction protocol!")
                mood_contradiction_active = True
                # Find an opposite mood category if possible
                # This is a simplistic way; could be more robust
                opposite_mood_cats = []
                if "mood_joy_words_" in mood_cats_to_use and "mood_gloom_words_" not in mood_cats_to_use:
                    opposite_mood_cats.append("mood_gloom_words_")
                elif "mood_gloom_words_" in mood_cats_to_use and "mood_joy_words_" not in mood_cats_to_use:
                    opposite_mood_cats.append("mood_joy_words_")
                if "mood_serenity_words_" in mood_cats_to_use and "mood_chaos_words_" not in mood_cats_to_use: # Chaos is already a mood cat
                    opposite_mood_cats.append("mood_chaos_words_") # Use chaos words if current mood is serene

                if opposite_mood_cats:
                    # Try to get a contradictory word, otherwise proceed normally
                    contradictory_word, contradictory_s_count = self._get_random_word(syllables_left, [], opposite_mood_cats, 1.0)
                    if contradictory_word:
                        line_words.append(f"{contradictory_word}*") # Mark with asterisk for fun
                        syllables_left -= contradictory_s_count
                        word_count += 1
                        if syllables_left <= 0 or word_count >= max_words_per_line:
                            continue # Move to next line or finish

            if not mood_contradiction_active or (mood_contradiction_active and (not contradictory_word)): # If not active or if contradictory word failed
                word, s_count = self._get_random_word(syllables_left, current_base_cats, mood_cats_to_use, mood_influence_factor)

            if word:
                line_words.append(word)
                syllables_left -= s_count
                word_count += 1
            else:
                # Could not find a suitable word, break to avoid infinite loop
                # This might mean the line is shorter than intended.
                break

        # Basic punctuation attempt for chaos/energy
        line_str = " ".join(line_words)
        if self.mood_vector.get('chaos', 0.0) > 0.6 and random.random() < 0.2:
            line_str += random.choice(["!", "?", "...", "?!"])
        elif self.mood_vector.get('energy', 0.0) > 0.7 and random.random() < 0.15:
            line_str += "!"

        return line_str.capitalize() if is_first_line or len(line_str) > 15 else line_str


    def generate_haiku(self, mood_vector: dict) -> list[str]:
        """
        Generates a haiku (list of three lines) based on the mood vector.
        """
        self.mood_vector = mood_vector
        if not self.vocab: # No vocabulary loaded
            return ["Error: No vocabulary.", "Cannot make a haiku now.", "File is missing perhaps."]

        haiku = [
            self._build_line(5, is_first_line=True),
            self._build_line(7),
            self._build_line(5)
        ]
        return haiku

if __name__ == '__main__':
    # Test assuming haiku_vocab.json is in ../data/ from this script's location
    # This relative path might need adjustment if running from a different CWD.
    # For agent environment, fixed path might be better or passed during init.

    # To make it runnable from the_absurdist_symphony directory:
    # python -m components.haiku_humourist
    vocab_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'haiku_vocab.json')
    if not os.path.exists(vocab_path):
        # Try an alternative path if running script directly from components/
        alt_vocab_path = os.path.join(os.path.dirname(__file__), '../data/haiku_vocab.json')
        if os.path.exists(alt_vocab_path):
            vocab_path = alt_vocab_path
        else:
            print(f"Warning: Could not find vocab at {vocab_path} or {alt_vocab_path}. Using fallback.")
            vocab_path = None


    humourist = HaikuHumourist(vocab_file_path=vocab_path)

    print("--- Test with a 'Joyful' Mood ---")
    joyful_mood = {
        'chaos': 0.1, 'serenity': 0.7, 'joy': 0.9,
        'gloom': 0.1, 'energy': 0.6, 'mystery': 0.1,
        'city': 'TestCitySunny'
    }
    haiku_joy = humourist.generate_haiku(joyful_mood)
    for line in haiku_joy: print(line)

    print("\n--- Test with a 'Gloomy & Chaotic' Mood ---")
    gloomy_mood = {
        'chaos': 0.8, 'serenity': 0.1, 'joy': 0.1,
        'gloom': 0.9, 'energy': 0.4, 'mystery': 0.7,
        'city': 'TestCityStormy'
    }
    haiku_gloom = humourist.generate_haiku(gloomy_mood)
    for line in haiku_gloom: print(line)

    print("\n--- Test with a 'Serene & Mysterious' Mood ---")
    serene_mood = {
        'chaos': 0.1, 'serenity': 0.9, 'joy': 0.2,
        'gloom': 0.2, 'energy': 0.1, 'mystery': 0.8,
        'city': 'TestCityFoggy'
    }
    haiku_serene = humourist.generate_haiku(serene_mood)
    for line in haiku_serene: print(line)

    print("\n--- Test with a 'High Energy' Mood ---")
    energetic_mood = {
        'chaos': 0.4, 'serenity': 0.2, 'joy': 0.5,
        'gloom': 0.1, 'energy': 0.9, 'mystery': 0.3,
        'city': 'TestCityWindy'
    }
    haiku_energy = humourist.generate_haiku(energetic_mood)
    for line in haiku_energy: print(line)

    print("\n--- Test with a Default/Error Mood (e.g., from WeatherWeaver failure) ---")
    error_mood = {
        'chaos': 0.1, 'serenity': 0.1, 'joy': 0.1,
        'gloom': 0.5, 'energy': 0.1, 'mystery': 0.2, 'error': 1.0
    }
    haiku_error = humourist.generate_haiku(error_mood)
    for line in haiku_error: print(line)

    # Example of using it with WeatherWeaver (conceptual, assuming files are accessible)
    # from weather_weaver import WeatherWeaver
    # print("\n--- Test with WeatherWeaver ---")
    # weaver = WeatherWeaver() # This would need path setup for utils.cities
    # mood = weaver.get_mood("Kyoto")
    # if mood and not mood.get('error'):
    #     print(f"Mood for Kyoto: {mood}")
    #     haiku_weather = humourist.generate_haiku(mood)
    #     for line in haiku_weather: print(line)
    # else:
    #     print(f"Could not generate weather based haiku. Mood: {mood}")
