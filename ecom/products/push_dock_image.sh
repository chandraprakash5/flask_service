#!/bin/bash
set -e

export PATH=$PATH:/home/jenkins/.local/bin
IMAGE_TAG=$(git log --format="%H" -n 1)

cd ecom/products
DOCKER_ID_USER=chanprak
docker build -t ecom-products:$IMAGE_TAG  .
docker tag ecom-products:$IMAGE_TAG $DOCKER_ID_USER/ecom-products:$IMAGE_TAG
docker push $DOCKER_ID_USER/ecom-products:$IMAGE_TAG
cd ../..
