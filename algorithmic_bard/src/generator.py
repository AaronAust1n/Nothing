import random

# Simple templates for generating poetic lines
LINE_TEMPLATES = [
    "Behold, the mighty function: {name}, its purpose grand!",
    "A class named {name}, a blueprint in the land.",
    "The variable {name}, a value it does hold,",
    "Consider {name}, a story to be told.",
    "Let's speak of {name}, in digital domain,",
    "The essence of {name}, again and yet again.",
    "In realms of code, where {name} takes its flight,",
    "We find {name}, shining ever so bright."
]

# Templates for different types of elements
FUNCTION_TEMPLATES = [
    "The function {name}, with purpose clear and bold,",
    "Behold {name}, a story to unfold.",
    "Function {name} begins its noble quest,",
    "Let {name} work, and put us to the test.",
    "Within the script, {name} plays its part,"
]

CLASS_TEMPLATES = [
    "The class {name}, a structure grand and deep,",
    "Observe {name}, secrets it will keep.",
    "{name} the class, a master of design,",
    "A blueprint {name}, so perfectly aligned."
]

VARIABLE_TEMPLATES = [
    "A variable, {name}, holds data tight,",
    "The humble {name}, bathed in digital light.",
    "{name} appears, a value to convey,",
    "Remember {name}, it's vital to the play."
]

POEM_STRUCTURE = {
    "title": "Ode to the Code",
    "stanzas": 3, # Number of stanzas
    "lines_per_stanza": 4
}

def generate_poem(analysis_results: dict) -> str:
    """
    Generates a simple poem based on the analyzed code elements.

    Args:
        analysis_results: A dictionary from the analyzer, e.g.,
                          {"functions": ["f1"], "classes": ["c1"], "variables": ["v1"]}

    Returns:
        A string representing the poem.
    """
    poem_lines = []
    title = POEM_STRUCTURE["title"]

    all_elements = []
    if analysis_results.get("functions"):
        for func_name in analysis_results["functions"]:
            all_elements.append({"name": func_name, "type": "function"})
    if analysis_results.get("classes"):
        for class_name in analysis_results["classes"]:
            all_elements.append({"name": class_name, "type": "class"})
    if analysis_results.get("variables"):
        for var_name in analysis_results["variables"]:
            all_elements.append({"name": var_name, "type": "variable"})

    if not all_elements:
        return f"{title}\\n\\n(The code was silent, no tales to tell today.)"

    poem_lines.append(f"{title}\\n")

    for _ in range(POEM_STRUCTURE["stanzas"]):
        stanza_lines = []
        for _ in range(POEM_STRUCTURE["lines_per_stanza"]):
            if not all_elements: # Should not happen if check above is done
                break

            chosen_element = random.choice(all_elements)
            element_name = chosen_element["name"]
            element_type = chosen_element["type"]

            if element_type == "function":
                template = random.choice(FUNCTION_TEMPLATES)
            elif element_type == "class":
                template = random.choice(CLASS_TEMPLATES)
            elif element_type == "variable":
                template = random.choice(VARIABLE_TEMPLATES)
            else: # Fallback, should not happen
                template = random.choice(LINE_TEMPLATES)

            line = template.format(name=element_name)
            stanza_lines.append(line)

        poem_lines.append("\\n".join(stanza_lines))
        poem_lines.append("") # Add a blank line between stanzas

    return "\\n".join(poem_lines)

if __name__ == '__main__':
    sample_analysis = {
        "functions": ["calculate_sum", "process_data", "helper_function"],
        "classes": ["DataProcessor", "UserManager"],
        "variables": ["count", "is_active", "MAX_USERS", "DataProcessor", "UserManager", "calculate_sum"]
        # Including class/func names as vars, as per analyzer
    }

    print("--- Poem 1 ---")
    poem1 = generate_poem(sample_analysis)
    print(poem1)

    print("\\n--- Poem 2 (different random choices) ---")
    poem2 = generate_poem(sample_analysis)
    print(poem2)

    empty_analysis = {"functions": [], "classes": [], "variables": []}
    print("\\n--- Poem from empty analysis ---")
    poem_empty = generate_poem(empty_analysis)
    print(poem_empty)

    minimal_analysis = {"functions": ["main"]}
    print("\\n--- Poem from minimal analysis ---")
    poem_minimal = generate_poem(minimal_analysis)
    print(poem_minimal)
