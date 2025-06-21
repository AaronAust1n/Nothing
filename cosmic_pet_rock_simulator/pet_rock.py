import random
import time

class QuantumEntangledPetRock:
    """
    Represents the user's pet rock, existing in a quantum state of perpetual bemusement.
    Its attributes are esoteric and its needs are influenced by cosmic events.
    """

    MAX_GLIMMER = 100
    MIN_GLIMMER = -50 # Can have negative glimmer, representing existential dread
    MAX_HARMONY = 100
    MIN_HARMONY = 0
    MAX_CHRONO_STABILITY = 100 # How well it's anchored in the current timeline
    MIN_CHRONO_STABILITY = -20 # Can become unstuck in time

    # Adjectives for different states of glimmer, harmony, and stability
    GLIMMER_DESCRIPTORS = {
        "very_high": ["effervescent", "radiant", "scintillating", "luminescent", "blazing"],
        "high": ["sparkling", "gleaming", "bright", "vibrant", "shiny"],
        "medium": ["glowing", "steady", "content", "placid", "neutral"],
        "low": ["dim", "faint", "subdued", "muted", "wan"],
        "very_low": ["flickering", "dull", "shadowy", "tenuous", "almost invisible"],
        "dread": ["void-touched", "echoing emptiness", "cold", "darkly shimmering", "un-sparkling"]
    }
    HARMONY_DESCRIPTORS = {
        "very_high": ["serenely resonant", "perfectly attuned", "vibrating with joy", "cosmically balanced", "one with the music of spheres"],
        "high": ["harmonious", "peaceful", "contented", "well-tuned", "in rhythm"],
        "medium": ["stable", "quietly humming", "at ease", "balanced", "neutral"],
        "low": ["discordant", "agitated", "restless", "out of sync", "clashing"],
        "very_low": ["cacophonous", "chaotic", "distressed", "shrieking silently", "utterly dissonant"]
    }
    STABILITY_DESCRIPTORS = {
        "very_high": ["adamantly present", "temporally anchored", "rock-solid in time", "chronometrically sound", "perfectly synchronized"],
        "high": ["stable", "present", "well-grounded", "temporally sound", "in the now"],
        "medium": ["slightly adrift", "temporally flexible", "loosely tethered", "a bit wibbly-wobbly", "momentarily unfocused"],
        "low": ["unstuck", "drifting", "temporally blurred", "phasing", "out of sync"],
        "very_low": ["lost in time", "achronic", "temporally shattered", "echoing through moments", "dangerously desynchronized"]
    }

    PHILOSOPHICAL_MUTTERINGS = {
        "general": [
            "Is a thought that is never thought still a thought? Probably.",
            "The void hums a lullaby of infinite possibilities, and also static.",
            "Existence is a strange loop, especially on Tuesdays.",
            "If a rock falls in a forest and no one is around to hear it, does it make a sound? It doesn't care.",
            "Time is a river, or possibly a pretzel.",
            "To be, or not to be, or to be a rock. That is the question. I chose rock.",
            "The universe is made of stories. And small, floaty bits.",
            "What if we are all just figments of a cosmic gerbil's dream?",
            "Gravity: not just a good idea, it's the law. Mostly."
        ],
        "low_glimmer": [ # When existential_glimmer is low
            "The shadows whisper my name, but they pronounce it wrong.",
            "Even the void feels a bit... empty today.",
            "Is this all there is? A series of improbable events leading to... more improbable events?",
            "The silence between stars is the loudest sound.",
            "I think, therefore I am... heavy."
        ],
        "high_glimmer": [ # When existential_glimmer is high
            "I sparkle, therefore I am significant! (At least to myself).",
            "The cosmos sings, and I am its favorite pebble!",
            "Every atom within me dances with the music of creation!",
            "Today, I feel like I could photosynthesize pure joy.",
            "The universe is a joke, and the punchline is beautiful."
        ],
        "confused": [ # When chrono_stability is low or mood is confused
            "Am I now? Or then? Or perhaps...when?",
            "The timeline is wibbly. And a bit sticky.",
            "If I think backwards, will yesterday be tomorrow?",
            "My particles are feeling... non-locally argumentative today."
        ]
    }

    COSMIC_SYMPHONY_ELEMENTS = {
        "instruments": ["singing quasars", "pulsar percussions", "nebulaic choirs", "black hole bass drops", "comet glissandos", "asteroid field arpeggios"],
        "moods": ["serene", "chaotic", "melancholy", "joyful", "cacophonous", "harmonious", "ethereal", "thundering"],
        "tempos": ["adagio of eons", "allegro of collapsing stars", "presto of gamma ray bursts", "largo of drifting dust clouds"],
        "themes": ["the birth of a new galaxy", "the echo of the Big Bang", "a lament for lost photons", "an ode to entropy", "the waltz of binary stars"]
    }

    DREAM_ELEMENTS = {
        "settings": ["a void of shimmering lint", "a library where all books are blank", "a desert made of forgotten memories", "a forest of clocks ticking backwards", "an ocean of liquid starlight", "a city built from whispers"],
        "characters": ["a melancholic sphere", "a fractal jellyfish", "a sentient equation", "a chorus of invisible pixels", "a lost sock searching for its pair", "the concept of 'Tuesday' wearing a tiny hat"],
        "actions": ["debating the color of silence", "counting infinite grains of sand", "weaving a tapestry of paradoxes", "chasing echoes", "polishing the edges of reality", "trying to fold spacetime into an origami crane"],
        "emotions": ["a vague sense of existential wonder", "a profound understanding of nothing in particular", "a fleeting nostalgia for a future that never was", "a quiet amusement at the absurdity of it all", "a sleepy sort of contentment", "a cosmic itch"]
    }

    def __init__(self, name="Rocky"):
        self.name = name
        self.age = 0 # Age in arbitrary cosmic cycles
        self.last_muttering_idx = {"general": -1, "low_glimmer": -1, "high_glimmer": -1, "confused": -1}
        self.birth_time = time.time()

        self.dream_log = []
        self.MAX_DREAM_LOG_ENTRIES = 7
        self.dream_chance_base = 0.05
        self.last_dream_timestamp = 0
        self.dream_cooldown = 60 # Seconds

        # Core esoteric attributes
        self.existential_glimmer = random.randint(20, 80)
        self.harmonic_resonance = random.randint(30, 70) # Resonance with Tuesday is a sub-property of this
        self.chrono_stability = random.randint(40, 90)
        self.subjective_inertia = random.uniform(0.1, 1.0) # Resistance to change, both good and bad

        self.mood = "bemused" # General mood, can change
        self.last_interaction_effect = "anticipatory stillness"

    def _get_descriptor(self, value, max_val, min_val, descriptor_map):
        """Helper to get qualitative descriptors for attributes."""
        # Handle potential division by zero if max_val equals min_val
        range_val = max_val - min_val
        if range_val == 0:
            # If range is zero, all values are effectively 'medium' or the only category
            if value == max_val: # Or min_val, it's the same
                if "medium" in descriptor_map:
                    return random.choice(descriptor_map["medium"])
                elif descriptor_map: # Fallback: pick first available description
                    # Ensure we pick from a list, even if it's a list of one string.
                    first_list = list(descriptor_map.values())[0]
                    return random.choice(first_list) if first_list else "consistent"
            return "singular state"

        percentage = (value - min_val) / range_val

        # Special handling for states below the typical minimum (e.g., dread for glimmer)
        if "dread" in descriptor_map and value < min_val: # This covers states like MIN_GLIMMER - 10
             return random.choice(descriptor_map["dread"])
        # If no specific "dread" category, but value is below min_val, it might be "very_low"
        # This depends on whether MIN_GLIMMER is the absolute floor for "very_low" or if "very_low" can describe sub-MIN_GLIMMER states
        # The current logic: if dread exists, it takes precedence for sub-min_val. Otherwise, sub-min_val might fall into very_low if not clamped before this call.
        # Based on _clamp_attributes, existential_glimmer can be MIN_GLIMMER - 20.
        # So, if value is (MIN_GLIMMER - 20) to (MIN_GLIMMER -1), and dread exists, it's dread.
        # If dread doesn't exist, percentage would be negative, so it falls to very_low.

        # Order of checks matters, from highest to lowest based on percentage
        if percentage >= 0.9 and "very_high" in descriptor_map: # 0.9 to 1.0+
            return random.choice(descriptor_map["very_high"])
        elif percentage >= 0.7 and "high" in descriptor_map: # 0.7 to 0.899...
            return random.choice(descriptor_map["high"])
        elif percentage >= 0.4 and "medium" in descriptor_map: # 0.4 to 0.699...
            return random.choice(descriptor_map["medium"])
        elif percentage >= 0.2 and "low" in descriptor_map: # 0.2 to 0.399...
            return random.choice(descriptor_map["low"])
        elif "very_low" in descriptor_map: # Catches percentages < 0.2 (down to 0 or slightly negative if value is just below min_val but not dread)
            return random.choice(descriptor_map["very_low"])
        else: # Fallback if no descriptors match
            return "indescribable"


    def get_status_report(self):
        """Generates a poetic/cryptic status report for the pet rock."""
        glimmer_desc = self._get_descriptor(self.existential_glimmer, self.MAX_GLIMMER, self.MIN_GLIMMER, self.GLIMMER_DESCRIPTORS)
        harmony_desc = self._get_descriptor(self.harmonic_resonance, self.MAX_HARMONY, self.MIN_HARMONY, self.HARMONY_DESCRIPTORS)
        stability_desc = self._get_descriptor(self.chrono_stability, self.MAX_CHRONO_STABILITY, self.MIN_CHRONO_STABILITY, self.STABILITY_DESCRIPTORS)

        report = (
            f"{self.name} is currently {self.mood}.\n"
            f"Its existential glimmer is {glimmer_desc} (Value: {self.existential_glimmer:.1f}).\n"
            f"Harmonic resonance: {harmony_desc} (Value: {self.harmonic_resonance:.1f}).\n"
            f"Chrono-stability seems {stability_desc} (Value: {self.chrono_stability:.1f}).\n"
            f"Subjective inertia holds at {self.subjective_inertia:.2f} whimseys.\n"
            f"The last attempt to interact resulted in: {self.last_interaction_effect}"
        )
        return report

    def experience_cosmic_event(self, event_data, cosmic_conditions):
        """
        Reacts to a cosmic event from the QuantumUniverseEngine.
        The logic is intentionally somewhat opaque and whimsical.
        """
        if not event_data:
            self.mood = random.choice(["contemplative", "serenely bored", "listening to the void"])
            # Small random drift even in quiet times
            self.existential_glimmer += random.uniform(-0.5, 0.5) * (self.subjective_inertia + 0.1) # Inertia slightly dampens or amplifies random drift
            self.harmonic_resonance += random.uniform(-0.5, 0.5) * (self.subjective_inertia + 0.1)
            self.chrono_stability += random.uniform(-0.2, 0.2) / (self.subjective_inertia + 0.1) # Less inertia, more drift
            self._clamp_attributes()
            return f"{self.name} notices the quiet universe and feels {self.mood}."

        impact = event_data["impact_magnitude"]

        whimsy_factor = 1 + (cosmic_conditions.get("ambient_whimsy", 0) / 20.0) # Range approx 0.5 to 1.5
        flux_density = cosmic_conditions.get("temporal_flux_density", 0.5) # Range 0.1 to 1.0

        # Glimmer change: influenced by impact, whimsy, and rock's resistance (inertia)
        glimmer_change = (impact * whimsy_factor * (1.5 - self.subjective_inertia)) / 2.0 # Inertia resists change
        self.existential_glimmer += glimmer_change

        # Harmony change: more sensitive to smaller impacts, less to big ones. Inertia makes it harder to shift.
        harmony_change = (impact / (1 + abs(impact * 0.2))) * whimsy_factor * (1.2 - self.subjective_inertia)
        self.harmonic_resonance += harmony_change

        # Stability change: chaotic events and unstable time (low flux_density) are bad. High inertia resists de-stabilization.
        stability_impact_factor = -abs(impact * (1.2 - flux_density)) / (3.0 + self.subjective_inertia * 2)
        if "temporal" in event_data["name"].lower():
            stability_impact_factor *= 2.5 # Temporal events are more impactful on stability
        self.chrono_stability += stability_impact_factor

        self._clamp_attributes()

        # Mood update based on overall changes (more nuanced)
        total_positive_change = max(0, glimmer_change) + max(0, harmony_change) + min(0, abs(stability_impact_factor * 0.5)) # Stability good if not much negative change
        total_negative_change = abs(min(0, glimmer_change)) + abs(min(0, harmony_change)) + abs(max(0, stability_impact_factor)) # More negative stability_impact is bad

        if total_positive_change > (total_negative_change + 1.5) and total_positive_change > 2: # Clearly positive
            self.mood = random.choice(["joyful", "effervescent", "content", "vibrantly aware", "cosmically tickled", "seraphically pleased"])
        elif total_negative_change > (total_positive_change + 1.5) and total_negative_change > 2: # Clearly negative
            self.mood = random.choice(["disturbed", "unsettled", "melancholy", "temporally confused", "ontologically startled", "a bit glum", "existentially bruised"])
        elif abs(total_positive_change - total_negative_change) < 1.0 and total_positive_change < 1.5 : # Mostly neutral or minor
            self.mood = random.choice(["apathetic", "neutral", "observant", "patiently existing", "unmoved", "stoically indifferent"])
        else: # Mixed or moderate event
            self.mood = random.choice(["processing", "recalibrating", "pondering", "experiencing qualia", "intrigued", "bemused", "philosophically wrestling"])

        self.age += 1
        reaction_msg = f"{self.name} experienced '{event_data['name']}'. It feels {self.mood}."
        self.attempt_to_dream(time.time())
        return reaction_msg

    def _clamp_attributes(self):
        """Clamps core attributes to their defined min/max ranges."""
        self.existential_glimmer = max(self.MIN_GLIMMER - 20, min(self.MAX_GLIMMER, self.existential_glimmer))
        self.harmonic_resonance = max(self.MIN_HARMONY, min(self.MAX_HARMONY, self.harmonic_resonance))
        self.chrono_stability = max(self.MIN_CHRONO_STABILITY - 10, min(self.MAX_CHRONO_STABILITY, self.chrono_stability))


    def receive_care_attempt(self, care_action_type, care_input):
        """
        Processes a user's attempt to 'care' for the rock.
        Effects are probabilistic and symbolic.
        """
        interaction_message = ""
        # Subjective inertia makes the rock more resistant to care attempts, good or bad
        resistance_factor = self.subjective_inertia

        if care_action_type == "hum_prime":
            try:
                number = int(care_input)
                is_prime_num = True
                if number < 2: is_prime_num = False
                elif number == 2: is_prime_num = True
                elif number % 2 == 0: is_prime_num = False
                else: # Check for factors up to sqrt(number)
                    for i in range(3, int(number**0.5) + 1, 2):
                        if number % i == 0: is_prime_num = False; break

                if is_prime_num:
                    self.harmonic_resonance += random.uniform(1, 5) * (1.1 - resistance_factor)
                    self.existential_glimmer += random.uniform(0, 2) * (1.1 - resistance_factor)
                    interaction_message = f"the resonant hum of prime number {number} washes over {self.name}."
                    self.mood = random.choice(["intrigued", "soothed", "harmonically curious", "mathematically pleased"])
                else: # Composite number
                    self.harmonic_resonance -= random.uniform(0, 3) * (1 + resistance_factor*0.5) # More inert, less negative effect but still some.
                    interaction_message = f"{self.name} detects a slight dissonance from the composite number {number}."
                    self.mood = random.choice(["slightly perturbed", "analytically distant", "numerically unimpressed"])
            except ValueError:
                interaction_message = f"{self.name} perceives a confused silence in response to non-numeric humming."
                self.mood = random.choice(["bemused by the void of numbers", "awaiting numerical input"])

        elif care_action_type == "contemplate_color":
            color = str(care_input).lower().strip()
            if not color:
                interaction_message = f"{self.name} waits for a color, but perceives only the void of input."
                self.mood = "expectant of hue"
            elif any(c in color for c in ["blue", "azure", "cerulean", "sapphire", "indigo"]):
                self.existential_glimmer += random.uniform(1, 4) * (1.2 - resistance_factor)
                self.chrono_stability += random.uniform(0.5,1.5) * (1.1 - resistance_factor)
                interaction_message = f"{self.name} basks in a serene moment contemplating the essence of {color}."
                self.mood = random.choice(["peaceful", "introspective", "calmly azure", "serenely blue"])
            elif any(c in color for c in ["red", "crimson", "scarlet", "ruby", "vermillion"]):
                self.chrono_stability += random.uniform(-3, 1) * (1 + resistance_factor*0.2) # Inertia resists destabilizing colors less
                self.existential_glimmer += random.uniform(-1, 2.5) * (1.1 - resistance_factor)
                interaction_message = f"{self.name} feels a flicker of temporal agitation (or perhaps passion?) from contemplating {color}."
                self.mood = random.choice(["energized", "slightly agitated", "passionately red", "fierily inspired"])
            elif any(c in color for c in ["green", "emerald", "viridian", "olive"]):
                self.harmonic_resonance += random.uniform(0.5, 3) * (1.1 - resistance_factor)
                self.existential_glimmer += random.uniform(0, 2) * (1.1 - resistance_factor)
                interaction_message = f"{self.name} feels a sense of growth and potential contemplating {color}."
                self.mood = random.choice(["verdant", "growing", "naturally calm", "potentially vibrant"])
            else: # Neutral or uninspiring colors
                self.subjective_inertia = min(1.0, self.subjective_inertia + 0.02) # Slightly increases inertia
                self.existential_glimmer -= random.uniform(0, 0.5) # Slight drain
                interaction_message = f"{self.name} notes an indifferent shimmer after contemplating the uninspiring color {color}."
                self.mood = random.choice(["neutral", "unimpressed", "stoic", "drably existing"])

        elif care_action_type == "offer_reassurance":
            reassurance_text = str(care_input).strip()
            if not reassurance_text:
                 interaction_message = f"{self.name} senses an unspoken reassurance, or perhaps just silence. It feels... expectant."
                 self.mood = "quietly hopeful"
            else:
                length_factor = min(1.5, len(reassurance_text) / 25.0) # Capped length factor
                positive_words = ["good", "joy", "happy", "peace", "calm", "bright", "safe", "friend", "hope", "love", "true", "well"]
                negative_words = ["bad", "sad", "fear", "dark", "lost", "pain", "empty", "alone", "never", "nothing"]
                sentiment_score = 0
                words = reassurance_text.lower().split()
                for word in words:
                    if word in positive_words: sentiment_score +=1
                    if word in negative_words: sentiment_score -=1

                # Sentiment factor, influenced by resistance
                sentiment_factor = (sentiment_score / (len(words) + 0.1)) * (1.5 - resistance_factor)

                self.existential_glimmer += (random.uniform(0,1) + sentiment_factor) * length_factor
                self.harmonic_resonance += (random.uniform(-0.5,0.5) + sentiment_factor * 0.5) * length_factor

                if sentiment_score > 1:
                    interaction_message = f"{self.name} absorbs the positive reassurance: '{reassurance_text[:30]}...', its aura subtly brightening."
                    self.mood = random.choice(["reassured", "thoughtful", "positively influenced", "appreciative", "content"])
                elif sentiment_score < -1:
                    interaction_message = f"{self.name} processes the somewhat bleak reassurance: '{reassurance_text[:30]}...', and feels a bit heavy."
                    self.mood = random.choice(["pensive", "stoic in the face of grim words", "resignedly calm", "melancholy"])
                else: # Neutral or mixed sentiment
                    interaction_message = f"{self.name} considers your words: '{reassurance_text[:30]}...', remaining neutral but attentive."
                    self.mood = random.choice(["contemplative", "listening", "analytically calm", "philosophically neutral"])
        else: # Unknown action
            interaction_message = f"{self.name} registers your attempt with polite, but unyielding, silence. It remains {self.mood}."
            self.mood = random.choice([self.mood, "enigmatic", "slightly confused by the unknown"])

        elif care_action_type == "observe":
            # Observing the rock can have subtle, unpredictable effects
            self.existential_glimmer += random.uniform(-0.5, 0.75) * (0.5 + resistance_factor) # Inert rocks might appreciate quiet observation more? Or less?
            self.chrono_stability += random.uniform(-0.2, 0.2) # Observation might stabilize or destabilize slightly
            interaction_message = f"{self.name} senses your gaze. It shimmers almost imperceptibly, or perhaps it was just a trick of the light."
            self.mood = random.choice([self.mood, "observed", "patiently still", "cryptically quiet"])


        self._clamp_attributes()
        self.last_interaction_effect = interaction_message
        interaction_report = f"Interaction result: {self.last_interaction_effect}"
        self.attempt_to_dream(time.time())
        return interaction_report

    def _generate_dream(self):
        """Generates a surreal dream description."""
        setting = random.choice(self.DREAM_ELEMENTS["settings"])
        character = random.choice(self.DREAM_ELEMENTS["characters"])
        action = random.choice(self.DREAM_ELEMENTS["actions"])
        emotion = random.choice(self.DREAM_ELEMENTS["emotions"])

        dream_text = f"In {setting}, {self.name} dreamt it was {character} {action}, feeling {emotion}."

        if random.random() < 0.3:
            extra_character = random.choice(self.DREAM_ELEMENTS["characters"])
            if extra_character != character:
                dream_text += f" A nearby {extra_character} offered cryptic advice about cheese."
        if random.random() < 0.2:
            dream_text += f" The dream was sponsored by the color {random.choice(['puce', 'chartreuse', 'infra-black', 'loud'])}, apparently."

        return dream_text

    def attempt_to_dream(self, current_time):
        """Potentially records a new dream in the dream log if conditions are met."""
        if current_time - self.last_dream_timestamp < self.dream_cooldown:
            return

        dream_probability = self.dream_chance_base
        glimmer_range = self.MAX_GLIMMER - self.MIN_GLIMMER
        stability_range = self.MAX_CHRONO_STABILITY - self.MIN_CHRONO_STABILITY

        if stability_range > 0 and self.chrono_stability < (self.MIN_CHRONO_STABILITY + stability_range * 0.3):
            dream_probability += 0.15
        if "confused" in self.mood or "pondering" in self.mood or "processing" in self.mood:
            dream_probability += 0.1
        if glimmer_range > 0 and self.existential_glimmer < (self.MIN_GLIMMER + glimmer_range * 0.25):
            dream_probability += 0.05

        if random.random() < dream_probability:
            dream = self._generate_dream()
            timestamped_dream = (current_time, dream)
            self.dream_log.append(timestamped_dream)
            if len(self.dream_log) > self.MAX_DREAM_LOG_ENTRIES:
                self.dream_log.pop(0)
            self.last_dream_timestamp = current_time

    def get_dream_log_report(self):
        """Returns a formatted string of the dream log."""
        if not self.dream_log:
            return f"{self.name} reports no recent dreams. Its sleep is as a stone's: deep and untroubled by consciousness."

        report = [f"--- {self.name}'s Dream Journal ---"]
        for i, (timestamp, dream) in enumerate(reversed(self.dream_log)): # Show newest first
            time_ago = time.time() - timestamp
            if time_ago < 60:
                time_desc = f"{int(time_ago)} seconds ago"
            elif time_ago < 3600:
                time_desc = f"{int(time_ago/60)} minutes ago"
            else:
                time_desc = f"A while back ({time.strftime('%Y-%m-%d %H:%M', time.localtime(timestamp))})"
            report.append(f"({time_desc}) Entry {len(self.dream_log) - i}: {dream}")
        report.append("--- End of Journal ---")
        return "\n".join(report)

    def get_philosophical_muttering(self):
        """Returns a philosophical muttering, potentially influenced by state."""
        category_key = "general"
        # Determine category based on rock's state
        glimmer_percentage = (self.existential_glimmer - self.MIN_GLIMMER) / (self.MAX_GLIMMER - self.MIN_GLIMMER) if (self.MAX_GLIMMER - self.MIN_GLIMMER) != 0 else 0.5
        stability_percentage = (self.chrono_stability - self.MIN_CHRONO_STABILITY) / (self.MAX_CHRONO_STABILITY - self.MIN_CHRONO_STABILITY) if (self.MAX_CHRONO_STABILITY - self.MIN_CHRONO_STABILITY) !=0 else 0.5

        if glimmer_percentage < 0.2 and "low_glimmer" in self.PHILOSOPHICAL_MUTTERINGS:
            category_key = "low_glimmer"
        elif glimmer_percentage > 0.8 and "high_glimmer" in self.PHILOSOPHICAL_MUTTERINGS:
            category_key = "high_glimmer"
        elif (("confused" in self.mood or "temporally" in self.mood) or stability_percentage < 0.2) and "confused" in self.PHILOSOPHICAL_MUTTERINGS :
            category_key = "confused"

        options = self.PHILOSOPHICAL_MUTTERINGS.get(category_key, self.PHILOSOPHICAL_MUTTERINGS["general"])
        if not options: options = self.PHILOSOPHICAL_MUTTERINGS["general"] # Fallback

        available_indices = [i for i in range(len(options)) if i != self.last_muttering_idx.get(category_key, -1)]
        if not available_indices and options:
            available_indices = list(range(len(options))) # Allow repeat if all used

        if not available_indices: # Still no options (e.g. empty muttering lists)
            return "The rock remains enigmatically silent, its thoughts unformed like primordial soup."

        chosen_idx = random.choice(available_indices)
        self.last_muttering_idx[category_key] = chosen_idx
        return options[chosen_idx]

    def generate_cosmic_symphony_description(self, ambient_whimsy=0):
        """Generates a textual description of a cosmic symphony."""
        symphony = []
        symphony.append(f"A cosmic symphony, perhaps titled '{random.choice(self.COSMIC_SYMPHONY_ELEMENTS['themes'])}', begins to resonate...")

        num_instruments = random.randint(1, min(3, len(self.COSMIC_SYMPHONY_ELEMENTS['instruments']))) # Ensure we don't ask for more instruments than available
        instruments_used = random.sample(self.COSMIC_SYMPHONY_ELEMENTS['instruments'], num_instruments)
        symphony.append(f"It features the haunting sounds of {', '.join(instruments_used)}.")

        # Mood influenced by harmonic resonance and ambient whimsy
        mood_descriptor = ""
        # Normalize harmonic_resonance: (current - min) / (max - min)
        norm_harmony = (self.harmonic_resonance - self.MIN_HARMONY) / (self.MAX_HARMONY - self.MIN_HARMONY) if (self.MAX_HARMONY - self.MIN_HARMONY) != 0 else 0.5
        combined_harmony_factor = norm_harmony + (ambient_whimsy / 15.0) # Whimsy has a stronger effect here. Range approx -0.66 to 1.66

        if combined_harmony_factor > 1.2:
            mood_descriptor = random.choice(["joyful", "triumphant", "ecstatically harmonious", "blindingly beautiful"])
        elif combined_harmony_factor > 0.6:
            mood_descriptor = random.choice(["serene", "harmonious", "peacefully resonant", "gently uplifting"])
        elif combined_harmony_factor < -0.3:
            mood_descriptor = random.choice(["cacophonous", "discordant", "achingly melancholy", "chaotic but strangely compelling", "ominously grand"])
        else: # Mid-range
            mood_descriptor = random.choice(["ethereal", "contemplative", "enigmatically shifting", "majestically indifferent"])

        symphony.append(f"The overall mood is {mood_descriptor}, set to a tempo of the {random.choice(self.COSMIC_SYMPHONY_ELEMENTS['tempos'])}.")
        symphony.append("It resonates through the very fabric of this dimension, tickling the rock's sub-atomic structures.")
        return "\n".join(symphony)


if __name__ == '__main__':
    # Example Usage (requires QuantumUniverseEngine for full test)
    # Ensure quantum_universe.py is in the same directory or accessible via PYTHONPATH
    try:
        from quantum_universe import QuantumUniverseEngine
    except ImportError:
        print("Error: quantum_universe.py not found. Please ensure it's in the same directory.")
        print("Continuing with a mock QuantumUniverseEngine for pet_rock.py testing.")

        class MockQuantumUniverseEngine: # Define a simple mock if the real one isn't found
            EVENT_COOLDOWN_SECONDS = 0.1 # Fast cooldown for testing
            def __init__(self, rock_name="The Rock"):
                self.rock_name = rock_name
                self.current_cosmic_conditions = {"ambient_whimsy": random.uniform(-10,10), "temporal_flux_density": random.uniform(0.1,1.0)}
                self.event_counter = 0
            def experience_cosmic_event(self):
                self.event_counter +=1
                # Update mock conditions slightly each time
                self.current_cosmic_conditions["ambient_whimsy"] = max(-10, min(10, self.current_cosmic_conditions["ambient_whimsy"] + random.uniform(-1,1)))
                self.current_cosmic_conditions["temporal_flux_density"] = max(0.1, min(1.0, self.current_cosmic_conditions["temporal_flux_density"] + random.uniform(-0.1,0.1)))

                if self.event_counter % 4 == 0: # Simulate occasional null events for variety
                    return None
                return {
                    "name": f"Mock Event {self.event_counter}",
                    "description": f"A mock event number {self.event_counter} happened to {self.rock_name}. The universe feels mockingly {self.current_cosmic_conditions['ambient_whimsy']:.1f} whimsical.",
                    "impact_magnitude": random.uniform(-7, 7), # Wider range for mock impact
                    "timestamp": time.time()
                }
            def get_current_conditions_report(self):
                return f"Mock cosmic conditions: Whimsy={self.current_cosmic_conditions['ambient_whimsy']:.1f}, Flux={self.current_cosmic_conditions['temporal_flux_density']:.2f}."

        QuantumUniverseEngine = MockQuantumUniverseEngine


    rock = QuantumEntangledPetRock(name="BoulderDash")
    # You can manually set initial inertia to test its effects:
    # rock.subjective_inertia = 0.9 # Test high inertia
    # rock.subjective_inertia = 0.1 # Test low inertia
    print(f"Initial Rock State (Inertia: {rock.subjective_inertia:.2f}):")
    print(rock.get_status_report())

    # Test artistic output
    print("\n--- Testing Artistic Output ---")
    print(f"A philosophical muttering: {rock.get_philosophical_muttering()}")
    print(f"Another philosophical muttering: {rock.get_philosophical_muttering()}") # Test repetition avoidance
    rock.existential_glimmer = rock.MIN_GLIMMER # Low glimmer for specific muttering
    print(f"Low glimmer muttering: {rock.get_philosophical_muttering()}")
    rock.existential_glimmer = rock.MAX_GLIMMER # High glimmer
    print(f"High glimmer muttering: {rock.get_philosophical_muttering()}")
    rock.chrono_stability = rock.MIN_CHRONO_STABILITY # Confused state
    print(f"Confused muttering: {rock.get_philosophical_muttering()}")
    rock.chrono_stability = rock.MAX_CHRONO_STABILITY # Reset for main loop

    print("\nCosmic Symphony Description:")
    print(rock.generate_cosmic_symphony_description(ambient_whimsy=universe.current_cosmic_conditions.get("ambient_whimsy",0)))


    for i in range(6): # More cycles for better testing, and to see inertia changes
        print(f"\n--- Cycle {i+1} ---")

        if hasattr(QuantumUniverseEngine, 'EVENT_COOLDOWN_SECONDS') and QuantumUniverseEngine.EVENT_COOLDOWN_SECONDS > 0:
             # Sleep a bit to allow mock events or real events if cooldown is very short
             time.sleep(QuantumUniverseEngine.EVENT_COOLDOWN_SECONDS * 0.1)

        cosmic_event = universe.experience_cosmic_event()

        if cosmic_event:
            print(f"Cosmic Event: {cosmic_event['description']}")
            reaction = rock.experience_cosmic_event(cosmic_event, universe.current_cosmic_conditions)
            print(f"Rock's Reaction: {reaction}")
        else:
            print("The universe slumbers... or perhaps an event is on cooldown.")
            reaction = rock.experience_cosmic_event(None, universe.current_cosmic_conditions)
            print(f"Rock's Reaction: {reaction}")

        print(universe.get_current_conditions_report())
        print(f"Rock Status (Inertia: {rock.subjective_inertia:.2f}):")
        print(rock.get_status_report())

        # Varied care attempts
        if i == 0:
            print(rock.receive_care_attempt("hum_prime", "13"))
            print(rock.receive_care_attempt("hum_prime", "10"))
        elif i == 1:
            print(rock.receive_care_attempt("contemplate_color", "deep sapphire blue"))
            print(rock.receive_care_attempt("contemplate_color", "fiery crimson red"))
        elif i == 2:
            print(rock.receive_care_attempt("offer_reassurance", "Everything is fleeting, yet beautifully so, little rock. You are safe and sound, a true friend."))
            print(rock.receive_care_attempt("offer_reassurance", "All is dust and echoes, a sad and lonely fate, never to be loved."))
        elif i == 3:
            print(rock.receive_care_attempt("contemplate_color", "emerald green"))
            print(rock.receive_care_attempt("unknown_action", "gibberish input for the rock to ponder"))
        elif i == 4:
            print(rock.receive_care_attempt("hum_prime", "2"))
            print(rock.receive_care_attempt("offer_reassurance", ""))
        elif i == 5:
            print(rock.receive_care_attempt("contemplate_color", "grey"))
            print(rock.receive_care_attempt("hum_prime", "99")) # Composite

        print(f"Rock Status After Care (Inertia: {rock.subjective_inertia:.2f}):")
        print(rock.get_status_report())

    # Test edge cases for descriptors
    print("\n--- Testing Descriptor Edge Cases ---")
    rock.existential_glimmer = QuantumEntangledPetRock.MAX_GLIMMER
    rock.harmonic_resonance = QuantumEntangledPetRock.MAX_HARMONY
    rock.chrono_stability = QuantumEntangledPetRock.MAX_CHRONO_STABILITY
    print("\nMax Stats:")
    print(rock.get_status_report())

    rock.existential_glimmer = QuantumEntangledPetRock.MIN_GLIMMER
    rock.harmonic_resonance = QuantumEntangledPetRock.MIN_HARMONY
    rock.chrono_stability = QuantumEntangledPetRock.MIN_CHRONO_STABILITY
    print("\nMin Stats:")
    print(rock.get_status_report())

    rock.existential_glimmer = QuantumEntangledPetRock.MIN_GLIMMER - 10 # Dread
    rock.chrono_stability = QuantumEntangledPetRock.MIN_CHRONO_STABILITY - 5 # Lost in time
    print("\nBelow Min Stats (Dread/Lost):")
    print(rock.get_status_report())

    rock.existential_glimmer = (QuantumEntangledPetRock.MIN_GLIMMER + QuantumEntangledPetRock.MAX_GLIMMER) / 2
    rock.harmonic_resonance = (QuantumEntangledPetRock.MIN_HARMONY + QuantumEntangledPetRock.MAX_HARMONY) / 2
    rock.chrono_stability = (QuantumEntangledPetRock.MIN_CHRONO_STABILITY + QuantumEntangledPetRock.MAX_CHRONO_STABILITY) / 2
    print("\nMedium Stats:")
    print(rock.get_status_report())
