#!/bin/bash

# Define the destination directory and filename
DEST_DIR=~/Downloads
LOCAL_CSV_FILE="$DEST_DIR/matching_logic_analysis.csv"

# Loop every 10 seconds
while true; do
  # Create a temporary container and copy the file to the local system
  CONTAINER_ID=$(docker create -v softeam_softeam_runtime_data:/mnt busybox)
  docker cp "$CONTAINER_ID:/mnt/matching_logic_analysis.csv" "$LOCAL_CSV_FILE"
  docker rm "$CONTAINER_ID" > /dev/null

  echo "Saved $LOCAL_CSV_FILE"
  sleep 10
done