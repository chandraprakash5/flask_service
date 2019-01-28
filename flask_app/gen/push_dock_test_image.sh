#!/bin/bash
set -e

GIT_ROOT=$1
docker build -t flask-sample-one:test $GIT_ROOT/services/flask_app/
docker tag flask-sample-one:test $DOCKER_ID_USER/flask-sample-one:test
docker push $DOCKER_ID_USER/flask-sample-one
