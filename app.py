from flask import Flask, send_file, render_template_string
import subprocess
import os
import random
import string

app = Flask(__name__)

# HTML template to display the image and a button to refresh
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kaleidoscope</title>
    <style>
        body { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background-color: #282c34; color: white; font-family: Arial, sans-serif; margin: 0; }
        img { border: 5px solid #61dafb; margin-bottom: 20px; max-width: 90%; max-height: 70vh; }
        button { background-color: #61dafb; color: #282c34; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 5px; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Kaleidoscopic Wonder</h1>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% else %}
        <img src="{{ url_for('get_image', filename=image_filename) }}" alt="Kaleidoscope Image">
    {% endif %}
    <form method="GET" action="/">
        <button type="submit">New Vision</button>
    </form>
</body>
</html>
"""

def generate_random_filename(length=10, extension=".png"):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string + extension

@app.route('/')
def home():
    image_filename = generate_random_filename()
    eps_filename = image_filename.replace(".png", ".eps")
    output_eps_path = os.path.join('static', eps_filename)
    output_png_path = os.path.join('static', image_filename)

    # Ensure static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    # Clean up old images (optional, but good practice)
    for f in os.listdir('static'):
        if f.endswith(".png") or f.endswith(".eps"):
            try:
                os.remove(os.path.join('static', f))
            except OSError:
                # Handle cases where file might be in use or already deleted
                pass

    error_message = None
    try:
        # Run the kaleidoscope script
        # The script needs to be executable and have correct shebang, or called with python interpreter
        # Ensure kaleidoscope.py is in the same directory or provide the correct path
        # The kaleidoscope.py script saves to "kaleidoscope.eps" by default.
        # We need to modify it to save to a dynamic path or handle the fixed name.
        # For now, let's assume kaleidoscope.py saves to a fixed "kaleidoscope.eps"
        # and we rename/move it.

        # Let's modify kaleidoscope.py to accept an output filename.
        # For now, we'll assume it creates 'kaleidoscope.eps' and we rename it.
        # This is a simplification. A better approach would be to pass the desired filename to the script.

        # Forcing the kaleidoscope script to output to a specific path
        # This requires modifying kaleidoscope.py or careful handling here.
        # Let's assume kaleidoscope.py will be modified to output to 'static/kaleidoscope.eps'
        # Or, more robustly, pass the output path to it.
        # For now, let's run it and expect "kaleidoscope.eps" in the current dir, then move it.

        # Adjusting to run kaleidoscope.py and manage its output
        # The kaleidoscope.py script currently saves to "kaleidoscope.eps" in its CWD.
        # We need to run it, then convert its output.

        # Step 1: Run kaleidoscope.py
        # It will create 'kaleidoscope.eps' in the root directory of the flask app
        subprocess.run(["python", "kaleidoscope.py"], check=True, timeout=30) # Added timeout

        # Step 2: Move and convert the .eps file to .png
        # Source path of the generated .eps file
        source_eps_path = "kaleidoscope.eps" # As per kaleidoscope.py

        if not os.path.exists(source_eps_path):
            raise FileNotFoundError("kaleidoscope.eps was not created by the script.")

        # Move kaleidoscope.eps to static/eps_filename
        os.rename(source_eps_path, output_eps_path)

        # Convert .eps to .png using Ghostscript (gs)
        # This assumes Ghostscript is installed in the environment.
        # gs -sDEVICE=pngalpha -o static/output.png -r150 static/input.eps
        subprocess.run([
            "gs",
            "-sDEVICE=pngalpha",
            f"-o{output_png_path}",
            "-r150", # Resolution
            output_eps_path
        ], check=True, timeout=30) # Added timeout

        if not os.path.exists(output_png_path):
            raise FileNotFoundError(f"{output_png_path} was not created after conversion.")

    except subprocess.CalledProcessError as e:
        error_message = f"Error generating kaleidoscope: {e}. Make sure Ghostscript is installed and kaleidoscope.py runs correctly."
        print(f"Error during subprocess execution: {e}")
    except FileNotFoundError as e:
        error_message = f"Error: A required file was not found. {e}"
        print(f"FileNotFoundError: {e}")
    except subprocess.TimeoutExpired:
        error_message = "Error: The kaleidoscope generation or conversion timed out."
        print("TimeoutExpired during subprocess execution.")
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(f"Unexpected error: {e}")

    if error_message:
        return render_template_string(HTML_TEMPLATE, error=error_message)
    else:
        return render_template_string(HTML_TEMPLATE, image_filename=image_filename)

@app.route('/images/<filename>')
def get_image(filename):
    return send_file(os.path.join('static', filename), mimetype='image/png')

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True, host='0.0.0.0', port=5000)
