#!/bin/bash
set -e

GIT_ROOT=$1
docker build -t flask-sample-one:prod $GIT_ROOT/services/flask_app/
docker tag flask-sample-one:prod $DOCKER_ID_USER/flask-sample-one:prod
docker push $DOCKER_ID_USER/flask-sample-one
