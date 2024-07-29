#!/bin/bash

# Get the current date and time in the desired format
current_time=$(date +"%Y-%m-%dT%H:%M:%S%z")

# Format the time zone offset with a colon
formatted_time="${current_time:0:22}:${current_time:22:2}"

# Print the result
echo "date = \"$formatted_time\""
