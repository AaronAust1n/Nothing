# Handles input for the Universal Miscommunication Device

def get_text_input(prompt: str = "Enter your message: ") -> str:
    """
    Prompts the user for text input.
    """
    return input(prompt)

if __name__ == '__main__':
    # Example usage
    message = get_text_input()
    print(f"You entered: {message}")
