#!/bin/bash

echo "Current containers:"
docker ps -a

# Check if there are any non-Kubernetes containers
echo "Looking for non-Kubernetes containers to remove..."
NON_K8S_CONTAINERS=$(docker ps -a --format "{{.ID}}" | grep -v "k8s_")

if [ -n "$NON_K8S_CONTAINERS" ]; then
    echo "Removing non-Kubernetes containers..."
    echo "$NON_K8S_CONTAINERS" | xargs docker rm -f
else
    echo "No non-Kubernetes containers found."
fi

# For Kubernetes containers, we'll be more selective
# We'll keep essential system containers and remove any that might be related to your application
echo "Checking for unnecessary Kubernetes containers..."

# List containers that might be related to your application
APP_CONTAINERS=$(docker ps -a --format "{{.Names}}" | grep -E "k8s_.*_nginx-" | grep -v "k8s_POD_")

if [ -n "$APP_CONTAINERS" ]; then
    echo "Found application-related containers. These are likely needed for your Kubernetes setup."
    echo "If you want to remove these, you should use kubectl to manage your deployments."
fi

echo "Remaining containers:"
docker ps -a
