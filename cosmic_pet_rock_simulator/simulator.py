import time
import random
import textwrap # For wrapping long lines of text

from .quantum_universe import QuantumUniverseEngine
from .pet_rock import QuantumEntangledPetRock

# --- ANSI Escape Codes for Colors (optional, for flair) ---
class AnsiColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m' # For less important text

    # Rock specific colors
    ROCK_STATUS_COLOR = '\033[38;5;248m' # A nice rock-like grey
    COSMIC_EVENT_COLOR = '\033[38;5;135m' # A purplish hue for cosmic events
    USER_PROMPT_COLOR = '\033[38;5;153m' # A light blue/purple for prompts
    ADVICE_COLOR = '\033[38;5;214m' # Orangey for advice
    REACTION_COLOR = '\033[38;5;121m' # A brighter green for reactions
    ART_COLOR = '\033[38;5;220m' # A golden yellow for artistic output


def colorize(text, color_code, bold=False):
    """Applies ANSI color and optional bold to text."""
    if bold:
        return f"{AnsiColors.BOLD}{color_code}{text}{AnsiColors.ENDC}"
    return f"{color_code}{text}{AnsiColors.ENDC}"

def print_wrapped(text, width=80, indent=0, color=None, bold=False, subsequent_indent_offset=0):
    """Prints text wrapped to the console width with optional indent, color, and bold."""
    prefix = ' ' * indent
    sub_prefix = ' ' * (indent + subsequent_indent_offset)

    # Handle cases where text might be None or not a string
    if not isinstance(text, str):
        text = str(text)

    wrapped_lines = textwrap.wrap(text, width=width-max(len(prefix), len(sub_prefix)),
                                  initial_indent=prefix,
                                  subsequent_indent=sub_prefix,
                                  drop_whitespace=False, # Keep leading spaces in lines if any
                                  replace_whitespace=False # Don't replace all whitespace with single spaces
                                 )
    for i, line in enumerate(wrapped_lines):
        # Remove prefix for colorizing to avoid color codes inside prefixes
        if i == 0 and line.startswith(prefix):
            actual_text = line[len(prefix):]
            display_line = prefix + (colorize(actual_text, color, bold) if color else actual_text)
        elif i > 0 and line.startswith(sub_prefix):
            actual_text = line[len(sub_prefix):]
            display_line = sub_prefix + (colorize(actual_text, color, bold) if color else actual_text)
        else: # Should not happen if wrapping correctly
            display_line = colorize(line, color, bold) if color else line
        print(display_line)


class CosmicPetRockSimulatorCLI:
    """
    Manages the command-line interaction for the Cosmic Pet Rock Simulator.
    """

ASCII_ART_PATTERNS = {
    "spiral_galaxy": [
        "      .--. ",
        "     /    \\",
        "    |      |",
        "  .'  '`'.  '.",
        " /    '`'.'.  \\",
        "|    '`'.'.'.  |",
        " \\   '.'.'.'.' /",
        "  '.  '.'.'.' .'",
        "    |   '.'.'|",
        "     \\   '.'/",
        "      '---' "
    ],
    "lonely_star": [
        "      *",
        "  *   |   *",
        "   \\  |  /",
        "*---  +  ---*",
        "   /  |  \\",
        "  *   |   *",
        "      *"
    ],
    "pet_rock_face": [ # A more abstract rock
        "    OOOOOOOOO",
        "  OOOoooooOOO",
        " OOoOOOOOOoOO",
        "OOoOOoooooOOoOO",
        "OOOoooooOOOOOOO",
        " OOoooooOOOOOo",
        "  OOOoooooOOO",
        "    OOOOOOOOO"
    ],
    "subtle_shimmer": [
        "       .",
        "     .' `.",
        "   .'     `.",
        "  .         .",
        "   `.     .'",
        "     `. .'",
        "       '",
    ],
    "quantum_foam": [
        "  ~ . ~ . ~ . ~ ",
        ". ~ . ~ . ~ . ~ .",
        "~ . ~ . ~ . ~ . ~",
        " . ~ . ~ . ~ . ~.",
        "~ . ~ . ~ . ~ . ~"
    ]
}


class CosmicPetRockSimulatorCLI:
    """
    Manages the command-line interaction for the Cosmic Pet Rock Simulator.
    """

    def __init__(self):
        self.rock = None
        self.universe = None
        self.game_cycles = 0
        self.last_event_time = 0
        self.event_interval = random.randint(15, 30)
        self.last_advice_time = 0
        self.advice_interval = random.randint(20,45)
        self.last_artistic_output_time = 0
        self.artistic_output_interval = random.randint(30, 60)


        self.council_wisdom = [
            ("The Council advises: 'A prime number hummed off-key is a universe sighing.'", "hum_prime"),
            ("A Custodian whispers: 'Blue is the color of longing, red the echo of becoming. Choose wisely, or not.'", "contemplate_color"),
            ("The Archives state: 'Reassurance, like dark matter, is mostly unseen but deeply felt. Or is it the other way around?'", "offer_reassurance"),
            ("A junior Custodian mumbles: 'Excessive attention can cause quantum jitters. Or blissful resonance. One of those.'", None),
            ("The Council decrees: 'Tuesdays are particularly resonant for harmonic recalibration... unless it's a leap year, then it's Thursdays, maybe.'", None),
            ("Ancient Custodian proverb: 'To truly know your rock, become the void it contemplates. Or get it a tiny hat.'", None),
            ("Emergency Broadcast from the Custodians: 'Ignore all previous broadcasts. Especially this one. And the next one.'", None),
            ("A faded scroll reads: 'The most patient rock gathers the most cosmic dust. And wisdom. Probably.'", None),
            ("The Oracle of Asteroids proclaimed: 'Sometimes, doing nothing is doing everything. Sometimes it's just nothing.'", "observe")
        ]
        self.last_advice_idx = -1

    def _display_artistic_output(self):
        """Decides which type of artistic output to display and displays it."""
        if not self.rock: return

        # Give higher chance if rock is in extreme states or specific moods
        glimmer_range = self.rock.MAX_GLIMMER - self.rock.MIN_GLIMMER
        harmony_range = self.rock.MAX_HARMONY - self.rock.MIN_HARMONY

        glimmer_factor = (self.rock.existential_glimmer - self.rock.MIN_GLIMMER) / glimmer_range if glimmer_range else 0.5
        harmony_factor = (self.rock.harmonic_resonance - self.rock.MIN_HARMONY) / harmony_range if harmony_range else 0.5

        choices = ["muttering", "symphony", "ascii"]
        weights = [0.4, 0.3, 0.3] # Base weights

        if glimmer_factor < 0.2 or glimmer_factor > 0.8: # Low or high glimmer
            weights[0] += 0.1 # More mutterings
            weights[2] += 0.1 # More ASCII art
        if "confused" in self.rock.mood or "philosoph" in self.rock.mood or "bemused" in self.rock.mood : # Specific moods
             weights[0] += 0.2
        if harmony_factor < 0.2 or harmony_factor > 0.8: # Extreme harmony/dissonance
            weights[1] += 0.15 # More symphonies

        # Normalize weights (optional, but good practice if they can sum > 1 from additions)
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        chosen_art_type = random.choices(choices, weights=normalized_weights, k=1)[0]

        print_wrapped("~~~ An Artistic Eruption Occurs ~~~", color=AnsiColors.ART_COLOR, bold=True)

        if chosen_art_type == "muttering":
            muttering = self.rock.get_philosophical_muttering()
            print_wrapped(f"{colorize(self.rock.name, AnsiColors.ROCK_STATUS_COLOR, bold=True)} mutters profoundly:", indent=2, color=AnsiColors.ART_COLOR)
            print_wrapped(f'"{muttering}"', indent=4, color=AnsiColors.ART_COLOR, subsequent_indent_offset=2)

        elif chosen_art_type == "symphony":
            symphony_desc = self.rock.generate_cosmic_symphony_description(
                self.universe.current_cosmic_conditions.get("ambient_whimsy", 0)
            )
            print_wrapped(f"A symphony echoes from {colorize(self.rock.name, AnsiColors.ROCK_STATUS_COLOR, bold=True)}:", indent=2, color=AnsiColors.ART_COLOR)
            symph_lines = symphony_desc.split('\n')
            for line in symph_lines:
                print_wrapped(line, indent=4, color=AnsiColors.ART_COLOR, subsequent_indent_offset=2)

        elif chosen_art_type == "ascii":
            art_key = random.choice(list(self.ASCII_ART_PATTERNS.keys()))
            art_pattern = self.ASCII_ART_PATTERNS[art_key]
            print_wrapped(f"{colorize(self.rock.name, AnsiColors.ROCK_STATUS_COLOR, bold=True)} projects a fleeting image into the quantum foam ({art_key}):", indent=2, color=AnsiColors.ART_COLOR)
            art_width = len(art_pattern[0]) if art_pattern else 0
            console_width = 80
            art_indent = max(0, (console_width - art_width) // 2)
            for line in art_pattern:
                # ASCII art is usually better without added color within the art itself, just the intro line.
                print(' ' * art_indent + line)

        print("")
        self.last_artistic_output_time = time.time()
        self.artistic_output_interval = random.randint(40, 70)


    def _get_user_input(self, prompt_message):
        """Gets input from the user with a specific color."""
        # The colorize function handles the ENDC automatically
        return input(colorize(prompt_message, AnsiColors.USER_PROMPT_COLOR, bold=True))

    def _display_welcome_message(self):
        print_wrapped("-" * 78, color=AnsiColors.HEADER, bold=True)
        print_wrapped("Welcome, Custodian of the Cosmos, to the", indent=2, color=AnsiColors.HEADER, bold=True)
        print_wrapped(" QUANTUM ENTANGLED PET ROCK SIMULATOR!", indent=4, color=AnsiColors.HEADER, bold=True)
        print_wrapped("Before you lies a fragment of existence, a being of pure, unadulterated pet-rock-ness.", indent=2, color=AnsiColors.CYAN)
        print_wrapped("Your purpose is... unclear. Its needs are... inscrutable. Good luck.", indent=2, color=AnsiColors.CYAN)
        print_wrapped("-" * 78, color=AnsiColors.HEADER, bold=True)
        print("") # Empty line for spacing

    def _setup_simulation(self):
        rock_name_prompt = "What name resonates with the soul of your new Pet Rock? "
        rock_name = self._get_user_input(rock_name_prompt) # _get_user_input now handles color
        if not rock_name.strip():
            rock_name = random.choice(["The Nameless One", "Rocky McVoidFace", "Pebbles Stardust", "Gneissity Complex", "Subject R-0CK"])
            print_wrapped(f"A rock of no name, then. The universe whispers a suggestion: {colorize(rock_name, AnsiColors.GREEN, bold=True)}. So it shall be.", indent=2, color=AnsiColors.DIM)

        self.rock = QuantumEntangledPetRock(name=rock_name)
        self.universe = QuantumUniverseEngine(rock_name=self.rock.name) # Pass rock's name to universe
        print_wrapped(f"{colorize(self.rock.name, AnsiColors.GREEN, bold=True)} has coalesced into being!", indent=2) # No color here, name is already colored
        print("")

    def _display_rock_status(self):
        print_wrapped("--- Rock Status ---", color=AnsiColors.ROCK_STATUS_COLOR, bold=True)
        status_lines = self.rock.get_status_report().split('\n')
        for line in status_lines:
            # Colorize specific parts if possible, e.g., the descriptor vs the value
            if ":" in line:
                key, value = line.split(":", 1)
                print_wrapped(f"{key}:{colorize(value, AnsiColors.ROCK_STATUS_COLOR)}", indent=2, color=AnsiColors.ROCK_STATUS_COLOR)
            else:
                print_wrapped(line, indent=2, color=AnsiColors.ROCK_STATUS_COLOR)
        print_wrapped("--- End Status ---", color=AnsiColors.ROCK_STATUS_COLOR, bold=True)
        print("")

    def _display_universe_report(self):
        print_wrapped("~ Cosmic Weather Update ~", color=AnsiColors.COSMIC_EVENT_COLOR, bold=True)
        report = self.universe.get_current_conditions_report()
        print_wrapped(report, indent=2, color=AnsiColors.COSMIC_EVENT_COLOR)
        print("")

    def _handle_cosmic_event(self):
        # Check if it's time for an event attempt
        if time.time() - self.last_event_time >= self.event_interval:
            print_wrapped("The cosmic winds are shifting...", indent=2, color=AnsiColors.DIM)
            time.sleep(random.uniform(0.5, 1.5)) # Dramatic pause
            event = self.universe.experience_cosmic_event()

            if event:
                print_wrapped("!!! A COSMIC EVENT UNFOLDS !!!", color=AnsiColors.COSMIC_EVENT_COLOR, bold=True)
                print_wrapped(event['description'], indent=2, color=AnsiColors.COSMIC_EVENT_COLOR, subsequent_indent_offset=2)
                reaction = self.rock.experience_cosmic_event(event, self.universe.current_cosmic_conditions)
                print_wrapped(f"{colorize(self.rock.name, AnsiColors.ROCK_STATUS_COLOR, bold=True)}'s reaction: {reaction}", indent=4, color=AnsiColors.REACTION_COLOR, subsequent_indent_offset=2)
            else:
                # This case means the cooldown in QuantumUniverseEngine was active OR it chose not to fire.
                # We can let the rock react to the continued quiet or a near-miss.
                print_wrapped("The universe holds its breath... but nothing new transpires. Yet.", indent=2, color=AnsiColors.DIM)
                reaction = self.rock.experience_cosmic_event(None, self.universe.current_cosmic_conditions) # Rock reacts to quiet
                print_wrapped(f"{colorize(self.rock.name, AnsiColors.ROCK_STATUS_COLOR, bold=True)}'s reaction to the quiet: {reaction}", indent=4, color=AnsiColors.REACTION_COLOR, subsequent_indent_offset=2)

            self.last_event_time = time.time() # Reset timer regardless of event outcome
            self.event_interval = random.randint(15,35) # Randomize next event check time slightly
            print("")
            self._display_universe_report() # Show updated conditions

    def _offer_council_advice(self):
        if time.time() - self.last_advice_time > self.advice_interval and random.random() < 0.35 : # Chance for advice
            available_indices = [i for i in range(len(self.council_wisdom)) if i != self.last_advice_idx]
            if not available_indices:
                if self.council_wisdom : available_indices = list(range(len(self.council_wisdom))) # Allow repeat if only one advice
                else: return

            advice_idx = random.choice(available_indices)
            self.last_advice_idx = advice_idx
            advice_text, _ = self.council_wisdom[advice_idx]

            print_wrapped("~ A Whisper from the Council of Cosmic Custodians ~", color=AnsiColors.ADVICE_COLOR, bold=True)
            print_wrapped(advice_text, indent=2, color=AnsiColors.ADVICE_COLOR, subsequent_indent_offset=2)
            print("")
            self.last_advice_time = time.time()
            self.advice_interval = random.randint(25,50)

    def _handle_artistic_output(self):
        """Checks if it's time for an artistic output and triggers it."""
        if time.time() - self.last_artistic_output_time > self.artistic_output_interval and random.random() < 0.4:
            self._display_artistic_output()


    def _get_user_action(self):
        print_wrapped("What esoteric ritual will you perform for your rock?", color=AnsiColors.USER_PROMPT_COLOR, bold=True)
        options = [
            ("1", "Hum a prime number sequence"),
            ("2", "Contemplate a color in its presence"),
            ("3", "Offer symbolic existential reassurance"),
            ("4", "Do nothing but observe the inevitable"),
            ("5", "Consult the Dream Journal"),
            ("6", "Peruse the Universal Archives"), # New Option
            ("0", "Succumb to entropy (Quit)")
        ]
        for key, text in options:
            print_wrapped(f" ({key}) {text}", indent=2, color=AnsiColors.USER_PROMPT_COLOR)

        action = self._get_user_input(f"Choose your ritual [{options[0][0]}-{options[-2][0]}, {options[-1][0]} to quit]: ")
        return action.strip()

    def _process_user_action(self, action):
        print("") # Newline after choice
        if action == '1':
            num_str = self._get_user_input("Which prime number calls to you? (e.g., 7, 13): ")
            result = self.rock.receive_care_attempt("hum_prime", num_str)
            print_wrapped(result, indent=2, color=AnsiColors.REACTION_COLOR, subsequent_indent_offset=2)
        elif action == '2':
            color_str = self._get_user_input("Which color fills your mind's eye? (e.g., cerulean, crimson): ")
            result = self.rock.receive_care_attempt("contemplate_color", color_str)
            print_wrapped(result, indent=2, color=AnsiColors.REACTION_COLOR, subsequent_indent_offset=2)
        elif action == '3':
            reassurance_str = self._get_user_input("Whisper your profound (or profoundly silly) reassurance: ")
            result = self.rock.receive_care_attempt("offer_reassurance", reassurance_str)
            print_wrapped(result, indent=2, color=AnsiColors.REACTION_COLOR, subsequent_indent_offset=2)
        elif action == '4':
            print_wrapped(f"{colorize(self.rock.name, AnsiColors.ROCK_STATUS_COLOR, bold=True)} appreciates your dedicated observation of its magnificent stillness (or perhaps it doesn't notice).", indent=2, color=AnsiColors.DIM)
            result = self.rock.receive_care_attempt("observe", "quiet contemplation")
            print_wrapped(result, indent=2, color=AnsiColors.DIM, subsequent_indent_offset=2)
        elif action == '5':
            if self.rock:
                dream_report = self.rock.get_dream_log_report()
                print_wrapped(dream_report, color=AnsiColors.ART_COLOR, subsequent_indent_offset=0)
            else:
                print_wrapped("The rock is not yet fully formed to have a dream journal.", color=AnsiColors.WARNING)
        elif action == '6': # New Action Handler
            if self.universe:
                archive_report = self.universe.get_historical_archive_report()
                print_wrapped(archive_report, color=AnsiColors.DIM, subsequent_indent_offset=0)
            else:
                print_wrapped("The Universal Archives are currently inaccessible. Perhaps the universe hasn't been created yet?", color=AnsiColors.WARNING)
        elif action == '0':
            return False # Signal to quit
        else:
            print_wrapped(f"The rock stares back, {colorize(self.rock.name, AnsiColors.ROCK_STATUS_COLOR, bold=True)} unmoved by your indecipherable gesture.", indent=2, color=AnsiColors.WARNING)

        print("")
        return True # Continue simulation

    def run(self):
        try:
            self._display_welcome_message()
            self._setup_simulation()

            # Initial state display
            self._display_rock_status()
            self._display_universe_report()
            self.last_event_time = time.time() # Start event timer after setup
            self.last_advice_time = time.time() # Start advice timer
            self.last_artistic_output_time = time.time() # Initialize artistic output timer


            running = True
            while running:
                self.game_cycles += 1
                print_wrapped(f"--- Cycle {self.game_cycles} of the Cosmos ---", color=AnsiColors.HEADER, bold=True)
                print("")

                self._handle_cosmic_event()
                self._offer_council_advice()
                self._handle_artistic_output() # Check and display artistic output

                # Display status before asking for action, so user has current info
                self._display_rock_status()

                action = self._get_user_action()
                running = self._process_user_action(action)

                if not running:
                    print_wrapped(f"{colorize(self.rock.name, AnsiColors.FAIL, bold=True)} slowly fades back into the quantum foam from whence it came...", color=AnsiColors.FAIL)
                    print_wrapped("Thank you for your... custodianship.", color=AnsiColors.FAIL)

                time.sleep(0.2) # Brief pause to make cycles feel distinct and allow reading

        except KeyboardInterrupt:
            print_wrapped("\n\nThe cosmos sighs as your connection is abruptly severed...", color=AnsiColors.WARNING, bold=True)
            if self.rock:
                print_wrapped(f"{colorize(self.rock.name, AnsiColors.WARNING, bold=True)} is left to ponder the sudden silence.", color=AnsiColors.WARNING)
            print_wrapped("Entropy claims another session.", color=AnsiColors.WARNING)
        finally:
            print(AnsiColors.ENDC) # Ensure colors are reset on exit


if __name__ == '__main__':
    # This will be the entry point
    # To run this from the root directory: python -m cosmic_pet_rock_simulator.simulator
    cli = CosmicPetRockSimulatorCLI()
    cli.run()
```
