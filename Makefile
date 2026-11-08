.PHONY: install dev build run push release release-multi deploy

PACKAGE_NAME=fuzzyoctodisco
DOCKER_REPOSITERY=dixneuf19
IMAGE_NAME=fuzzy-octo-disco
IMAGE_TAG=$(shell git rev-parse --short HEAD)
DOCKER_IMAGE_PATH=$(DOCKER_REPOSITERY)/$(IMAGE_NAME):$(IMAGE_TAG)
APP_NAME=fuzzy-octo-disco
KUBE_NAMESPACE=dank-face-bot

install:
	uv sync

dev:
	uv run uvicorn ${PACKAGE_NAME}.main:app --reload

format:
	uv run isort .
	uv run black .

check-format:
	uv run isort --check ${PACKAGE_NAME}
	uv run black --check ${PACKAGE_NAME}

test:
	uv run pytest --cov=${PACKAGE_NAME} --cov-report=xml

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
