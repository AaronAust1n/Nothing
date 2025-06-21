# Whimsical Creature Generator

Welcome to the Whimsical Creature Generator! This Python script conjures up fantastical, absurd, and hopefully delightful creatures from the digital ether. Each creature comes complete with a unique name, a quirky description, a charmingly nonsensical backstory, and its very own ASCII art portrait.

## Features

*   Randomly generated creature names, appearances, abilities, habits, and personalities.
*   ASCII art representation of each unique creature.
*   A simple command-line interface to summon your new friends.

## Running the Generator

1.  Ensure you have Python 3 installed.
2.  Navigate to the root directory of this project in your terminal.
3.  Run the script using:
    ```bash
    python main.py
    ```
4.  Follow the on-screen prompts to decide how many creatures to generate.
5.  Marvel at the beings that appear!

## Project Structure

*   `main.py`: The main executable script for the CLI.
*   `creature.py`: Contains the `Creature` class that orchestrates creature generation.
*   `creature_parts/`: This directory holds modules for generating different textual components of a creature:
    *   `names.py`: Generates creature names.
    *   `body.py`: Generates body features and colors.
    *   `characteristics.py`: Generates abilities, habits, and personality traits.
    *   `backstory.py`: Generates whimsical backstories.
*   `ascii_art/`: This directory is responsible for the visual aspect:
    *   `parts_library.py`: A collection of predefined ASCII art snippets for various body parts.
    *   `engine.py`: The `AsciiArtEngine` class that assembles parts from the library into a full creature image.

## Have Fun!

This project was created for the joy of it. Feel free to expand upon it, add new creature parts, characteristics, or even more elaborate ASCII art. The only limit is your imagination!
