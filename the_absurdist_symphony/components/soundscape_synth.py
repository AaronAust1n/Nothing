import random

class SoundscapeSynth:
    """
    Generates a description of a musical soundscape based on a mood vector.
    It doesn't produce actual audio, but a textual/structural representation.
    """
    def __init__(self):
        self.mood_vector = {}
        self.notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.octaves = [2, 3, 4, 5] # Range of octaves
        self.durations = {
            "whole": 4.0, "half": 2.0, "quarter": 1.0,
            "eighth": 0.5, "sixteenth": 0.25,
            "dotted_quarter": 1.5, "dotted_eighth": 0.75
        }
        self.duration_names = list(self.durations.keys())

        self.instrument_families = {
            "strings": ["violin", "viola", "cello", "double bass", "harp"],
            "woodwinds": ["flute", "oboe", "clarinet", "bassoon", "piccolo", "saxophone"],
            "brass": ["trumpet", "trombone", "french horn", "tuba"],
            "percussion_pitched": ["glockenspiel", "xylophone", "marimba", "vibraphone", "timpani"],
            "percussion_unpitched": ["snare drum", "bass drum", "cymbal", "triangle", "tambourine", "cowbell"],
            "keyboards": ["piano", "harpsichord", "organ", "celesta"],
            "electronic": ["synth pad", "synth lead", "theremin-like sound", "electronic pulse", "glitchy beat"],
            "whimsical": ["kazoo", "slide whistle", "rubber chicken", "bicycle horn", "cat's meow sample"]
        }

    def _get_tempo_description(self) -> tuple[str, int]:
        """Determines tempo based on mood."""
        energy = self.mood_vector.get('energy', 0.0)
        serenity = self.mood_vector.get('serenity', 0.0)
        gloom = self.mood_vector.get('gloom', 0.0)
        chaos = self.mood_vector.get('chaos', 0.0)

        base_bpm = 90 # Neutral average

        bpm = base_bpm + (energy * 60) - (serenity * 40) - (gloom * 30) + (random.uniform(-10, 10) * chaos)
        bpm = max(30, min(200, int(bpm))) # Clamp BPM

        desc = ""
        if bpm < 50: desc = "Very Slow (Largo/Grave)"
        elif bpm < 70: desc = "Slow (Adagio/Lento)"
        elif bpm < 90: desc = "Moderately Slow (Andante)"
        elif bpm < 110: desc = "Moderate (Moderato)"
        elif bpm < 130: desc = "Moderately Fast (Allegretto)"
        elif bpm < 160: desc = "Fast (Allegro/Vivace)"
        else: desc = "Very Fast (Presto/Prestissimo)"

        if chaos > 0.7 and random.random() < 0.3:
            desc += " with erratic fluctuations"
        elif energy > 0.8 and random.random() < 0.2:
            desc += " and a driving pulse"

        return desc, bpm

    def _get_key_mode_description(self) -> str:
        """Determines key/mode based on mood."""
        joy = self.mood_vector.get('joy', 0.0)
        gloom = self.mood_vector.get('gloom', 0.0)
        mystery = self.mood_vector.get('mystery', 0.0)
        chaos = self.mood_vector.get('chaos', 0.0)

        root_note = random.choice(self.notes)

        if chaos > 0.8:
            return f"Atonal and chaotic, centered loosely around {root_note} but frequently departing."
        if mystery > 0.7:
            modes = [
                f"{root_note} whole-tone scale, creating an ambiguous, floating feel.",
                f"{root_note} diminished scale, full of tension and uncertainty.",
                f"Ambiguous tonality, perhaps {root_note} Phrygian or Locrian, sounding exotic or unresolved."
            ]
            return random.choice(modes)

        if joy > gloom and joy > 0.4:
            if mystery > 0.5:
                return f"{root_note} Lydian dominant, bright but with a quirky, unexpected twist."
            return f"{root_note} Major, generally upbeat and bright."
        elif gloom > joy and gloom > 0.4:
            if mystery > 0.5:
                return f"{root_note} Harmonic Minor, melancholic with an exotic, slightly tense flavor."
            return f"{root_note} minor, conveying a somber or introspective mood."

        return f"A simple, perhaps pentatonic scale based on {root_note}, neither overtly major nor minor."

    def _get_instrumentation_description(self, num_instruments=3) -> list[str]:
        """Suggests instrumentation based on mood."""
        joy = self.mood_vector.get('joy', 0.0)
        gloom = self.mood_vector.get('gloom', 0.0)
        serenity = self.mood_vector.get('serenity', 0.0)
        chaos = self.mood_vector.get('chaos', 0.0)
        energy = self.mood_vector.get('energy', 0.0)
        mystery = self.mood_vector.get('mystery', 0.0)

        chosen_instruments = set()

        # Mood-based preferences
        if joy > 0.6:
            chosen_instruments.add(random.choice(self.instrument_families["keyboards"] + self.instrument_families["woodwinds"]))
            if energy > 0.5: chosen_instruments.add(random.choice(self.instrument_families["brass"]))
        if gloom > 0.6:
            chosen_instruments.add(random.choice(self.instrument_families["strings"]))
            if mystery > 0.5 : chosen_instruments.add(random.choice(["pipe organ", "bass clarinet"]))
        if serenity > 0.6:
            chosen_instruments.add(random.choice(["flute", "harp", "celesta", "synth pad"]))
        if chaos > 0.6:
            chosen_instruments.add(random.choice(self.instrument_families["percussion_unpitched"] + self.instrument_families["electronic"] + self.instrument_families["whimsical"]))
            if random.random() < chaos * 0.5 : chosen_instruments.add(random.choice(self.instrument_families["whimsical"])) # More whimiscal for high chaos
        if energy > 0.6:
            chosen_instruments.add(random.choice(self.instrument_families["percussion_pitched"] + self.instrument_families["brass"]))
        if mystery > 0.6:
            chosen_instruments.add(random.choice(["theremin-like sound", "glass harmonica (effect)", "prepared piano (effect)"]))

        # Extreme whimsical instrumentation for high chaos
        if chaos > 0.85 and random.random() < 0.5: # 50% chance for ALL whimsical if super chaotic
            print("SOUNDSCAPE SYNTH: Engaging extreme whimsical instrumentation!")
            chosen_instruments.clear()
            for _ in range(num_instruments):
                chosen_instruments.add(random.choice(self.instrument_families["whimsical"]))
        elif chaos > 0.7: # Higher chance for at least one whimsical
             if random.random() < 0.6 : chosen_instruments.add(random.choice(self.instrument_families["whimsical"]))


        # Fill remaining slots if not all whimsical takeover
        all_inst_choices = [inst for family_name, family_instruments in self.instrument_families.items() if family_name != "whimsical" for inst in family_instruments]

        # If chosen_instruments is still small (e.g. chaos wasn't high enough for full whimsical)
        # or if it became empty due to clearing for whimsical but then not filling it enough.
        if not chosen_instruments and not all_inst_choices : # prevent infinite loop if all_inst_choices is empty
             chosen_instruments.add(random.choice(self.instrument_families["keyboards"])) # absolute fallback

        while len(chosen_instruments) < num_instruments and all_inst_choices:
            chosen_instruments.add(random.choice(all_inst_choices))

        return list(chosen_instruments)[:num_instruments]

    def _generate_rhythmic_feel(self) -> str:
        chaos = self.mood_vector.get('chaos', 0.0)
        energy = self.mood_vector.get('energy', 0.0)
        serenity = self.mood_vector.get('serenity', 0.0)
        gloom = self.mood_vector.get('gloom', 0.0)

        if chaos > 0.7: return "Highly syncopated, unpredictable, with sudden pauses and bursts of notes."
        if chaos > 0.7: return "Highly syncopated, unpredictable, with notes scattered like confetti in a hurricane and sudden, deafening silences."
        if energy > 0.85: return "A relentlessly driving rhythm, like a caffeinated woodpecker drumming on a rocket."
        elif energy > 0.7: return "Driving and repetitive, possibly with a strong backbeat or ostinato that drills into your soul."
        if serenity > 0.85: return "So smooth and flowing, it's like time itself has dissolved into a gentle sonic river."
        elif serenity > 0.7: return "Smooth, flowing, with long note values and gentle articulations."
        if gloom > 0.85 and serenity > 0.4: return "Excruciatingly slow, sparse, and legato, each note's decay lasting an eternity."
        elif gloom > 0.6 and serenity > 0.4: return "Slow, sparse, and legato, emphasizing long decays."
        if gloom > 0.85: return "Heavy and plodding, like the footsteps of a melancholic giant trudging through molasses."
        elif gloom > 0.6: return "Heavy and plodding, perhaps with emphasis on downbeats."
        if energy > 0.5 and joy > 0.5: return "Bouncy and dance-like, bordering on uncontrollably jubilant."
        return "A mix of simple, straightforward rhythms, occasionally interrupted by a sneeze."

    def _generate_melodic_harmonic_character(self) -> str:
        joy = self.mood_vector.get('joy', 0.0)
        gloom = self.mood_vector.get('gloom', 0.0)
        serenity = self.mood_vector.get('serenity', 0.0)
        chaos = self.mood_vector.get('chaos', 0.0)
        energy = self.mood_vector.get('energy', 0.0)
        mystery = self.mood_vector.get('mystery', 0.0)

        descs = []
        # Melody
        if joy > 0.6: descs.append("Melodies are generally ascending, playful, and ornamented.")
        if gloom > 0.6: descs.append("Melodic lines are often descending, sparse, or fragmented.")
        if serenity > 0.6: descs.append("Smooth, conjunct (stepwise) melodic motion dominates.")
        if chaos > 0.6: descs.append("Features wide, erratic leaps in melody, possibly dissonant intervals.")
        if energy > 0.6: descs.append("Melodies are agile and active, with rapid passages.")
        if mystery > 0.6: descs.append("Melodic lines are questioning, perhaps using microtonal inflections or unusual scales.")

        # Harmony
        if serenity > 0.7 and joy > 0.3: descs.append("Harmony is primarily consonant, with simple, clear chords (triads, sevenths).")
        elif serenity > 0.7: descs.append("Harmony is sparse and open, using sustained tones or simple intervals.")
        if gloom > 0.5: descs.append("Minor key harmony with occasional suspensions or dissonances for expressive effect.")
        if chaos > 0.7: descs.append("Harmony is highly dissonant, featuring tone clusters, polytonality, or no clear harmonic center.")
        if mystery > 0.5: descs.append("Ambiguous harmonies, unresolved chords, or slowly shifting drones create suspense.")

        if not descs: return "Standard melodic and harmonic content."
        return " ".join(random.sample(descs, min(len(descs), 2))) # Pick 1 or 2 characteristics

    def _generate_simple_event_list(self, num_events=8, bpm=120) -> list[str]:
        """Generates a very simple list of musical events (note, duration, instrument)."""
        events = []
        current_time = 0.0
        seconds_per_beat = 60.0 / bpm

        instruments = self._get_instrumentation_description(num_instruments=max(1, int(num_events/3)))
        if not instruments: instruments = ["piano"] # Fallback

        for _ in range(num_events):
            note = random.choice(self.notes) + str(random.choice(self.octaves))
            duration_name = random.choice(self.duration_names)
            duration_beats = self.durations[duration_name]
            instrument = random.choice(instruments)

            # Chaos factor: random rests or very short/long notes
            absurd_detail = ""
            if self.mood_vector.get('chaos', 0.0) > 0.7 and random.random() < 0.3:
                if random.random() < 0.5:
                    note = "REST"
                    absurd_detail = "(a sudden, awkward silence)"
                else: # extreme duration or bizarre instruction
                    duration_name = random.choice(["sixteenth", "whole", "a fleeting moment", "an eternity"])
                    if isinstance(self.durations.get(duration_name), (int,float)):
                        duration_beats = self.durations[duration_name]
                    else: # custom duration string
                        duration_beats = random.uniform(0.1, 4.0) # assign a beat value anyway

                    if random.random() < 0.3: # bizarre instruction
                        absurd_instruction = random.choice([
                            "played with existential dread", "somehow, make it purple",
                            "while juggling teacups", "louder than strictly necessary",
                            "as if tickling a sleeping badger"
                        ])
                        absurd_detail = f"({absurd_instruction})"

            event_time_sec = current_time * seconds_per_beat
            event_string = f"Time: {event_time_sec:.2f}s - Note: {note}, Duration: {duration_name} ({duration_beats:.1f} beats), Instrument: {instrument}"
            if absurd_detail:
                event_string += f" {absurd_detail}"
            events.append(event_string)

            current_time += duration_beats # Simple progression
            if current_time * seconds_per_beat > 15: # Limit to ~15s of "music"
                break
        return events


    def generate_soundscape_description(self, mood_vector: dict) -> dict:
        """
        Generates a textual description of the soundscape.
        """
        self.mood_vector = mood_vector

        tempo_desc, bpm = self._get_tempo_description()
        key_mode_desc = self._get_key_mode_description()
        num_instruments = random.randint(2, 4 + int(self.mood_vector.get('chaos', 0.0)*2))
        instrumentation_desc = self._get_instrumentation_description(num_instruments)
        rhythmic_feel = self._generate_rhythmic_feel()
        melodic_harmonic_char = self._generate_melodic_harmonic_character()

        # Overall texture/dynamics
        texture = "Varied"
        if self.mood_vector.get('serenity',0) > 0.7: texture = "Mostly thin and transparent"
        elif self.mood_vector.get('energy',0) > 0.7: texture = "Often thick and layered"
        elif self.mood_vector.get('chaos',0) > 0.6: texture = "Erratic, shifting from sparse to dense unpredictably"

        dynamics = "Moderate, with some variation."
        if self.mood_vector.get('energy',0) > 0.7 or self.mood_vector.get('joy',0) > 0.7: dynamics = "Generally Loud (Forte) with energetic accents."
        if self.mood_vector.get('gloom',0) > 0.7 or self.mood_vector.get('serenity',0) > 0.7: dynamics = "Generally Quiet (Piano) with subtle swells."
        if self.mood_vector.get('chaos',0) > 0.7: dynamics = "Extreme and sudden shifts in dynamics (subito piano/forte)."


        # Generate a short, conceptual event list
        event_list = self._generate_simple_event_list(num_events=random.randint(5, 10 + int(self.mood_vector.get('energy',0)*5)), bpm=bpm)

        return {
            "title": f"Symphony of {self.mood_vector.get('city', 'Randomness')}",
            "overall_mood": f"A piece reflecting: Joy({self.mood_vector.get('joy',0):.1f}), Gloom({self.mood_vector.get('gloom',0):.1f}), Chaos({self.mood_vector.get('chaos',0):.1f}), Serenity({self.mood_vector.get('serenity',0):.1f}), Energy({self.mood_vector.get('energy',0):.1f}), Mystery({self.mood_vector.get('mystery',0):.1f})",
            "tempo": tempo_desc + f" (approx. {bpm} BPM)",
            "key_mode": key_mode_desc,
            "instrumentation": instrumentation_desc,
            "rhythmic_feel": rhythmic_feel,
            "melodic_harmonic_character": melodic_harmonic_char,
            "texture": texture,
            "dynamics": dynamics,
            "conceptual_event_list": event_list,
            "absurd_annotation": self._get_absurd_annotation()
        }

    def _get_absurd_annotation(self) -> str:
        """Adds a final absurd touch."""
        chaos = self.mood_vector.get('chaos', 0.0)
        mystery = self.mood_vector.get('mystery', 0.0)
        joy = self.mood_vector.get('joy', 0.0)

        options = [
            "May cause spontaneous interpretive dance.",
            "Pairs well with lukewarm tea and existential dread.",
            "Listener may experience a sudden craving for cheese.",
            "The conductor is a sentient garden gnome.",
            "Composed entirely during a lucid dream about flying toast.",
            "Warning: May attract squirrels.",
            "If played backwards, reveals a recipe for invisible scones."
        ]
        if chaos > 0.7: options.append("All musicians are advised to wear helmets.")
        if mystery > 0.7: options.append("The final chord is silent and invisible.")
        if joy > 0.8: options.append("Side effects include uncontrollable giggling.")

        return random.choice(options)

if __name__ == '__main__':
    synth = SoundscapeSynth()

    print("--- Test with a 'Joyful' Mood ---")
    joyful_mood = {
        'chaos': 0.1, 'serenity': 0.7, 'joy': 0.9,
        'gloom': 0.1, 'energy': 0.6, 'mystery': 0.1,
        'city': 'Sunshine City'
    }
    desc_joy = synth.generate_soundscape_description(joyful_mood)
    for k, v in desc_joy.items():
        if k == "conceptual_event_list":
            print(f"  {k}:")
            for event in v[:3]: print(f"    {event}") # Print first 3 events
            if len(v) > 3: print("    ...")
        else:
            print(f"  {k}: {v}")

    print("\n--- Test with a 'Gloomy & Chaotic' Mood ---")
    gloomy_mood = {
        'chaos': 0.8, 'serenity': 0.1, 'joy': 0.1,
        'gloom': 0.9, 'energy': 0.4, 'mystery': 0.7,
        'city': 'Stormville'
    }
    desc_gloom = synth.generate_soundscape_description(gloomy_mood)
    for k, v in desc_gloom.items():
        if k == "conceptual_event_list":
            print(f"  {k}:")
            for event in v[:3]: print(f"    {event}")
            if len(v) > 3: print("    ...")
        else:
            print(f"  {k}: {v}")

    print("\n--- Test with a 'Serene & Mysterious' Mood ---")
    serene_mood = {
        'chaos': 0.1, 'serenity': 0.9, 'joy': 0.2,
        'gloom': 0.2, 'energy': 0.1, 'mystery': 0.8,
        'city': 'Foggy Bottoms'
    }
    desc_serene = synth.generate_soundscape_description(serene_mood)
    for k, v in desc_serene.items():
        if k == "conceptual_event_list":
            print(f"  {k}:")
            for event in v[:3]: print(f"    {event}")
            if len(v) > 3: print("    ...")
        else:
            print(f"  {k}: {v}")
