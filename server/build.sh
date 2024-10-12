#!/bin/bash

# Check if version number and Docker account are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <version> <docker_account>"
    exit 1
fi

# Check if version number respects format v?.?.?
if [[ ! "$1" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Invalid version number format. Please use the format 'vX.Y.Z' where X, Y, and Z are numbers. For example: v1.2.3"
    exit 1
fi

VERSION=$1
DOCKER_ACCOUNT=$2
IMAGE_NAME="$DOCKER_ACCOUNT/ai-course-assistant-server"

# Build the Docker image with both version and latest tags
docker build -t $IMAGE_NAME:$VERSION -t $IMAGE_NAME:latest .

# Ask for confirmation before pushing the Docker images
read -p "Do you want to push the Docker images to Docker Hub? (y/N): " CONFIRM
if [[ "$CONFIRM" != "y" ]]; then
    echo "Aborting push."
    exit 0
fi

# Push the Docker image with the version tag to Docker Hub
docker push $IMAGE_NAME:$VERSION

# Push the Docker image with the latest tag to Docker Hub
docker push $IMAGE_NAME:latest