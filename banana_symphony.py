# === The Algorithmic Symphony of Bouncing Bananas ===
# A Pygame application where bouncing bananas create generative music and visuals.
# Conceived and coded by Jules, purely for the joy of delightful absurdity.

import pygame
import random
import os
import math # For trigonometric functions, vector math, etc.

# --- Core Game Setup & Display Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60  # Frames Per Second - affects simulation speed and responsiveness

# --- Color Palette ---
# Defines common colors used throughout the application.
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)   # Default rich yellow for bananas
GREEN = (0, 128, 0)      # Used for banana tips, suggesting freshness
BROWN = (139, 69, 19)    # Used for banana stalks
WHITE = (255, 255, 255)  # General purpose (e.g., default particle color)
BACKGROUND_COLOR = BLACK # Initial background color; cycles during runtime for ambiance

# --- Physics & Banana Behavior Constants ---
GRAVITY = 0.5            # Initial gravitational acceleration; adjustable by user (Up/Down arrows)
BOUNCINESS = 0.7         # Default bounciness factor for wall collisions (screen edges)
BANANA_BOUNCINESS_INTERNAL = 0.5 # Bounciness factor for banana-to-banana collisions
MAX_IMPACT_VELOCITY_FOR_SOUND = 20 # Max velocity considered for scaling sound volume and influencing note choice
ROTATION_SPEED_FACTOR = 2  # Multiplier determining how much X/Y movement translates to banana spin

# --- Sound Configuration & Management ---
# All sound files (.wav) are assumed to be in the same directory as this script.

# Generic sound for non-musical events
WALL_HIT_SOUND_FILE = "plink.wav" # Played when a banana hits a side wall or the ceiling

# Musical Scale Definition: C Major Pentatonic (C,D,E,G,A) plus a higher C
# Each key (e.g., "C4") maps to its corresponding .wav filename.
SCALE_NOTE_FILES = {
    "C4": "C4.wav", "D4": "D4.wav", "E4": "E4.wav",
    "G4": "G4.wav", "A4": "A4.wav", "C5": "C5.wav", # C5 provides a higher note for variety
}
musical_notes = {} # This dictionary will store the loaded pygame.Sound objects for the scale notes.
scale_keys_ordered = ["C4", "D4", "E4", "G4", "A4", "C5"] # Defines the pitch order for mapping values (like velocity) to notes.

wall_hit_sound = None # Will hold the loaded pygame.Sound object for wall_hit_sound_file.

# Parameters for Algorithmic Music Generation Logic
NOTE_ZONES_FLOOR = len(scale_keys_ordered) # Used to divide impact velocity range into segments for floor bounce note selection
COLLISION_VELOCITY_FOR_NOTE_CHOICE = 20    # Max relative velocity considered for banana-banana collision note choice

# --- "Juice" - Visual & Experiential Enhancement Parameters ---
MAX_PARTICLES = 100    # Limits the total number of concurrent particles to maintain performance
particles = []         # Global list to hold all active Particle objects

# Defines colors for particles, mapped from the musical note that triggered them
NOTE_COLORS = {
    "C4": (255, 0, 0),   # Red
    "D4": (255, 128, 0), # Orange
    "E4": (255, 255, 0), # Yellow
    "G4": (0, 255, 0),   # Green
    "A4": (0, 0, 255),   # Blue
    "C5": (128, 0, 255)  # Purple
}
DEFAULT_PARTICLE_COLOR = WHITE # Fallback color if a note isn't in NOTE_COLORS

class Particle:
    """
    Represents a single visual particle.
    Particles are typically emitted when a sound is made, adding visual feedback.
    They have a limited lifespan, move, fade, and shrink.
    """
    def __init__(self, x, y, color, size, life):
        """
        Initializes a particle.
        Args:
            x (float): Initial x-coordinate.
            y (float): Initial y-coordinate.
            color (tuple[int, int, int]): RGB color tuple.
            size (float): Initial size (radius for circles).
            life (int): Lifespan in frames.
        """
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)  # Horizontal velocity
        self.vy = random.uniform(-1.5, -0.5) # Vertical velocity (tends to move upwards initially)
        self.color = color
        self.size = size
        self.life = life  # Remaining lifespan in frames

    def update(self):
        """Updates the particle's state for one frame (position, life, size)."""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # A bit of gravity or drag affecting particles
        self.life -= 1
        self.size = max(0, self.size - 0.1) # Particles shrink over time

    def draw(self, screen):
        """Draws the particle on the given screen if it's still alive and visible."""
        if self.life > 0 and self.size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


def create_sound_particles(x, y, note_key):
    """
    Generates a burst of particles at a specified location, colored based on the musical note.
    Args:
        x (float): X-coordinate for particle emission center.
        y (float): Y-coordinate for particle emission center.
        note_key (str): The key of the note (e.g., "C4") that triggered the particles, used for coloring.
    """
    if len(particles) > MAX_PARTICLES - 10: # Optimization: Don't create if particle list is nearly full
        return

    base_particle_color = NOTE_COLORS.get(note_key, DEFAULT_PARTICLE_COLOR)
    num_new_particles = random.randint(5, 10) # Create a small burst

    for _ in range(num_new_particles):
        # Slightly vary color for a more dynamic effect
        color_variation = random.randint(-20, 20) # Small random adjustment to each RGB component
        color = (
            max(0, min(255, base_particle_color[0] + color_variation)),
            max(0, min(255, base_particle_color[1] + color_variation)),
            max(0, min(255, base_particle_color[2] + color_variation))
        )
        size = random.uniform(2, 5)  # Random initial size
        life = random.randint(20, 40) # Random lifespan in frames
        particles.append(Particle(x, y, color, size, life))


class Banana:
    """
    Represents a single bouncing banana.
    Each banana has physics properties, a visual representation (a pre-rendered surface),
    and interacts with the environment and other bananas to produce sounds.
    """
    def __init__(self, x, y, width=40, height=20):
        """
        Initializes a banana.
        Args:
            x (int): Initial x-coordinate of the top-left corner.
            y (int): Initial y-coordinate of the top-left corner.
            width (int): Width of the banana's bounding box.
            height (int): Height of the banana's bounding box (for the arc drawing, actual visual height is more).
        """
        self.rect = pygame.Rect(x, y, width, height) # Collision and positioning rectangle
        self.vx = random.uniform(-3, 3)  # Initial horizontal velocity
        self.vy = random.uniform(-5, 0)  # Initial vertical velocity (usually starts falling)

        self.base_color = YELLOW        # Original color, used for ripening calculations
        self.color = self.base_color    # Current color of the banana body
        self.width = width
        self.height = height

        self.angle = random.uniform(0, 360)  # Initial rotation angle in degrees
        self.angular_velocity = random.uniform(-2, 2) # Initial spin speed in degrees per frame

        self.bounciness = random.uniform(0.65, 0.75) # Individual bounciness for this banana
        self.notes_played = 0            # Counter for how many musical notes this banana has triggered (used for ripening)

        # Pre-render the banana's visual appearance onto a surface for efficient rotation and drawing
        self.surface = pygame.Surface((width, height * 2), pygame.SRCALPHA) # Height * 2 for the arc
        # Note: The self.rect height is for the main body part of the arc, visual banana is taller.
        # This might need adjustment if collision box is to tightly fit the visual.
        # For now, self.rect.height is more like the "thickness" of the banana body.
        # Let's adjust surface creation to be more accurate to drawn shape:
        # The arc is drawn in a rect of (width, height*2), but banana is half of that vertically.
        # The actual visual height of the banana shape is closer to `height`.
        # Let's make the surface `(width, height)` and adjust drawing coordinates in `draw_banana_shape`.
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)


        self.last_played_note_time = 0   # Timestamp of the last note played by this banana (for sound cooldown)
        self.draw_banana_shape()         # Create the initial visual of the banana

    def draw_banana_shape(self):
        """
        Draws the banana's shape onto its `self.surface`.
        This includes the main yellow body (an arc), a brown stalk, and a green tip.
        Uses `self.color` for the body, allowing for ripening effects.
        """
        self.surface.fill((0,0,0,0)) # Clear surface with transparency

        # Main body (arc) - drawn to fill the surface height.
        # The arc is part of an ellipse of self.width and self.height*2, but we only take a segment.
        # To make it fit self.height, the arc's bounding box for drawing is (0,0,self.width, self.height)
        # and the arc itself is drawn to look like half of an ellipse.
        # Let's use a bounding box that is self.width x (self.height * 2) but ensure arc is centered.
        # The true bounding box of the banana visual is roughly self.width x self.height.
        # The arc method: pygame.draw.arc(surface, color, rect, start_angle, stop_angle, width)
        # We want a crescent. Rect is the bounding box of the *ellipse* the arc is part of.
        # To make a banana shape of height `h`, the ellipse might be `w x 2h`.
        # Centering it on a surface of `w x h`:
        pygame.draw.arc(self.surface, self.color, (0, 0, self.width, self.height * 2),
                        math.pi * 1.05, math.pi * 1.95, self.height // 2 +1) # Thicker arc

        # Stalk (small rectangle) - positioned at one end of the arc
        stalk_width = self.width // 8
        stalk_height = self.height // 3
        # Position relative to the arc. Assuming arc points "upwards" or "downwards" on the surface.
        # If arc is like a smile, stalk at one end.
        pygame.draw.rect(self.surface, BROWN, (stalk_width //2 , self.height // 2 - stalk_height, stalk_width, stalk_height))

        # Tip (small circle) - positioned at the other end
        tip_radius = self.width // 10
        pygame.draw.circle(self.surface, GREEN, (self.width - tip_radius - stalk_width//2, self.height // 2), tip_radius)


    def update(self):
        """Updates the banana's state for one frame (physics, sound events, ripening)."""
        # --- Physics ---
        self.vy += GRAVITY  # Apply gravity
        self.angle = (self.angle + self.angular_velocity) % 360 # Update rotation
        self.rect.x += self.vx # Move horizontally
        self.rect.y += self.vy # Move vertically

        current_time = pygame.time.get_ticks() # For sound cooldowns

        # --- Collision with Screen Edges & Sound Events ---
        # Left wall
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx *= -BOUNCINESS # Reverse horizontal velocity, apply wall bounciness
            self.angular_velocity = -self.angular_velocity * BOUNCINESS + self.vy * 0.1 # Spin on wall hit
            if wall_hit_sound and (current_time - self.last_played_note_time > 100): # Cooldown
                wall_hit_sound.play()
                self.last_played_note_time = current_time
        # Right wall
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vx *= -BOUNCINESS
            self.angular_velocity = -self.angular_velocity * BOUNCINESS - self.vy * 0.1
            if wall_hit_sound and (current_time - self.last_played_note_time > 100):
                wall_hit_sound.play()
                self.last_played_note_time = current_time

        # Ceiling
        if self.rect.top < 0:
            self.rect.top = 0
            self.vy *= -BOUNCINESS # Reverse vertical velocity
            self.angular_velocity += self.vx * 0.1 # Spin on ceiling hit
            # Optional: Play wall_hit_sound for ceiling too, or a different sound
            if wall_hit_sound and (current_time - self.last_played_note_time > 100):
                 wall_hit_sound.play() # Using same wall hit sound for now
                 self.last_played_note_time = current_time
        # Floor
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            impact_vy = abs(self.vy) # Magnitude of vertical velocity at impact

            # Play musical note on significant floor bounce
            if impact_vy > GRAVITY * 1.5 :
                if musical_notes and (current_time - self.last_played_note_time > 100): # Cooldown
                    # Determine note based on impact velocity
                    note_idx = min(len(scale_keys_ordered) - 1, int((impact_vy / MAX_IMPACT_VELOCITY_FOR_SOUND) * len(scale_keys_ordered)))
                    note_to_play_key = scale_keys_ordered[note_idx]
                    sound_to_play = musical_notes.get(note_to_play_key)

                    if sound_to_play:
                        volume = min(1.0, impact_vy / MAX_IMPACT_VELOCITY_FOR_SOUND) # Scale volume
                        sound_to_play.set_volume(volume)
                        sound_to_play.play()
                        create_sound_particles(self.rect.centerx, self.rect.bottom, note_to_play_key) # Visual feedback
                        self.last_played_note_time = current_time
                        self.notes_played += 1 # For ripening

            self.vy *= -self.bounciness # Reverse vertical velocity, use individual bounciness
            self.angular_velocity *= 0.95 # Dampen spin on floor bounce
            self.vx *= 0.98 # Apply some friction to horizontal movement

            # Rest condition: if moving very slowly on the floor, stop vertical movement and reduce horizontal/spin
            if abs(self.vy) < GRAVITY * 1.5 : # Effectively GRAVITY threshold for stopping bounce
                 self.vy = 0
                 self.vx *= 0.9 # Extra friction when nearly stopped
                 if abs(self.vx) < 0.1: self.vx = 0
                 if abs(self.angular_velocity) < 0.1: self.angular_velocity = 0 # Stop spinning when resting
            if self.rect.bottom == SCREEN_HEIGHT and self.vy == 0: # If resting on floor
                self.vx *= 0.95 # Continuous friction while on ground

        # --- Ripening Logic ---
        # Banana "ripens" (changes color) every 10 notes it plays.
        if self.notes_played > 0 and self.notes_played % 10 == 0:
            ripening_stage = min(5, self.notes_played // 10) # Max 5 stages of ripening

            # Base color is YELLOW (255, 220, 0). Ripening makes it more orange/brown.
            new_green = max(0, self.base_color[1] - ripening_stage * 20) # Reduce green component
            new_red = min(255, self.base_color[0] + ripening_stage * 5)   # Slightly increase red

            # Update color and redraw surface only if color actually changes
            if self.color != (new_red, new_green, self.base_color[2]):
                self.color = (new_red, new_green, self.base_color[2])
                self.draw_banana_shape() # Re-render the banana's surface with the new color
            # Note: self.notes_played continues to accumulate, but ripening effect is capped.
            # To make it re-trigger, notes_played could be reset or handled differently,
            # but for now, this ensures it doesn't try to redraw the surface every frame once ripened.


    def draw(self, screen):
        """Draws the (potentially rotated) banana onto the main screen."""
        # Rotate the pre-rendered banana surface
        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        # Get the new rectangle for the rotated surface, centering it on the banana's original center
        new_rect = rotated_surface.get_rect(center = self.rect.center)
        screen.blit(rotated_surface, new_rect.topleft) # Draw the rotated surface

def handle_banana_collisions(bananas):
    """
    Handles collisions between all pairs of bananas.
    Implements a simplified elastic collision response and triggers musical notes.
    Args:
        bananas (list[Banana]): A list of all active Banana objects.
    """
    global screen_shake_timer # Access global for triggering screen shake
    num_bananas = len(bananas)

    # Iterate through all unique pairs of bananas
    for i in range(num_bananas):
        for j in range(i + 1, num_bananas):
            b1 = bananas[i]
            b2 = bananas[j]

            # Check for collision using rectangle overlap
            if b1.rect.colliderect(b2.rect):
                # --- Collision Physics (Simplified 1D Elastic Collision along Normal) ---
                # Calculate normal vector between banana centers
                dx = b2.rect.centerx - b1.rect.centerx
                dy = b2.rect.centery - b1.rect.centery
                distance = math.sqrt(dx*dx + dy*dy)
                if distance == 0: distance = 1 # Avoid division by zero if perfectly overlapped

                nx = dx / distance # Normalized x-component of normal
                ny = dy / distance # Normalized y-component of normal

                # Relative velocity components
                rvx = b1.vx - b2.vx
                rvy = b1.vy - b2.vy

                # Velocity along the normal direction
                vel_along_normal = rvx * nx + rvy * ny

                # Do not resolve if velocities are already separating (prevents sticking/re-collision)
                if vel_along_normal > 0:
                    continue

                # Calculate impulse scalar (assuming equal mass for all bananas for simplicity)
                e = BANANA_BOUNCINESS_INTERNAL # Coefficient of restitution for banana-banana
                impulse_scalar = -(1 + e) * vel_along_normal
                # impulse_scalar /= (1/mass1 + 1/mass2) # If mass were variable, it'd be here.
                                                       # For mass=1, this is impulse_scalar / 2.
                                                       # However, the common 1D formula applies impulse directly.
                                                       # Let's use the standard formula where impulse is distributed.

                # Apply impulse to change velocities
                # (Assuming mass = 1 for both, so impulse is directly applied to velocity change)
                b1.vx -= impulse_scalar * nx
                b1.vy -= impulse_scalar * ny
                b2.vx += impulse_scalar * nx
                b2.vy += impulse_scalar * ny

                # Adjust angular velocity based on collision (add some spin)
                b1.angular_velocity += random.uniform(-1,1) * vel_along_normal * 0.05 # Reduced factor
                b2.angular_velocity -= random.uniform(-1,1) * vel_along_normal * 0.05 # Reduced factor

                # --- Musical Note & Effects for Banana Collision ---
                current_time = pygame.time.get_ticks()
                # Cooldown to prevent sound spam from a single prolonged collision event
                if musical_notes and \
                   (current_time - b1.last_played_note_time > 100) and \
                   (current_time - b2.last_played_note_time > 100):

                    rel_vel_mag = math.sqrt(rvx**2 + rvy**2) # Magnitude of relative velocity
                    # Choose note based on collision energy (approximated by relative velocity)
                    note_idx = min(len(scale_keys_ordered) - 1, int((rel_vel_mag / COLLISION_VELOCITY_FOR_NOTE_CHOICE) * len(scale_keys_ordered)))
                    note_to_play_key = scale_keys_ordered[note_idx]
                    sound_to_play = musical_notes.get(note_to_play_key)

                    if sound_to_play:
                        volume = min(1.0, rel_vel_mag / MAX_IMPACT_VELOCITY_FOR_SOUND)
                        sound_to_play.set_volume(volume)

                        channel = pygame.mixer.find_channel(True) # Find an available channel
                        if channel:
                            channel.play(sound_to_play)
                            # Create particles at collision midpoint
                            mid_x = (b1.rect.centerx + b2.rect.centerx) / 2
                            mid_y = (b1.rect.centery + b2.rect.centery) / 2
                            create_sound_particles(mid_x, mid_y, note_to_play_key)

                            # Update last played time and notes counter for both bananas
                            b1.last_played_note_time = current_time
                            b2.last_played_note_time = current_time
                            b1.notes_played += 1
                            b2.notes_played += 1

                            # Trigger screen shake on energetic collisions
                            if rel_vel_mag > COLLISION_VELOCITY_FOR_NOTE_CHOICE * 0.8:
                                screen_shake_timer = max(screen_shake_timer, 10) # Shake for 10 frames

                # --- Resolve Overlap (Anti-sticking) ---
                # Simple position correction to prevent bananas from getting stuck inside each other.
                overlap = (b1.width / 2 + b2.width / 2) - distance # Approximate overlap based on centers and widths
                if overlap > 0 :
                    separation_factor = 0.5 # How much to push them apart
                    move_x = overlap * nx * separation_factor
                    move_y = overlap * ny * separation_factor
                    b1.rect.x -= move_x
                    b1.rect.y -= move_y
                    b2.rect.x += move_x
                    b2.rect.y += move_y


def main():
    """
    Main function to initialize the game, run the game loop, and handle events.
    """
    # Declare globals that are modified in this function for clarity (though Python handles module-level globals)
    global GRAVITY, BACKGROUND_COLOR, screen_shake_timer
    # Note: wall_hit_sound, musical_notes, particles are also global but primarily modified elsewhere or read here.

    pygame.init()      # Initialize all Pygame modules
    pygame.mixer.init() # Initialize Pygame's sound mixer
    pygame.mixer.set_num_channels(16) # Increase available audio channels for more simultaneous sounds

    # --- Initialize Game Variables ---
    screen_shake_timer = 0 # Duration for screen shake effect, in frames

    # Background color cycling setup
    bg_color_idx = 0
    bg_colors_palette = [ # A palette of gentle, darkish colors for the background
        (20, 20, 30), (30, 20, 20), (20, 30, 20), (30, 30, 40), (25, 25, 25)
    ]
    BACKGROUND_COLOR = bg_colors_palette[bg_color_idx]
    bg_change_timer = 0 # Timer to track when to change background color
    BG_CHANGE_INTERVAL = FPS * 10 # Change background color every 10 seconds

    # --- Load Sound Assets ---
    # Load general wall hit sound
    wall_hit_sound_path = os.path.join(os.path.dirname(__file__), WALL_HIT_SOUND_FILE)
    if os.path.exists(wall_hit_sound_path):
        try:
            wall_hit_sound = pygame.mixer.Sound(wall_hit_sound_path) # Direct assignment to module-level global
        except pygame.error as e:
            print(f"Could not load sound file '{WALL_HIT_SOUND_FILE}': {e}")
            wall_hit_sound = None # Ensure it's None if loading fails
    else:
        print(f"Wall hit sound file '{WALL_HIT_SOUND_FILE}' not found.")
        wall_hit_sound = None

    # Load musical note samples
    for note_key, note_filename in SCALE_NOTE_FILES.items():
        note_path = os.path.join(os.path.dirname(__file__), note_filename)
        if os.path.exists(note_path):
            try:
                musical_notes[note_key] = pygame.mixer.Sound(note_path) # musical_notes is global
            except pygame.error as e:
                print(f"Could not load note '{note_filename}': {e}")
        else:
            print(f"Note file '{note_filename}' for note '{note_key}' not found.")

    if not musical_notes:
        print("Warning: No musical notes were loaded. The symphony will be very quiet!")

    # --- Pygame Display Setup ---
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Algorithmic Symphony of Bouncing Bananas")
    clock = pygame.time.Clock() # Clock for controlling FPS

    # --- Initialize Game Objects ---
    bananas = [Banana(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 200)) for _ in range(5)]
    # Spawn a couple more bananas near center for initial collision testing, if screen is large enough
    if len(bananas) < 2 and SCREEN_WIDTH > 100 and SCREEN_HEIGHT > 100:
         bananas.append(Banana(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, width=40, height=20))
         bananas.append(Banana(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2, width=40, height=20))

    # --- Main Game Loop ---
    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Handle window close button
                running = False

            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1: # Left click: Spawn a new banana at mouse position
                    new_banana = Banana(mouse_pos[0], mouse_pos[1], width=40, height=20)
                    new_banana.vy = random.uniform(-2, -5) # Give it a little upward pop
                    bananas.append(new_banana)

                elif event.button == 3: # Right click: Nudge nearby bananas
                    nudge_strength = 5 # How strong the nudge is
                    for b in bananas:
                        dist_x = b.rect.centerx - mouse_pos[0]
                        dist_y = b.rect.centery - mouse_pos[1]
                        distance = math.sqrt(dist_x**2 + dist_y**2)
                        if distance < 50: # Nudge if mouse is within 50 pixels of banana center
                            if distance == 0: distance = 1 # Avoid division by zero
                            # Apply force outwards from the mouse cursor
                            b.vx += (dist_x / distance) * nudge_strength
                            b.vy += (dist_y / distance) * nudge_strength
                            b.angular_velocity += random.uniform(-2,2) # Add some spin

            # Keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Spacebar: Spawn a banana at a random top position
                    bananas.append(Banana(random.randint(0, SCREEN_WIDTH - 40), random.randint(0, 50), width=40, height=20))
                elif event.key == pygame.K_UP: # Up arrow: Increase gravity
                    GRAVITY = min(2.0, GRAVITY + 0.05) # Cap maximum gravity
                    print(f"Gravity increased to: {GRAVITY:.2f}")
                elif event.key == pygame.K_DOWN: # Down arrow: Decrease gravity
                    GRAVITY = max(0.05, GRAVITY - 0.05) # Cap minimum gravity (must be > 0)
                    print(f"Gravity decreased to: {GRAVITY:.2f}")

        # --- Game Logic Updates ---
        # Update all bananas
        for banana_obj in bananas: # Use banana_obj to avoid conflict with banana module name
            banana_obj.update()

        # Handle collisions between bananas
        handle_banana_collisions(bananas)

        # Update all active particles
        particles[:] = [p for p in particles if p.life > 0] # Efficiently remove dead particles
        for p in particles:
            p.update()

        # Background color cycling logic
        bg_change_timer += 1
        if bg_change_timer >= BG_CHANGE_INTERVAL:
            bg_change_timer = 0
            bg_color_idx = (bg_color_idx + 1) % len(bg_colors_palette)
            BACKGROUND_COLOR = bg_colors_palette[bg_color_idx]

        # Screen shake timer update
        screen_offset_x, screen_offset_y = 0, 0
        if screen_shake_timer > 0:
            screen_shake_timer -= 1
            screen_offset_x = random.randint(-5, 5) # Random offset for X
            screen_offset_y = random.randint(-5, 5) # Random offset for Y

        # --- Drawing & Rendering ---
        screen.fill(BACKGROUND_COLOR) # Clear screen with current background color

        # Screen Shake Implementation:
        # If shaking, render the entire scene to a temporary surface, then blit that surface
        # to the main screen at the calculated offset. This is less efficient than a camera system
        # but provides a simple full-screen shake effect.
        if screen_shake_timer > 0 :
            temp_surface = screen.copy() # Create a temporary drawing surface
            temp_surface.fill(BACKGROUND_COLOR) # Fill temp surface
            # Draw game objects to the temporary surface
            for banana_obj in bananas:
                banana_obj.draw(temp_surface)
            for p in particles:
                p.draw(temp_surface)
            # Blit the shaken temporary surface to the main screen
            screen.blit(temp_surface, (screen_offset_x, screen_offset_y))
        else: # No screen shake: Draw directly to the main screen
            for banana_obj in bananas:
                banana_obj.draw(screen)
            for p in particles:
                p.draw(screen)

        pygame.display.flip() # Update the full display
        clock.tick(FPS)       # Maintain the desired frame rate

    pygame.quit() # Uninitialize Pygame modules when the loop ends

if __name__ == "__main__":
    # This ensures main() is called only when the script is executed directly
    main()
