import math
import random

class FractalFlowerEngine:
    """
    Generates fractal data for a "Word-Flower" based on linguistic features
    and a unique flower seed.

    For this initial implementation, we'll use a simplified L-system
    to generate a branching structure. The "fractal" will be a list of
    line segments (start_x, start_y, end_x, end_y, thickness, color_intensity).
    """

    def __init__(self, linguistic_features: dict, flower_seed: int):
        self.features = linguistic_features
        self.rng = random.Random(flower_seed) # Initialize RNG with the flower's unique seed

        # Base parameters - these will be modulated by linguistic features
        self.base_iterations = 3
        self.base_angle_variance = 25.0  # degrees
        self.base_length = 10.0
        self.base_thickness = 3.0
        self.base_length_decay = 0.7

    def _apply_linguistic_modulation(self):
        """Modulate base fractal parameters using linguistic features."""

        # Iterations influenced by word length (more letters, more complex flower)
        # Max length capped to avoid overly complex fractals initially
        iterations = self.base_iterations + int(self.features.get('length', 0) / 5)
        iterations = min(iterations, 5) # Cap iterations

        # Angle variance influenced by vowel ratio (more vowels, more open/spread out)
        # vowel_ratio is 0-1. Map it to a multiplier for angle.
        angle_variance_multiplier = 1.0 + (self.features.get('vowel_ratio', 0.5) - 0.5) # e.g. 0.5 -> 1.0, 1.0 -> 1.5, 0.0 -> 0.5
        angle = self.base_angle_variance * angle_variance_multiplier
        angle = max(15.0, min(angle, 45.0)) # Clamp angle

        # Initial length influenced by word_count (longer phrases have slightly larger presence)
        initial_length = self.base_length * (1 + (self.features.get('word_count', 1) -1) * 0.1)
        initial_length = max(5.0, min(initial_length, 15.0))

        # Thickness could be influenced by presence of rare characters (thicker strokes for emphasis)
        thickness = self.base_thickness
        if self.features.get('has_rare_char', False):
            thickness *= 1.5
        thickness = max(1.0, min(thickness, 5.0))

        # Color intensity from sentiment_score (-1 to 1). We'll map this to 0-1.
        # For now, this is just a value; actual color mapping is for the visualizer.
        # Positive sentiment -> higher intensity, negative -> lower (or a different hue later)
        color_intensity = (self.features.get('sentiment_score', 0.0) + 1) / 2.0 # Maps -1 to 1 -> 0 to 1

        return iterations, angle, initial_length, thickness, color_intensity

    def generate_l_system_flower(self):
        """
        Generates a flower structure using a simple L-system.
        Axiom: "F"
        Rules: "F" -> "F[+F][-F]F" (example, can be varied)
               or "F" -> "FF-[-F+F+F]+[+F-F-F]" for more complexity
               or simpler "F" -> "F[-F][+F]"

        We'll use a simplified turtle-graphics like approach.
        The state is (x, y, angle, length, current_thickness).
        Output: list of (x1, y1, x2, y2, thickness, color_intensity_at_segment)
        """
        iterations, angle_delta, current_length, base_thickness, color_intensity = self._apply_linguistic_modulation()

        segments = []
        stack = []

        # Initial state: start at (0,0), angle pointing upwards (90 deg), given length and thickness
        current_pos = (0.0, 0.0)
        current_angle_deg = 90.0

        # L-system string generation (simplified: direct recursive calls instead of string)
        # We'll use a direct recursive generation for simplicity here.

        def draw_recursive(x, y, angle_deg, length, thick, depth):
            if depth <= 0:
                return

            # Calculate end point
            rad = math.radians(angle_deg)
            nx = x + length * math.cos(rad)
            ny = y - length * math.sin(rad) # Screen coordinates typically Y-down

            # Add segment. Color intensity can be uniform or vary along branches.
            # For now, uniform per flower.
            segments.append((x, y, nx, ny, thick, color_intensity))

            # New parameters for next segments
            new_length = length * self.base_length_decay
            new_thick = max(1.0, thick * 0.8)

            # Branching: this is where L-system rules would be applied.
            # Rule: F -> F[-branch1][+branch2]F (simplified)
            # We'll make two main branches and one continuing segment

            # 1. Left Branch
            draw_recursive(nx, ny, angle_deg - self.rng.uniform(angle_delta*0.8, angle_delta*1.2), new_length, new_thick, depth - 1)

            # 2. Right Branch
            draw_recursive(nx, ny, angle_deg + self.rng.uniform(angle_delta*0.8, angle_delta*1.2), new_length, new_thick, depth - 1)

            # 3. (Optional) Continue main stem slightly or add another central element
            # For more bushiness, can add another recursive call here with a smaller angle change
            if self.rng.random() < 0.3: # Probabilistic middle branch
                 draw_recursive(nx, ny, angle_deg + self.rng.uniform(-angle_delta*0.3, angle_delta*0.3), new_length * 0.8, new_thick, depth-1)


        # Start the recursive drawing
        # Initial call is for the main "stem" before branching starts in recursion
        stem_end_x = current_pos[0] + current_length * 0.2 * math.cos(math.radians(current_angle_deg))
        stem_end_y = current_pos[1] - current_length * 0.2 * math.sin(math.radians(current_angle_deg))
        segments.append((*current_pos, stem_end_x, stem_end_y, base_thickness, color_intensity))

        draw_recursive(stem_end_x, stem_end_y, current_angle_deg, current_length, base_thickness, int(iterations))

        return segments

if __name__ == '__main__':
    # Mock LinguisticAnalyzer and its output for testing
    class MockLinguisticAnalyzer:
        def analyze(self, text_input: str):
            # Simplified features for testing
            if "joy" in text_input:
                return {'sentiment_score': 0.8, 'length': 10, 'vowel_ratio': 0.6, 'has_rare_char': False, 'word_count': 2, 'cleaned_words': ['joy', 'flower']}
            elif "sad" in text_input:
                return {'sentiment_score': -0.7, 'length': 8, 'vowel_ratio': 0.3, 'has_rare_char': True, 'word_count': 1, 'cleaned_words': ['sadxyz']}
            else:
                return {'sentiment_score': 0.1, 'length': 15, 'vowel_ratio': 0.45, 'has_rare_char': False, 'word_count': 3, 'cleaned_words': ['neutral', 'example', 'text']}

    analyzer = MockLinguisticAnalyzer()

    test_cases = [
        ("joyful flower", 12345),
        ("sadxyz", 67890),
        ("neutral example text", 101112)
    ]

    for text, seed in test_cases:
        print(f"\n--- Testing for text: '{text}', seed: {seed} ---")
        features = analyzer.analyze(text)
        print(f"Linguistic Features: {features}")

        engine = FractalFlowerEngine(features, seed)
        iterations, angle, length, thickness, color_int = engine._apply_linguistic_modulation() # Check modulated params
        print(f"Modulated Params: Iter={iterations}, Angle={angle:.2f}, Len={length:.2f}, Thick={thickness:.2f}, ColorInt={color_int:.2f}")

        flower_data = engine.generate_l_system_flower()
        print(f"Generated {len(flower_data)} segments for the flower.")

        if flower_data:
            print("First 3 segments (sample):")
            for i, seg in enumerate(flower_data[:3]):
                print(f"  Seg {i}: ({seg[0]:.1f},{seg[1]:.1f}) to ({seg[2]:.1f},{seg[3]:.1f}), Thick={seg[4]:.1f}, CI={seg[5]:.2f}")
        else:
            print("No segments generated.")

    # Test with minimal features
    print("\n--- Testing with minimal features ---")
    min_features = {'sentiment_score': 0.0, 'length': 1, 'vowel_ratio': 0.1, 'has_rare_char': False, 'word_count': 1, 'cleaned_words':['a']}
    min_seed = 1
    engine_min = FractalFlowerEngine(min_features, min_seed)
    iterations, angle, length, thickness, color_int = engine_min._apply_linguistic_modulation()
    print(f"Modulated Params (min): Iter={iterations}, Angle={angle:.2f}, Len={length:.2f}, Thick={thickness:.2f}, ColorInt={color_int:.2f}")
    flower_data_min = engine_min.generate_l_system_flower()
    print(f"Generated {len(flower_data_min)} segments for the minimal flower.")
    if flower_data_min:
        print(f"  First segment: ({flower_data_min[0][0]:.1f},{flower_data_min[0][1]:.1f}) to ({flower_data_min[0][2]:.1f},{flower_data_min[0][3]:.1f})")

    # Ensure iterations are capped
    print("\n--- Testing iteration cap ---")
    max_len_features = {'sentiment_score': 0.0, 'length': 100, 'vowel_ratio': 0.5, 'has_rare_char': False, 'word_count': 1, 'cleaned_words':['longword']}
    engine_maxlen = FractalFlowerEngine(max_len_features, 1)
    iterations_capped, _, _, _, _ = engine_maxlen._apply_linguistic_modulation()
    print(f"Iterations for long word (capped): {iterations_capped}")
    assert iterations_capped <= 5

    print("\nBasic functionality tests seem OK.")
