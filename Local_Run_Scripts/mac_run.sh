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

echo "Beginning setup of SoFTEAM project from scratch"

if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

if [ "$DEBUG_MODE" = "true" ]; then
    WORKER_COUNT=1
fi

export DEBUG_MODE WORKER_COUNT

docker-compose up --build -d

if nc -z localhost 6379; then
    echo "Redis server is running on port 6379."
else
    echo "Failed to start Redis server on port 6379, aborting application start"
    exit 1
fi

if nc -z localhost 9092; then
    echo "Kafka is running on port 9092."
else
    echo "Failed to start Kafka on port 9092, aborting application start"
    exit 1
fi