#!/bin/bash

set -e

docker build -t gcr.io/${PROJECT_NAME}/${DOCKER_IMAGE_NAME}:${TRAVIS_COMMIT} .

docker push gcr.io/${PROJECT_NAME}/${DOCKER_IMAGE_NAME}:${TRAVIS_COMMIT}

envsubst < kubernetes.template.yml > kubernetes.yml

# Apply the persistent volume storage
kubectl apply -f nfs-server.yml

# Apply the app
kubectl apply -f kubernetes.yml
kubectl rollout status deployment "${KUBE_DEPLOYMENT_NAME}-deployment"


