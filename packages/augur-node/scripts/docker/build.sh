#!/bin/bash

TAG=core-$(node scripts/core-version.js)

# Make sure you're up to date
docker pull node:10.12

IMAGE_NAME=augurproject/augur-node
docker build --no-cache . -t $IMAGE_NAME:$TAG -t $IMAGE_NAME:dev
