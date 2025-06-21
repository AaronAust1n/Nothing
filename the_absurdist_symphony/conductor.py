from .components.weather_weaver import WeatherWeaver
from .components.visual_poet import VisualPoet
from .components.haiku_humourist import HaikuHumourist
from .components.soundscape_synth import SoundscapeSynth
from .components.philosophical_goldfish import PhilosophicalGoldfish
import random
import os

class Conductor:
    """
    Orchestrates the various components of The Absurdist Symphony.
    Initializes all components and manages a single cycle of the symphony.
    """
    def __init__(self, visual_poet_width=400, visual_poet_height=300):
        # Determine base path for data files, assuming conductor.py is in the project root
        # and components can find their data relative to their own location or a common data dir.
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Paths for components that load data files
        # Components themselves handle the relative path logic from their location.
        # So, we don't need to pass full paths here if components are robust.
        # However, explicit paths can be safer if cwd is unpredictable.
        # For now, relying on components' internal path logic.
        # Example: haiku_vocab_path = os.path.join(base_dir, 'data', 'haiku_vocab.json')
        # goldfish_quotes_path = os.path.join(base_dir, 'data', 'goldfish_quotes.txt')

        self.weather_weaver = WeatherWeaver()
        self.visual_poet = VisualPoet(width=visual_poet_width, height=visual_poet_height)
        self.haiku_humourist = HaikuHumourist() # Relies on its own relative path to data
        self.soundscape_synth = SoundscapeSynth()
        self.philosophical_goldfish = PhilosophicalGoldfish() # Relies on its own relative path to data

        self.symphony_cycle_count = 0

    def run_symphony_cycle(self, city: str = None) -> dict:
        """
        Runs one full cycle of the Absurdist Symphony.
        1. Fetches weather to get a mood vector.
        2. Generates visual poetry.
        3. Generates a haiku.
        4. Generates a soundscape description.
        5. Optionally, gets wisdom from the goldfish.
        Returns a dictionary containing all generated artifacts.
        """
        self.symphony_cycle_count += 1
        print(f"\n--- Starting Symphony Cycle {self.symphony_cycle_count} ---")

        # 1. WeatherWeaver
        print("Conductor: Consulting the Weather Weaver...")
        mood_vector = self.weather_weaver.get_mood(city=city)
        if mood_vector.get('error'):
            print(f"Conductor: Weather Weaver reported an error. Using default mood. City: {mood_vector.get('city', 'Unknown')}")
        else:
            print(f"Conductor: Mood received for {mood_vector.get('city', 'Unknown')}.")
            # print(f"Mood Vector: {mood_vector}") # Can be verbose

        # 2. VisualPoet
        print("Conductor: Cueing the Visual Poet...")
        svg_poem = self.visual_poet.generate_poem(mood_vector)
        print("Conductor: Visual Poem received.")

        # 3. HaikuHumourist
        print("Conductor: Summoning the Haiku Humourist...")
        haiku = self.haiku_humourist.generate_haiku(mood_vector)
        print("Conductor: Haiku received.")

        # 4. SoundscapeSynth
        print("Conductor: Engaging the Soundscape Synthesizer...")
        soundscape_description = self.soundscape_synth.generate_soundscape_description(mood_vector)
        print("Conductor: Soundscape Description received.")

        # 5. PhilosophicalGoldfish
        goldfish_wisdom = None
        # Goldfish appears randomly, more often if chaos is high or it's a special cycle
        chaos_level = mood_vector.get('chaos', 0.0)
        goldfish_appearance_chance = 0.3 + (chaos_level * 0.4) # Base 30%, up to 70% with max chaos

        if self.symphony_cycle_count == 1 or random.random() < goldfish_appearance_chance:
            print("Conductor: The Philosophical Goldfish has something to say...")
            goldfish_wisdom = self.philosophical_goldfish.dispense_wisdom(mood_vector)
            print(f"Conductor: Goldfish wisdom: \"{goldfish_wisdom}\"")
        else:
            print("Conductor: The Philosophical Goldfish remains pensively silent this cycle.")

        cycle_output = {
            "cycle_number": self.symphony_cycle_count,
            "mood_vector": mood_vector, # Contains city, weather_desc, temp_c, etc.
            "visual_poem_svg": svg_poem,
            "haiku_lines": haiku,
            "soundscape": soundscape_description,
            "goldfish_wisdom": goldfish_wisdom,
            "city_name": mood_vector.get('city', 'Unknown City'),
            "weather_description": mood_vector.get('weather_desc', 'Weather unclear')
        }

        print(f"--- Symphony Cycle {self.symphony_cycle_count} Complete ---")
        return cycle_output

if __name__ == '__main__':
    print("Initializing the Conductor for a test run...")
    conductor = Conductor()

    # Run a few cycles
    for i in range(3):
        print(f"\n>>> Requesting Symphony Cycle {i+1} from Conductor...")
        # On the first cycle, let's pick a specific city, then random
        # city_for_cycle = "Timbuktu" if i == 0 else None
        # For simplicity in testing without relying on specific city data being available always:
        city_for_cycle = None

        output = conductor.run_symphony_cycle(city=city_for_cycle)

        print(f"\nConductor Test Output for Cycle {output['cycle_number']}:")
        print(f"  City: {output['city_name']} ({output['weather_description']})")
        print(f"  Mood (Joy): {output['mood_vector'].get('joy', 0.0):.2f}, (Chaos): {output['mood_vector'].get('chaos', 0.0):.2f}")
        print(f"  Visual Poem SVG: {len(output['visual_poem_svg'])} bytes")
        print(f"  Haiku: {' / '.join(output['haiku_lines'])}")
        print(f"  Soundscape Title: {output['soundscape']['title']}")
        print(f"  Soundscape Tempo: {output['soundscape']['tempo']}")
        if output['goldfish_wisdom']:
            print(f"  Goldfish Says: {output['goldfish_wisdom']}")
        else:
            print("  Goldfish Says: Nothing this time.")

    print("\nConductor test run finished.")
