import argparse
import os
import datetime
from analyzer import analyze_code
from generator import generate_poem

# Ensure the poems directory exists
POEMS_DIR = os.path.join(os.path.dirname(__file__), "..", "poems")
if not os.path.exists(POEMS_DIR):
    os.makedirs(POEMS_DIR)

def read_file_content(filepath: str) -> str | None:
    """Reads the content of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def save_poem(poem_content: str, source_filename: str) -> None:
    """Saves the poem to a file in the poems directory."""
    base_source_name = os.path.splitext(os.path.basename(source_filename))[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    poem_filename = f"{base_source_name}_poem_{timestamp}.txt"
    poem_filepath = os.path.join(POEMS_DIR, poem_filename)

    try:
        with open(poem_filepath, 'w', encoding='utf-8') as f:
            f.write(poem_content)
        print(f"\\nPoem saved to: {poem_filepath}")
    except Exception as e:
        print(f"Error saving poem to {poem_filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(description="The Algorithmic Bard: Generates poems from Python source code.")
    parser.add_argument("filepath", help="Path to the Python file to poeticize.")

    args = parser.parse_args()
    source_filepath = args.filepath

    print(f"The Algorithmic Bard gazes upon: {source_filepath}\\n")

    code_content = read_file_content(source_filepath)
    if code_content is None:
        return

    analysis_results = analyze_code(code_content)
    if not analysis_results.get("functions") and \
       not analysis_results.get("classes") and \
       not analysis_results.get("variables"):
        print("The Bard found the scroll empty of grand tales (no functions, classes, or variables detected).")
        # Still generate a simple "empty" poem
        poem = generate_poem(analysis_results)
    else:
        print("The Bard ponders the essence of the code...")
        # print("Debug: Analysis Results:", analysis_results) # For debugging
        poem = generate_poem(analysis_results)

    print("\\n--- Your Poem ---")
    print(poem)

    save_poem(poem, source_filepath)

if __name__ == "__main__":
    # To test this, you would run from the root `algorithmic_bard` directory:
    # python src/bard.py src/analyzer.py
    # or
    # python src/bard.py src/generator.py
    #
    # For a quick internal test (though not using argparse):
    # Create a dummy file for testing if needed, or use existing ones.
    # For example, to simulate:
    # args = parser.parse_args(["src/analyzer.py"])
    # main() would then run with this.
    #
    # Better to run via command line to test fully.
    # Example:
    # 1. Ensure you are in the `algorithmic_bard` directory.
    # 2. Run: `python src/bard.py src/analyzer.py`
    main()
