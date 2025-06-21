# Handles the display of original and misinterpreted content

def display_results(original_text: str, misinterpreted_text: str):
    """
    Displays the original input and the misinterpreted output.
    """
    print("\n--- Miscommunication Breakdown ---")
    print(f"You said:        {original_text}")
    print(f"The UMD heard:   {misinterpreted_text}")
    print("--------------------------------\n")

if __name__ == '__main__':
    # Example usage
    display_results("This is a test.", "This is knot a test.")
