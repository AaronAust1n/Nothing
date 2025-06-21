# player.py - Manages player state, inventory, and actions

class Player:
    def __init__(self, start_room_id):
        self.current_room_id = start_room_id
        self.inventory = [] # List of item objects (or item IDs)
        self.health = 100 # Example player attribute
        self.flags = {} # For tracking game progress/events

    def move(self, new_room_id):
        self.current_room_id = new_room_id
        # Potentially trigger room entry events here

    def add_item_to_inventory(self, item_name):
        # For now, just store item names. Later, could be item objects.
        if item_name not in self.inventory:
            self.inventory.append(item_name)
            return True
        return False # Item already in inventory or some other reason

    def remove_item_from_inventory(self, item_name):
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            return True
        return False # Item not found

    def has_item(self, item_name):
        return item_name in self.inventory

    def get_inventory_display(self):
        if not self.inventory:
            return "Your inventory is empty."
        else:
            return "You are carrying:\n" + "\n".join(f"- {item}" for item in self.inventory)

# Global player object (can be instantiated in main.py)
# player_instance = None # To be created when the game starts.
