#!/bin/bash
set -e

export PATH=$PATH:/home/jenkins/.local/bin
DOCKER_ID_USER=chanprak
IMAGE_TAG=$(git log --format="%H" -n 1)

cd ecom/orders
docker build -t ecom-orders:$IMAGE_TAG  .
docker tag ecom-orders:$IMAGE_TAG $DOCKER_ID_USER/ecom-orders:$IMAGE_TAG
docker push $DOCKER_ID_USER/ecom-orders:$IMAGE_TAG
cd ../..

