import time
import os

from ephemeral_echo_garden.garden import Garden
from ephemeral_echo_garden.text_visualizer import TextVisualizer

# --- Configuration ---
INITIAL_QUOTE = "The silence of eternity, interpreted by love."
# Alt Quotes:
# "A fleeting glimpse of impossible geometries."
# "Whispers of starlight in a digital dawn."
# "Where logic dances with chaotic grace."

GARDEN_WIDTH = 100  # Characters
GARDEN_HEIGHT = 40 # Characters
SIMULATION_STEPS = 60  # Reduced for faster testing
FRAME_DELAY = 0.05  # Reduced for faster testing
ENABLE_COLORS = True # Set to False if your terminal has issues with ANSI colors

# --- Interaction Settings ---
ENABLE_INTERACTION = True # Set to False to disable user input during simulation
INTERACTION_PROMPT_INTERVAL = 15 # Reduced for more frequent interaction testing

def get_user_input_non_blocking():
    """
    Attempts to get user input without blocking the main loop.
    This is a very basic approach and might not work reliably on all systems
    or without dedicated libraries like 'select' or 'msvcrt'.
    For this project, we'll simulate it with a simple prompt that expects quick input.
    A more robust solution is out of scope for pure Python standard library on all OS.
    """
    # This is a placeholder for true non-blocking input.
    # In a real scenario, you'd use select.select on sys.stdin for POSIX
    # or msvcrt.kbhit() / msvcrt.getch() on Windows.
    # For simplicity, we'll just use a timed input, which IS blocking.
    # The alternative is to prompt less frequently or make it a distinct phase.

    # Given the constraints, we will use standard input() which is blocking.
    # The 'non-blocking' aspect will be handled by prompting infrequently.
    try:
        # Move cursor to a line below the garden for the prompt
        # The number of lines depends on GARDEN_HEIGHT + a few for status
        # This is tricky without curses; \033[<L>;<C>H can move cursor
        # Assuming visualizer clears screen and prints garden, then status line.
        # We print the prompt *after* the visualizer's output.
        prompt_line = GARDEN_HEIGHT + 2
        # \033[s (save cursor) \033[<L>;0H (move to line) <prompt> \033[u (restore cursor)
        # This is still a bit of a hack.
        # A simpler way: just print the prompt and let it scroll.

        print(f"\033[{prompt_line};0H\033[K", end='') # Move to line, clear it
        print("Enter a new word or phrase to sow (or press Enter to skip): ", end='', flush=True)

        # A true non-blocking read is hard. We will use a timeout mechanism
        # which is not available in standard input() directly.
        # For this exercise, we'll stick to blocking input when prompted.
        user_text = input()
        return user_text.strip()
    except EOFError: # If stdin is closed
        return None
    except KeyboardInterrupt:
        raise # Re-raise to be caught by main loop


def run_simulation():
    """Initializes and runs the Ephemeral Echo Garden simulation."""

    print("Initializing Ephemeral Echo Garden...")
    print(f"Quote: \"{INITIAL_QUOTE}\"")
    print(f"Garden Size: {GARDEN_WIDTH}x{GARDEN_HEIGHT}")
    print(f"Simulation Steps: {SIMULATION_STEPS}")
    print(f"Frame Delay: {FRAME_DELAY}s")
    print(f"Colors: {'Enabled' if ENABLE_COLORS else 'Disabled'}")
    time.sleep(2) # Pause to read config

    try:
        garden = Garden(initial_quote=INITIAL_QUOTE, width=GARDEN_WIDTH, height=GARDEN_HEIGHT)
        visualizer = TextVisualizer(GARDEN_WIDTH, GARDEN_HEIGHT, use_colors=ENABLE_COLORS)

        # Sow the initial quote into the garden
        # Center the initial phrase roughly
        initial_sow_position = (GARDEN_WIDTH / 2, GARDEN_HEIGHT / 2)
        garden.sow_phrase(INITIAL_QUOTE, base_position=initial_sow_position)

        print("Simulation starting... Press Ctrl+C to exit early.")
        time.sleep(1)

        for step in range(SIMULATION_STEPS):
            garden.evolve()
            render_data = garden.get_renderable_flowers()
            visualizer.render(render_data)

            current_status = f"Step: {step+1}/{SIMULATION_STEPS} | Entities: {len(render_data)} | Time Factor: {garden.current_time_effect:.2f}"
            # Print status below the garden. Visualizer already prints a footer.
            # We need to make sure this status line is correctly positioned.
            # The visualizer's last print is its own footer. We add to that.
            # The visualizer should be modified to accept an extra status line or leave space.
            # For now, let's assume visualizer prints its content, then its footer.
            # This print command will appear after the visualizer's output.

            # Interaction Point
            if ENABLE_INTERACTION and (step + 1) % INTERACTION_PROMPT_INTERVAL == 0:
                # The get_user_input_non_blocking is actually blocking for now.
                # It will print its own prompt.
                try:
                    # To make the prompt appear nicely, we should print it *after* visualizer's full output.
                    # The visualizer clears the screen.
                    # So, the prompt should be printed by get_user_input_non_blocking
                    # *after* visualizer.render() has completed.
                    # The current structure of get_user_input_non_blocking attempts to position cursor.

                    # Let's ensure the main status is printed before asking for input.
                    # The visualizer prints: Garden content, then its own footer.
                    # We want: Garden content, Garden footer, Sim status, then Input prompt.
                    # This is getting complex without a dedicated screen management library like curses.

                    # Simplification: Visualizer prints garden. Main loop prints status. Then prompt.
                    # The visualizer.render() already clears and prints.
                    # The status line will be printed by the visualizer.
                    # The prompt will be printed by get_user_input_non_blocking.

                    # Modify visualizer to take an extra status line.
                    # visualizer.render(render_data, current_status) # Ideal
                    # For now, the visualizer has its own footer. We'll let input overwrite last lines.

                    user_text = get_user_input_non_blocking() # This is blocking.
                    if user_text:
                        # Sow user's text at a random position
                        rand_x = garden.rng.uniform(garden.width * 0.1, garden.width * 0.9)
                        rand_y = garden.rng.uniform(garden.height * 0.1, garden.height * 0.9)
                        garden.sow_phrase(user_text, base_position=(rand_x, rand_y))

                        # Render one more frame immediately to show the new flower starting to grow
                        # And to clear the input prompt text from the screen.
                        garden.evolve() # Evolve once more to make it appear
                        visualizer.render(garden.get_renderable_flowers())

                except KeyboardInterrupt: # Allow Ctrl+C during input
                    raise
                except EOFError: # If stdin is closed during input
                    print("\nInput stream closed. Disabling further interaction.")
                    ENABLE_INTERACTION = False # Disable further attempts

            time.sleep(FRAME_DELAY)

        # Final clear and message
        if os.name == 'nt': os.system('cls')
        else: os.system('clear')
        print("\nSimulation finished.")

    except KeyboardInterrupt:
        print("\nSimulation interrupted by user. Exiting.")
    except Exception as e:
        # Clear screen one last time to show error cleanly
        if os.name == 'nt': os.system('cls')
        else: os.system('clear')
        print(f"An error occurred during the simulation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print(f"{COLORS['reset']}Thank you for visiting the Ephemeral Echo Garden!")


if __name__ == "__main__":
    run_simulation()
