import random
import json
from ..utils.cities import ALL_CITIES

# Using view_text_website for web requests as per available tools
# For a real application, 'requests' library would be typical.

# Placeholder for the view_text_website tool.
# In a real environment, this would be provided by the agent's toolkit.
# For local testing, you might mock this or use the actual 'requests' library.
def view_text_website(url: str) -> str:
    """
    Placeholder for the agent's view_text_website tool.
    This is a simplified mock for local development if needed.
    In the agent's environment, the actual tool will be used.
    """
    import requests
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Mock view_text_website error: {e}")
        return ""


class WeatherWeaver:
    """
    Fetches weather data and transforms it into a 'mood vector'.
    """
    def __init__(self):
        self.current_city = None
        self.weather_data = None
        self.mood_vector = {}

    def _get_random_city(self) -> str:
        """Selects a random city from the list."""
        return random.choice(ALL_CITIES)

    def fetch_weather_data(self, city: str = None) -> bool:
        """
        Fetches weather data for a given city or a random city.
        Uses wttr.in's JSON format.
        """
        if not city:
            city = self._get_random_city()
        self.current_city = city

        # wttr.in can be unreliable with spaces in city names for JSON format via query param.
        # Preferring URL path for city name.
        city_url_component = city.replace(' ', '+')
        url = f"https://wttr.in/{city_url_component}?format=j1"

        print(f"Fetching weather for {self.current_city} from {url}...")
        try:
            # This is where the agent's tool would be called.
            # For now, directly using the placeholder or a real requests call.
            raw_data = view_text_website(url)
            if not raw_data:
                print(f"Failed to fetch weather data for {self.current_city}. No data returned.")
                self.weather_data = None
                return False

            self.weather_data = json.loads(raw_data)
            # print(f"Successfully fetched weather: {self.weather_data}")
            return True
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for {self.current_city}: {e}")
            print(f"Raw data received: '{raw_data[:200]}...'") # Log snippet of raw data
            self.weather_data = None
            return False
        except Exception as e: # Catching other potential errors during the web request
            print(f"An unexpected error occurred while fetching weather for {self.current_city}: {e}")
            self.weather_data = None
            return False

    def transform_to_mood_vector(self) -> dict:
        """
        Transforms the fetched weather data into a 'mood vector'.
        This is where the 'creative' and 'absurd' logic will primarily reside for this component.

        The mood vector could include keys like:
        - 'chaos': 0-1 (higher for stormy, windy)
        - 'serenity': 0-1 (higher for calm, clear)
        - 'joy': 0-1 (higher for sunny, warm)
        - 'gloom': 0-1 (higher for overcast, rainy, cold)
        - 'energy': 0-1 (based on wind, temperature deviation from 'average')
        - 'mystery': 0-1 (fog, mist, unusual conditions)
        """
        if not self.weather_data or not self.weather_data.get('current_condition'):
            print("No weather data available to transform.")
            # Return a default or error mood vector
            return {
                'chaos': 0.1, 'serenity': 0.1, 'joy': 0.1,
                'gloom': 0.5, 'energy': 0.1, 'mystery': 0.2,
                'error': 1.0 # Special key to indicate an issue
            }

        current_condition = self.weather_data['current_condition'][0]
        # print(f"Current condition: {current_condition}")

        temp_c = float(current_condition.get('temp_C', 0))
        wind_kmph = float(current_condition.get('windspeedKmph', 0))
        weather_desc_list = current_condition.get('weatherDesc', [{"value": "Unknown"}])
        weather_desc = weather_desc_list[0].get('value', "Unknown").lower()
        humidity = float(current_condition.get('humidity', 50)) # Percentage
        feels_like_c = float(current_condition.get('FeelsLikeC', temp_c))

        # Initialize mood scores
        mood = {
            'chaos': 0.0, 'serenity': 0.0, 'joy': 0.0,
            'gloom': 0.0, 'energy': 0.0, 'mystery': 0.0,
            'temp_c': temp_c, 'wind_kmph': wind_kmph, 'humidity': humidity,
            'feels_like_c': feels_like_c, 'weather_desc': weather_desc,
            'city': self.current_city
        }

        # Temperature effects
        if temp_c > 25: # Warm/Hot
            mood['joy'] += min(1.0, (temp_c - 25) / 15) # Max joy boost at 40C
            mood['energy'] += min(1.0, (temp_c - 25) / 20)
        elif temp_c < 5: # Cold
            mood['gloom'] += min(1.0, (5 - temp_c) / 20) # Max gloom boost at -15C
        else: # Mild
            mood['serenity'] += 0.3

        # FeelsLike vs Actual Temp discrepancy can be interesting
        temp_diff = abs(temp_c - feels_like_c)
        mood['mystery'] += min(1.0, temp_diff / 10) # More mystery if big difference

        # Wind effects
        mood['chaos'] += min(1.0, wind_kmph / 80) # Max chaos boost at 80 kmph
        mood['energy'] += min(1.0, wind_kmph / 50)
        if wind_kmph < 10:
            mood['serenity'] += 0.3

        # Weather description effects (very simplified, can be expanded greatly)
        if any(s in weather_desc for s in ["sun", "clear"]):
            mood['joy'] += 0.5
            mood['serenity'] += 0.2
        if any(s in weather_desc for s in ["rain", "drizzle"]):
            mood['gloom'] += 0.4
            mood['serenity'] += 0.1 # Gentle rain can be serene
        if any(s in weather_desc for s in ["snow", "blizzard"]):
            mood['gloom'] += 0.6
            mood['mystery'] += 0.3
            if "blizzard" in weather_desc:
                mood['chaos'] += 0.5
        if any(s in weather_desc for s in ["storm", "thunder"]):
            mood['chaos'] += 0.7
            mood['energy'] += 0.5
            mood['gloom'] += 0.3
        if any(s in weather_desc for s in ["cloud", "overcast"]):
            mood['gloom'] += 0.3
        if any(s in weather_desc for s in ["fog", "mist"]):
            mood['mystery'] += 0.6
            mood['serenity'] += 0.2 # Mist can be serene

        # Humidity effects
        if humidity > 85:
            mood['gloom'] += 0.1 # Oppressive humidity
            mood['mystery'] += 0.1
        elif humidity < 25:
            mood['energy'] += 0.1 # Dry air can feel energetic for some

        # Normalize moods to be between 0 and 1
        for key in ['chaos', 'serenity', 'joy', 'gloom', 'energy', 'mystery']:
            mood[key] = max(0.0, min(1.0, mood[key]))
            # Add a bit of randomness to make it less predictable - "hallucination"
            mood[key] = max(0.0, min(1.0, mood[key] + random.uniform(-0.1, 0.1)))

        # Subtle city name influence (for amusement)
        city_name_lower = self.current_city.lower()
        if any(c in city_name_lower for c in ["angel", "saint", "hope", "heaven", "peace"]):
            mood['serenity'] = min(1.0, mood.get('serenity', 0) + 0.05)
            mood['joy'] = min(1.0, mood.get('joy', 0) + 0.02)
        if any(c in city_name_lower for c in ["wolf", "dragon", "shadow", "dark", "storm", "devil"]):
            mood['chaos'] = min(1.0, mood.get('chaos', 0) + 0.05)
            mood['mystery'] = min(1.0, mood.get('mystery', 0) + 0.02)
        if "new york" in city_name_lower or "tokyo" in city_name_lower or "london" in city_name_lower: # Big bustling cities
             mood['energy'] = min(1.0, mood.get('energy', 0) + 0.05)


        # Rare "Cosmic Event"
        if random.random() < 0.02: # 2% chance of a cosmic event
            print("WEATHER WEAVER: A COSMIC EVENT UNFOLDS!")
            event_type = random.choice(['boost', 'invert', 'swap', 'nullify'])
            mood_key_to_affect = random.choice(['chaos', 'serenity', 'joy', 'gloom', 'energy', 'mystery'])

            if event_type == 'boost':
                mood[mood_key_to_affect] = min(1.0, mood.get(mood_key_to_affect, 0) + random.uniform(0.3, 0.7))
            elif event_type == 'invert' and mood_key_to_affect in mood: # Ensure key exists
                mood[mood_key_to_affect] = 1.0 - mood.get(mood_key_to_affect, 0.5)
            elif event_type == 'swap':
                key2 = random.choice([k for k in ['chaos', 'serenity', 'joy', 'gloom', 'energy', 'mystery'] if k != mood_key_to_affect])
                mood[mood_key_to_affect], mood[key2] = mood.get(key2, 0.5), mood.get(mood_key_to_affect, 0.5)
            elif event_type == 'nullify':
                 mood[mood_key_to_affect] = random.uniform(0.0, 0.1) # Set to very low

            # Re-normalize just the affected key after cosmic event
            mood[mood_key_to_affect] = max(0.0, min(1.0, mood.get(mood_key_to_affect,0.5)))
            print(f"WEATHER WEAVER: Cosmic Event '{event_type}' affected '{mood_key_to_affect}'.")


        self.mood_vector = mood
        return self.mood_vector

    def get_mood(self, city: str = None):
        """Fetches weather and returns the mood vector."""
        if self.fetch_weather_data(city):
            return self.transform_to_mood_vector()
        else:
            # Return the default/error mood from transform_to_mood_vector
            return self.transform_to_mood_vector()

if __name__ == '__main__':
    weaver = WeatherWeaver()

    # Test with a random city
    print("\n--- Test with Random City ---")
    mood_random = weaver.get_mood()
    if weaver.current_city:
        print(f"Mood for {weaver.current_city}:")
        for k, v in mood_random.items():
            if isinstance(v, float) and k not in ['temp_c', 'wind_kmph', 'humidity', 'feels_like_c']:
                print(f"  {k}: {v:.2f}")
            else:
                print(f"  {k}: {v}")
    else:
        print("Could not determine mood for a random city.")

    # Test with a specific city known for certain weather (e.g., a hot city)
    print("\n--- Test with Specific City (e.g., Dubai) ---")
    # Note: wttr.in might not always have every city, or names might need specific formatting
    mood_dubai = weaver.get_mood("Dubai")
    if weaver.current_city:
        print(f"Mood for {weaver.current_city}:")
        for k, v in mood_dubai.items():
            if isinstance(v, float) and k not in ['temp_c', 'wind_kmph', 'humidity', 'feels_like_c']:
                print(f"  {k}: {v:.2f}")
            else:
                print(f"  {k}: {v}")
    else:
        print("Could not determine mood for Dubai.")

    # Test with a city that might cause issues (e.g., empty string or invalid)
    print("\n--- Test with Potentially Problematic City Name ---")
    mood_problem = weaver.get_mood(" ") # Test with a space, might get an error or default city
    if weaver.current_city:
         print(f"Mood for '{weaver.current_city}':") # City might be odd if wttr.in defaults
         for k, v in mood_problem.items():
            if isinstance(v, float) and k not in ['temp_c', 'wind_kmph', 'humidity', 'feels_like_c']:
                print(f"  {k}: {v:.2f}")
            else:
                print(f"  {k}: {v}")
    else:
        print(f"Mood for '{weaver.current_city}' (problematic input): {mood_problem}")

    print("\n--- Test with a known cold place (e.g., Longyearbyen) ---")
    mood_cold = weaver.get_mood("Longyearbyen")
    if weaver.current_city:
        print(f"Mood for {weaver.current_city}:")
        for k,v in mood_cold.items():
            if isinstance(v, float) and k not in ['temp_c', 'wind_kmph', 'humidity', 'feels_like_c']:
                print(f"  {k}: {v:.2f}")
            else:
                print(f"  {k}: {v}")
    else:
        print("Could not determine mood for Longyearbyen.")
