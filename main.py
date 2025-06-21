from creature import Creature
import time

def display_welcome_message():
    """Displays a fun welcome message."""
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + " " * 10 + "Welcome to the Whimsical Creature Generator!" + " " * 9 + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\nPrepare to meet some truly unique beings from the depths of imagination!\n")

def main():
    """Main function to run the CLI."""
    display_welcome_message()

    while True:
        try:
            num_creatures_str = input("How many creatures would you like to summon? (Enter a number, or 'quit' to exit): ")

            if num_creatures_str.lower() == 'quit':
                print("\nFarewell, brave adventurer! May your path be filled with whimsy.")
                break

            num_creatures = int(num_creatures_str)
            if num_creatures <= 0:
                print("Please enter a positive number of creatures.")
                continue

            print(f"\nSummoning {num_creatures} creature(s)...\n")
            time.sleep(0.5) # A little dramatic pause

            for i in range(num_creatures):
                print("-" * 20 + f" Creature #{i+1} " + "-" * 20)
                creature = Creature()
                creature.display()
                if num_creatures > 1 and i < num_creatures - 1:
                    time.sleep(1) # Pause between multiple creatures

        except ValueError:
            print("Invalid input. Please enter a number or 'quit'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Optionally, you could log the error here

        print("-" * 60)
        another_round = input("Would you like to summon more creatures? (yes/no): ")
        if another_round.lower() not in ['yes', 'y']:
            print("\nThank you for visiting the menagerie! Goodbye!")
            break
        print("\n")

if __name__ == "__main__":
    main()
