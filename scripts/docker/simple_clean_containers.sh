#!/bin/bash

# List all containers
echo "Current containers:"
docker ps -a

# Remove all stopped containers
echo "Removing all stopped containers..."
docker container prune -f

# List remaining containers
echo "Remaining containers:"
docker ps -a
