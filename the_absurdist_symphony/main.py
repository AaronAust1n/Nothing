from conductor import Conductor # Assuming conductor.py is in the same directory or PYTHONPATH
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import sys

# Simple function to capture prints (for cosmic event logs etc.)
# This is a bit of a hack for this specific use case.
# A more robust solution would involve proper logging in components.
class PrintInterceptor:
    def __init__(self):
        self.captured_output = []
        self.original_stdout = sys.stdout

    def start(self):
        self.captured_output = []
        sys.stdout = self

    def write(self, text):
        # self.original_stdout.write(text) # Uncomment to also print to console
        if "WEATHER WEAVER: A COSMIC EVENT UNFOLDS!" in text or \
           "WEATHER WEAVER: Cosmic Event" in text:
            self.captured_output.append(text.strip())

    def flush(self):
        self.original_stdout.flush()

    def stop(self):
        sys.stdout = self.original_stdout
        return "\n".join(self.captured_output)


def main(city_name=None, output_filename="the_symphony_output.html"):
    """
    Runs one cycle of the Absurdist Symphony and generates an HTML output file.
    """
    print("Initializing The Absurdist Symphony Conductor...")
    symphony_conductor = Conductor()

    # --- Capture specific prints from WeatherWeaver for cosmic events ---
    interceptor = PrintInterceptor()
    interceptor.start()

    print(f"Running a symphony cycle... (City: {city_name if city_name else 'Random'})")
    cycle_data = symphony_conductor.run_symphony_cycle(city=city_name)

    cosmic_event_log = interceptor.stop()
    # --- End print capture ---


    # Prepare data for Jinja2 template
    template_vars = {
        "cycle_number": cycle_data["cycle_number"],
        "city_name": cycle_data["city_name"],
        "weather_description": cycle_data["weather_description"],
        "temp_c": cycle_data["mood_vector"].get("temp_c", "N/A"),
        "feels_like_c": cycle_data["mood_vector"].get("feels_like_c", "N/A"),
        "wind_kmph": cycle_data["mood_vector"].get("wind_kmph", "N/A"),
        "humidity": cycle_data["mood_vector"].get("humidity", "N/A"),

        "joy": cycle_data["mood_vector"].get("joy", 0),
        "gloom": cycle_data["mood_vector"].get("gloom", 0),
        "chaos": cycle_data["mood_vector"].get("chaos", 0),
        "serenity": cycle_data["mood_vector"].get("serenity", 0),
        "energy": cycle_data["mood_vector"].get("energy", 0),
        "mystery": cycle_data["mood_vector"].get("mystery", 0),
        "cosmic_event_log": cosmic_event_log if cosmic_event_log else None,

        "visual_poem_svg": cycle_data["visual_poem_svg"],
        "haiku_lines": cycle_data["haiku_lines"],

        "soundscape_title": cycle_data["soundscape"]["title"],
        "soundscape_overall_mood": cycle_data["soundscape"]["overall_mood"],
        "soundscape_tempo": cycle_data["soundscape"]["tempo"],
        "soundscape_key_mode": cycle_data["soundscape"]["key_mode"],
        "soundscape_instrumentation": cycle_data["soundscape"]["instrumentation"],
        "soundscape_rhythmic_feel": cycle_data["soundscape"]["rhythmic_feel"],
        "soundscape_melodic_harmonic_character": cycle_data["soundscape"]["melodic_harmonic_character"],
        "soundscape_texture": cycle_data["soundscape"]["texture"],
        "soundscape_dynamics": cycle_data["soundscape"]["dynamics"],
        "soundscape_conceptual_event_list": cycle_data["soundscape"]["conceptual_event_list"],
        "soundscape_absurd_annotation": cycle_data["soundscape"]["absurd_annotation"],

        "goldfish_wisdom": cycle_data["goldfish_wisdom"],
    }

    # Setup Jinja2 environment
    # Assumes web_display/index.html and web_display/style.css are in a 'web_display' subdirectory
    # relative to this main.py script.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    web_display_dir = os.path.join(current_dir, "web_display")

    env = Environment(
        loader=FileSystemLoader(web_display_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    try:
        template = env.get_template("index.html")
        html_output = template.render(template_vars)
    except Exception as e:
        print(f"Error loading or rendering Jinja2 template: {e}")
        # Create a very basic HTML output on error
        html_output = f"<html><body><h1>Error</h1><p>Could not render symphony output: {e}</p><pre>{cycle_data}</pre></body></html>"


    # Save the output HTML file in the project root
    output_file_path = os.path.join(current_dir, output_filename)
    try:
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"Symphony output successfully written to: {os.path.abspath(output_file_path)}")
        print(f"You can open this file in your web browser to view the symphony.")
    except IOError as e:
        print(f"Error writing HTML output to file: {e}")

if __name__ == "__main__":
    # You can run this script with an optional city name argument
    # e.g., python main.py "Paris"
    # or python main.py
    selected_city = None
    if len(sys.argv) > 1:
        selected_city = sys.argv[1]
        print(f"City name provided: {selected_city}")

    main(city_name=selected_city)
