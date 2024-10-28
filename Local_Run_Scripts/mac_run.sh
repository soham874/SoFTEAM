#!/bin/bash
clear

DEBUG_MODE=false  # Default debug mode is false
WORKER_COUNT=8

echo "Beginning setup of SoFTEAM project from scratch"

if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

export DEBUG_MODE WORKER_COUNT

# List of directories to copy D into
directories=("Mission-Control" "Trading-Engine" "News-Gateway" "TechniSight" "Market-Gateway")

# Loop through each directory and delete D
for dir in "${directories[@]}"; do
  if [ -d "$dir/Common-Utils" ]; then
    rm -rf "$dir/Common-Utils"
    echo "Deleted Common-Utils from $dir"
  else
    echo "Common-Utils does not exist in $dir"
  fi
done

# Loop through each directory and copy D
for dir in "${directories[@]}"; do
  if [ -d "$dir" ] && [ -d "Common-Utils" ]; then
    cp -r Common-Utils "$dir"/
    echo "Copied Common-Utils into $dir"
  else
    echo "Directory $dir or Common-Utils does not exist"
  fi
done

root_env="./.env"

# Remove the root .env file if it already exists
if [ -f "$root_env" ]; then
  rm "$root_env"
  echo "Existing root .env file removed."
fi

# Loop through each directory and append the content of its .env file to the root .env
for dir in "${directories[@]}"; do
  env_file="$dir/.env"
  
  if [ -f "$env_file" ]; then
    cat "$env_file" >> "$root_env"
    echo "Appended $env_file to root .env"
  else
    echo "$env_file does not exist, skipping..."
  fi
done

echo "All .env files merged into $root_env."

docker-compose up --build -d

# Remove the root .env file if it already exists
if [ -f "$root_env" ]; then
  rm "$root_env"
  echo "Existing root .env file removed."
fi

echo "Services created and copied env variables and common util packages removed"

# Loop through each directory and delete D
for dir in "${directories[@]}"; do
  if [ -d "$dir/Common-Utils" ]; then
    rm -rf "$dir/Common-Utils"
    echo "Deleted Common-Utils from $dir"
  else
    echo "Common-Utils does not exist in $dir"
  fi
done

docker stats -a
echo "Allowing grace period of 3 sec before bringing down project..."
sleep 3
docker compose down