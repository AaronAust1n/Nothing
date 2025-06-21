import random
from ascii_art import parts_library as lib

def _get_part(collection, key, default_key='default'):
    """Safely retrieves a part from a collection, falling back to a default if the key is missing."""
    if key in collection:
        return collection[key]
    # Try a more generic key if specific one not found (e.g. "round" from "round_head")
    simple_key = str(key).split('_')[0] if isinstance(key, str) else None
    if simple_key and simple_key in collection:
        return collection[simple_key]
    return collection.get(default_key, [" ??? ", " ??? ", " ??? "]) # Fallback for missing default

def _center_art(art_lines, width):
    """Centers each line of ASCII art within a given width."""
    centered = []
    for line in art_lines:
        padding = width - len(line)
        left_pad = padding // 2
        right_pad = padding - left_pad
        centered.append(" " * left_pad + line + " " * right_pad)
    return centered

def _combine_horizontally(art1_lines, art2_lines, art1_align='left', art2_align='left', separator=" "):
    """Combines two pieces of ASCII art side-by-side."""
    # Ensure both arts have the same number of lines by padding the shorter one
    len1, len2 = len(art1_lines), len(art2_lines)
    max_len = max(len1, len2)

    width1 = max(len(line) for line in art1_lines) if art1_lines else 0
    width2 = max(len(line) for line in art2_lines) if art2_lines else 0

    padded_art1 = []
    for i in range(max_len):
        if i < len1:
            line = art1_lines[i]
            if art1_align == 'right':
                padded_art1.append(line.rjust(width1))
            else: # default left
                padded_art1.append(line.ljust(width1))
        else:
            padded_art1.append(" " * width1)

    padded_art2 = []
    for i in range(max_len):
        if i < len2:
            line = art2_lines[i]
            if art2_align == 'right':
                padded_art2.append(line.rjust(width2))
            else: # default left
                padded_art2.append(line.ljust(width2))
        else:
            padded_art2.append(" " * width2)

    combined_lines = []
    for i in range(max_len):
        combined_lines.append(padded_art1[i] + separator + padded_art2[i])
    return combined_lines


class AsciiArtEngine:
    def __init__(self, creature_details):
        self.details = creature_details

    def _render_head(self):
        head_shape = self.details.get("head_shape", "default")
        num_eyes = self.details.get("num_eyes", 2)

        head_art = list(_get_part(lib.HEADS, head_shape, "default")) # Make a copy

        eye_char = lib.EXTRAS["eye_default"]
        # Generate the string for eyes, e.g., "o", "o o", "o o o"
        if isinstance(num_eyes, int):
            if num_eyes == 1:
                eye_str = eye_char
            elif num_eyes > 1:
                # Create a string of eyes like "o o o". Max 4 'o's to prevent extreme width.
                actual_eye_count = min(num_eyes, 4)
                eye_str = (eye_char + " ") * (actual_eye_count - 1) + eye_char if actual_eye_count > 0 else ""
            else: # 0 or negative, default to 2 visual eyes
                eye_str = eye_char + " " + eye_char
        elif num_eyes == "many" or num_eyes == "a cluster of":
            eye_str = eye_char + " " + eye_char + " " + eye_char # "o o o" for many/cluster
        else: # default 2 eyes if unexpected string
            eye_str = eye_char + " " + eye_char

        # Attempt to replace placeholders in head art
        placed_eyes = False
        for i, line in enumerate(head_art):
            placeholders = {
                " o o ": 3,
                "o  o": 4,
                "o o": 3
            }

            for p_holder, p_len in placeholders.items():
                if p_holder in line:
                    if len(eye_str) <= p_len: # Only use placeholder if eye_str fits comfortably
                        fitted_eye_str = eye_str.center(p_len)
                        head_art[i] = line.replace(p_holder, fitted_eye_str, 1)
                        placed_eyes = True
                        break
                    # If eye_str is too long for this specific placeholder,
                    # we don't use this placeholder. Loop continues to check other placeholders
                    # or other lines. If no placeholder is ever suitable, fallback will be used.
            if placed_eyes:
                break # Eyes placed for this head (found a suitable placeholder on this line)

        # Fallback: If no placeholder was hit (either not found, or eye_str was too long for all found),
        # and head has multiple lines, try to insert eyes into a suitable middle line.
        if not placed_eyes and len(head_art) > 1:
            # Prefer a line that looks like it's meant for content (e.g., not just " /---\ ")
            # Typically, this would be the second line or a line with internal spaces.
            # A simple heuristic: pick the middle-ish line.
            target_line_idx = len(head_art) // 2
            if target_line_idx == 0 and len(head_art) > 1 : target_line_idx = 1 # Avoid very top if possible

            line_content = head_art[target_line_idx]
            line_len = len(line_content)

            # Only attempt if the line is long enough and eye_str is not empty
            if line_len >= len(eye_str) and eye_str:
                # Try to insert eye_str, centered, into the line
                start_pos = (line_len - len(eye_str)) // 2
                # Ensure we don't overwrite non-space characters unless it's a very basic line
                # This part is tricky; for now, we'll overwrite.
                # A safer way would be to ensure line_content[start_pos : start_pos+len(eye_str)] is mostly spaces.
                head_art[target_line_idx] = (line_content[:start_pos] +
                                             eye_str +
                                             line_content[start_pos+len(eye_str):])
        return head_art

    def _render_body(self):
        body_shape = self.details.get("body_shape", "default")
        return _get_part(lib.BODIES, body_shape, "default")

    def _render_legs(self):
        num_legs = self.details.get("num_legs", 2)
        leg_style = self.details.get("leg_style", "default_two")

        if num_legs == 0 or "no legs" in leg_style:
            if "slithers" in leg_style:
                return _get_part(lib.LEGS_SETS, "no_legs_slithers_base", "no_legs_flat_base")
            return _get_part(lib.LEGS_SETS, "no_legs_flat_base", "no_legs_slithers_base")

        key = leg_style.replace(" ", "_")

        # Attempt to find a match for number of legs + style
        if isinstance(num_legs, int):
            if num_legs == 2 and f"{key}_two" in lib.LEGS_SETS:
                return _get_part(lib.LEGS_SETS, f"{key}_two")
            # Use "_many" for any number > 2 if a specific count isn't found
            elif num_legs > 2 and f"{key}_many" in lib.LEGS_SETS:
                return _get_part(lib.LEGS_SETS, f"{key}_many")
            elif f"{key}_{num_legs}" in lib.LEGS_SETS:
                return _get_part(lib.LEGS_SETS, f"{key}_{num_legs}")
        elif num_legs == "many": # Handle "many" string explicitly
            if f"{key}_many" in lib.LEGS_SETS:
                return _get_part(lib.LEGS_SETS, f"{key}_many")
            else: # Fallback for "many" if specific style_many doesn't exist
                return _get_part(lib.LEGS_SETS, "default_four") # Or some other "many legs" default

        # Fallback to default leg types based on number if it's an int
        if isinstance(num_legs, int):
            if num_legs == 2:
                return _get_part(lib.LEGS_SETS, "default_two")
            elif num_legs > 2:
                return _get_part(lib.LEGS_SETS, "default_four")

        return _get_part(lib.LEGS_SETS, "no_legs_flat_base")


    def _render_wings(self):
        wing_type = self.details.get("wing_type")
        if not wing_type:
            return None, None

        # Try to match specific wing type, e.g. "feathery_large"
        # This assumes wing_type might be "feathery" and wing_span "large"
        span = self.details.get("wing_span", "small")
        base_key = wing_type.replace(" ", "_").split("_")[0] # "feathery", "leathery" etc.

        left_key = f"{base_key}_{span}_left"
        right_key = f"{base_key}_{span}_right"

        if left_key not in lib.WINGS or right_key not in lib.WINGS:
            # Fallback to generic small wings of the type
            left_key = f"{base_key}_small_left"
            right_key = f"{base_key}_small_right"
            if left_key not in lib.WINGS or right_key not in lib.WINGS:
                 # Fallback to absolute default small wings
                left_key = "default_small_left"
                right_key = "default_small_right"

        return _get_part(lib.WINGS, left_key), _get_part(lib.WINGS, right_key)


    def _render_tail(self):
        tail_form = self.details.get("tail_form")
        if not tail_form:
            return None

        key = tail_form.replace(" ", "_").replace("-","_") # e.g. "fluffy_pom_pom"
        return _get_part(lib.TAILS, key, "default_stubby")

    def assemble_creature(self):
        head = self._render_head()
        body = self._render_body()
        legs = self._render_legs()

        # Basic vertical assembly: head, body, legs
        # Determine max width for centering these core parts
        core_parts = [head, body, legs]
        max_width = 0
        for part_lines in core_parts:
            if part_lines: # Legs can be None if no legs
                current_max_width = max(len(line) for line in part_lines)
                if current_max_width > max_width:
                    max_width = current_max_width

        # Center each core part
        centered_head = _center_art(head, max_width) if head else []
        centered_body = _center_art(body, max_width) if body else []
        centered_legs = _center_art(legs, max_width) if legs else []

        # Combine core parts vertically
        assembled_art_lines = centered_head + centered_body + centered_legs

        # --- Wings ---
        wing_art_left, wing_art_right = self._render_wings()
        if wing_art_left and wing_art_right:
            # Attempt to attach wings to the sides of the body part
            # This is tricky. For now, align wings with the body section.
            body_start_idx = len(centered_head)
            body_end_idx = body_start_idx + len(centered_body)

            # Pad body lines to make space for wings, or combine side-by-side
            # This simple version just prepends/appends wing art to existing lines
            # It assumes wings are roughly the same height as the body

            temp_canvas = [""] * len(assembled_art_lines) # placeholder for width calculation

            # Get widths
            wing_left_width = max(len(l) for l in wing_art_left) if wing_art_left else 0
            core_width = max(len(l) for l in assembled_art_lines) if assembled_art_lines else 0
            wing_right_width = max(len(l) for l in wing_art_right) if wing_art_right else 0

            new_art_lines = []
            for i, core_line in enumerate(assembled_art_lines):
                l_wing_line = ""
                r_wing_line = ""

                # Try to align wings vertically with the body portion
                if body_start_idx <= i < body_end_idx:
                    wing_line_idx = i - body_start_idx
                    if wing_line_idx < len(wing_art_left):
                        l_wing_line = wing_art_left[wing_line_idx].ljust(wing_left_width)
                    else:
                        l_wing_line = " " * wing_left_width

                    if wing_line_idx < len(wing_art_right):
                        r_wing_line = wing_art_right[wing_line_idx].rjust(wing_right_width) # rjust for right wing
                    else:
                        r_wing_line = " " * wing_right_width
                else: # No wings for head/legs part
                    l_wing_line = " " * wing_left_width
                    r_wing_line = " " * wing_right_width

                new_art_lines.append(l_wing_line + core_line + r_wing_line)
            assembled_art_lines = new_art_lines
            # Update max_width if wings made it wider
            if assembled_art_lines:
                max_width = max(len(line) for line in assembled_art_lines)


        # --- Tail ---
        # --- Tail ---
        tail_art = self._render_tail()
        if tail_art:
            # Center the tail art independently first
            tail_max_line_width = max(len(line) for line in tail_art) if tail_art else 0
            centered_tail_art = _center_art(tail_art, tail_max_line_width)

            # Determine the width for the final canvas (creature + tail)
            current_creature_max_width = 0
            if assembled_art_lines:
                current_creature_max_width = max(len(line) for line in assembled_art_lines) if assembled_art_lines else 0

            # The final width will be the max of creature's width or tail's width
            # This ensures that if the tail is very wide, the creature lines get padded too, and vice-versa.
            final_canvas_width = max(current_creature_max_width, tail_max_line_width)

            # Pad existing creature lines to the new final_canvas_width if necessary
            padded_creature_lines = []
            for line in assembled_art_lines:
                padding = final_canvas_width - len(line)
                left_pad = padding // 2
                right_pad = padding - left_pad
                padded_creature_lines.append(" " * left_pad + line + " " * right_pad)
            assembled_art_lines = padded_creature_lines

            # Pad tail lines to the final_canvas_width and append
            for line in centered_tail_art:
                padding = final_canvas_width - len(line)
                left_pad = padding // 2
                right_pad = padding - left_pad
                assembled_art_lines.append(" " * left_pad + line + " " * right_pad)

        # Final pass to ensure all lines have consistent width (especially if no tail, or wings changed things)
        # This also handles the case where assembled_art_lines was initially empty.
        if assembled_art_lines:
            final_max_width = max(len(line) for line in assembled_art_lines)
            # Use ljust for the final alignment to keep things from shifting unexpectedly if some lines were shorter.
            # However, if parts are meant to be centered, they should have been centered already.
            # For a blocky look, ljust is fine. If perfect centering of all lines is desired,
            # each line should be individually centered to final_max_width.
            # Given previous steps center parts, ljust should be okay to just ensure rectangular output.
            final_art_lines = []
            for line in assembled_art_lines:
                padding = final_max_width - len(line)
                left_pad = padding // 2 # Re-center each line to the true final_max_width
                right_pad = padding - left_pad
                final_art_lines.append(" " * left_pad + line.strip() + " " * right_pad) # strip then center
            assembled_art_lines = final_art_lines

        return "\n".join(assembled_art_lines)


if __name__ == '__main__':
    # Test with some dummy data
    dummy_details_1 = {
        "head_shape": "round", "num_eyes": 2,
        "body_shape": "plump",
        "num_legs": 2, "leg_style": "tiny tiptoe feet",
        "wing_type": "feathery", "wing_span": "large",
        "tail_form": "bushy"
    }
    engine1 = AsciiArtEngine(dummy_details_1)
    print("--- Creature 1 ---")
    print(engine1.assemble_creature())

    dummy_details_2 = {
        "head_shape": "square-ish", "num_eyes": "many",
        "body_shape": "boxy",
        "num_legs": 0, "leg_style": "no legs (slithers)",
        "wing_type": "leathery", "wing_span": "small",
        "tail_form": "spiky"
    }
    engine2 = AsciiArtEngine(dummy_details_2)
    print("\n--- Creature 2 ---")
    print(engine2.assemble_creature())

    dummy_details_3 = {
        "head_shape": "pointy", "num_eyes": 1,
        "body_shape": "serpentine",
        "num_legs": "many", "leg_style": "wiggly tentacles", # 'many' legs
        # No wings
        # No tail
    }
    engine3 = AsciiArtEngine(dummy_details_3)
    print("\n--- Creature 3 ---")
    print(engine3.assemble_creature())
