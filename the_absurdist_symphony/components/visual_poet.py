import random

class VisualPoet:
    """
    Generates abstract SVG visual poems based on a mood vector.
    """
    def __init__(self, width=300, height=200):
        self.width = width
        self.height = height
        self.svg_elements = []
        self.mood_vector = {}

    def _get_color_palette(self) -> dict:
        """
        Determines a color palette based on the mood vector.
        Returns a dictionary like {'background': '#RRGGBB', 'primary': ..., 'secondary': ...}
        """
        joy = self.mood_vector.get('joy', 0.0)
        gloom = self.mood_vector.get('gloom', 0.0)
        serenity = self.mood_vector.get('serenity', 0.0)
        chaos = self.mood_vector.get('chaos', 0.0)
        energy = self.mood_vector.get('energy', 0.0)
        mystery = self.mood_vector.get('mystery', 0.0)

        # Background color
        bg_r, bg_g, bg_b = 255, 255, 255 # Default white
        if gloom > 0.5:
            level = int(200 - gloom * 150) # Darker for more gloom
            bg_r, bg_g, bg_b = level, level, int(level * 1.1) # Slightly bluish grey
        if serenity > 0.6 and joy < 0.3: # Serene and not joyful -> light cool colors
            bg_r, bg_g, bg_b = 220, 230, 240 # Light blue/grey
        if joy > 0.5:
            bg_r = max(bg_r - 50, int(255 - joy * 50)) # Less red in bg if joyful (yellowish)
            bg_g = max(bg_g - 20, int(255 - joy * 20))
            bg_b = int(255 - joy * 100) # More blue makes it feel less warm for bg

        palette = {
            'background': f"#{bg_r:02x}{bg_g:02x}{bg_b:02x}",
            'shapes': []
        }

        # Shape colors - let's aim for 2-4 shape colors
        num_shape_colors = random.randint(2, 4)
        for i in range(num_shape_colors):
            r, g, b = random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)
            opacity = 0.7 + random.uniform(0, 0.3) # Mostly opaque

            if joy > gloom and joy > 0.3: # Joyful: warm colors
                r = random.randint(180, 255)
                g = random.randint(100, 220)
                b = random.randint(0, 100)
                if serenity > 0.5 : # Joyful serene: pastels
                    r = (r+255)//2
                    g = (g+255)//2
                    b = (b+200)//2
            elif gloom > joy and gloom > 0.3: # Gloomy: cool, dark colors
                r = random.randint(0, 100)
                g = random.randint(50, 150)
                b = random.randint(100, 200)
                if mystery > 0.5: # Gloomy mysterious: darker, desaturated
                    r,g,b = r//2, g//2, b//2
                    opacity = max(0.4, opacity - 0.3)

            if chaos > 0.6: # Chaotic: potentially clashing, more variance
                r,g,b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
                opacity = max(0.5, opacity - chaos * 0.3) # More transparent/overlap chaos

            if energy > 0.5: # Energetic: more vibrant
                # Make one component dominant
                choice = random.choice(['r','g','b'])
                if choice == 'r': r = min(255, r + int(energy*100))
                elif choice == 'g': g = min(255, g + int(energy*100))
                else: b = min(255, b + int(energy*100))

            if mystery > 0.5:
                opacity = max(0.3, opacity - mystery*0.4)


            palette['shapes'].append(f"rgba({r},{g},{b},{opacity:.2f})")

        if not palette['shapes']: # Ensure at least one shape color
            palette['shapes'].append("rgba(100,100,100,0.8)")

        # Chaotic color injection
        if self.mood_vector.get('chaos', 0.0) > 0.75 and random.random() < 0.25: # 25% chance if chaos is high
            print("VISUAL POET: Injecting chaotic color!")
            # Add a completely random, non-mood-related color
            rc, gc, bc = random.randint(0,255), random.randint(0,255), random.randint(0,255)
            ro = random.uniform(0.5, 1.0)
            palette['shapes'].append(f"rgba({rc},{gc},{bc},{ro:.2f})")
            random.shuffle(palette['shapes']) # Mix it in

        return palette

    def _add_background(self, color: str):
        self.svg_elements.append(f'<rect width="{self.width}" height="{self.height}" fill="{color}" />')

    def _add_random_shape(self, palette: dict):
        """Adds a random shape influenced by mood."""
        shape_type = random.choice(['rect', 'circle', 'ellipse', 'polygon', 'line'])

        fill_color = random.choice(palette['shapes'])
        stroke_color = random.choice(palette['shapes']) if random.random() < 0.7 else "none"
        stroke_width = 0
        if stroke_color != "none":
            stroke_width = random.randint(1, int(1 + self.mood_vector.get('energy', 0.0) * 5 + self.mood_vector.get('chaos',0.0)*5))


        # Common attributes
        common_attrs = f'fill="{fill_color}" stroke="{stroke_color}" stroke-width="{stroke_width}"'

        # Whimsical transformations based on mood
        transformations = []
        chaos = self.mood_vector.get('chaos', 0.0)
        energy = self.mood_vector.get('energy', 0.0)
        serenity = self.mood_vector.get('serenity', 0.0)

        # Rotation
        if random.random() < (chaos + energy) * 0.5:
            angle = random.randint(-90, 90) * (chaos + energy)
            cx = random.randint(0, self.width)
            cy = random.randint(0, self.height)
            transformations.append(f"rotate({angle} {cx} {cy})")

        # Skew (more chaotic)
        if random.random() < chaos * 0.4:
            skew_x = random.randint(-20, 20) * chaos
            skew_y = random.randint(-20, 20) * chaos
            if random.choice([True, False]):
                transformations.append(f"skewX({skew_x})")
            else:
                transformations.append(f"skewY({skew_y})")

        # Scale (more energy, less serenity)
        if random.random() < energy * 0.5 and serenity < 0.5:
            scale_factor = 0.5 + energy + random.uniform(-0.2, 0.2)
            scale_factor = max(0.2, min(2.0, scale_factor)) # clamp
            transformations.append(f"scale({scale_factor})")

        transform_str = f'transform="{" ".join(transformations)}"' if transformations else ""

        if shape_type == 'rect':
            x = random.randint(0, self.width - 20)
            y = random.randint(0, self.height - 20)
            w = random.randint(10, int(self.width / 2 * (1 + energy - serenity)))
            h = random.randint(10, int(self.height / 2 * (1 + energy - serenity)))
            rx = random.randint(0, int(w/2 * self.mood_vector.get('joy',0))) # Rounded corners for joy
            ry = random.randint(0, int(h/2 * self.mood_vector.get('joy',0)))
            self.svg_elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{ry}" {common_attrs} {transform_str}/>')

        elif shape_type == 'circle':
            cx = random.randint(20, self.width - 20)
            cy = random.randint(20, self.height - 20)
            r_base = (self.width + self.height) / 4
            r = random.randint(5, int(r_base / 3 * (1 + energy - serenity*0.5)))
            self.svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" {common_attrs} {transform_str}/>')

        elif shape_type == 'ellipse':
            cx = random.randint(20, self.width - 20)
            cy = random.randint(20, self.height - 20)
            rx_base = self.width / 3
            ry_base = self.height / 3
            rx = random.randint(5, int(rx_base * (1 + energy - serenity*0.5)))
            ry = random.randint(5, int(ry_base * (1 + energy - serenity*0.5)))
            self.svg_elements.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" {common_attrs} {transform_str}/>')

        elif shape_type == 'line':
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            # Lines don't have fill, override common_attrs for fill
            line_attrs = f'stroke="{random.choice(palette["shapes"])}" stroke-width="{stroke_width+1}"' # Make lines a bit thicker
            self.svg_elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {line_attrs} {transform_str}/>')

        elif shape_type == 'polygon':
            points = []
            num_points = random.randint(3, 3 + int(chaos * 5 + energy * 3)) # More points for chaos/energy
            for _ in range(num_points):
                px = random.randint(0, self.width)
                py = random.randint(0, self.height)
                points.append(f"{px},{py}")
            points_str = " ".join(points)
            self.svg_elements.append(f'<polygon points="{points_str}" {common_attrs} {transform_str}/>')


    def generate_poem(self, mood_vector: dict) -> str:
        """
        Generates an SVG string based on the provided mood vector.
        """
        self.mood_vector = mood_vector
        self.svg_elements = [] # Reset for new poem

        palette = self._get_color_palette()
        self._add_background(palette['background'])

        # Number of shapes based on mood
        base_shapes = 3
        num_shapes = base_shapes + \
                     int(mood_vector.get('chaos', 0.0) * 10) + \
                     int(mood_vector.get('energy', 0.0) * 5) - \
                     int(mood_vector.get('serenity', 0.0) * 2)
        num_shapes = max(1, min(25, num_shapes)) # Clamp number of shapes

        for _ in range(num_shapes):
            self._add_random_shape(palette)

        # Add a filter for mystery/gloom?
        filters = ""
        if mood_vector.get('mystery', 0.0) > 0.6 or mood_vector.get('gloom', 0.0) > 0.7:
            blur_amount = mood_vector.get('mystery', 0.0) * 3 + mood_vector.get('gloom', 0.0) * 2
            filters = f"""
  <defs>
    <filter id="moodFilter">
      <feGaussianBlur stdDeviation="{blur_amount:.1f}" />
    </filter>
  </defs>
"""
            # Apply filter to a group of all shapes
            shapes_str = "\n  ".join(self.svg_elements[1:]) # All except background
            self.svg_elements = [self.svg_elements[0]] # Keep background
            self.svg_elements.append(f'<g filter="url(#moodFilter)">\n  {shapes_str}\n</g>')


        svg_string = f"""<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
{filters}
  {"\n  ".join(self.svg_elements)}
</svg>"""
        return svg_string

if __name__ == '__main__':
    poet = VisualPoet(width=400, height=300)

    print("--- Test with a 'Joyful' Mood ---")
    joyful_mood = {
        'chaos': 0.1, 'serenity': 0.7, 'joy': 0.9,
        'gloom': 0.1, 'energy': 0.6, 'mystery': 0.1,
        'city': 'TestCitySunny'
    }
    svg_joy = poet.generate_poem(joyful_mood)
    with open("joyful_poem.svg", "w") as f:
        f.write(svg_joy)
    print("Generated joyful_poem.svg")

    print("\n--- Test with a 'Gloomy & Chaotic' Mood ---")
    gloomy_mood = {
        'chaos': 0.8, 'serenity': 0.1, 'joy': 0.1,
        'gloom': 0.9, 'energy': 0.4, 'mystery': 0.7,
        'city': 'TestCityStormy'
    }
    svg_gloom = poet.generate_poem(gloomy_mood)
    with open("gloomy_poem.svg", "w") as f:
        f.write(svg_gloom)
    print("Generated gloomy_poem.svg")

    print("\n--- Test with a 'Serene & Mysterious' Mood ---")
    serene_mood = {
        'chaos': 0.1, 'serenity': 0.9, 'joy': 0.2,
        'gloom': 0.2, 'energy': 0.1, 'mystery': 0.8,
        'city': 'TestCityFoggy'
    }
    svg_serene = poet.generate_poem(serene_mood)
    with open("serene_poem.svg", "w") as f:
        f.write(svg_serene)
    print("Generated serene_poem.svg")

    print("\n--- Test with a 'High Energy' Mood ---")
    energetic_mood = {
        'chaos': 0.4, 'serenity': 0.2, 'joy': 0.5,
        'gloom': 0.1, 'energy': 0.9, 'mystery': 0.3,
        'city': 'TestCityWindy'
    }
    svg_energy = poet.generate_poem(energetic_mood)
    with open("energetic_poem.svg", "w") as f:
        f.write(svg_energy)
    print("Generated energetic_poem.svg")

    # Example of using it with the WeatherWeaver (if in the same directory for testing)
    # from weather_weaver import WeatherWeaver # This would need path adjustments if run directly
    # print("\n--- Test with WeatherWeaver ---")
    # weaver = WeatherWeaver()
    # mood = weaver.get_mood("Paris") # Get mood for a specific city
    # if mood and not mood.get('error'):
    #     print(f"Mood for Paris: {mood}")
    #     svg_weather = poet.generate_poem(mood)
    #     with open("weather_based_poem.svg", "w") as f:
    #         f.write(svg_weather)
    #     print("Generated weather_based_poem.svg for Paris")
    # else:
    #     print(f"Could not generate weather based poem. Mood: {mood}")
