import time
import random
import math

from .cosmic_seed_generator import CosmicSeedGenerator
from .linguistic_analyzer import LinguisticAnalyzer
from .fractal_flower_engine import FractalFlowerEngine

class WordFlower:
    """Represents a single flower in the garden."""
    def __init__(self, source_word: str, linguistic_features: dict, fractal_data: list, position: tuple, initial_seed: int):
        self.source_word = source_word
        self.linguistic_features = linguistic_features
        self.fractal_data = fractal_data # List of (x1, y1, x2, y2, thickness, color_intensity)
        self.position = position # (x, y) in garden coordinates
        self.initial_seed = initial_seed # For potential regeneration or evolution

        self.age = 0
        self.max_age = 100 + random.randint(-20, 20) # Base lifespan
        self.current_scale = 0.1 # Starts small and grows
        self.max_scale = 1.0 + (linguistic_features.get('length',5)/10 - 0.5) # Larger words can grow a bit bigger
        self.growth_rate = 0.05 + (random.random() * 0.05)

        # Color will be derived from sentiment_score and other factors by the visualizer
        # Store effective color_intensity which might be modulated by garden effects
        self.effective_color_intensity = linguistic_features.get('sentiment_score', 0.0)
        self.is_fading = False
        self.is_dead = False

    def update(self, time_effect: float):
        self.age += 1

        if not self.is_fading:
            if self.current_scale < self.max_scale:
                self.current_scale += self.growth_rate * time_effect # time_effect can slow/speed growth
                self.current_scale = min(self.current_scale, self.max_scale)

            if self.age > self.max_age * (0.75 + random.random()*0.2) : # Start fading after ~75-95% of lifespan
                self.is_fading = True

        if self.is_fading:
            self.current_scale -= (self.growth_rate * 0.5) * time_effect # Fade a bit slower than growth
            if self.current_scale <= 0.01:
                self.is_dead = True

        # Example: Modulate color intensity based on age (e.g. vibrant when young, duller when old)
        # This is a simple way, could be more complex.
        age_factor = max(0.5, 1 - (self.age / (self.max_age * 1.5)))
        self.effective_color_intensity = self.linguistic_features.get('sentiment_score', 0.0) * age_factor


class Garden:
    """
    Manages the collection of WordFlowers, their evolution,
    and interactions within the Ephemeral Echo Garden.
    """
    def __init__(self, initial_quote: str, width: int, height: int):
        self.width = width
        self.height = height

        self.seed_generator = CosmicSeedGenerator(initial_quote)
        self.master_seed = self.seed_generator.generate_master_seed()
        self.rng = random.Random(self.master_seed) # Garden's master RNG

        self.linguistic_analyzer = LinguisticAnalyzer()

        self.word_flowers = []
        self.current_time_effect = 1.0 # Modulates growth, etc.
        self.garden_time = 0

        # For Nomad generation
        self._markov_corpus = self._build_markov_corpus(initial_quote)
        self._nomad_spawn_chance = 0.02 # Chance per evolution step to spawn a nomad

    def _build_markov_corpus(self, text: str) -> dict:
        """Builds a simple character-level markov chain model from text."""
        model = {}
        words = self.linguistic_analyzer._normalize_word(text).split() # Use analyzer's normalizer
        if not words: # Handle empty or non-alpha text
            words = ["placeholder"]

        for word in words:
            if not word: continue
            w = "^" + word + "$" # Add start/end markers
            for i in range(len(w) - 1):
                char = w[i]
                next_char = w[i+1]
                if char not in model:
                    model[char] = []
                model[char].append(next_char)
        return model

    def _generate_markov_text(self, min_len=3, max_len=8) -> str:
        """Generates a word-like string using the markov model."""
        if not self._markov_corpus or '^' not in self._markov_corpus:
            return "nomad" # Fallback

        current_char = '^'
        result = []
        length = 0
        max_attempts = max_len * 3 # Avoid infinite loops with sparse models

        while length < max_len and max_attempts > 0:
            max_attempts -=1
            if current_char not in self._markov_corpus or not self._markov_corpus[current_char]:
                break
            next_char = self.rng.choice(self._markov_corpus[current_char])
            if next_char == '$':
                if length >= min_len:
                    break
                else: # Too short, try to continue or pick another path
                    continue
            result.append(next_char)
            current_char = next_char
            length += 1

        return "".join(result) if length >= min_len else "echo" # Fallback if too short

    def _get_flower_seed(self, word: str, position_in_phrase: int) -> int:
        """Generate a unique seed for each flower based on master seed and word specifics."""
        word_hash = hash(word)
        return (self.master_seed + word_hash + position_in_phrase * 101) % 2**32 # Ensure positive int

    def sow_phrase(self, phrase: str, base_position: tuple = None):
        """Sows a new phrase into the garden. Words become flowers."""
        analysis = self.linguistic_analyzer.analyze(phrase)
        cleaned_words = analysis.get('cleaned_words', [])

        if not cleaned_words:
            # If phrase was empty or non-alphabetic, maybe sow a "silence" flower or skip
            # For now, we skip.
            return

        num_words = len(cleaned_words)

        # Distribute flowers somewhat randomly around the base_position or garden center
        # This layout can be much more sophisticated.
        for i, word_str in enumerate(cleaned_words):
            if not base_position:
                # Attempt to find a relatively open spot, or just random
                px = self.rng.uniform(self.width * 0.1, self.width * 0.9)
                py = self.rng.uniform(self.height * 0.1, self.height * 0.9)
            else:
                # Spread words in a phrase a bit
                angle = (i / num_words) * 2 * math.pi + self.rng.uniform(-0.2, 0.2)
                radius = 20 + num_words * 5 + self.rng.uniform(-5,5)
                px = base_position[0] + math.cos(angle) * radius
                py = base_position[1] + math.sin(angle) * radius

            px = max(0, min(px, self.width))
            py = max(0, min(py, self.height))

            # Analyze each word individually for its own features for the flower engine
            # (though the phrase analysis gave us the cleaned words)
            word_features = self.linguistic_analyzer.analyze(word_str)
            if not word_features or word_features['length'] == 0: # Skip empty normalized words
                continue

            flower_seed = self._get_flower_seed(word_str, i)
            flower_engine = FractalFlowerEngine(word_features, flower_seed)
            fractal_data = flower_engine.generate_l_system_flower()

            if fractal_data:
                flower = WordFlower(word_str, word_features, fractal_data, (px, py), flower_seed)
                self.word_flowers.append(flower)

    def _spawn_nonsense_nomad(self):
        nomad_text = self._generate_markov_text(min_len=4, max_len=10)
        if nomad_text:
            # Nomads appear at random edge positions
            edge = self.rng.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top': pos = (self.rng.uniform(0, self.width), 0)
            elif edge == 'bottom': pos = (self.rng.uniform(0, self.width), self.height)
            elif edge == 'left': pos = (0, self.rng.uniform(0, self.height))
            else: pos = (self.width, self.rng.uniform(0, self.height))

            # Give nomads slightly different characteristics, e.g., faster fading, unique color hints
            analysis = self.linguistic_analyzer.analyze(nomad_text)
            analysis['sentiment_score'] = self.rng.uniform(-0.2, 0.2) # Nomads are mostly neutral but varied

            flower_seed = self._get_flower_seed(nomad_text, -1) # -1 for nomads
            engine = FractalFlowerEngine(analysis, flower_seed)
            fractal_data = engine.generate_l_system_flower()

            if fractal_data:
                nomad_flower = WordFlower(nomad_text, analysis, fractal_data, pos, flower_seed)
                nomad_flower.max_age *= 0.5 # Nomads are more ephemeral
                nomad_flower.is_nomad = True # Tag for special rendering or behavior
                self.word_flowers.append(nomad_flower)


    def _handle_cross_pollination(self):
        # Simple proximity based cross-pollination. Could be more complex.
        # Limit checks to avoid N^2 complexity on large number of flowers
        if len(self.word_flowers) < 2 or self.rng.random() > 0.1: # Only try sometimes
            return

        eligible_parents = [f for f in self.word_flowers if f.age > f.max_age * 0.3 and not f.is_fading and not getattr(f, 'is_nomad', False)]
        if len(eligible_parents) < 2:
            return

        # Pick two random parents from eligible ones
        # This is not true proximity but simpler for now
        parent1 = self.rng.choice(eligible_parents)
        parent2 = self.rng.choice(eligible_parents)

        if parent1 == parent2:
            return

        # Combine words in a simple way
        # e.g., half of parent1's word + half of parent2's word
        p1_word = parent1.source_word
        p2_word = parent2.source_word

        new_word = p1_word[:len(p1_word)//2] + p2_word[len(p2_word)//2:]

        if len(new_word) > 2 and len(new_word) < 15 : # Avoid tiny or huge words
            # New flower appears near the "midpoint" of parents
            mid_x = (parent1.position[0] + parent2.position[0]) / 2
            mid_y = (parent1.position[1] + parent2.position[1]) / 2
            # Add some jitter to the position
            mid_x += self.rng.uniform(-10,10)
            mid_y += self.rng.uniform(-10,10)

            #print(f"Cross-pollination: '{parent1.source_word}' + '{parent2.source_word}' -> '{new_word}' at ({mid_x:.0f},{mid_y:.0f})")
            self.sow_phrase(new_word, base_position=(mid_x, mid_y))


    def evolve(self):
        self.garden_time += 1
        # Update time effect (e.g., based on a sine wave for day/night cycle)
        self.current_time_effect = 0.8 + 0.2 * math.sin(self.garden_time * 0.01) # Slow cycle

        for flower in self.word_flowers:
            flower.update(self.current_time_effect)

        # Remove dead flowers
        self.word_flowers = [f for f in self.word_flowers if not f.is_dead]

        # Spawn Nomads
        if self.rng.random() < self._nomad_spawn_chance:
            self._spawn_nonsense_nomad()

        # Cross-pollination
        if self.garden_time % 10 == 0: # Attempt cross-pollination less frequently
             self._handle_cross_pollination()

        # Limit total flowers to avoid performance issues (simple cap for now)
        max_flowers = 100
        if len(self.word_flowers) > max_flowers:
            # Remove oldest flowers first if over capacity
            self.word_flowers.sort(key=lambda f: f.age, reverse=True)
            self.word_flowers = self.word_flowers[:max_flowers]


    def get_renderable_flowers(self) -> list:
        """Returns data needed for rendering."""
        render_list = []
        for flower in self.word_flowers:
            if flower.current_scale > 0.01: # Only render visible flowers
                render_list.append({
                    'fractal_data': flower.fractal_data,
                    'position': flower.position,
                    'scale': flower.current_scale,
                    'color_intensity': flower.effective_color_intensity,
                    'source_word': flower.source_word,
                    'is_nomad': getattr(flower, 'is_nomad', False),
                    'thickness_multiplier': flower.linguistic_features.get('has_rare_char', False) # Example
                })
        return render_list

if __name__ == '__main__':
    print("Initializing Garden...")
    # A nice, absurd quote for testing
    #quote = "The Jabberwocky, with eyes of flame, came whiffling through the tulgey wood"
    quote = "Colourless green ideas sleep furiously." # Chomsky

    garden_width, garden_height = 80, 40 # For a conceptual text grid

    my_garden = Garden(initial_quote=quote, width=garden_width, height=garden_height)
    print(f"Garden Master Seed: {my_garden.master_seed}")
    print(f"Initial Markov Corpus sample ('^'): {my_garden._markov_corpus.get('^', [])[:5]}")
    print(f"Generated Nomad sample: {my_garden._generate_markov_text()}")


    print("\nSowing initial phrase...")
    my_garden.sow_phrase(quote) # Sow the initial quote itself
    print(f"Number of flowers after initial sowing: {len(my_garden.word_flowers)}")
    if my_garden.word_flowers:
        print(f"First flower: {my_garden.word_flowers[0].source_word} at {my_garden.word_flowers[0].position}")

    print("\nSimulating garden evolution for a few steps...")
    for i in range(50):
        my_garden.evolve()
        if (i+1) % 10 == 0:
            print(f"Step {i+1}: {len(my_garden.word_flowers)} flowers. Time effect: {my_garden.current_time_effect:.2f}")
            # Check for new nomads or cross-pollinated flowers
            new_creations = [f for f in my_garden.word_flowers if f.age <= 1]
            for nc in new_creations:
                type = "Nomad" if getattr(nc, 'is_nomad', False) else "Flower"
                #print(f"  New {type}: {nc.source_word}")


    print("\nFinal state of some flowers:")
    for i, flower in enumerate(my_garden.word_flowers[:5]):
        print(f"  Flower {i} ('{flower.source_word}'): Age {flower.age}, Scale {flower.current_scale:.2f}, Dead: {flower.is_dead}")

    render_data = my_garden.get_renderable_flowers()
    print(f"\nNumber of flowers to render: {len(render_data)}")
    if render_data:
        print(f"Sample render data for '{render_data[0]['source_word']}': Scale {render_data[0]['scale']:.2f}, Pos {render_data[0]['position']}")

    print("\nTesting sowing another phrase...")
    my_garden.sow_phrase("A new bloom appears.", base_position=(garden_width/2, garden_height/2))
    print(f"Number of flowers after second sowing: {len(my_garden.word_flowers)}")

    # Simulate more
    for i in range(50):
        my_garden.evolve()

    print(f"\nAfter more evolution: {len(my_garden.word_flowers)} flowers.")
    print("Garden simulation basic tests seem OK.")
