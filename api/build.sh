#!/bin/bash
NOW=$(date +"%Y-%m-%d")
REPO=registry.apps.arreg.la/public
IMAGE=fix-ntp-hisense

docker build --no-cache -t ${REPO}/${IMAGE}:${NOW} -t ${REPO}/${IMAGE}:latest .
docker push ${REPO}/${IMAGE}:${NOW}
docker push ${REPO}/${IMAGE}:latest