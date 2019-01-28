#!/bin/bash
set -e

GIT_ROOT=$1
docker build -t flask-sample-one:dev $GIT_ROOT/services/flask_app/
docker tag flask-sample-one:dev $DOCKER_ID_USER/flask-sample-one:dev
docker push $DOCKER_ID_USER/flask-sample-one

