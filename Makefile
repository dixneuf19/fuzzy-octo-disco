.PHONY: install install-dev dev build run push release release-multi deploy

PACKAGE_NAME=fuzzyoctodisco
DOCKER_REPOSITERY=dixneuf19
IMAGE_NAME=fuzzy-octo-disco
IMAGE_TAG=$(shell git rev-parse --short HEAD)
DOCKER_IMAGE_PATH=$(DOCKER_REPOSITERY)/$(IMAGE_NAME):$(IMAGE_TAG)
APP_NAME=fuzzy-octo-disco
KUBE_NAMESPACE=dank-face-bot

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt

dev:
	uvicorn ${PACKAGE_NAME}.main:app --reload

format:
	isort .
	black .

check-format:
	isort --profile black --check ${PACKAGE_NAME}
	black --check ${PACKAGE_NAME}
	# flake8 ${PACKAGE_NAME}

test:
	PYTHONPATH=. pytest --cov=${PACKAGE_NAME} --cov-report=xml tests

build:
	docker build -t $(DOCKER_IMAGE_PATH) .

build-multi:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(DOCKER_IMAGE_PATH) .


run: build
	docker run -p 8000:80 --env-file=.env -v "$(shell pwd)/pictures/:/tmp/pictures" $(DOCKER_IMAGE_PATH)

push:
	docker push $(DOCKER_IMAGE_PATH)

release: build push

release-multi:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(DOCKER_IMAGE_PATH) . --push

deploy:
	kubectl apply -f $(APP_NAME).yaml

secret:
	kubectl create secret generic radio-france-api-token --from-env-file=.env

kube-credentials:
	NAMESPACE=${KUBE_NAMESPACE} ./scripts/generate-kubeconfig.sh
