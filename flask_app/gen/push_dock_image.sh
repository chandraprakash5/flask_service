#!/bin/bash
set -e

GIT_ROOT=$1
IMAGE_TAG=$2
docker build -t flask-sample-one:$IMAGE_TAG $GIT_ROOT/services/flask_app/
docker tag flask-sample-one:$IMAGE_TAG $DOCKER_ID_USER/flask-sample-one:$IMAGE_TAG
docker push $DOCKER_ID_USER/flask-sample-one
