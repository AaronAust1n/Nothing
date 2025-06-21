import random
import time

class QuantumUniverseEngine:
    """
    Simulates a pocket dimension of whimsy, generating unpredictable cosmic events
    that influence the QuantumEntangledPetRock.
    """

    COSMIC_EVENT_CATALOG = [
        # Event Name, Base Impact (on a scale of -10 to 10), Description Template
        ("Nebula Noodle Nibbling", 5, "A school of cosmic noodles has gently nibbled on the fabric of spacetime near {rock_name}."),
        ("Quasar Quinceañera", 7, "The nearby quasar, XR-7Z, is celebrating its 15-billion-year Quinceañera. Confetti made of pure energy rains down on {rock_name}."),
        ("Black Hole Burping Contest", -3, "The supermassive black hole at the dimension's center just won a burping contest. {rock_name} shivers from the gravitational indigestion."),
        ("Temporal Tide Shift", 0, "The temporal tides are shifting. {rock_name} seems momentarily out of sync with the present."),
        ("Whispers from Beyond the Veil", 2, "Incomprehensible whispers echo from beyond the dimensional veil, tickling {rock_name}'s quantum awareness."),
        ("Spontaneous Generation of Lost Socks", 1, "A flurry of mismatched socks spontaneously materializes around {rock_name}, then vanishes. The universe feels slightly more chaotic."),
        ("The Great Attractor's Annual Picnic", 8, "The Great Attractor is having its annual picnic. {rock_name} basks in the distant glow of cosmic bonhomie and gravy anomalies."),
        ("Stray Cosmic Ray Tickle", 3, "A stray cosmic ray, probably looking for the bathroom, tickles {rock_name}'s atomic structure."),
        ("Subspace Serenade", 4, "A pod of subspace whales is serenading the local cluster. {rock_name} vibrates with faint, melodic tunes."),
        ("Dark Matter Disco Party", -2, "The local dark matter is throwing a disco party. The rhythmic thumping is giving {rock_name} a slight headache."),
        ("Reality Readjustment Hiccup", -1, "The universe experienced a minor reality readjustment hiccup. {rock_name} briefly flickered out of existence, but it's probably fine."),
        ("Galactic Gumdrop Shower", 6, "A galactic cloud of pure sugar has condensed, showering {rock_name} with ethereal gumdrops."),
        ("Zero-Point Energy Fluctuation Fizz", 0, "The zero-point energy field is fizzing like cosmic champagne. {rock_name} feels... bubbly."),
        ("Cosmic Bureaucracy Audit", -5, "Auditors from the Cosmic Bureaucracy are performing a routine check of this dimension. {rock_name} feels scrutinized."),
        ("Multiverse Mumble Marathon", -1, "The multiverse is mumbling in its sleep again. {rock_name} is trying to ignore the incoherent ramblings.")
    ]

    LAST_EVENT_TIMESTAMP = 0
    EVENT_COOLDOWN_SECONDS = 10 # Minimum time between events
    MAX_HISTORICAL_EVENTS = 10 # Max number of events to keep in history

    def __init__(self, rock_name="The Rock"):
        self.rock_name = rock_name
        self.event_history = []
        self.current_cosmic_conditions = {
            "ambient_whimsy": 0, # General mood of the universe
            "temporal_flux_density": 0.5 # How stable is time?
        }

    def _generate_random_event(self):
        """Selects and formats a random cosmic event."""
        event_name, base_impact, description_template = random.choice(self.COSMIC_EVENT_CATALOG)

        # Introduce slight randomness to impact
        actual_impact = base_impact + random.uniform(-1.5, 1.5)

        # Personalize description
        description = description_template.format(rock_name=self.rock_name)

        return {
            "name": event_name,
            "description": description,
            "impact_magnitude": actual_impact, # This will be interpreted by the Pet Rock
            "timestamp": time.time()
        }

    def experience_cosmic_event(self):
        """
        Generates a new cosmic event if enough time has passed.
        Updates ambient cosmic conditions.
        """
        current_time = time.time()
        if current_time - self.LAST_EVENT_TIMESTAMP < self.EVENT_COOLDOWN_SECONDS:
            return None # Too soon for another event

        event = self._generate_random_event()
        self.LAST_EVENT_TIMESTAMP = event["timestamp"]

        # Update ambient conditions based on the event (in a nonsensical way)
        self.current_cosmic_conditions["ambient_whimsy"] += event["impact_magnitude"] * 0.1
        self.current_cosmic_conditions["ambient_whimsy"] = max(-10, min(10, self.current_cosmic_conditions["ambient_whimsy"])) # Clamp

        self.current_cosmic_conditions["temporal_flux_density"] += random.uniform(-0.2, 0.2)
        self.current_cosmic_conditions["temporal_flux_density"] = max(0.1, min(1.0, self.current_cosmic_conditions["temporal_flux_density"]))

        if event:
            event_summary = {
                "name": event["name"],
                "timestamp": event["timestamp"],
                "reported_impact": f"{event['impact_magnitude']:.2f} units of undefined cosmic force",
                "historical_note": self._generate_historical_note(event)
            }
            self.event_history.append(event_summary)
            if len(self.event_history) > self.MAX_HISTORICAL_EVENTS:
                self.event_history.pop(0)

        return event

    def _generate_historical_note(self, event_data):
        """Generates a cryptic historical note for an event."""
        notes = [
            "Its echoes are still felt in the sub-etheric resonances.",
            "This event is noted in the lost chronicles of Xylos.",
            "A temporal distortion of 0.003 picoseconds was later attributed to this.",
            "The Council of Custodians debated this for three millennia and reached no conclusion.",
            "Considered a minor precursor to the Great Unraveling of the 7th Epoch (or possibly just a Tuesday).",
            "Triggered a wave of existential poetry in Dimension 4.7-beta.",
            "Caused the price of primordial soup futures to fluctuate wildly.",
            "Subsequent divinations revealed its true meaning remains stubbornly opaque."
        ]
        if "Nebula" in event_data["name"] or "Quasar" in event_data["name"]:
            notes.append("Stargazers still speak of the colors it painted on the void.")
        if abs(event_data["impact_magnitude"]) > 6: # Check if impact_magnitude exists
            notes.append("A truly momentous occasion, or perhaps a statistical anomaly.")

        return random.choice(notes)

    def get_historical_archive_report(self):
        """Returns a formatted string of the event history."""
        if not self.event_history:
            return "The annals of the universe are curiously blank regarding recent noteworthy events. A sign of peace, or the calm before a cosmic storm?"

        report = ["--- The Universal Archives: Recent Cosmic Phenomena ---"]
        for i, entry in enumerate(reversed(self.event_history)):
            time_obj = time.localtime(entry["timestamp"])
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_obj)
            report.append(f"Record {len(self.event_history) - i} (Stardate {time_str}):")
            report.append(f"  Event: {entry['name']}")
            report.append(f"  Impact: {entry['reported_impact']}")
            report.append(f"  Archival Note: {entry['historical_note']}")
            report.append("-" * 20)
        report.append("--- End of Archive Transmission ---")
        return "\n".join(report)

    def get_current_conditions_report(self):
        """Returns a textual report of current cosmic conditions."""
        whimsy_report = "The ambient whimsy is cautiously optimistic."
        if self.current_cosmic_conditions["ambient_whimsy"] > 5:
            whimsy_report = "The universe is practically giddy with whimsy!"
        elif self.current_cosmic_conditions["ambient_whimsy"] < -5:
            whimsy_report = "A palpable sense of existential ennui permeates the cosmos."
        elif self.current_cosmic_conditions["ambient_whimsy"] < 0:
            whimsy_report = "The universe is feeling a bit meh today."

        flux_report = f"Temporal flux density is at {self.current_cosmic_conditions['temporal_flux_density']:.2f} chronitons per square moment."
        if self.current_cosmic_conditions['temporal_flux_density'] < 0.3:
            flux_report += " Time feels sluggish and sticky."
        elif self.current_cosmic_conditions['temporal_flux_density'] > 0.8:
            flux_report += " Time is zipping about like a caffeinated hummingbird."

        return f"Cosmic Weather Report: {whimsy_report} {flux_report}"

if __name__ == '__main__':
    # Example Usage
    universe = QuantumUniverseEngine(rock_name="Rocky McRockFace")
    print("Initializing Quantum Universe Engine...")
    for _ in range(5):
        print("\nAttempting to experience a cosmic event...")
        event = universe.experience_cosmic_event()
        if event:
            print(f"EVENT: {event['name']}")
            print(f"DESCRIPTION: {event['description']}")
            print(f"IMPACT: {event['impact_magnitude']:.2f}")
        else:
            print("The universe is quiet for now...")
        print(universe.get_current_conditions_report())
        time.sleep(3) # Simulating time passing, less than cooldown for testing
