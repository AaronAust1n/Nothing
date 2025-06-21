import random
from creature_parts import names, body, characteristics, backstory
from ascii_art import engine as ascii_engine # Renamed to avoid conflict

class Creature:
    def __init__(self):
        self.name = names.generate_name()
        self.body_details = body.generate_body_details()
        self.characteristics = characteristics.generate_characteristics()
        self.backstory = backstory.generate_backstory()

        # Combine all textual details for the ASCII engine and description
        self.all_details = {
            "name": self.name,
            **self.body_details,
            **self.characteristics,
            "backstory": self.backstory # Backstory is not directly used by ASCII but good to have
        }

        self.art_engine = ascii_engine.AsciiArtEngine(self.all_details)
        self.ascii_art = self.art_engine.assemble_creature()

    def describe(self):
        """Returns a string describing the creature."""
        desc = []
        desc.append(f"Behold the magnificent {self.name}!")
        desc.append(f"It has a {self.body_details['head_shape']} head with {self.body_details['num_eyes']} eyes and a {self.body_details['mouth_style']}.")
        desc.append(f"Its body is {self.body_details['body_shape']} and covered in {self.body_details['body_texture']} {self.body_details['primary_color']} skin, with {self.body_details['accent_color1']} accents.")
        if self.body_details['accent_color2']:
            desc.append(f"You might also spot hints of {self.body_details['accent_color2']}.")

        if self.body_details['num_legs'] == 0:
            desc.append(f"It has no legs and moves by {self.body_details['leg_style']}.")
        else:
            desc.append(f"It stands on {self.body_details['num_legs']} {self.body_details['leg_style']}.")

        if self.body_details['wing_type']:
            desc.append(f"It sports {self.body_details['wing_span']} {self.body_details['wing_type']} wings.")

        if self.body_details['tail_form']:
            desc.append(f"A notable feature is its {self.body_details['tail_form']} tail.")

        desc.append("\nThis creature:")
        desc.append(f"- {self.characteristics['primary_ability']}.")
        desc.append(f"- Is known for its habit of {self.characteristics['quirky_habit']}.")
        desc.append(f"- Is generally considered {self.characteristics['personality_trait']}.")

        desc.append(f"\nLegend says that {self.name} {self.backstory}")

        return "\n".join(desc)

    def display(self):
        """Prints the creature's ASCII art and description."""
        print(self.ascii_art)
        print("\n" + "=" * 40 + "\n")
        print(self.describe())
        print("\n" + "=" * 40 + "\n")

if __name__ == '__main__':
    print("Generating a few whimsical creatures...\n")
    for i in range(2):
        print(f"----- Creature #{i+1} -----")
        creature = Creature()
        creature.display()
        print("\n\n")
