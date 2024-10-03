#!/bin/bash
clear

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Build the Docker image
docker build -t nse_analyser .

# Check if a container named 'nse_analyser' exists
if [ "$(docker ps -aq -f name=nse_analyser)" ]; then
    # If it does, stop it
    docker stop nse_analyser
    # Then remove it
    docker container rm nse_analyser
fi

# Run the Docker container
docker run --name nse_analyser -it -p 8080:8080 nse_analyser