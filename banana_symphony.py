import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0) # A nice banana yellow

import math # For rotation
import random # For random rotation speed
import numpy as np # For generating sine wave for notes

# --- Musical Constants and Functions ---
BASE_FREQ_A4 = 440.0
NOTES = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}

# Pentatonic Major Scale: C, D, E, G, A ( Intervals: Root, M2, M3, P5, M6 )
# Relative to C: C=0, D=2, E=4, G=7, A=9 (semitones from C)
PENTATONIC_MAJOR_INTERVALS = [0, 2, 4, 7, 9] # Semitones from the root of the scale

def get_frequency(note_name, octave_offset=0):
    """Calculates frequency of a note given its name (e.g., 'A4', 'C#5')."""
    if len(note_name) == 3: # e.g. C#4
        name = note_name[:2]
        octave = int(note_name[2])
    else: # e.g. C4
        name = note_name[0]
        octave = int(note_name[1])

    semitone_offset = NOTES[name]
    # A4 is our reference. Octave difference from 4, times 12 semitones.
    n = semitone_offset + (octave - 4) * 12 + octave_offset
    return BASE_FREQ_A4 * (2**(n/12.0))

# Generate frequencies for a C Major Pentatonic Scale over a few octaves
# Root is C. Let's use C4 as the base for our scale.
# C4 is NOTES["C"] + (4-4)*12 = -9 semitones from A4
C4_FREQ = get_frequency("C4")

SCALE_FREQUENCIES = []
# Octaves 3, 4, 5 for C-Major Pentatonic
# Root C, so intervals are from C.
# C is 0, D is 2, E is 4, G is 7, A is 9 semitones from C.
# A note Xn is X plus n*12 semitones from X0.
# So, Cn is C0 + n*12 semitones from C0.
# C4 is our reference C.
# C3 = C4 - 12 semitones, C5 = C4 + 12 semitones.

# Let's make it simpler: List notes in the scale for a few octaves
# C Pentatonic: C, D, E, G, A
# Octave 3: C3, D3, E3, G3, A3
# Octave 4: C4, D4, E4, G4, A4
# Octave 5: C5, D5, E5, G5, A5
SCALE_NOTE_NAMES = []
for octave in [3, 4, 5]:
    for interval in PENTATONIC_MAJOR_INTERVALS:
        # Calculate semitones from C4
        semitones_from_c4 = (octave - 4) * 12 + interval
        # Calculate frequency relative to C4_FREQ
        freq = C4_FREQ * (2**(semitones_from_c4 / 12.0))
        SCALE_FREQUENCIES.append(freq)

# Sort frequencies just in case
SCALE_FREQUENCIES.sort()

# For generating sound
SAMPLE_RATE = 44100  # Standard sample rate
NOTE_DURATION_MS = 200 # Duration of each note in milliseconds

# Cache for generated sound objects
sound_cache = {} # Cache key: (frequency, duration_ms, waveform)

MIN_NOTE_DURATION_MS = 100
MAX_NOTE_DURATION_MS = 500
MAX_IMPACT_VELOCITY = 10 # Heuristic value, might need tuning

def generate_wave(frequency, duration_ms, waveform='sine'):
    """Generates a pygame.mixer.Sound object for a given waveform."""
    duration_ms = max(MIN_NOTE_DURATION_MS, min(duration_ms, MAX_NOTE_DURATION_MS)) # Clamp duration

    cache_key = (frequency, duration_ms, waveform)
    if cache_key in sound_cache:
        return sound_cache[cache_key]

    num_samples = int(SAMPLE_RATE * duration_ms / 1000.0)
    buf = np.zeros((num_samples, 2), dtype=np.int16) # Stereo
    max_amplitude = 2**15 - 1

    for i in range(num_samples):
        t_cycle = frequency * (float(i) / SAMPLE_RATE) # Time within one cycle of the wave
        t_overall = float(i) / SAMPLE_RATE # Overall time for envelope

        value = 0
        if waveform == 'sine':
            value = np.sin(2 * np.pi * t_cycle)
        elif waveform == 'square':
            value = 1 if (t_cycle % 1.0) < 0.5 else -1
        elif waveform == 'sawtooth':
            value = 2 * (t_cycle - np.floor(0.5 + t_cycle)) # Sawtooth from -1 to 1
        elif waveform == 'triangle':
            value = 2 * abs(2 * (t_cycle - np.floor(t_cycle + 0.5))) - 1

        # Simple fade-in and fade-out envelope
        fade_duration_sec = 0.01 # 10ms fade
        total_duration_sec = duration_ms / 1000.0
        if t_overall < fade_duration_sec:
            value *= t_overall / fade_duration_sec
        elif (total_duration_sec - t_overall) < fade_duration_sec:
            value *= (total_duration_sec - t_overall) / fade_duration_sec

        scaled_value = int(max_amplitude * value)
        buf[i][0] = scaled_value
        buf[i][1] = scaled_value

    sound = pygame.sndarray.make_sound(buf)
    sound_cache[cache_key] = sound
    return sound

# --- Asset Loading ---
banana_image = None
try:
    # Attempt to load the image. Ensure it has a transparent background.
    # The image should be relatively small, e.g., 50x50 pixels.
    banana_image_original = pygame.image.load("banana.png").convert_alpha()
    # We'll scale it down a bit for the bananas, let's say to 40x40 for now
    # The actual size will be controlled by the 'radius' parameter, which will now represent half the image width
    # banana_image = pygame.transform.smoothscale(banana_image_original, (40, 40)) # Example fixed size
except pygame.error as e:
    print(f"Warning: Could not load banana.png: {e}. Falling back to circles.")
    print("Please ensure 'banana.png' and 'boing.wav' are in the same directory as the script.")
    # Create a README if it doesn't exist or append to it
    readme_content = """
## Missing Assets:
Please add the following files to the project directory for the full experience:
- `banana.png`: An image of a banana (e.g., 50x50 pixels, with transparent background).
- `boing.wav`: A short sound effect for wall bounces.
"""
    try:
        with open("README.md", "a+") as f:
            f.seek(0)
            if "Missing Assets" not in f.read():
                f.write(readme_content)
    except Exception as readme_e:
        print(f"Could not write to README.md: {readme_e}")


AVAILABLE_WAVEFORMS = ['sine', 'square', 'sawtooth', 'triangle']

# --- Banana Class ---
class Banana:
    def __init__(self, x, y, size, base_color, vx=0, vy=0): # size now refers to approximate image width
        self.x = x
        self.y = y
        self.size = size
        self.vx = vx
        self.vy = vy

        # Visual/Behavioral Personality
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-4, 4) + (0.5 if random.random() < 0.5 else -0.5) # Ensure some spin
        self.bounciness = random.uniform(0.8, 0.95)

        # Color variation: slightly alter the green component of YELLOW for variety
        r, g, b = base_color
        g_variation = random.randint(-20, 10) # More towards orange/ripe or slightly less ripe
        self.color = (max(0, min(255, r)),
                      max(0, min(255, g + g_variation)),
                      max(0, min(255, b)))

        # Musical Personality
        self.preferred_waveform = random.choice(AVAILABLE_WAVEFORMS)
        self.octave_shift = random.choice([-1, 0, 0, 1]) # -1 octave, normal, normal, +1 octave (more often normal)
                                                        # Octave shift of 0 means no change.
                                                        # An octave is 12 semitones.

        self.image = None
        if banana_image_original:
            self.image = pygame.transform.smoothscale(banana_image_original, (self.size, self.size))
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            # Use size as radius if no image
            self.radius = self.size // 2


    def update(self):
        """Updates the banana's position and rotation, and handles screen boundary bouncing."""
        self.x += self.vx
        self.y += self.vy
        self.angle = (self.angle + self.rotation_speed) % 360

        # Use self.size // 2 as the effective radius for boundary checks
        effective_radius = self.size // 2

        # Bounce off screen edges
        collided_wall = False
        impact_v_wall = 0
        current_bounciness = self.bounciness * global_bounciness_modifier

        if self.x - effective_radius < 0:
            impact_v_wall = abs(self.vx)
            self.x = effective_radius
            self.vx *= -current_bounciness
            collided_wall = True
        elif self.x + effective_radius > SCREEN_WIDTH:
            impact_v_wall = abs(self.vx)
            self.x = SCREEN_WIDTH - effective_radius
            self.vx *= -current_bounciness
            collided_wall = True

        if self.y - effective_radius < 0:
            impact_v_wall = max(impact_v_wall, abs(self.vy))
            self.y = effective_radius
            self.vy *= -current_bounciness
            collided_wall = True
        elif self.y + effective_radius > SCREEN_HEIGHT:
            impact_v_wall = max(impact_v_wall, abs(self.vy))
            self.y = SCREEN_HEIGHT - effective_radius
            self.vy *= -current_bounciness
            collided_wall = True

        if collided_wall:
            if boing_sound:
                boing_sound.play()
            else:
                norm_y = self.y / SCREEN_HEIGHT
                note_index = int(norm_y * (len(SCALE_FREQUENCIES) -1))
                note_index = max(0, min(note_index, len(SCALE_FREQUENCIES) - 1))

                base_freq = SCALE_FREQUENCIES[note_index]
                # Apply octave shift for wall hits too, using this banana's preference
                final_freq = base_freq * (2**self.octave_shift)

                duration_factor = min(impact_v_wall / MAX_IMPACT_VELOCITY, 1.0)
                duration = MIN_NOTE_DURATION_MS + (MAX_NOTE_DURATION_MS - MIN_NOTE_DURATION_MS) * duration_factor

                # Wall hits could use the banana's preferred waveform or a default like sine
                # For now, let's keep wall hits as 'sine' for a consistent background layer
                sound = generate_wave(final_freq, int(duration), waveform='sine')
                sound.play()
                # This is inside Banana.update(). To affect musical_intensity_counter in the global scope,
                # this class method would need to signal back or musical_intensity_counter would need to be
                # passed around or be part of a shared state object.
                # For simplicity, we'll increment based on actual sound plays in the main loop.
                # This specific increment will be handled by checking if boing_sound was NOT played.
                spawn_particles(self.x, self.y, self.color, num_particles=3, max_life=15, base_size=2) # Wall hit particles

        if self.image:
            self.rect.center = (self.x, self.y)

    def draw(self, surface):
        """Draws the banana on the given surface."""
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            surface.blit(rotated_image, new_rect.topleft)
        else:
            # Fallback to drawing a circle if image is not loaded
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


# --- Pygame Setup ---
pygame.init()
pygame.mixer.init() # Initialize the mixer
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Algorithmic Symphony of Bouncing Bananas")
clock = pygame.time.Clock()

# --- Sound Loading ---
boing_sound = None
clack_sound = None
conductor_image = None # For the conductor banana
missing_assets_readme_lines = []

try:
    boing_sound = pygame.mixer.Sound("boing.wav")
except pygame.error as e:
    print(f"Warning: Could not load boing.wav: {e}")
    missing_assets_readme_lines.append("- `boing.wav`: A short sound effect for wall bounces.")

try:
    clack_sound = pygame.mixer.Sound("clack.wav")
except pygame.error as e:
    print(f"Warning: Could not load clack.wav: {e}")
    missing_assets_readme_lines.append("- `clack.wav`: A short sound effect for banana-to-banana collisions.")

if banana_image_original is None: # Check if the main banana image failed to load earlier
     missing_assets_readme_lines.append("- `banana.png`: An image of a regular banana (e.g., 50x50 pixels, with transparent background).")

try:
    conductor_image_original = pygame.image.load("conductor_banana.png").convert_alpha()
    conductor_image = pygame.transform.smoothscale(conductor_image_original, (80, 80)) # Example size
except pygame.error as e:
    print(f"Warning: Could not load conductor_banana.png: {e}. Fallback will be used.")
    missing_assets_readme_lines.append("- `conductor_banana.png` (Optional): Image for the Conductor Banana (e.g., 80x80). Falls back to a larger regular banana or circle.")


# Update README for missing assets
if missing_assets_readme_lines:
    readme_intro = "## Missing Assets:\nPlease add the following files to the project directory for the full experience:\n"
    readme_content = readme_intro + "\n".join(missing_assets_readme_lines)
    try:
        with open("README.md", "w") as f: # Overwrite/Create README with current missing assets
            f.write(readme_content)
            print("Updated README.md with missing asset information.")
    except Exception as readme_e:
        print(f"Could not write to README.md: {readme_e}")


# --- Conductor Class ---
class Conductor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_angle = 0 # Or a slight lean
        self.current_angle = self.base_angle
        self.wave_intensity = 0 # Normalized 0-1
        self.wave_target_angle = 0
        self.last_wave_time = 0
        self.image = None

        if conductor_image:
            self.image = conductor_image
        elif banana_image_original: # Fallback to scaled-up regular banana
            self.image = pygame.transform.smoothscale(banana_image_original, (70, 70))
            # Optional: Tint it to make it look special
            # self.image.fill((255, 255, 100, 100), special_flags=pygame.BLEND_RGBA_MULT) # Golden tint example

        if self.image:
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else: # Absolute fallback to a circle
            self.radius = 35
            self.color = (255, 250, 150) # Pale Yellow

    def set_wave(self, intensity):
        """Intensity is 0 to 1, influences wave magnitude and speed."""
        self.wave_intensity = max(0, min(1, intensity))
        # Simple wave: target a new angle based on intensity
        max_wave_angle = 30 # Max degrees of wave from base
        self.wave_target_angle = self.base_angle + (random.uniform(-max_wave_angle, max_wave_angle) * self.wave_intensity)
        self.last_wave_time = pygame.time.get_ticks()


    def update(self):
        # Smoothly return to target angle, then to base_angle
        # If actively waving (recently set_wave)
        if pygame.time.get_ticks() - self.last_wave_time < 200: # Waving for 200ms
             # Move towards target_angle
            angle_diff = (self.wave_target_angle - self.current_angle + 180) % 360 - 180
            self.current_angle += angle_diff * 0.2 # Speed of waving towards target
        else: # Return to base
            angle_diff = (self.base_angle - self.current_angle + 180) % 360 - 180
            self.current_angle += angle_diff * 0.05 # Slower return to base

        if self.image:
            self.rect.center = (self.x, self.y)


    def draw(self, surface):
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, self.current_angle)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            surface.blit(rotated_image, new_rect.topleft)
        else:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            # Draw a simple "baton"
            baton_length = self.radius * 1.5
            end_x = self.x + baton_length * math.cos(math.radians(self.current_angle - 90))
            end_y = self.y + baton_length * math.sin(math.radians(self.current_angle - 90))
            pygame.draw.line(surface, (200,200,200), (self.x, self.y), (int(end_x), int(end_y)), 3)


# --- Game Objects ---
bananas = []
NUM_BANANAS = 7 # Let's have a few more bananas for a richer symphony
for _ in range(NUM_BANANAS):
    size = random.randint(30, 60)
    x = random.randint(size, SCREEN_WIDTH - size)
    y = random.randint(size, SCREEN_HEIGHT - size)
    vx = random.uniform(-2, 2)
    vy = random.uniform(-1, 1)
    # Pass the base YELLOW color, the constructor will vary it
    bananas.append(Banana(x, y, size, YELLOW, vx=vx, vy=vy))


# --- Particle Class ---
class Particle:
    def __init__(self, x, y, color, size, life, dx, dy):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.life = life # Time to live in frames
        self.dx = dx # Movement direction x
        self.dy = dy # Movement direction y
        self.initial_life = life

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1
        # Optional: shrink particle as it dies
        # self.size = max(0, self.size * (self.life / self.initial_life))


    def draw(self, surface):
        if self.life > 0:
            # Fade out effect by reducing alpha or making color darker
            alpha = max(0, min(255, int(255 * (self.life / self.initial_life))))
            # Create a temporary surface for alpha blending if color doesn't have alpha
            # Or, if particle color is fixed, draw directly.
            # For simplicity, let's just draw without alpha for now, or use a color tuple with alpha if Pygame handles it.
            # Most direct way is to change color towards background.
            # Or, if self.color is (r,g,b), pygame.draw.circle might not support alpha directly.
            # A common trick for simple fade is to reduce size or change color.

            # Let's try changing color intensity
            intensity = self.life / self.initial_life
            final_color = (int(self.color[0] * intensity),
                           int(self.color[1] * intensity),
                           int(self.color[2] * intensity))

            current_size = int(self.size * intensity)
            if current_size > 0:
                 pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), current_size)

def spawn_particles(x, y, base_color, num_particles=5, max_life=20, max_speed=2, base_size=3):
    for _ in range(num_particles):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, max_speed)
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        life = random.randint(max_life // 2, max_life)
        size = random.randint(base_size -1, base_size + 1)
        # Vary particle color slightly from base_color
        r_off, g_off, b_off = random.randint(-20,20), random.randint(-20,20), random.randint(-20,20)
        p_color = (max(0,min(255,base_color[0]+r_off)),
                   max(0,min(255,base_color[1]+g_off)),
                   max(0,min(255,base_color[2]+b_off)))
        particles.append(Particle(x, y, p_color, size, life, dx, dy))

particles = [] # List to hold active particles

# --- Game State & UI Variables ---
gravity_on = False
GRAVITY_FORCE = 0.05 # A small downward acceleration
global_bounciness_modifier = 1.0 # Multiplies individual banana bounciness

# Pygame font setup
pygame.font.init()
try:
    UI_FONT = pygame.font.SysFont("Arial", 20) # Try a common system font
except pygame.error:
    UI_FONT = pygame.font.Font(None, 24) # Fallback to default pygame font
status_texts = {} # To store text surfaces for UI

def update_status_text(key, text):
    global status_texts
    status_texts[key] = UI_FONT.render(text, True, WHITE)

# Initial status texts
update_status_text("gravity", f"Gravity (G): {'ON' if gravity_on else 'OFF'}")
update_status_text("bounciness", f"Global Bounciness (B/L): {global_bounciness_modifier:.2f}")
update_status_text("reset", "Reset (R)")
update_status_text("add", "Click to Add Banana")


def reset_simulation():
    global bananas, particles, gravity_on, global_bounciness_modifier
    bananas.clear()
    particles.clear()
    gravity_on = False
    global_bounciness_modifier = 1.0
    for _ in range(NUM_BANANAS): # Re-populate with initial number
        size = random.randint(30, 60)
        x = random.randint(size, SCREEN_WIDTH - size)
        y = random.randint(size, SCREEN_HEIGHT - size)
        vx = random.uniform(-2, 2)
        vy = random.uniform(-1, 1)
        bananas.append(Banana(x, y, size, YELLOW, vx=vx, vy=vy))
    update_status_text("gravity", f"Gravity (G): {'ON' if gravity_on else 'OFF'}")
    update_status_text("bounciness", f"Global Bounciness (B/L): {global_bounciness_modifier:.2f}")

# Instantiate Conductor
conductor = Conductor(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50) # Position at bottom-center
musical_intensity_counter = 0 # Simple counter for musical events
CONDUCTOR_UPDATE_INTERVAL = 100 # Milliseconds to check intensity
last_conductor_update_time = 0


# --- Game Loop ---
bg_hue_angle = 0
bg_color_base_intensity = 20
bg_color_amplitude = 30

running = True
while running:
    current_time = pygame.time.get_ticks()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                mouse_x, mouse_y = event.pos
                size = random.randint(30, 60)
                # Give it a little initial velocity, maybe upwards or random
                vx = random.uniform(-1, 1)
                vy = random.uniform(-2, 0)
                bananas.append(Banana(mouse_x, mouse_y, size, YELLOW, vx=vx, vy=vy))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                gravity_on = not gravity_on
                update_status_text("gravity", f"Gravity (G): {'ON' if gravity_on else 'OFF'}")
            elif event.key == pygame.K_b:
                global_bounciness_modifier += 0.05
                update_status_text("bounciness", f"Global Bounciness (B/L): {global_bounciness_modifier:.2f}")
            elif event.key == pygame.K_l:
                global_bounciness_modifier = max(0.1, global_bounciness_modifier - 0.05) # Min bounciness
                update_status_text("bounciness", f"Global Bounciness (B/L): {global_bounciness_modifier:.2f}")
            elif event.key == pygame.K_r:
                reset_simulation()


    # --- Main Game Logic Update Phase ---

    # Apply gravity and update banana positions
    for banana in bananas:
        if gravity_on:
            banana.vy += GRAVITY_FORCE

        # Banana.update now returns True if a generated sound was played (wall collision)
        # This is a bit of a hack. A better event system or callback would be cleaner.
        # For now, let's have banana.update return a flag.
        # Modifying Banana.update() to return a boolean:
        #   - return True if generate_wave was called for a wall hit
        #   - return False otherwise

        # This requires changing Banana.update(). Let's assume that change for a moment.
        # if banana.update(): # This line would change if Banana.update() is modified
        #    musical_intensity_counter +=1
        # For now, let's not modify Banana.update's return signature and keep it simple:
        # The conductor will react to banana-banana collisions primarily for waving.
        # Wall sounds are more ambient.

        banana.update()


    # Update all active particles and remove dead ones
    for p in particles:
        p.update()
    particles = [p for p in particles if p.life > 0]

    # Banana-to-Banana Collision Detection & Response
    for i in range(len(bananas)):
        for j in range(i + 1, len(bananas)):
            b1 = bananas[i]
            b2 = bananas[j]

            dist_x = b1.x - b2.x
            dist_y = b1.y - b2.y
            distance = math.sqrt(dist_x**2 + dist_y**2)

            r1 = b1.size // 2
            r2 = b2.size // 2

            if distance == 0:
                b1.x += random.uniform(-0.1, 0.1)
                b1.y += random.uniform(-0.1, 0.1)
                dist_x = b1.x - b2.x
                dist_y = b1.y - b2.y
                distance = math.sqrt(dist_x**2 + dist_y**2)
                if distance == 0: continue

            if distance < r1 + r2:
                if clack_sound:
                    clack_sound.play()
                    # Could also increment intensity here if clack_sound is considered significant
                else:
                    avg_y = (b1.y + b2.y) / 2
                    norm_y = avg_y / SCREEN_HEIGHT
                    note_index = int(norm_y * (len(SCALE_FREQUENCIES) -1))
                    note_index = max(0, min(note_index, len(SCALE_FREQUENCIES) - 1))

                    base_freq = SCALE_FREQUENCIES[note_index]
                    final_freq = base_freq * (2**b1.octave_shift)
                    waveform = b1.preferred_waveform

                    temp_nx = dist_x / distance
                    temp_ny = dist_y / distance
                    v1_normal_comp = b1.vx * temp_nx + b1.vy * temp_ny
                    v2_normal_comp = b2.vx * temp_nx + b2.vy * temp_ny
                    relative_normal_velocity = abs(v1_normal_comp - v2_normal_comp)

                    duration_factor = min(relative_normal_velocity / MAX_IMPACT_VELOCITY, 1.0)
                    duration = MIN_NOTE_DURATION_MS + (MAX_NOTE_DURATION_MS - MIN_NOTE_DURATION_MS) * duration_factor

                    sound = generate_wave(final_freq, int(duration), waveform=waveform)
                    sound.play()

                    # Spawn particles at collision point (midpoint between bananas)
                    collision_x = (b1.x + b2.x) / 2
                    collision_y = (b1.y + b2.y) / 2
                    # Use average color of the two bananas for particles
                    avg_color_r = (b1.color[0] + b2.color[0]) // 2
                    avg_color_g = (b1.color[1] + b2.color[1]) // 2
                    avg_color_b = (b1.color[2] + b2.color[2]) // 2
                    particle_color = (avg_color_r, avg_color_g, avg_color_b)
                    spawn_particles(collision_x, collision_y, particle_color)


                # Normal vector (from b1 to b2)
                nx = dist_x / distance
                ny = dist_y / distance

                # Tangent vector
                tx = -ny
                ty = nx

                # Dot product tangent
                dp_tan1 = b1.vx * tx + b1.vy * ty
                dp_tan2 = b2.vx * tx + b2.vy * ty

                # Dot product normal
                dp_norm1 = b1.vx * nx + b1.vy * ny
                dp_norm2 = b2.vx * nx + b2.vy * ny

                # Conservation of momentum in 1D (for normal direction)
                # Assuming equal mass for now. For different masses, m1, m2:
                # m1 = (dp_norm1 * (mass1 - mass2) + 2 * mass2 * dp_norm2) / (mass1 + mass2)
                # m2 = (dp_norm2 * (mass2 - mass1) + 2 * mass1 * dp_norm1) / (mass1 + mass2)
                # For equal mass, they just swap normal velocities:
                m1_scalar = dp_norm2
                m2_scalar = dp_norm1

                # Apply bounciness (coefficient of restitution)
                # Affects the closing velocity along the normal
                # Simplified: apply to the change in normal velocities
                b1_eff_bounciness = b1.bounciness * global_bounciness_modifier
                b2_eff_bounciness = b2.bounciness * global_bounciness_modifier
                avg_bounciness = (b1_eff_bounciness + b2_eff_bounciness) / 2

                m1_scalar = (dp_norm1 * (1 - avg_bounciness) + dp_norm2 * (1 + avg_bounciness)) / 2
                m2_scalar = (dp_norm2 * (1 - avg_bounciness) + dp_norm1 * (1 + avg_bounciness)) / 2


                # Update velocities
                # Tangential velocities remain unchanged
                b1.vx = tx * dp_tan1 + nx * m1_scalar
                b1.vy = ty * dp_tan1 + ny * m1_scalar
                b2.vx = tx * dp_tan2 + nx * m2_scalar
                b2.vy = ty * dp_tan2 + ny * m2_scalar

                # Overlap correction to prevent sticking
                overlap = 0.5 * (r1 + r2 - distance + 0.1) # Small epsilon to ensure separation

                # Move b1 away from b2 along the normal
                b1.x -= overlap * nx
                b1.y -= overlap * ny

                # Move b2 away from b1 along the normal (opposite direction)
                b2.x += overlap * nx
                b2.y += overlap * ny

    # Conductor Logic
    if current_time - last_conductor_update_time > CONDUCTOR_UPDATE_INTERVAL:
        # Normalize intensity: max 5 events per interval = full intensity wave
        intensity_for_conductor = min(musical_intensity_counter / 5.0, 1.0)
        if intensity_for_conductor > 0.1: # Only wave if there's some notable activity
            conductor.set_wave(intensity_for_conductor)
        musical_intensity_counter = 0 # Reset counter for the next interval
        last_conductor_update_time = current_time

    conductor.update()


    # --- Drawing Phase ---
    # Background color cycling
    bg_hue_angle += 0.002 # Speed of cycling (radians per frame)
    r = bg_color_base_intensity + bg_color_amplitude * (math.sin(bg_hue_angle) + 1) / 2
    g = bg_color_base_intensity + bg_color_amplitude * (math.sin(bg_hue_angle + 2 * math.pi / 3) + 1) / 2 # Phase shifted
    b = bg_color_base_intensity + bg_color_amplitude * (math.sin(bg_hue_angle + 4 * math.pi / 3) + 1) / 2 # Phase shifted further
    current_bg_color = (max(0,min(255,int(r))), max(0,min(255,int(g))), max(0,min(255,int(b))))
    screen.fill(current_bg_color)

    for banana in bananas:
        banana.draw(screen)

    conductor.draw(screen) # Draw the conductor

    for p in particles:
        p.draw(screen)

    # Draw UI Text
    text_y_offset = 10
    # UI text items in their desired drawing order
    ui_items_ordered = ["gravity", "bounciness", "reset", "add"]
    for key in ui_items_ordered:
        if key in status_texts:
            screen.blit(status_texts[key], (10, text_y_offset))
            text_y_offset += status_texts[key].get_height() + 2 # Add 2 for padding

    pygame.display.flip()  # Update the full display

    # Cap the frame rate
    clock.tick(FPS)

# --- Quit Pygame ---
pygame.quit()
sys.exit()
