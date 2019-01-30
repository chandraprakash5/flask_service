#!/bin/bash
set -e

IMAGE_TAG=$(git log --format="%H" -n 1)
echo $pwd

cd flask_app
docker login
docker build -t flask-sample-one:$IMAGE_TAG .
docker tag flask-sample-one:$IMAGE_TAG $DOCKER_ID_USER/flask-sample-one:$IMAGE_TAG
docker push $DOCKER_ID_USER/flask-sample-one
cd ..
