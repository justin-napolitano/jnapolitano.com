# Use the Alpine Linux base image
FROM alpine:latest

# Set the working directory inside the container
WORKDIR /app

# Copy a simple script that prints "Hello, World!" into the container
COPY hello.sh .

# Make the script executable
RUN chmod +x hello.sh

# Define the command to run when the container starts
CMD ["./hello.sh"]
