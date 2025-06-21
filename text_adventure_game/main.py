# main.py - Game entry point and main loop

import player
import world
import parser

# Global player object
player_instance = None

def print_current_location():
    """Prints the description of the player's current location."""
    global player_instance
    if not player_instance:
        return

    room_data = world.get_room_data(player_instance.current_room_id)
    if room_data:
        print(f"\n--- {room_data['name']} ---")
        print(room_data['description'])

        # Display items in the room
        if room_data.get("items"):
            print("\nYou see here:")
            for item_id in room_data["items"]:
                item_data = world.get_item_data(item_id)
                if item_data:
                    print(f"- {item_data['name']}")

        # Display characters in the room
        if room_data.get("characters"):
            print("\nCharacters present:")
            for char_id in room_data["characters"]:
                char_data = world.get_character_data(char_id)
                if char_data:
                    print(f"- {char_data['name']}")

        print("Exits:", ", ".join(room_data['exits'].keys()) if room_data['exits'] else "None")
    else:
        print("Error: Current room data not found!")

def handle_command(command, argument):
    """Processes the parsed command."""
    global player_instance
    if not player_instance:
        print("Error: Player not initialized.")
        return True # Signal to quit

    if command == "quit":
        print("Thanks for playing CodeCraft! Goodbye.")
        return True # Signal to quit

    elif command == "look" or command == "l":
        print_current_location()

    elif command == "look_at":
        # First, check if it's an item in the room
        current_room_data = world.get_room_data(player_instance.current_room_id)
        found_item = None
        if argument:
            for item_id in current_room_data.get("items", []):
                item_data = world.get_item_data(item_id)
                if item_data and argument.lower() in item_data["name"].lower():
                    found_item = item_data
                    break
            # If not in room, check player's inventory
            if not found_item:
                for item_id in player_instance.inventory:
                    item_data = world.get_item_data(item_id)
                    if item_data and argument.lower() in item_data["name"].lower():
                        found_item = item_data
                        break
            # Check characters in the room
            if not found_item:
                 for char_id in current_room_data.get("characters", []):
                    char_data = world.get_character_data(char_id)
                    if char_data and argument.lower() in char_data["name"].lower():
                        print(char_data["description"])
                        return False


        if found_item:
            print(found_item["description"])
        elif argument:
            print(f"You don't see any '{argument}' here to look at closely.")
        else:
            print("Look at what?")


    elif command == "go":
        if argument:
            current_room_data = world.get_room_data(player_instance.current_room_id)
            if current_room_data and argument in current_room_data.get("exits", {}):
                new_room_id = current_room_data["exits"][argument]
                # Future: Add any logic for on_exit from current room or on_enter to new room
                player_instance.move(new_room_id)
                print_current_location()
            else:
                print(f"You can't go {argument} from here.")
        else:
            print("Go where? (e.g., 'go north', 'n', 'e', 's', 'w')")

    elif command == "inventory" or command == "i":
        print(player_instance.get_inventory_display())

    elif command == "take":
        if argument:
            current_room_data = world.get_room_data(player_instance.current_room_id)
            item_to_take_id = None
            item_to_take_data = None

            for item_id in current_room_data.get("items", []):
                item_data = world.get_item_data(item_id)
                # Check if argument matches item name (case-insensitive substring match for flexibility)
                if item_data and argument.lower() in item_data["name"].lower():
                    item_to_take_id = item_id
                    item_to_take_data = item_data
                    break

            if item_to_take_id and item_to_take_data:
                if item_to_take_data["properties"].get("can_take", False):
                    if player_instance.add_item_to_inventory(item_to_take_id):
                        current_room_data["items"].remove(item_to_take_id) # Remove from room
                        print(f"You took the {item_to_take_data['name']}.")
                    else:
                        # This case should ideally not happen if can_take is true and it's not already in inventory
                        print(f"You can't take the {item_to_take_data['name']} right now.")
                else:
                    print(f"You can't take the {item_to_take_data['name']}.")
            else:
                print(f"You don't see any '{argument}' here to take.")
        else:
            print("Take what?")

    elif command == "drop":
        if argument:
            item_to_drop_id = None
            item_to_drop_data = None

            # Find the item in player's inventory
            for item_id_in_inv in player_instance.inventory:
                item_data_in_inv = world.get_item_data(item_id_in_inv)
                if item_data_in_inv and argument.lower() in item_data_in_inv["name"].lower():
                    item_to_drop_id = item_id_in_inv
                    item_to_drop_data = item_data_in_inv
                    break

            if item_to_drop_id and item_to_drop_data:
                if player_instance.remove_item_from_inventory(item_to_drop_id):
                    current_room_data = world.get_room_data(player_instance.current_room_id)
                    if "items" not in current_room_data:
                        current_room_data["items"] = []
                    current_room_data["items"].append(item_to_drop_id) # Add to room
                    print(f"You dropped the {item_to_drop_data['name']}.")
                else:
                    # Should not happen if item was found in inventory
                    print(f"Error: Could not drop {item_to_drop_data['name']}.")
            else:
                print(f"You don't have any '{argument}' to drop.")
        else:
            print("Drop what?")

    elif command == "help" or command == "h":
        print("\nAvailable commands:")
        print("  look (l)              - Describe the current room and its contents.")
        print("  look at <object>    - Examine an object or character more closely.")
        print("  go <direction>      - Move in a direction (north, south, east, west, up, down, or n,s,e,w,u,d).")
        print("  take <item>         - Pick up an item from the room.")
        print("  drop <item>         - Drop an item from your inventory into the room.")
        print("  inventory (i)       - Check your inventory.")
        print("  talk to <character> - Speak to a character (e.g., 'talk to gnome').")
        # print("  use <item> [on <target>] - Use an item from your inventory.")
        print("  quit (q)              - Exit the game.")
        print("  help (h)              - Show this help message.")

    elif command == "talk": # Covers "talk to X" via parser
        if argument:
            current_room_data = world.get_room_data(player_instance.current_room_id)
            character_to_talk_to_id = None
            character_to_talk_to_data = None

            for char_id in current_room_data.get("characters", []):
                char_data = world.get_character_data(char_id)
                # Check if argument matches character name (case-insensitive substring match)
                if char_data and argument.lower() in char_data["name"].lower():
                    character_to_talk_to_id = char_id
                    character_to_talk_to_data = char_data
                    break

            if character_to_talk_to_id and character_to_talk_to_data:
                dialogue_lines = character_to_talk_to_data.get("dialogue")
                if isinstance(dialogue_lines, list) and dialogue_lines:
                    # Cycle through dialogue options
                    dialogue_index = character_to_talk_to_data.get("dialogue_index", 0)
                    print(f"\n{character_to_talk_to_data['name']} says: \"{dialogue_lines[dialogue_index]}\"")
                    character_to_talk_to_data["dialogue_index"] = (dialogue_index + 1) % len(dialogue_lines)
                elif isinstance(dialogue_lines, str): # Single string dialogue
                     print(f"\n{character_to_talk_to_data['name']} says: \"{dialogue_lines}\"")
                else:
                    print(f"{character_to_talk_to_data['name']} doesn't seem to have much to say.")
            else:
                print(f"You don't see anyone named '{argument}' here to talk to.")
        else:
            print("Talk to whom?")

    else:
        print(f"I don't understand '{command}{' ' + argument if argument else ''}'. Try 'help' (h) for commands.")

    return False # Signal to continue game

def main():
    global player_instance
    player_instance = player.Player(start_room_id="start_room") # Initialize player at the start room

    print("Welcome to the Wondrous World of CodeCraft!")
    print("Your adventure begins now...")
    print("(Type 'quit' to exit, 'help' for a list of commands.)")

    print_current_location()

    while True:
        raw_input = input("\n> ").strip()
        if not raw_input:
            continue

        command, argument = parser.parse_command(raw_input)

        if command:
            if handle_command(command, argument):
                break # Quit game
        else:
            print("I didn't understand that. Try 'help' or a simple command.")

if __name__ == "__main__":
    main()
