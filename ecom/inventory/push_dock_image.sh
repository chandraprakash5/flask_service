#!/bin/bash
set -e

export PATH=$PATH:/home/jenkins/.local/bin
IMAGE_TAG=$(git log --format="%H" -n 1)

cd ecom/inventory
DOCKER_ID_USER=chanprak
docker build -t ecom-inventory:$IMAGE_TAG  .
docker tag ecom-inventory:$IMAGE_TAG $DOCKER_ID_USER/ecom-inventory:$IMAGE_TAG
docker push $DOCKER_ID_USER/ecom-inventory:$IMAGE_TAG
cd ../..
