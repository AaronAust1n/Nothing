import os
import time
import math

# ANSI escape codes for colors (limited palette for broad terminal compatibility)
COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
    "reset": "\033[0m"
}

# Characters for drawing flowers - intensity can map to different chars
# More dense characters for higher intensity/thickness
FLOWER_CHARS_BY_THICKNESS = [
    '.', # Lightest / thinnest
    ':',
    '*',
    'o',
    'O',
    '@', # Heaviest / thickest
]
# Max index for FLOWER_CHARS_BY_THICKNESS
MAX_CHAR_IDX = len(FLOWER_CHARS_BY_THICKNESS) - 1

class TextVisualizer:
    """
    Renders the Garden state to the console using ASCII/Unicode characters.
    """
    def __init__(self, width: int, height: int, use_colors: bool = True):
        self.width = width
        self.height = height
        self.use_colors = use_colors and self._has_color_support()

        # Initialize the grid with empty characters (e.g., spaces)
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        # For color, store color per cell. For simplicity, one color dominant.
        # Or, store (char, color_code) tuple. Let's try simple first.
        # We can also store 'depth' or 'intensity' to resolve overlaps.
        self.depth_buffer = [[-float('inf') for _ in range(width)] for _ in range(height)]


    def _has_color_support(self):
        """Check if the terminal likely supports ANSI colors."""
        if os.name == 'nt': # Windows
            # Basic ANSI support was added in newer Win10 versions.
            # For broader compatibility, might need colorama or similar,
            # but for now, let's assume modern terminals or allow disabling.
            return True # Tentatively enable, can be overridden by user
        # For POSIX systems, check if TERM is set to something that supports color
        term = os.getenv('TERM')
        if term and 'color' in term:
            return True
        return False # Default to no colors if unsure

    def _get_color_from_sentiment(self, sentiment_score: float, is_nomad: bool) -> str:
        """Maps sentiment score (-1 to 1) to an ANSI color code."""
        if not self.use_colors:
            return ""

        if is_nomad: # Nomads get special, perhaps more muted or distinct colors
            # Cycle through cyan, magenta, yellow for nomads based on sentiment value
            # to make them visually distinct.
            val = (sentiment_score + 1) / 2 # Normalize to 0-1
            if val < 0.33: return COLORS.get("bright_cyan", "")
            if val < 0.66: return COLORS.get("bright_magenta", "")
            return COLORS.get("bright_yellow", "")

        # Normalize sentiment to 0-1 range
        normalized_sentiment = (sentiment_score + 1) / 2.0

        if normalized_sentiment > 0.75: return COLORS.get("bright_green", "") # Very positive
        if normalized_sentiment > 0.55: return COLORS.get("green", "")      # Positive
        if normalized_sentiment > 0.45: return COLORS.get("bright_yellow", "") # Slightly positive/neutral leaning positive
        if normalized_sentiment > 0.25: return COLORS.get("yellow", "")     # Slightly negative/neutral leaning negative
        if normalized_sentiment > 0.05: return COLORS.get("red", "")        # Negative
        return COLORS.get("bright_red", "")                                 # Very negative
        # Could add more gradations or use blue/purple for neutral if desired

    def _get_char_from_thickness(self, thickness: float) -> str:
        """Maps line thickness to a character."""
        # Normalize thickness to an index for FLOWER_CHARS_BY_THICKNESS
        # Assuming base thickness is around 1-5 from FractalFlowerEngine
        # Let's say thickness maps from 0.5 to 5.0
        char_idx = int( (thickness / 5.0) * MAX_CHAR_IDX )
        char_idx = max(0, min(char_idx, MAX_CHAR_IDX))
        return FLOWER_CHARS_BY_THICKNESS[char_idx]

    def _draw_line(self, x1, y1, x2, y2, char_to_draw, color_code, depth):
        """Draws a line on the grid using Bresenham's or similar.
           A simpler version for char grid: iterate along dominant axis.
           Depth is used to decide if this line segment overwrites an existing one.
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        curr_x, curr_y = int(x1), int(y1)

        while True:
            if 0 <= curr_x < self.width and 0 <= curr_y < self.height:
                # Only draw if this segment is "closer" (higher depth value)
                # Depth could be related to flower scale or a fixed value per flower
                if depth >= self.depth_buffer[curr_y][curr_x]:
                    self.grid[curr_y][curr_x] = color_code + char_to_draw + (COLORS['reset'] if self.use_colors else "")
                    self.depth_buffer[curr_y][curr_x] = depth

            if curr_x == int(x2) and curr_y == int(y2):
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                curr_x += sx
            if e2 < dx:
                err += dx
                curr_y += sy

    def render(self, garden_data: list):
        """
        Renders the garden_data onto the grid.
        garden_data is a list of flower dictionaries.
        """
        # Clear grid for new frame
        self.grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.depth_buffer = [[-float('inf') for _ in range(self.width)] for _ in range(self.height)]


        # Sort flowers by scale or a defined z-order if needed.
        # Smaller scales (presumably further away or younger) drawn first.
        # Or, use depth buffer more effectively.
        # Let's sort by scale, so larger (closer) flowers are drawn on top if segments overlap at same depth.
        # However, the depth buffer should handle this pixel by pixel.
        # Sorting might help if depth values are very similar.
        # garden_data.sort(key=lambda f: f['scale'])


        for flower_info in garden_data:
            pos_x, pos_y = flower_info['position']
            scale = flower_info['scale']
            color_intensity = flower_info['color_intensity'] # This is sentiment derived, -1 to 1
            is_nomad = flower_info.get('is_nomad', False)

            # Determine base color from sentiment
            base_color_code = self._get_color_from_sentiment(color_intensity, is_nomad)

            # Each segment in fractal_data is (x1, y1, x2, y2, thickness, segment_color_intensity_mod)
            # segment_color_intensity_mod is currently uniform per flower in engine.
            for segment in flower_info['fractal_data']:
                fx1, fy1, fx2, fy2, base_thickness, _ = segment # segment_color_intensity_mod ignored for now

                # Apply flower's overall scale and position offset
                # Fractal coordinates are relative to flower's own origin (0,0)
                # Scale affects size and apparent thickness

                scaled_x1 = fx1 * scale + pos_x
                scaled_y1 = fy1 * scale + pos_y
                scaled_x2 = fx2 * scale + pos_x
                scaled_y2 = fy2 * scale + pos_y

                current_thickness = base_thickness * scale
                # Add effect from 'has_rare_char' if that's a general flower property
                if flower_info.get('thickness_multiplier', False): # This was a quick add to garden render data
                    current_thickness *= 1.2 # Example boost

                char_to_draw = self._get_char_from_thickness(current_thickness)

                # Depth can be related to scale: larger scale means "closer"
                # Or simply use a fixed value if flowers don't overlap much
                # A higher scale means it should be drawn on top.
                # Depth value should be positive.
                depth_val = scale

                self._draw_line(scaled_x1, scaled_y1, scaled_x2, scaled_y2, char_to_draw, base_color_code, depth_val)

        # Assemble the grid into a single string for printing
        output = "\n".join("".join(row) for row in self.grid)

        # Print to console (clear previous frame first)
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        print(output)
        footer_text = f"--- Ephemeral Echo Garden --- Entities: {len(garden_data)} --- Colors: {'On' if self.use_colors else 'Off'} ---"
        print(footer_text)
        # Leave one blank line for potential input prompt below this
        # The main loop's input prompt will try to position itself.
        # print("", flush=True)


if __name__ == '__main__':
    # Mock Garden data for testing visualizer
    mock_garden_data = [
        { # Flower 1: Happy, medium size
            'fractal_data': [
                (0, 0, 0, -10, 2.0, 0.8), # Stem
                (0, -10, -5, -15, 1.5, 0.8), # Branch 1
                (0, -10, 5, -15, 1.5, 0.8),  # Branch 2
                (-5, -15, -7, -12, 1.0, 0.8), # Petal
                (5, -15, 7, -12, 1.0, 0.8)    # Petal
            ],
            'position': (20, 30), # Center X, Bottom Y (since fractal grows upwards)
            'scale': 1.0,
            'color_intensity': 0.9, # Very positive
            'source_word': 'joy',
            'thickness_multiplier': False
        },
        { # Flower 2: Sad, smaller, different position
            'fractal_data': [
                (0, 0, 0, -8, 1.5, -0.7),
                (0, -8, -4, -12, 1.0, -0.7),
                (0, -8, 4, -12, 1.0, -0.7),
            ],
            'position': (50, 25),
            'scale': 0.7,
            'color_intensity': -0.8, # Very negative
            'source_word': 'gloom',
            'thickness_multiplier': True
        },
        { # Flower 3: Nomad, distinct color
            'fractal_data': [
                (0,0, 5,5, 1.0, 0.1),
                (5,5, 0,10, 1.0, 0.1),
                (0,10, 5,15, 1.0, 0.1),
            ],
            'position': (10,10),
            'scale': 0.9,
            'color_intensity': 0.1, # Neutral-ish for nomad
            'source_word': 'zylph',
            'is_nomad': True,
            'thickness_multiplier': True
        }
    ]

    width, height = 80, 40
    visualizer = TextVisualizer(width, height, use_colors=True)

    print("Testing TextVisualizer. This will clear the screen and draw.")
    print("If colors are not supported or misaligned, try TextVisualizer(..., use_colors=False)")
    time.sleep(3)

    try:
        for i in range(5): # Animate scale for a simple test
            # Slightly change scale and position for dynamic effect
            mock_garden_data[0]['scale'] = 1.0 + 0.2 * math.sin(i * 0.5)
            mock_garden_data[0]['position'] = (20 + i*2, 30 - i)

            mock_garden_data[1]['scale'] = 0.7 + 0.1 * math.cos(i*0.5)
            mock_garden_data[1]['position'] = (50 - i*2, 25 + i)

            mock_garden_data[2]['position'] = (10 + i*3, 10 + i*2)


            visualizer.render(mock_garden_data)
            time.sleep(0.2)
        print("\nVisualizer test finished.")
    except Exception as e:
        print(f"Error during visualization: {e}")
        print("This might be due to terminal capabilities or other issues.")

    # Test without colors
    print("\nTesting TextVisualizer without colors in 3 seconds...")
    time.sleep(3)
    visualizer_no_color = TextVisualizer(width, height, use_colors=False)
    try:
        visualizer_no_color.render(mock_garden_data) # Render one static frame
        time.sleep(0.5)
        print("\nVisualizer (no color) test finished.")
    except Exception as e:
        print(f"Error during no-color visualization: {e}")

    # Test line drawing to specific coords
    # visualizer_line_test = TextVisualizer(20,10, use_colors=False)
    # visualizer_line_test.grid = [[' ' for _ in range(20)] for _ in range(10)] # Reset grid
    # visualizer_line_test.depth_buffer = [[-1 for _ in range(20)] for _ in range(10)]
    # visualizer_line_test._draw_line(1,1, 18,1, '#', '', 1) # Horizontal
    # visualizer_line_test._draw_line(1,1, 1,8, '|', '', 1) # Vertical
    # visualizer_line_test._draw_line(1,8, 18,1, '*', '', 1) # Diagonal
    # output = "\n".join("".join(row) for row in visualizer_line_test.grid)
    # os.system('clear')
    # print("Line Test:")
    # print(output)

    print("Basic visualizer tests complete.")
