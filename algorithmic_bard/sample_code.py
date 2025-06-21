# A sample Python script for the Algorithmic Bard to ponder.

# A noble constant
THE_ANSWER = 42

# A class of great import
class Greeter:
    """A friendly class that offers greetings."""
    default_greeting = "Salutations"

    def __init__(self, name: str):
        self.name = name # An instance variable, not captured by current analyzer's "variables" list

    def greet(self, specific_message: str = None):
        """Generates a greeting message."""
        message_to_send = specific_message or Greeter.default_greeting
        # 'message_to_send' is a local variable, should be captured.
        return f"{self.name} says: {message_to_send}, and knows THE_ANSWER is {THE_ANSWER}!"

# A standalone function of utility
def combine_strings(str1: str, str2: str) -> str:
    """Combines two strings with a space."""
    # 'combined' is a local variable, should be captured.
    combined = str1 + " " + str2
    internal_var = "hidden" # another local variable
    return combined

# Some global variables
hero_name = "Sir Codealot"
quest_item = "The Golden Semicolon"

if __name__ == "__main__":
    print("Sample code is preparing for poetic analysis...")
    greeter_instance = Greeter("Bard")
    # 'greeter_instance' is a local variable in __main__, should be captured if main is analyzed.
    # However, the bard analyzes the file as a string, not by running it, so __main__ context is just more code.

    greeting = greeter_instance.greet("Good day")
    # 'greeting' is a local variable.
    print(greeting)

    combined_text = combine_strings("Code", "Poetry")
    # 'combined_text' is a local variable.
    print(combined_text)

    # Let's see what the analyzer picks up from this __main__ block if the whole file is fed.
    # It should pick up 'greeter_instance', 'greeting', 'combined_text' as variables.
    # And 'Greeter', 'combine_strings', 'THE_ANSWER', 'hero_name', 'quest_item'
    # and the function names 'greet', '__init__'.
    # Plus, local vars inside functions like 'message_to_send', 'combined', 'internal_var'.
    pass
