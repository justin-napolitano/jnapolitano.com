# # Use the Alpine Linux base image
# FROM alpine:latest

# # Set the working directory inside the container
# WORKDIR /app

# # Copy a simple script that prints "Hello, World!" into the container
# COPY /src/hello.sh .

# # Make the script executable
# RUN chmod +x hello.sh

# # Define the command to run when the container starts
# CMD ["./hello.sh"]


# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app
COPY requirements.txt /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
# EXPOSE 8080

# Run the Python script when the container launches
CMD ["python", "loc_flattener.py"]
