#!/bin/bash

# The image we want to keep
KEEP_IMAGE="sentiment-analysis:latest"
echo "Keeping image: $KEEP_IMAGE"

# Check for specific images we know we can remove
echo "Looking for specific images to remove..."

# Check for flask-metrics-app
if docker images | grep -q "flask-metrics-app"; then
    echo "Removing flask-metrics-app image..."
    docker rmi -f $(docker images flask-metrics-app -q)
fi

# Check for <none> images (dangling images)
if docker images | grep -q "<none>"; then
    echo "Removing dangling images..."
    docker image prune -f
fi

# List remaining images
echo "Remaining images:"
docker images
