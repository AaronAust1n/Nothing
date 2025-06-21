# Main orchestrator for the Universal Miscommunication Device

from input_handler import get_text_input
from misinterpreter import misinterpret_text
from output_display import display_results

def run_miscommunication_loop():
    """
    Main loop for the Universal Miscommunication Device.
    Gets input, misinterprets it, and displays the result.
    Allows the user to continue or exit.
    """
    print("Welcome to the Universal Miscommunication Device (UMD)!")
    print("----------------------------------------------------")
    print("Type 'exit' or 'quit' to stop the delightful madness.")
    print("----------------------------------------------------\n")

    while True:
        original_text = get_text_input("You say: ")

        if original_text.lower() in ['exit', 'quit']:
            print("\nExiting the UMD. Hope you enjoyed the chaos!")
            break

        if not original_text.strip():
            print("UMD heard silence... and is slightly confused. Try saying something!")
            continue

        misinterpreted_output = misinterpret_text(original_text)
        display_results(original_text, misinterpreted_output)

if __name__ == "__main__":
    run_miscommunication_loop()
