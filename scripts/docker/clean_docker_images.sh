#!/bin/bash

# The image we want to keep
KEEP_IMAGE="sentiment-analysis"
KEEP_TAG="latest"

echo "Keeping image: $KEEP_IMAGE:$KEEP_TAG"
echo "Image ID to keep: $(docker images "$KEEP_IMAGE:$KEEP_TAG" -q)"

# First, list all running containers
echo "Current running containers:"
docker ps

# Stop and remove all containers
echo "Stopping and removing all containers..."
docker stop $(docker ps -q) || true
docker rm $(docker ps -a -q) || true

# Now remove all images except the one we want to keep
echo "Removing all other images..."
docker images | grep -v "REPOSITORY" | grep -v "$KEEP_IMAGE.*$KEEP_TAG" | awk '{print $3}' | xargs -r docker rmi -f

echo "Cleanup complete. Remaining images:"
docker images
