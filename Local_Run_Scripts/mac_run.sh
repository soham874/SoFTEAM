#!/bin/bash
clear

docker network create my-network

# Check if the redis-server container is running
if [ "$(docker ps -q -f name=redis-server)" ]; then
    echo "Redis server is already running."
else
    echo "Redis server is not running. Checking for existing containers..."

    # Check if any Redis container is stopped
    if [ "$(docker ps -aq -f status=exited -f name=redis-server)" ]; then
        echo "Starting existing redis-server container..."
        docker start redis-server
    else
        echo "Pulling Redis image and starting a new container..."
        docker pull redis:latest
        
        # Start the redis-server container
        docker run -d --network my-network --name redis-server -it -p 6379:6379 redis:latest
    fi
fi

# Check if Redis is running on port 6379
if nc -z localhost 6379; then
    echo "Redis server is running on port 6379."
else
    echo "Failed to start Redis server on port 6379."
fi


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
docker run --network my-network --name nse_analyser -it -p 8080:8080 nse_analyser