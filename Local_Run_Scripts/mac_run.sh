#!/bin/bash
clear

DEBUG_MODE=false  # Default debug mode is false
WORKER_COUNT=8

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --DEBUG) DEBUG_MODE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Define the network name
NETWORK_NAME="softeam-network"

# Check if the network already exists
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    echo "Creating network: $NETWORK_NAME"
    docker network create "$NETWORK_NAME"
else
    echo "Network $NETWORK_NAME already exists."
fi

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

if [ $DEBUG_MODE = "true" ]
then
    echo "Starting application in debug mode with 1 worker"
    WORKER_COUNT=1
fi

# Build the Docker image
docker build --build-arg WORKER_COUNT=$WORKER_COUNT -t softeam .

# Check if a container named 'softeam' exists
if [ "$(docker ps -aq -f name=softeam)" ]; then
    # If it does, stop it
    docker stop softeam
    # Then remove it
    docker container rm softeam
fi

# Run the Docker container
docker run --network my-network --name softeam -it -p 8080:8080 -p 5678:5678 \
    -e DEBUG_MODE=$DEBUG_MODE \
    softeam