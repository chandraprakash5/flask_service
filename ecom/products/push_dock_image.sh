#!/bin/bash
set -e

export PATH=$PATH:/home/jenkins/.local/bin
IMAGE_TAG=$(git log --format="%H" -n 1)

cd ecom/products
$(aws ecr get-login --no-include-email --region us-west-2)
docker build -t ecom/products:$IMAGE_TAG  .
docker tag ecom/products:$IMAGE_TAG 725566882860.dkr.ecr.us-west-2.amazonaws.com/ecom/products:$IMAGE_TAG
docker push 725566882860.dkr.ecr.us-west-2.amazonaws.com/ecom/products:$IMAGE_TAG
cd ../..
