# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
# - tk for tkinter (turtle dependency)
# - ghostscript for .eps to .png conversion
RUN apt-get update && apt-get install -y \
    tk \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
# For this project, Flask is the main Python dependency.
# Turtle is part of the standard library in versions of Python that include tkinter.
RUN pip install --no-cache-dir Flask

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
