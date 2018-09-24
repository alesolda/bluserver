# Credits: ALS (2017)

SELECTOR ?= bluserver

# Fixed Params
DOCKER_IMAGE_TAG := ${SELECTOR}:latest
DOCKER_CONTAINER_NAME := ${SELECTOR}
HOST_PERSISTENCE_DIR := ${PWD}/home-${SELECTOR}
SRC_DIR := ${PWD}

MY_UID := $(shell id -u)
MY_GID := $(shell id -g)
MY_UNAME := ${SELECTOR}


docker-build-image:
	docker build \
	--build-arg MY_UID=${MY_UID} \
	--build-arg MY_GID=${MY_GID} \
	--build-arg MY_UNAME=${MY_UNAME} \
	-t ${DOCKER_IMAGE_TAG} ./


docker-build-wheel: clean docker-build-image
	docker run --rm \
	-v ${SRC_DIR}:/src \
	--name=${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_TAG} \
	python setup.py bdist_wheel


docker-shell: docker-rm docker-build-image
	-docker run --rm -ti \
	-v ${SRC_DIR}:/src \
	--name=${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_TAG} \
	/bin/ash


docker-run-server: docker-rm docker-build-image
	-docker run --rm \
	-p 1982:1982 \
	-v ${SRC_DIR}:/src \
	--name=${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_TAG}


docker-tests: docker-rm clean docker-build-image
	-docker run --rm \
	-v ${SRC_DIR}:/src \
	--name=${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_TAG} \
	"./docker_tests.sh"

docker-stop:
	-docker stop ${DOCKER_CONTAINER_NAME}

docker-rm: docker-stop
	-docker rm ${DOCKER_CONTAINER_NAME}

clean:
	rm -fr bluserver.egg-info
	rm -fr build
	rm -fr dist
	rm -fr venv
	rm -fr .eggs
	rm -fr .pytest_cache
	rm -fr bluserver/calculator/parser.out
	rm -fr bluserver/calculator/parsetab.py
	find -iname __pycache__ | xargs rm -fr


.PHONY: docker-build-image docker-build-wheel docker-shell docker-run-server docker-stop docker-rm clean