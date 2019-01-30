#!/bin/bash
set -e

DOCKER_ID_USER=chanprak
IMAGE_TAG=$(git log --format="%H" -n 1)
echo $IMAGE_TAG
echo $DOCKER_ID_USER
echo $PWD
echo `whoami`

cd flask_app
docker build -t flask-sample-one:$IMAGE_TAG .
docker tag flask-sample-one:$IMAGE_TAG $DOCKER_ID_USER/flask-sample-one:$IMAGE_TAG
docker push $DOCKER_ID_USER/flask-sample-one
cd ..
