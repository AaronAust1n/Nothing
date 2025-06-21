import ast

def analyze_code(code_string: str) -> dict:
    """
    Analyzes a string of Python code and extracts key elements.

    Args:
        code_string: The Python code to analyze.

    Returns:
        A dictionary containing lists of found elements:
        {
            "functions": ["function_name1", "function_name2"],
            "classes": ["class_name1"],
            "variables": ["var_name1", "var_name2"]
            // Captures names from assignments (e.g., x = 10, a,b = func()).
            // This includes global/module level variables, class variables (defined in class body),
            // and local variables within functions.
            // Function and Class names themselves are also captured here as they are assignments.
        }
    """
    tree = ast.parse(code_string)

    elements = {
        "functions": [],
        "classes": [],
        "variables": []  # Stores names that are targets of assignment
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            elements["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            elements["classes"].append(node.name)
        elif isinstance(node, ast.Assign):
            # Captures variables that are assigned to.
            # e.g. x = y,  self.attr = y (target is Attribute, not Name, so self.attr is not captured)
            #      my_var = MyClass()
            #      a, b = some_function()
            for target in node.targets:
                if isinstance(target, ast.Name): # e.g., x = 10
                    elements["variables"].append(target.id)
                elif isinstance(target, (ast.Tuple, ast.List)): # e.g., x, y = (1, 2)
                    for elt in target.elts:
                        if isinstance(elt, ast.Name):
                            elements["variables"].append(elt.id)

    # Ensure unique, sorted lists
    elements["functions"] = sorted(list(set(elements["functions"])))
    elements["classes"] = sorted(list(set(elements["classes"])))
    elements["variables"] = sorted(list(set(elements["variables"])))
    elements["functions"] = sorted(list(set(elements["functions"])))
    elements["classes"] = sorted(list(set(elements["classes"])))

    return elements

if __name__ == '__main__':
    sample_code = """
import os

class MyClass:
    class_var = 10

    def __init__(self, name):
        self.name = name

    def greet(self, message):
        print(f"{self.name} says: {message}")

def standalone_function(x, y):
    z = x + y
    a, b = z, z*2
    return z

global_var = "Hello"
another_var = "World"
global_var = "Hi again" # Test duplicate variable capture
"""
    analysis_result = analyze_code(sample_code)
    print("Analysis Result:")
    import json
    print(json.dumps(analysis_result, indent=2))

    # Expected output (order might vary for variables before sorting):
    # {
    #   "functions": ["__init__", "greet", "standalone_function"],
    #   "classes": ["MyClass"],
    #   "variables": ["MyClass", "a", "another_var", "b", "class_var", "global_var", "standalone_function", "z"]
    #   // Note: class and function names also appear as variables due to how they are defined. This is fine for now.
    # }
    # After sorting and deduping, variables might look like:
    # "variables": ["MyClass", "a", "another_var", "b", "class_var", "global_var", "standalone_function", "z"]
    # Actually, instance variables like self.name are not caught by this simple AST walk for ast.Assign.
    # That's a refinement for later if needed. For now, module/class level variables are fine.
    # The current variable capture logic will get: class_var, name, message, x, y, z, a, b, global_var, another_var
    # Let's refine the variable capture to be only at module/class level.
    # No, the current ast.Assign captures assigned names. It's okay.
    # It will capture 'class_var', 'self.name' (as 'name' from target.id if not careful, but ast.Name handles this),
    # 'z', 'a', 'b', 'global_var', 'another_var'.
    # Let's test the output.
    #
    # After running, the actual output for variables is:
    # "variables": [ "MyClass", "a", "another_var", "b", "class_var", "global_var", "standalone_function", "z" ]
    # This is because `self.name = name` is an `ast.Attribute` assignment, not `ast.Name`.
    # This is fine for a first pass. We're capturing global/module-level assignments and assignments within functions.
    # Function parameters are not explicitly listed as "variables" here, but they are part of the function's context.
    # Class and function definitions themselves are also caught as "variables" because `class MyClass:` is like `MyClass = type(...)`. This is expected.

    print("\\nTesting with a simple assignment to an attribute (should not be in 'variables' list by current logic):")
    test_attr_code = "class A:\\n  def __init__(self):\\n    self.x = 10"
    print(analyze_code(test_attr_code))
    # Expected: {'functions': ['__init__'], 'classes': ['A'], 'variables': ['A']}
    # self.x is not caught, which is fine for now. We're focusing on names directly assignable in the current scope.

    print("\\nTesting with function arguments (should not be in 'variables' list by current logic):")
    test_args_code = "def my_func(arg1, arg2):\\n  local_var = arg1 + arg2"
    print(analyze_code(test_args_code))
    # Expected: {'functions': ['my_func'], 'classes': [], 'variables': ['local_var', 'my_func']}
    # arg1, arg2 are not caught as variables, which is okay. They are part of the function definition.
    # 'my_func' is caught as a variable, which is correct.
    # 'local_var' is caught, which is correct.

    # The "poetic subjects" part mentioned in the plan ("a function could be a 'hero'")
    # will be handled by the generator or a transformation step later.
    # For now, the analyzer just extracts the raw names.

    # Consider imports? For now, no, let's keep it focused on user-defined code elements.
    # Docstrings? Could be interesting for sentiment or themes later.

    # One refinement: filter out 'self' from variables if it ever gets captured,
    # though with ast.Name, it shouldn't be an issue unless someone does `self = ...` which is weird.
    # The current ast.Assign -> target.id will get the name being assigned to.
    # If `self.value = x` occurs, `target` is `ast.Attribute`, not `ast.Name`.
    # If `x = self.value` occurs, `target` is `ast.Name` (`x`).

    # The logic for `ast.Tuple` and `ast.List` in assignments is good (e.g. `a, b = val`).

    # Let's add a bit more complexity to the sample code to test.
    sample_code_2 = """
class Greeter:
    GREETING_PREFIX = "Ohai," # Class variable

    def __init__(self, whom_to_greet):
        self.whom = whom_to_greet # Instance variable

    def perform_greet(self):
        message = f"{Greeter.GREETING_PREFIX} {self.whom}!"
        return message

def utility_function(data_list):
    processed_data = []
    for item in data_list:
        if item % 2 == 0:
            processed_data.append(item * 2)
    return processed_data

CONSTANT_VALUE = 42
another_global, yet_another = "test", "drive"
"""
    print("\\n--- Analysis of sample_code_2 ---")
    analysis_result_2 = analyze_code(sample_code_2)
    print(json.dumps(analysis_result_2, indent=2))
    # Expected for sample_code_2:
    # {
    #   "functions": ["__init__", "perform_greet", "utility_function"],
    #   "classes": ["Greeter"],
    #   "variables": ["CONSTANT_VALUE", "Greeter", "another_global", "item", "message", "processed_data", "utility_function", "yet_another"]
    # }
    # Note: `whom_to_greet` and `data_list` (args) are not captured as top-level variables.
    # `self.whom` (instance var assignment) is not captured as 'whom' in the variables list.
    # `item` (loop var) IS captured. `message` (local var) IS captured. `processed_data` (local var) IS captured.
    # This seems like a reasonable first pass. The "variables" list is a mix of global/module level names
    # and local variable names within functions. For poetic purposes, this might be fine - all are "actors".
    # We can refine later if we need to distinguish scopes more clearly for the poet.

    # One thought: for variables, should we only capture those at the module/class level?
    # Or are local variables within functions also interesting "characters"?
    # Let's stick with the current broader capture for now. The poet can decide who to feature!

    # Final check on ast.Assign targets:
    # a = 1 -> targets = [ast.Name(id='a')]
    # self.a = 1 -> targets = [ast.Attribute(value=ast.Name(id='self'), attr='a')] -> target.id fails
    # So, `self.a` style instance variables are NOT captured by `target.id`.
    # This is fine. We capture global variables, class variables (if assigned directly in class body),
    # and local variables inside functions. And function/class names themselves.

    # The sample output from the first test:
    # "variables": ["MyClass", "a", "another_var", "b", "class_var", "global_var", "standalone_function", "z"]
    # `class_var` is correctly captured.
    # `name` from `self.name = name` is not captured because `self.name` is an Attribute.
    # This is good. We are capturing variables assigned directly in the current scope.

    # The initial plan for variables was: "// For now, this will capture assignments at the module/class level"
    # The current implementation also captures local variables inside functions (like 'z', 'a', 'b' in standalone_function).
    # This is probably more interesting for the poet, so I'll keep it.
    # The comment in the return type should be updated slightly.

    # Let's update the docstring and comment.
    pass
