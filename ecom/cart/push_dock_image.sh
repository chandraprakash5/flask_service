#!/bin/bash
set -e

export PATH=$PATH:/home/jenkins/.local/bin
IMAGE_TAG=$(git log --format="%H" -n 1)

cd ecom/cart 
DOCKER_ID_USER=chanprak
docker build -t ecom-cart:$IMAGE_TAG  .
docker tag ecom-cart:$IMAGE_TAG $DOCKER_ID_USER/ecom-cart:$IMAGE_TAG
docker push $DOCKER_ID_USER/ecom-cart:$IMAGE_TAG
cd ../..
