# The Algorithmic Symphony of Bouncing Bananas

Welcome to a world of delightful absurdity! "The Algorithmic Symphony of Bouncing Bananas" is a Python application where physics, generative art, and algorithmic music collide in a cascade of spinning, bouncing, and musically expressive bananas. This project was created purely for the joy of it, embracing the unexpected and the fun.

## How to Run

1.  **Ensure Pygame is installed:**
    If you don't have Pygame, you can install it via pip:
    ```bash
    pip install pygame
    ```

2.  **Get the Sound Files:**
    This simulation relies on several `.wav` sound files for its full auditory experience. Please ensure the following files are present in the same directory as `banana_symphony.py`:
    *   `plink.wav` (for wall/ceiling hits)
    *   `C4.wav`
    *   `D4.wav`
    *   `E4.wav`
    *   `G4.wav`
    *   `A4.wav`
    *   `C5.wav`
    (These form a C Major Pentatonic scale + a higher C, but you can experiment with your own .wav files by editing `SCALE_NOTE_FILES` in the script!)

3.  **Run the Symphony:**
    Execute the Python script:
    ```bash
    python banana_symphony.py
    ```

## Features

*   **Bouncing Banana Physics:** Watch as bananas, each with slightly unique bounciness, tumble and spin under (adjustable!) gravity.
*   **Algorithmic Music Generation:**
    *   Bananas play musical notes from a C Major Pentatonic scale when they hit the floor or collide with each other.
    *   The specific note and its volume are determined by the impact velocity or collision energy.
    *   Wall and ceiling hits produce a distinct "plink" sound.
*   **Dynamic Visuals:**
    *   Each banana is a lovingly drawn (well, arced) rotating sprite.
    *   **Particle Effects:** Colorful particles burst forth when notes are played, their color corresponding to the note's pitch.
    *   **Banana Ripening:** Bananas subtly change color (ripening!) as they participate more in the musical mayhem.
    *   **Screen Shake:** Energetic collisions trigger a satisfying screen shake.
    *   **Cycling Background:** The background color slowly transitions through a palette of gentle, ambient tones.
*   **User Interaction:**
    *   **Left Mouse Click:** Spawn a new banana at the cursor position. Give it a little toss!
    *   **Right Mouse Click:** Gently "nudge" any bananas near your cursor.
    *   **UP/DOWN Arrow Keys:** Increase or decrease the force of gravity, changing the tempo and feel of the simulation.
    *   **SPACE Bar:** Spawn a banana at a random position near the top of the screen.

## The "Music" System Explained

The core of the symphony lies in how banana interactions are translated into sound:
*   A predefined musical scale (C Major Pentatonic: C, D, E, G, A, plus a higher C5) is used. Each note requires a corresponding `.wav` file.
*   **Floor Bounces:** When a banana hits the floor with enough force, it triggers a note. The impact velocity determines which note in the scale is played (higher velocity can mean a higher note) and how loud it is.
*   **Banana Collisions:** When two bananas collide, they also trigger a musical note. The intensity of the collision (relative velocity) influences the note choice and volume.
*   **Sound Cooldown:** A brief cooldown period prevents a single banana or collision from spamming sounds too rapidly, allowing for a clearer (though still potentially chaotic!) soundscape.
*   **Polyphony:** The system uses multiple Pygame mixer channels to allow several notes to play simultaneously.

## A Note on Absurdity

This project is an experiment in emergent behavior and creative coding. The "symphony" produced is entirely dependent on the physics, the user's interaction, and a healthy dose of randomness. Embrace the chaos, enjoy the unexpected harmonies (and dissonances!), and have fun!

---
Created with joy by Jules.
