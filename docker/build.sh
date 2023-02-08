#!/bin/bash

DOCKER_REPO="idps"  # SET IS!!!!!

if [[ ! -n ${DOCKER_REPO} ]]; then
    echo "Set you docker repo to contiune"
    exit -1
fi

PROJECT_NAME=czt_web_api

cd $(dirname $0)/../
DOCKERVERSION=`date +%Y%m%d%H%M`"_"`git log | head -1 | awk '{print $2}' | cut -c 1-10`

# build..
docker build --build-arg PROJECT_DIRNAME=${PROJECT_NAME} -t dockerhub.datagrand.com/${DOCKER_REPO}/${PROJECT_NAME}:${DOCKERVERSION} -f docker/Dockerfile .
#docker push dockerhub.datagrand.com/${DOCKER_REPO}/${PROJECT_NAME}:${DOCKERVERSION}
#
#docker tag dockerhub.datagrand.com/${DOCKER_REPO}/${PROJECT_NAME}:${DOCKERVERSION} dockerhub.datagrand.com/${DOCKER_REPO}/${PROJECT_NAME}:latest
#docker push dockerhub.datagrand.com/${DOCKER_REPO}/${PROJECT_NAME}:latest
