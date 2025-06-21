import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.tracer(0) # Turn off screen updates for smoother animation

# Create multiple turtles
num_turtles = 10
turtles = []
colors = ["red", "orange", "yellow", "green", "blue", "purple", "white", "cyan", "magenta", "lime"]

for i in range(num_turtles):
    t = turtle.Turtle()
    t.speed(0) # Fastest speed
    t.color(random.choice(colors))
    t.penup()
    t.goto(random.randint(-390, 390), random.randint(-290, 290))
    t.pendown()
    t.pensize(random.randint(1, 3))
    t.hideturtle()
    turtles.append(t)

# Animation loop
def animate():
    for t in turtles:
        # Random movement
        angle = random.randint(-45, 45)
        distance = random.randint(5, 20)

        t.right(angle)
        t.forward(distance)

        # Bounce off walls
        x, y = t.position()
        if x > 390 or x < -390:
            t.right(180)
        if y > 290 or y < -290:
            t.right(180)

    screen.update()
    screen.ontimer(animate, 100) # Call animate again after 100ms

animate()

# Save the drawing to a file (e.g., PostScript)
# Note: Turtle graphics are vector-based. Saving directly to PNG might require
# an external library or a different approach if not supported directly in all environments.
# For now, we'll save as PostScript, which can be converted.
try:
    # Get the canvas and save its content
    canvas = screen.getcanvas()
    canvas.postscript(file="kaleidoscope.eps", colormode='color')
    print("Kaleidoscope image saved as kaleidoscope.eps")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Continuing without saving image for now.")


# Keep the window open until manually closed if not saving to file
# screen.mainloop() # This line might be needed if running interactively
# For non-interactive saving, ensure the script exits after saving.
# Depending on the environment, turtle might exit automatically or hang.
# Adding a graceful exit.
# turtle.bye() # This can sometimes close the window too soon when saving.

# A short delay to ensure drawing completes before trying to save (if needed)
# import time
# time.sleep(2)

# If running in a headless environment where mainloop() or bye() causes issues,
# ensure the script finishes.
# For this project, we aim to save the output, so interactive display isn't the primary goal.

# The saving mechanism above attempts to save as EPS.
# This might need adjustment for Flask integration if direct PNG is required.
# For now, this script focuses on generating the pattern and saving it.
# Further adaptation for web display will be handled in the Flask app step.
